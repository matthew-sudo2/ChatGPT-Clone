"""
Position component for game entities
"""

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def reset_to_start(self):
        self.x = self.start_x
        self.y = self.start_y
    
    def get_grid_position(self, tile_size, offset_x, offset_y):
        """Convert pixel position to grid coordinates"""
        grid_x = (self.x - offset_x) // tile_size
        grid_y = (self.y - offset_y) // tile_size
        return grid_x, grid_y
    
    def distance_to(self, other_position):
        """Calculate Manhattan distance to another position"""
        return abs(self.x - other_position.x) + abs(self.y - other_position.y)
