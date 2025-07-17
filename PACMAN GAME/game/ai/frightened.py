"""
Frightened AI behavior for ghosts (when they're scared)
"""
import random

class FrightenedAI:
    @staticmethod
    def get_direction(ghost, pacman_position, possible_directions, tile_size):
        """Get direction to flee from Pac-Man"""
        if not possible_directions:
            return None
            
        # Try to move away from Pac-Man
        best_direction = None
        max_distance = -1
        
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
            
            # Calculate distance from Pac-Man
            distance = abs(next_x - pacman_position.x) + abs(next_y - pacman_position.y)
            
            if distance > max_distance:
                max_distance = distance
                best_direction = direction
        
        # Add some randomness to make it less predictable
        if random.random() < 0.3:  # 30% chance to move randomly
            return random.choice(possible_directions)
        
        return best_direction if best_direction else random.choice(possible_directions)
    
    @staticmethod
    def should_reverse_direction(ghost):
        """Check if ghost should reverse direction when becoming frightened"""
        # Ghosts typically reverse direction when becoming scared
        direction_opposites = {
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT',
            'UP': 'DOWN',
            'DOWN': 'UP'
        }
        return direction_opposites.get(ghost.direction, ghost.direction)
