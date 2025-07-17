"""
Level Manager - handles maze, collisions, and level progression
"""
from game.entities.dot import Dot

class LevelManager:
    def __init__(self, tile_size, window_width, window_height):
        self.tile_size = tile_size
        self.window_width = window_width
        self.window_height = window_height
        
        # Maze layout - Classic Pac-Man design
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
            "     #.##.###--###.##.#     ",
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
        """Check if position is a wall with bounds checking"""
        # Ensure coordinates are within bounds
        if x < 0 or y < 0:
            return True
            
        grid_x = (x - self.maze_offset_x) // self.tile_size
        grid_y = (y - self.maze_offset_y) // self.tile_size
        
        # Check bounds
        if (grid_x < 0 or grid_x >= len(self.maze[0]) or 
            grid_y < 0 or grid_y >= len(self.maze)):
            return True
        
        return self.maze[grid_y][grid_x] == '#'
    
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
        """Draw the maze walls with classic Pac-Man styling"""
        import pygame
        
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.tile_size + self.maze_offset_x
                y = row_idx * self.tile_size + self.maze_offset_y
                
                if cell == '#':
                    # Classic Pac-Man blue walls
                    pygame.draw.rect(screen, (33, 33, 255), (x, y, self.tile_size, self.tile_size))
                    # Add bright blue border for that authentic look
                    pygame.draw.rect(screen, (0, 100, 255), (x, y, self.tile_size, self.tile_size), 1)
                elif cell == '-':
                    # Ghost house door - different color
                    pygame.draw.rect(screen, (255, 184, 255), (x, y, self.tile_size, self.tile_size))
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, self.tile_size, self.tile_size), 1)
    
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
