"""
Play state for the game
"""
import pygame
import os
from game.manager.gamemanager import GameManager
from game.manager.stylemanager import style_manager

class PlayState:
    def __init__(self, window_width, window_height, tile_size):
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = tile_size
        self.game_manager = GameManager(window_width, window_height, tile_size)
        
        # Load Press Start 2P font ONLY - no fallbacks for UI elements
        font_path = os.path.join("assets", "fonts", "PressStart2P.ttf")
        try:
            self.ui_font = pygame.font.Font(font_path, style_manager.get_font_size('sm'))
            self.font_loaded = True
        except pygame.error:
            # If Press Start 2P is not available, don't show any text
            self.font_loaded = False
        
    def handle_input(self, event):
        """Handle play state input"""
        result = self.game_manager.handle_input(event)
        
        # Check for state transitions
        if result == "quit":
            return "menu"
        elif self.game_manager.game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "menu"
        
        return None
    
    def update(self):
        """Update play state"""
        self.game_manager.update()
    
    def draw(self, screen):
        """Draw play state with animated UI overlay (Press Start 2P font only)"""
        self.game_manager.draw(screen)
        
        # Only draw UI text if Press Start 2P font is loaded
        if self.font_loaded:
            # Draw animated UI overlay
            score = self.game_manager.score_manager.get_score()
            high_score = self.game_manager.score_manager.get_high_score()
            
            # Animated score display with pulsing effect when score changes
            score_pulse = style_manager.animate_pulse("score_pulse", 0.2, 3.0)
            score_color = tuple(int(c * (0.8 + score_pulse * 0.2)) for c in style_manager.get_color('light'))
            
            score_text = self.ui_font.render(f"SCORE: {score:06d}", True, score_color)
            
            # Add subtle glow effect to score
            score_glow = style_manager.apply_glow_effect(score_text, score_color, 2)
            screen.blit(score_glow, (8, 8))
            screen.blit(score_text, (10, 10))
            
            # High score display with golden glow
            high_score_color = style_manager.get_color('primary')
            high_score_text = self.ui_font.render(f"HI-SCORE: {high_score:06d}", True, high_score_color)
            
            # Position high score on the right
            high_score_glow = style_manager.apply_glow_effect(high_score_text, high_score_color, 2)
            high_score_x = self.window_width - high_score_text.get_width() - 10
            screen.blit(high_score_glow, (high_score_x - 2, 8))
            screen.blit(high_score_text, (high_score_x, 10))
            
            # Add power mode indicator with dramatic effects
            if hasattr(self.game_manager, 'power_mode') and self.game_manager.power_mode:
                power_scale = style_manager.animate_scale("power_mode", 0.3, 4.0)
                power_color = style_manager.animate_rainbow("power_mode_color", 2.0)
                
                power_text = self.ui_font.render("POWER MODE!", True, power_color)
                
                # Scale the power mode text
                scaled_width = int(power_text.get_width() * power_scale)
                scaled_height = int(power_text.get_height() * power_scale)
                power_text = pygame.transform.scale(power_text, (scaled_width, scaled_height))
                
                power_rect = power_text.get_rect(center=(self.window_width//2, 40))
                
                # Add intense glow effect
                power_glow = style_manager.apply_glow_effect(power_text, power_color, 5)
                power_glow_rect = power_glow.get_rect(center=power_rect.center)
                screen.blit(power_glow, power_glow_rect)
                screen.blit(power_text, power_rect)
    
    def reset(self):
        """Reset the play state"""
        self.game_manager.restart_game()
