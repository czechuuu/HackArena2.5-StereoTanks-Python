from typing import Tuple
from hackathon_bot import *
from strategy import Strategy
class Soldier():
    def _find_my_tank(self, game_state: GameState) -> Tank | None:  # from example.py
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
                    
        return None

    def _find_my_coordinates(self, game_state: GameState) -> tuple[int, int] | None:
        for y_coord, row in enumerate(game_state.map.tiles):
            for x_coord, tile in enumerate(row):
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return (x_coord, y_coord) 
                    
        return None

    def go_to_zone(self, game_state: GameState, strategy: Strategy) -> ResponseAction:
        """ Goes to the nearest unoccupied tile in the zone to the given position using Manhattan distance.
        Assumes there is always exactly one zone.
        """

        maybe_coords = self._find_my_coordinates(game_state)
        if maybe_coords is None:
            print("Tank not found ?!?")
            return Pass()
        x: int = maybe_coords[0]
        y: int = maybe_coords[1] 

        zone: Zone = game_state.map.zones[0]

        nearest_unoccupied_tile_coords: Tuple[int, int] | None = None
        min_dist_to_unoccupied_tile: float = float('inf')

        # Find an unoccupied tile in the zone
        for tile_x_in_zone_coord in range(zone.x, zone.x + zone.width):
            for tile_y_in_zone_coord in range(zone.y, zone.y + zone.height):
                # First the y coord!!!
                tile = game_state.map.tiles[tile_y_in_zone_coord][tile_x_in_zone_coord] 
                if not tile.entities:
                    distance_to_tile = abs(tile_x_in_zone_coord - x) + abs(tile_y_in_zone_coord - y)
                    if distance_to_tile < min_dist_to_unoccupied_tile:
                        min_dist_to_unoccupied_tile = distance_to_tile
                        nearest_unoccupied_tile_coords = (tile_x_in_zone_coord, tile_y_in_zone_coord)
        
        if nearest_unoccupied_tile_coords:
            return GoTo(nearest_unoccupied_tile_coords[0], nearest_unoccupied_tile_coords[1],
                           penalties=strategy.get_penalties())

        # If all tiles are occupied, just go to the corner of the zone
        return GoTo(zone.x, zone.y, penalties=strategy.get_penalties())

        return Pass()
    
    def shoot_if_should(self, game_state: GameState, strategy: Strategy) -> ResponseAction:
        pass  # Both soldiers implement this method

    def activate_radar(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        return None  # Light soldier overrides this method; Default behaviour for heavy soldier