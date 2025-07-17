"""
Game Over state
"""
import pygame
import os
import math
import time
from game.manager.stylemanager import style_manager

class GameOverState:
    def __init__(self, window_width, window_height, final_score, high_score):
        self.window_width = window_width
        self.window_height = window_height
        self.final_score = final_score
        self.high_score = high_score
        
        # Load Press Start 2P font ONLY - no fallbacks
        font_path = os.path.join("assets", "fonts", "PressStart2P.ttf")
        try:
            self.font_large = pygame.font.Font(font_path, style_manager.get_font_size('xl'))
            self.font_medium = pygame.font.Font(font_path, style_manager.get_font_size('lg'))
            self.font_small = pygame.font.Font(font_path, style_manager.get_font_size('sm'))
            self.font_loaded = True
        except pygame.error:
            # If Press Start 2P is not available, don't show any text
            self.font_loaded = False
            
        self.new_high_score = final_score > high_score
        self.explosion_particles = self._generate_explosion_particles() if self.new_high_score else []
        
        # Reset animations for this state
        style_manager.reset_animation("game_over_title")
        style_manager.reset_animation("score_display")
        
    def _generate_explosion_particles(self):
        """Generate celebration particles for new high score"""
        import random
        particles = []
        for _ in range(30):
            particles.append({
                'x': self.window_width // 2,
                'y': self.window_height // 2,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-8, -2),
                'life': random.uniform(2, 4),
                'color': random.choice(['primary', 'danger', 'success', 'warning']),
                'size': random.randint(2, 6)
            })
        return particles
        
    def handle_input(self, event):
        """Handle game over input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "restart"
            elif event.key == pygame.K_m:
                return "menu"
            elif event.key == pygame.K_q:
                return "exit"
        return None
    
    def update(self):
        """Update game over animations"""
        # Update explosion particles for new high score
        if self.new_high_score:
            for particle in self.explosion_particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.2  # Gravity
                particle['life'] -= 0.016  # Assuming 60 FPS
                
                if particle['life'] <= 0:
                    self.explosion_particles.remove(particle)
    
    def draw(self, screen):
        """Draw game over screen with CSS-like styling and animations"""
        # Animated background with darker gradient
        bg_surface = pygame.Surface((self.window_width, self.window_height))
        if self.new_high_score:
            # Golden gradient for new high score
            style_manager.create_gradient(bg_surface, 
                                        (20, 10, 0),
                                        (60, 40, 0), 
                                        vertical=True)
        else:
            # Dark red gradient for game over
            style_manager.create_gradient(bg_surface, 
                                        (20, 0, 0),
                                        (60, 20, 20), 
                                        vertical=True)
        screen.blit(bg_surface, (0, 0))
        
        # Only draw text if Press Start 2P font is loaded
        if not self.font_loaded:
            return
        
        # Animated title with dramatic effects
        if self.new_high_score:
            # New high score celebration
            title_text_content = "NEW HIGH SCORE!"
            title_color = style_manager.animate_rainbow("title_rainbow", 1.5)
            title_scale = style_manager.animate_scale("title_scale", 0.3, 1.5)
            title_bounce = style_manager.animate_bounce("title_bounce", 20, 2.0)
            
            # Draw explosion particles
            for particle in self.explosion_particles:
                alpha = int(255 * max(0, particle['life'] / 2))
                color = (*style_manager.get_color(particle['color']), alpha)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
                screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
                
        else:
            # Regular game over
            title_text_content = "GAME OVER"
            title_color = style_manager.get_color('danger')
            title_scale = 1.0
            title_bounce = 0
        
        # Create and scale title
        title_text = self.font_large.render(title_text_content, True, title_color)
        if title_scale != 1.0:
            scaled_width = int(title_text.get_width() * title_scale)
            scaled_height = int(title_text.get_height() * title_scale)
            title_text = pygame.transform.scale(title_text, (scaled_width, scaled_height))
        
        title_rect = title_text.get_rect(center=(self.window_width//2, 150 - title_bounce))
        
        # Add dramatic glow effect
        glow_surface = style_manager.apply_glow_effect(title_text, title_color, 8)
        glow_rect = glow_surface.get_rect(center=title_rect.center)
        screen.blit(glow_surface, glow_rect)
        screen.blit(title_text, title_rect)
        
        # Animated score displays with slide-in effects
        score_slide = style_manager.animate_slide_in("score_slide", -300, self.window_width//2, 1.5)
        high_score_slide = style_manager.animate_slide_in("high_score_slide", self.window_width + 300, self.window_width//2, 2.0)
        
        # Final score with pulsing effect
        score_pulse = style_manager.animate_pulse("score_pulse", 0.3, 2.0)
        score_color = tuple(int(c * score_pulse) for c in style_manager.get_color('primary'))
        
        score_text = self.font_medium.render(f"FINAL SCORE: {self.final_score}", True, score_color)
        score_rect = score_text.get_rect(center=(score_slide, 280))
        
        # Add glow to score
        score_glow = style_manager.apply_glow_effect(score_text, score_color, 4)
        score_glow_rect = score_glow.get_rect(center=score_rect.center)
        screen.blit(score_glow, score_glow_rect)
        screen.blit(score_text, score_rect)
        
        # High score display
        high_score_text = self.font_medium.render(f"HIGH SCORE: {self.high_score}", True, style_manager.get_color('light'))
        high_score_rect = high_score_text.get_rect(center=(high_score_slide, 330))
        screen.blit(high_score_text, high_score_rect)
        
        # Animated control options with fade-in
        options = [
            ("PRESS R TO RESTART", 420),
            ("PRESS M FOR MENU", 460),
            ("PRESS Q TO QUIT", 500)
        ]
        
        for i, (text, y) in enumerate(options):
            fade_alpha = style_manager.animate_fade_in(f"option_fade_{i}", 2.5 + i * 0.5)
            option_color = tuple(int(c * fade_alpha) for c in style_manager.get_color('muted'))
            
            # Add subtle pulsing to options
            pulse = style_manager.animate_pulse(f"option_pulse_{i}", 0.2, 1.5 + i * 0.3)
            option_color = tuple(int(c * (0.8 + pulse * 0.2)) for c in option_color)
            
            option_text = self.font_small.render(text, True, option_color)
            option_rect = option_text.get_rect(center=(self.window_width//2, y))
            screen.blit(option_text, option_rect)
