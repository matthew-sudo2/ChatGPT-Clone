"""
Score Manager - handles scoring and statistics
"""

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.dots_eaten = 0
        self.ghosts_eaten = 0
        self.lives = 3
        self.level = 1
        
        # Point values
        self.DOT_POINTS = 10
        self.POWER_PELLET_POINTS = 50
        self.GHOST_POINTS = 200
        self.FRUIT_POINTS = 100
        
        # Multipliers
        self.ghost_multiplier = 1
        
    def add_dot_score(self):
        """Add score for eating a dot"""
        self.score += self.DOT_POINTS
        self.dots_eaten += 1
        
    def add_power_pellet_score(self):
        """Add score for eating a power pellet"""
        self.score += self.POWER_PELLET_POINTS
        self.dots_eaten += 1
        self.ghost_multiplier = 1  # Reset ghost multiplier
        
    def add_ghost_score(self):
        """Add score for eating a ghost"""
        points = self.GHOST_POINTS * self.ghost_multiplier
        self.score += points
        self.ghosts_eaten += 1
        self.ghost_multiplier *= 2  # Double the points for next ghost
        return points
        
    def add_fruit_score(self):
        """Add score for eating fruit"""
        self.score += self.FRUIT_POINTS
        
    def lose_life(self):
        """Decrease lives count"""
        self.lives -= 1
        return self.lives <= 0  # Return True if game over
        
    def gain_life(self):
        """Increase lives count (bonus life)"""
        self.lives += 1
        
    def next_level(self):
        """Advance to next level"""
        self.level += 1
        self.ghost_multiplier = 1
        
    def reset_game(self):
        """Reset game statistics"""
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.dots_eaten = 0
        self.ghosts_eaten = 0
        self.lives = 3
        self.level = 1
        self.ghost_multiplier = 1
        
    def get_score(self):
        """Get current score"""
        return self.score
        
    def get_high_score(self):
        """Get high score"""
        return self.high_score
        
    def get_lives(self):
        """Get remaining lives"""
        return self.lives
        
    def get_level(self):
        """Get current level"""
        return self.level
        
    def check_bonus_life(self):
        """Check if player earned a bonus life (every 10,000 points)"""
        if self.score > 0 and self.score % 10000 == 0:
            return True
        return False
