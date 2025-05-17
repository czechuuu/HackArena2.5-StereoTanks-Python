from hackathon_bot import *
from soldier import Soldier
from strategy import Strategy

class LightSoldier(Soldier):
    def shoot_if_should(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        if not self.should_shoot_opponent(game_state, strategy):
            return None
        
        my_tank: Tank = self._find_my_tank(game_state)

        if my_tank.turret.ticks_to_double_bullet is None:
            return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
        elif my_tank.turret.ticks_to_stun_bullet is None:
            return AbilityUse(Ability.FIRE_STUN_BULLET)
        elif my_tank.turret.bullet_count > 0:
            return AbilityUse(Ability.FIRE_BULLET)
        else:
            return None
        
    def activate_radar(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        my_tank: Tank = self._find_my_tank(game_state)

        if my_tank.ticks_to_radar is None:
            return AbilityUse(Ability.USE_RADAR)
        else:
            return None
        