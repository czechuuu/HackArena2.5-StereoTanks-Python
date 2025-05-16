from hackathon_bot import *


class MyBot(StereoTanksBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None: ...

    def next_move(self, game_state: GameState) -> ResponseAction: ...

    def on_game_ended(self, game_result: GameResult) -> None: ...

    def on_warning_received(
        self, warning: WarningType, message: str | None
    ) -> None: ...


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
