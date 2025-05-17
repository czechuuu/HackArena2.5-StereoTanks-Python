from hackathon_bot import *
from soldier import Soldier
from light_soldier import LightSoldier
from heavy_soldier import HeavySoldier
from strategy import Strategy, Objective

class MyBot(StereoTanksBot):
    soldier: Soldier = None
    strategy: Strategy = None
    first_move: bool = True
    teammate_found: bool = False
    my_type: TankType = None
    my_teammate_id: str = None

    def __init__(self) -> None:
        super().__init__()
        self.strategy = Strategy()
    
    # NOT IMPLEMENTED
    def on_lobby_data_received(self, lobby_data: LobbyData) -> None: 
        return None
    
    def next_move(self, game_state: GameState) -> ResponseAction: 
        if self.first_move:
            self.first_move = False
            found_type: TankType = self._find_my_tank(game_state).type
            self.my_type = found_type
            if found_type == TankType.LIGHT:
                self.soldier = LightSoldier()
            elif found_type == TankType.HEAVY:
                self.soldier = HeavySoldier()
            else:
                raise ValueError(f"Unknown tank type: {found_type}")
            
        if not self.teammate_found:
            team = next(
            t
            for t in game_state.teams
            if any(map(lambda x: x.id == game_state.my_id, t.players))
            )
            teammate = next((p for p in team.players if p.id != game_state.my_id), None)
            if teammate is not None:
                self.my_teammate_id = teammate.id
                self.teammate_found = True
            
        # Find my tank on the map, if dead return Pass
        my_tank: Tank | None = self._find_my_tank(game_state)
        if my_tank is None:
            self.strategy.set_objective(Objective.GO_TO_ZONE)
            return Pass()
        
        # Check if it can shoot an opponent
        attack_action: AbilityUse | None = self.soldier.shoot_if_should(game_state, self.strategy)
        if attack_action is not None:
            return attack_action
        
        # Check if you can activate the radar
        activate_radar: AbilityUse | None = self.soldier.activate_radar(game_state, self.strategy)
        if activate_radar is not None:
            return activate_radar
        
        friendly_soldiers_in_zone: tuple[TankType] = self._find_friendly_soldiers_in_zone(game_state)
        match len(friendly_soldiers_in_zone):
            case 0:
                self.strategy.set_objective(Objective.GO_TO_ZONE)
            case 1:
                self.strategy.set_objective(Objective.DEFEND_AREA)
                if self.my_type in friendly_soldiers_in_zone:
                    self.strategy.set_defend_area_coords(self._calculate_zone_square(game_state))
                else:
                    self.strategy.set_defend_area_coords(self._calculate_default_square(game_state))
            case 2:
                self.strategy.set_objective(Objective.DEFEND_AREA)
                if self.my_type == TankType.HEAVY:
                    self.strategy.set_defend_area_coords(self._calculate_zone_square(game_state))
                else:
                    self.strategy.set_defend_area_coords(self._calculate_default_square(game_state))

        # If I am not in zone and see an enemy go to him
        found_enemy: tuple[int, int] | None = self._find_enemy(game_state)
        if found_enemy is not None and len(friendly_soldiers_in_zone) == 2 and self.my_type == TankType.LIGHT:
            self.strategy.set_objective(Objective.DEFEND_AREA)
            self.strategy.set_defend_area_coords(self._calculate_enemy_square(game_state, found_enemy))
            self.strategy.atacking_enemy = True
            
        if found_enemy is not None and len(friendly_soldiers_in_zone) == 1 and not self._in_zone(game_state):
            self.strategy.set_objective(Objective.DEFEND_AREA)
            self.strategy.set_defend_area_coords(self._calculate_enemy_square(game_state, found_enemy))
            self.strategy.atacking_enemy = True

        if self.strategy.atacking_enemy:
            self.strategy.apache_timeout -= 1
            if self.strategy.apache_timeout <= 0:
                self.strategy.atacking_enemy = False
                self.strategy.set_objective(Objective.DEFEND_AREA)
                self.strategy.set_defend_area_coords(self._calculate_zone_square(game_state))
                self.strategy.apache_timeout = 15
    
        # Continue with the current strategy
        match self.strategy.get_objective():
            case Objective.GO_TO_ZONE:
                return self.soldier.go_to_zone(game_state, self.strategy)
            case Objective.DEFEND_AREA:
                return self.soldier.defend_area(game_state, self.strategy)
            case default:
                return Pass()
    
    # NOT IMPLEMENTED
    def on_game_ended(self, game_result: GameResult) -> None: 
        return None
    
    def on_warning_received(
        self, warning: WarningType, message: str | None
    ) -> None: 
        print(f"Warning received: {warning} - {message}")
        return None

    def _find_my_tank(self, game_state: GameState) -> Tank | None:  # from example.py
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
        return None
    
    # FIRST FOUND ENEMY FROM TOP LEFT - MAYBE WE NEED CLOSEST TO ZONE?
    def _find_enemy(self, game_state: GameState) -> tuple[int, int] | None:
        for y in range(20):
            for x in range(20):
                for entity in game_state.map.tiles[y][x].entities:
                    if isinstance(entity, Tank) and entity.owner_id != game_state.my_id and self.teammate_found and entity.owner_id != self.my_teammate_id:
                        return (x, y)
        return None
    
    def _find_friendly_soldiers_in_zone(self, game_state: GameState) -> tuple[TankType]:
        y_zone: int = game_state.map.zones[0].y
        x_zone: int = game_state.map.zones[0].x
        zone_height: int = game_state.map.zones[0].height
        zone_width: int = game_state.map.zones[0].width
        
        if zone_height != zone_width:
            raise ValueError(f"Zone is not square: {zone_height} != {zone_width}")

        friendly_soldiers: list[TankType] = []

        for y in range(y_zone, y_zone + zone_height):
            for x in range(x_zone, x_zone + zone_width):
                tile = game_state.map.tiles[y][x]
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and (entity.owner_id == game_state.my_id or (self.teammate_found and entity.owner_id == self.my_teammate_id)):
                        friendly_soldiers.append(entity.type)

        return tuple(friendly_soldiers)
    
    def _calculate_zone_square(self, game_state: GameState) -> tuple[int, int, int]:
        y_zone: int = game_state.map.zones[0].y
        x_zone: int = game_state.map.zones[0].x
        zone_height: int = game_state.map.zones[0].height
        zone_width: int = game_state.map.zones[0].width

        if zone_height != zone_width:
            raise ValueError(f"Zone is not square: {zone_height} != {zone_width}")

        return tuple([x_zone, y_zone, zone_height])
    
    # Square two tiles larger than the zone
    def _calculate_default_square(self, game_state: GameState) -> tuple[int, int, int]:
        y_zone: int = game_state.map.zones[0].y
        x_zone: int = game_state.map.zones[0].x
        zone_height: int = game_state.map.zones[0].height
        zone_width: int = game_state.map.zones[0].width

        if zone_height != zone_width:
            raise ValueError(f"Zone is not square: {zone_height} != {zone_width}")
        
        x_square: int = max(x_zone - 4, 0)
        y_square: int = max(y_zone - 4, 0)
        square_length: int = zone_height + 4
        if x_square + square_length >= 20 or y_square + square_length >= 20:  # OK?
            square_length = min(20 - x_square - 1, 20 - y_square - 1)
        return tuple([x_square, y_square, square_length])

    def _calculate_enemy_square(self, game_state: GameState, enemy_coords: tuple[int, int]) -> tuple[int, int, int]:
        y_enemy: int = enemy_coords[1]
        x_enemy: int = enemy_coords[0]

        x_square: int = max(x_enemy - 1, 0)
        y_square: int = max(y_enemy - 1, 0)
        square_length: int = 3
        if x_square + square_length >= 20 or y_square + square_length >= 20:  # OK?
            square_length = min(20 - x_square, 20 - y_square)
        return tuple([x_square, y_square, square_length])
    
    def _in_zone(self, game_state: GameState) -> bool:
        my_coords: tuple[int, int] | None = self._find_my_coordinates(game_state)
        if my_coords is None:
            return False
        if (my_coords[0] >= game_state.map.zones[0].x
             and my_coords[0] < game_state.map.zones[0].x + game_state.map.zones[0].width
             and my_coords[1] >= game_state.map.zones[0].y
             and my_coords[1] < game_state.map.zones[0].y + game_state.map.zones[0].height):
            return True
    
    def _find_my_coordinates(self, game_state: GameState) -> tuple[int, int] | None:
        for y_coord, row in enumerate(game_state.map.tiles):
            for x_coord, tile in enumerate(row):
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return (x_coord, y_coord) 
                    
        return None

if __name__ == "__main__":
    bot = MyBot()
    bot.run()
