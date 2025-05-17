from hackathon_bot import *

class Soldier():
    def go_to_zone(self, game_state: GameState, x: int, y: int, costs = None) -> ResponseAction:
        """ Goes to the nearest unoccupied tile in the zone to the given position using Manhattan distance.
        Assumes there is always exactly one zone.
        """

        zones = game_state.map.zones
        single_zone_obj = zones[0]
        
        # The rest of the logic operates on this single_zone_obj
        nearest_unoccupied_tile_coords = None
        min_dist_to_unoccupied_tile = float('inf')
        
        # Assuming map.tiles is a list of lists (rows then columns)
        # and game_state.map.tiles[y][x] is the correct access pattern.
        # grid_dim_y = len(game_state.map.tiles)
        # grid_dim_x = len(game_state.map.tiles[0]) if grid_dim_y > 0 else 0
        # Using server_settings.grid_dimension for a square map as per hackathon_bot.protocols.ServerSettings
        grid_dim = game_state.map


        for tile_x_in_zone in range(single_zone_obj.x, single_zone_obj.x + single_zone_obj.width):
            for tile_y_in_zone in range(single_zone_obj.y, single_zone_obj.y + single_zone_obj.height):
                # Ensure tile coordinates are within map bounds
                if True:
                    # Corrected tile access: game_state.map.tiles[y][x]
                    tile = game_state.map.tiles[tile_y_in_zone][tile_x_in_zone] 
                    if not tile.entities: # Check if tile is unoccupied
                        distance_to_tile = abs(tile_x_in_zone - x) + abs(tile_y_in_zone - y)
                        if distance_to_tile < min_dist_to_unoccupied_tile:
                            min_dist_to_unoccupied_tile = distance_to_tile
                            nearest_unoccupied_tile_coords = (tile_x_in_zone, tile_y_in_zone)
        
        if nearest_unoccupied_tile_coords:
            # Use provided costs or default if None
            action_costs = costs if costs is not None else GoTo.Costs()
            return GoTo(nearest_unoccupied_tile_coords[0], nearest_unoccupied_tile_coords[1], costs=action_costs)

        return Pass()
