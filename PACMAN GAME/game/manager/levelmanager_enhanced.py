"""
Enhanced Level Manager with better maze rendering using sprite assets
"""
from game.entities.dot import Dot
import pygame

class LevelManager:
    def __init__(self, tile_size, window_width, window_height):
        self.tile_size = tile_size
        self.window_width = window_width
        self.window_height = window_height
        
        # Enhanced maze layout - using the classic Pac-Man maze
        self.maze = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o####.#####.##.#####.####o#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.#####.##.#####.######",
            "     #.#####.##.#####.#     ",
            "     #.##..........##.#     ",
            "     #.##.###  ###.##.#     ",
            "######.##.#      #.##.######",
            "      ....#      #....      ",
            "######.##.#      #.##.######",
            "     #.##.########.##.#     ",
            "     #.##..........##.#     ",
            "     #.##.########.##.#     ",
            "######.##.########.##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o..##................##..o#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################",
        ]
        
        self.maze_width = len(self.maze[0])
        self.maze_height = len(self.maze)
        self.maze_offset_x = (window_width - self.maze_width * tile_size) // 2
        self.maze_offset_y = 50
        
        # Create dots
        self.dots = []
        self.total_dots = 0
        self._create_dots()
        
        # Wall colors for better visual distinction
        self.wall_color = (0, 0, 255)  # Blue walls
        self.background_color = (0, 0, 0)  # Black background
        
    def _create_dots(self):
        """Create dot entities from maze layout"""
        self.dots.clear()
        self.total_dots = 0
        
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                if cell in ['.', 'o']:
                    x = col_idx * self.tile_size + self.maze_offset_x
                    y = row_idx * self.tile_size + self.maze_offset_y
                    is_power = (cell == 'o')
                    dot = Dot(x, y, is_power)
                    self.dots.append(dot)
                    self.total_dots += 1
    
    def is_wall(self, x, y):
        """Check if position is a wall with improved bounds checking"""
        # Ensure coordinates are within bounds
        if x < 0 or y < 0:
            return True
            
        grid_x = (x - self.maze_offset_x) // self.tile_size
        grid_y = (y - self.maze_offset_y) // self.tile_size
        
        # Check bounds more carefully
        if (grid_x < 0 or grid_x >= len(self.maze[0]) or 
            grid_y < 0 or grid_y >= len(self.maze)):
            return True
        
        # Check if the cell is a wall
        cell = self.maze[grid_y][grid_x]
        return cell == '#'
    
    def get_maze_cell(self, x, y):
        """Get maze cell at position"""
        grid_x = (x - self.maze_offset_x) // self.tile_size
        grid_y = (y - self.maze_offset_y) // self.tile_size
        
        if 0 <= grid_y < len(self.maze) and 0 <= grid_x < len(self.maze[0]):
            return self.maze[grid_y][grid_x]
        return '#'
    
    def check_dot_collision(self, pacman_position):
        """Check if Pac-Man collides with any dots with improved detection"""
        collected_dots = []
        points_earned = 0
        
        # Use center point of Pac-Man for dot collision
        center_x = pacman_position.x + self.tile_size // 2
        center_y = pacman_position.y + self.tile_size // 2
        
        for dot in self.dots:
            if not dot.active:
                continue
                
            # Check collision using center points and a reasonable radius
            dot_center_x = dot.position.x + self.tile_size // 2
            dot_center_y = dot.position.y + self.tile_size // 2
            
            distance = ((center_x - dot_center_x) ** 2 + (center_y - dot_center_y) ** 2) ** 0.5
            collision_radius = self.tile_size // 2
            
            if distance <= collision_radius:
                points = dot.collect()
                points_earned += points
                collected_dots.append(dot)
        
        return points_earned, collected_dots
    
    def all_dots_collected(self):
        """Check if all dots have been collected"""
        return all(dot.is_collected() for dot in self.dots)
    
    def get_remaining_dots(self):
        """Get count of remaining dots"""
        return sum(1 for dot in self.dots if not dot.is_collected())
    
    def draw_maze(self, screen):
        """Draw the maze walls with enhanced visuals"""
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.tile_size + self.maze_offset_x
                y = row_idx * self.tile_size + self.maze_offset_y
                
                if cell == '#':
                    # Draw wall with border for better definition
                    pygame.draw.rect(screen, self.wall_color, (x, y, self.tile_size, self.tile_size))
                    # Add a slight border effect
                    pygame.draw.rect(screen, (100, 100, 255), (x, y, self.tile_size, self.tile_size), 1)
    
    def draw_dots(self, screen):
        """Draw all active dots"""
        for dot in self.dots:
            if dot.active:
                dot.draw(screen, self.tile_size)
    
    def update_dots(self):
        """Update all dots (for animation)"""
        for dot in self.dots:
            dot.update()
    
    def reset_level(self):
        """Reset level (restore all dots)"""
        self._create_dots()
    
    def get_maze_info(self):
        """Get maze information for AI"""
        return {
            'width': self.maze_width,
            'height': self.maze_height,
            'offset_x': self.maze_offset_x,
            'offset_y': self.maze_offset_y
        }
    
    def get_valid_spawn_position(self, entity_type="pacman"):
        """Get a valid spawn position for entities"""
        if entity_type == "pacman":
            # Pac-Man starts at bottom center
            return (13 * self.tile_size + self.maze_offset_x, 
                   23 * self.tile_size + self.maze_offset_y)
        elif entity_type == "ghost":
            # Ghosts start in the center area
            return (13 * self.tile_size + self.maze_offset_x, 
                   11 * self.tile_size + self.maze_offset_y)
    
    def is_tunnel_position(self, x, y):
        """Check if position is in a tunnel (for wrapping)"""
        grid_y = (y - self.maze_offset_y) // self.tile_size
        # Check if we're in the middle rows where tunnels exist
        return 10 <= grid_y <= 15
