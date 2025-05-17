from hackathon_bot import *

class Soldier():
    
    def _find_my_tank(self, game_state: GameState) -> Tank | None:
        """Finds the agent in the game state."""
        for row in game_state.map.tiles:
            for tile in row:
                if tile.entities:
                    entity = tile.entities[0]
                    if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                        return entity
        return None

def should_shoot_opponent(self, game_state: GameState):
    map: Map = game_state.map
    my_tank: Tank = self._find_my_tank(game_state)        
    turret_direction: Direction = my_tank.turret.direction
    
    # Find my tank's position on the map
    my_x, my_y = None, None
    for y, row in enumerate(map.tiles):
        for x, tile in enumerate(row):
            for entity in tile.entities:
                if isinstance(entity, Tank) and entity.owner_id == game_state.my_id:
                    my_x, my_y = x, y
                    break
            if my_x is not None:
                break
        if my_x is not None:
            break
            
    
    # Define coordinate changes based on direction
    dx, dy = 0, 0
    if turret_direction == Direction.UP:
        dy = -1
    elif turret_direction == Direction.DOWN:
        dy = 1
    elif turret_direction == Direction.RIGHT:
        dx = 1
    elif turret_direction == Direction.LEFT:
        dx = -1
    
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
            if isinstance(entity, Tank) and entity.owner_id != game_state.my_id and entity.owner_id != game_state:
                
                return True
    
    # If no enemy tank was found in the line of fire
    return False