from hackathon_bot import *
from soldier import Soldier
from strategy import Strategy

class HeavySoldier(Soldier):
    def shoot_if_should(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        if not self.should_shoot_opponent(game_state, strategy):
            return None
        
        my_tank: Tank = self._find_my_tank(game_state)

        if my_tank.turret.ticks_to_laser is None:
            return AbilityUse(Ability.USE_LASER)
        elif my_tank.turret.ticks_to_stun_bullet is None:
            return AbilityUse(Ability.FIRE_STUN_BULLET)
        elif my_tank.turret.bullet_count > 0:
            return AbilityUse(Ability.FIRE_BULLET)
        else:
            return None