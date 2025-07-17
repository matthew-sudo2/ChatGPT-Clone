"""
Chase AI behavior for ghosts
"""

class ChaseAI:
    @staticmethod
    def get_direction(ghost, pacman_position, possible_directions, tile_size):
        """Get the best direction to chase Pac-Man"""
        if not possible_directions:
            return None
            
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
            
            # Calculate distance to Pac-Man
            distance = abs(next_x - pacman_position.x) + abs(next_y - pacman_position.y)
            
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        return best_direction
    
    @staticmethod
    def get_target_position(ghost_name, ghost_position, pacman_position, pacman_direction, tile_size):
        """Get target position based on ghost personality"""
        if ghost_name == "blinky":
            # Red ghost: Direct chase
            return pacman_position.x, pacman_position.y
        elif ghost_name == "pinky":
            # Pink ghost: Ambush (target 4 tiles ahead of Pac-Man)
            offset = 4 * tile_size
            target_x, target_y = pacman_position.x, pacman_position.y
            
            if pacman_direction == 'UP':
                target_y -= offset
            elif pacman_direction == 'DOWN':
                target_y += offset
            elif pacman_direction == 'LEFT':
                target_x -= offset
            elif pacman_direction == 'RIGHT':
                target_x += offset
                
            return target_x, target_y
        elif ghost_name == "inky":
            # Cyan ghost: Indirect chase (complex targeting)
            # Simplified: target position opposite to red ghost
            return pacman_position.x, pacman_position.y
        else:  # clyde
            # Orange ghost: Chase when far, scatter when close
            distance = abs(ghost_position.x - pacman_position.x) + abs(ghost_position.y - pacman_position.y)
            if distance > 8 * tile_size:
                return pacman_position.x, pacman_position.y
            else:
                # Scatter to corner
                return 0, 600  # Bottom left corner
