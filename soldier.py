from typing import Tuple
from hackathon_bot import *
from strategy import Strategy
import random 
class Soldier:
    def _find_my_coordinates(self, game_state: GameState) -> tuple[int, int] | None:
        for y_coord, row in enumerate(game_state.map.tiles):
            for x_coord, tile in enumerate(row):
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return (x_coord, y_coord) 
                    
        return None
    
    def _find_my_tank(self, game_state: GameState) -> Tank | None:
        """Finds the agent in the game state."""
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
        return None
    
    def _find_teammate_tank(self, game_state: GameState) -> Tank | None:
        """Finds the agent in the game state."""

        team = next(
            t
            for t in game_state.teams
            if any(map(lambda x: x.id == game_state.my_id, t.players))
        )

        teammate = next((p for p in team.players if p.id != game_state.my_id), None)

        if teammate is None:
            return None

        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == teammate.id:
                        return entity
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
    
    def shoot_if_should(self, game_state: GameState, strategy: Strategy) -> ResponseAction:
        return None  # Both soldiers implement this method

    def activate_radar(self, game_state: GameState, strategy: Strategy) -> ResponseAction | None:
        return None  # Light soldier overrides this method; Default behaviour for heavy soldier
    
    def should_shoot_opponent(self, game_state: GameState, strategy: Strategy) -> bool:
        map: Map = game_state.map
        my_tank: Tank = self._find_my_tank(game_state)
        teammate_tank: Tank = self._find_teammate_tank(game_state)
        turret_direction: Direction = my_tank.turret.direction
        
        my_x, my_y = self._find_my_coordinates(game_state)
        
        # Define coordinate changes based on direction
        dx, dy = 0, 0
        enemy_direction: list[Direction] = []
        if turret_direction == Direction.UP:
            dy = -1
            enemy_direction = [Direction.LEFT, Direction.RIGHT]
        elif turret_direction == Direction.DOWN:
            dy = 1
            enemy_direction = [Direction.LEFT, Direction.RIGHT]
        elif turret_direction == Direction.RIGHT:
            dx = 1
            enemy_direction = [Direction.UP, Direction.DOWN]
        elif turret_direction == Direction.LEFT:
            dx = -1
            enemy_direction = [Direction.UP, Direction.DOWN]
        
        # Check tiles in the direction of the turret
        current_x: int = my_x
        current_y: int = my_y
        while 0 <= current_x < 20 and 0 <= current_y < 20:
            current_x += dx
            current_y += dy
            
            # Check if we've gone out of bounds
            if not (0 <= current_x < len(map.tiles[0]) and 0 <= current_y < len(map.tiles)):
                break
            
            # Get the tile at the current position
            tile: Tile = map.tiles[current_y][current_x]
            
            # Check if the tile has a wall (can't shoot through walls)
            for entity in tile.entities:
                if isinstance(entity, Wall) and entity.type == WallType.SOLID:
                    return False
            
            # Check if there's an enemy tank in this tile
            for entity in tile.entities:
                if isinstance(entity, Tank) and teammate_tank is not None and entity.owner_id == teammate_tank.owner_id:
                    return False
                if isinstance(entity, Tank) and entity.owner_id != game_state.my_id:
                    return True
            
            tile_first: Tile = map.tiles[current_y + dx][current_x + dy]
            tile_second: Tile = map.tiles[current_y - dx][current_x - dy]
            
            for entity in tile_first.entities:
                if isinstance(entity, Tank) and teammate_tank is not None and entity.owner_id == teammate_tank.owner_id:
                    return False
                if isinstance(entity, Tank) and entity.owner_id != game_state.my_id and entity.direction in enemy_direction:
                    return True
            for entity in tile_second.entities:
                if isinstance(entity, Tank) and teammate_tank is not None and entity.owner_id == teammate_tank.owner_id:
                    return False
                if isinstance(entity, Tank) and entity.owner_id != game_state.my_id and entity.direction in enemy_direction:
                    return True
            
        # If no enemy tank was found in the line of fire
        return False
    
    def _in_zone(self, game_state: GameState) -> bool:
        my_coords: tuple[int, int] | None = self._find_my_coordinates(game_state)
        if my_coords is None:
            return False
        if (my_coords[0] >= game_state.map.zones[0].x
             and my_coords[0] < game_state.map.zones[0].x + game_state.map.zones[0].width
             and my_coords[1] >= game_state.map.zones[0].y
             and my_coords[1] < game_state.map.zones[0].y + game_state.map.zones[0].height):
            return True
    
    def defend_area(self, game_state: GameState, strategy: Strategy) -> ResponseAction:
        """Defends the area by first going to it and then randomly moving to a non-wall tile within it."""
        maybe_coords = self._find_my_coordinates(game_state)
        if maybe_coords is None:
            print("Tank not found ?!?")
            return Pass()
        x: int = maybe_coords[0]
        y: int = maybe_coords[1] 

        # Get the coordinates of the area to defend
        coords: list[int] = strategy.defend_area_coords
        area_x, area_y, area_length = coords[0], coords[1], coords[2]
        
        grid_dim_y = len(game_state.map.tiles)
        grid_dim_x = len(game_state.map.tiles[0])

        # Check if the tank is already in the area
        if area_x <= x < area_x + area_length and area_y <= y < area_y + area_length:
            # Try to cap every now and then
            if strategy.to_next_cap == 0:
                if self._in_zone(game_state):
                    strategy.to_next_cap = strategy.CAP_FREQUENCY
                    return CaptureZone()
            else:
                strategy.to_next_cap -= 1

            # Find all non-wall tiles (different from the current location) in the area
            non_wall_tiles_in_area: list[tuple[int, int]] = []
            for tile_x_in_area in range(area_x, area_x + area_length):
                for tile_y_in_area in range(area_y, area_y + area_length):
                    if 0 <= tile_x_in_area < grid_dim_x and 0 <= tile_y_in_area < grid_dim_y:
                        tile = game_state.map.tiles[tile_y_in_area][tile_x_in_area]
                        
                        is_wall_tile = False
                        if tile.entities:
                            for entity in tile.entities:
                                if isinstance(entity, Wall):
                                    is_wall_tile = True
                                    break
                        # If it's not a wall, and we're not on it already add it
                        if not is_wall_tile and (tile_x_in_area != x or tile_y_in_area != y):
                            non_wall_tiles_in_area.append((tile_x_in_area, tile_y_in_area))
            
            # Choose one of these random non-wall tiles to move to
            if non_wall_tiles_in_area:
                chosen_tile_coords = random.choice(non_wall_tiles_in_area)
                rotation_direction = RotationDirection.RIGHT # always spin CW
                return GoTo(chosen_tile_coords[0], chosen_tile_coords[1],
                               penalties=strategy.get_penalties(), turret_rotation=rotation_direction)
            else:
                # Unlikely case but if we can't move anywhere then we'll spin in place
                return Rotation(random.choice([RotationDirection.LEFT, RotationDirection.RIGHT]),
                                random.choice([RotationDirection.LEFT, RotationDirection.RIGHT]))
            
        # If not in the area, navigate to the center of the area
        center_x = area_x + area_length // 2
        center_y = area_y + area_length // 2
        return GoTo(center_x, center_y, penalties=strategy.get_penalties())