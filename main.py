from hackathon_bot import *
from light_soldier import LightSoldier
from heavy_soldier import HeavySoldier

class MyBot(StereoTanksBot):
    light_soldier: LightSoldier
    heavy_soldier: HeavySoldier


    def __init__(self) -> None:
        super().__init__()
        self.light_soldier = LightSoldier()
        self.heavy_soldier = HeavySoldier()
    
    def on_lobby_data_received(self, lobby_data: LobbyData) -> None: 
        self.light_soldier.on_lobby_data_received(lobby_data)
        self.heavy_soldier.on_lobby_data_received(lobby_data)
        return None
    
    def _find_my_tank(self, game_state: GameState) -> Tank | None:  # from example.py
        """Finds the agent in the game state."""
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
        return None
    
    def next_move(self, game_state: GameState) -> ResponseAction: 
        my_id = game_state.my_id
        my_type = self._find_my_tank(game_state).type
        if my_type == TankType.LIGHT:
            return self.light_soldier.next_move(game_state)
        elif my_type == TankType.HEAVY:
            return self.heavy_soldier.next_move(game_state)
        else:
            raise ValueError(f"Unknown tank type: {my_type}")
    
    def on_game_ended(self, game_result: GameResult) -> None: 
        self.light_soldier.on_game_ended(game_result)
        self.heavy_soldier.on_game_ended(game_result)
        return None
    
    # NOT IMPLEMENTED - DON'T CARE (?)
    def on_warning_received(
        self, warning: WarningType, message: str | None
    ) -> None: 
        pass



if __name__ == "__main__":
    bot = MyBot()
    bot.run()
