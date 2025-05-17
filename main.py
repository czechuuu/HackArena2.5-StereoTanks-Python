from hackathon_bot import *
from soldier import Soldier
from light_soldier import LightSoldier
from heavy_soldier import HeavySoldier
from strategy import Strategy, Objective

class MyBot(StereoTanksBot):
    soldiers: dict[TankType: Soldier] = {}
    strategy: Strategy = None

    def __init__(self) -> None:
        super().__init__()
        self.soldiers[TankType.LIGHT] = LightSoldier()
        self.soldiers[TankType.HEAVY] = HeavySoldier()
        self.strategy = Strategy()
    
    # NOT IMPLEMENTED
    def on_lobby_data_received(self, lobby_data: LobbyData) -> None: 
        return None
    
    def next_move(self, game_state: GameState) -> ResponseAction: 
        # Find my tank on the map
        my_type: TankType = self._find_my_tank(game_state).type  # CHECK IF NONE
        
        # Check if it can shoot an opponent
        attack_action: AbilityUse | None = self.soldiers[my_type].shoot_if_should(game_state, self.strategy)
        if attack_action is not None:
            return attack_action
        
        # Check if you can activate the radar
        activate_radar: AbilityUse | None = self.soldiers[my_type].activate_radar(game_state, self.strategy)
        if activate_radar is not None:
            return activate_radar
        
        # Continue with the current strategy
        match self.strategy.get_objective():
            case Objective.GO_TO_ZONE:
                return self.soldiers[my_type].go_to_zone(game_state, self.strategy)
            case default:
                return Pass()
    
    # NOT IMPLEMENTED
    def on_game_ended(self, game_result: GameResult) -> None: 
        return None
    
    # NOT IMPLEMENTED - DON'T CARE (?)
    def on_warning_received(
        self, warning: WarningType, message: str | None
    ) -> None: 
        pass

    def _find_my_tank(self, game_state: GameState) -> Tank | None:  # from example.py
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
        return None

if __name__ == "__main__":
    bot = MyBot()
    bot.run()
