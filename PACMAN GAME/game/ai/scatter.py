"""
Scatter AI behavior for ghosts
"""

class ScatterAI:
    @staticmethod
    def get_direction(ghost, maze_info, possible_directions, tile_size):
        """Get direction to move towards scatter corner"""
        if not possible_directions:
            return None
            
        target_x, target_y = ScatterAI.get_scatter_corner(ghost.name, maze_info, tile_size)
        
        best_direction = None
        min_distance = float('inf')
        
        for direction in possible_directions:
            next_x, next_y = ghost.position.x, ghost.position.y
            
            if direction == 'LEFT':
                next_x -= tile_size
            elif direction == 'RIGHT':
                next_x += tile_size
            elif direction == 'UP':
                next_y -= tile_size
            elif direction == 'DOWN':
                next_y += tile_size
            
            # Calculate distance to scatter corner
            distance = abs(next_x - target_x) + abs(next_y - target_y)
            
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        return best_direction
    
    @staticmethod
    def get_scatter_corner(ghost_name, maze_info, tile_size):
        """Get the scatter corner for each ghost"""
        maze_offset_x = maze_info['offset_x']
        maze_offset_y = maze_info['offset_y']
        maze_width = maze_info['width']
        maze_height = maze_info['height']
        
        if ghost_name == "blinky":  # Red ghost - top right
            return maze_offset_x + maze_width * tile_size, maze_offset_y
        elif ghost_name == "pinky":  # Pink ghost - top left
            return maze_offset_x, maze_offset_y
        elif ghost_name == "inky":  # Cyan ghost - bottom right
            return maze_offset_x + maze_width * tile_size, maze_offset_y + maze_height * tile_size
        else:  # Clyde - bottom left
            return maze_offset_x, maze_offset_y + maze_height * tile_size
