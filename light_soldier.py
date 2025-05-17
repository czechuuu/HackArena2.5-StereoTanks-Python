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
        elif my_tank.turret.bullet_count == 3:
            strategy.attack_mode = True
            strategy.bullets_left_in_attack_mode = 2 
            return AbilityUse(Ability.FIRE_BULLET)
        elif strategy.attack_mode == True:
            if strategy.bullets_left_in_attack_mode > 0:   # We fight.
                strategy.bullets_left_in_attack_mode -= 1
                return AbilityUse(Ability.FIRE_BULLET)
            else:       # We dip.
                my_coords = self._find_my_coordinates(game_state)
                if my_coords is None:
                    return Pass()
                    
                my_x, my_y = my_coords
                
                if strategy.dip_mode == False:
                    strategy.dip_mode = True
                    
                    # Define positions to check in order of preference
                    positions_to_check = []
                    if my_tank.turret.direction == Direction.DOWN or my_tank.turret.direction == Direction.UP:
                        # For vertical turret, check in this order: D, F, G, I, A, C, B, H
                        positions_to_check = [
                            (my_x-1, my_y),    # D - left
                            (my_x+1, my_y),    # F - right
                            (my_x-1, my_y+1),  # G - bottom-left
                            (my_x+1, my_y+1),  # I - bottom-right
                            (my_x-1, my_y-1),  # A - top-left
                            (my_x+1, my_y-1),  # C - top-right
                            (my_x, my_y-1),    # B - top
                            (my_x, my_y+1),    # H - bottom
                        ]
                    else:  # Direction.LEFT or Direction.RIGHT
                        # For horizontal turret, check in this order: B, H, A, G, C, I, D, F
                        positions_to_check = [
                            (my_x, my_y-1),    # B - top
                            (my_x, my_y+1),    # H - bottom
                            (my_x-1, my_y-1),  # A - top-left
                            (my_x-1, my_y+1),  # G - bottom-left
                            (my_x+1, my_y-1),  # C - top-right
                            (my_x+1, my_y+1),  # I - bottom-right
                            (my_x-1, my_y),    # D - left
                            (my_x+1, my_y),    # F - right
                        ]
                    
                    # Check each position in order
                    for pos_x, pos_y in positions_to_check:
                        # Check if position is valid (within bounds)
                        if 0 <= pos_x < 20 and 0 <= pos_y < 20:
                            tile = game_state.map.tiles[pos_y][pos_x]
                            
                            # Check if tile is empty (no walls)
                            if not any(isinstance(entity, Wall) for entity in tile.entities):
                                strategy.where_to_escape = (pos_x, pos_y)
                                
                                return GoTo(pos_x, pos_y, penalties=strategy.get_penalties())
                    
                    # If no valid move found, reset attack mode
                    strategy.attack_mode = False
                    strategy.dip_mode = False
                    return Pass()
                elif my_coords == strategy.where_to_escape:
                    strategy.attack_mode = False
                    strategy.dip_mode = False
                else:
                    return GoTo(strategy.where_to_escape[0], strategy.where_to_escape[1], penalties=strategy.get_penalties())
        else:
            return None
        
    def activate_radar(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        my_tank: Tank = self._find_my_tank(game_state)

        if my_tank.ticks_to_radar is None:
            return AbilityUse(Ability.USE_RADAR)
        else:
            return None
        