"""
Menu state for the game
"""
import pygame
import os
import math
import time
from game.manager.stylemanager import style_manager

class MenuState:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        
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
            
        self.selected_option = 0
        self.menu_options = ["START GAME", "HIGH SCORES", "EXIT"]
        self.background_stars = self._generate_background_stars()
        
    def _generate_background_stars(self):
        """Generate animated background stars"""
        import random
        stars = []
        for _ in range(50):
            stars.append({
                'x': random.randint(0, self.window_width),
                'y': random.randint(0, self.window_height),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(1, 3)
            })
        return stars
        
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # Start Game
                    return "start_game"
                elif self.selected_option == 1:  # High Scores
                    return "high_scores"
                elif self.selected_option == 2:  # Exit
                    return "exit"
        return None
    
    def update(self):
        """Update menu animations"""
        # Update background stars
        for star in self.background_stars:
            star['y'] += star['speed']
            if star['y'] > self.window_height:
                star['y'] = 0
                import random
                star['x'] = random.randint(0, self.window_width)
    
    def draw(self, screen):
        """Draw menu with CSS-like styling and animations"""
        # Animated gradient background
        bg_surface = pygame.Surface((self.window_width, self.window_height))
        style_manager.create_gradient(bg_surface, 
                                    style_manager.get_color('dark'),
                                    (20, 20, 60), 
                                    vertical=True)
        screen.blit(bg_surface, (0, 0))
        
        # Draw animated background stars
        for star in self.background_stars:
            pulse = style_manager.animate_pulse(f"star_{id(star)}", 0.5, 3.0)
            color = tuple(int(c * pulse) for c in style_manager.get_color('light'))
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])
        
        # Only draw text if Press Start 2P font is loaded
        if not self.font_loaded:
            return
        
        # Animated title with rainbow effect and bounce
        title_bounce = style_manager.animate_bounce("title", 15, 1.5)
        title_color = style_manager.animate_rainbow("title", 0.5)
        title_scale = style_manager.animate_scale("title", 0.1, 1.0)
        
        # Create title with scaling
        title_text = self.font_large.render("PAC-MAN", True, title_color)
        scaled_width = int(title_text.get_width() * title_scale)
        scaled_height = int(title_text.get_height() * title_scale)
        title_text = pygame.transform.scale(title_text, (scaled_width, scaled_height))
        
        title_rect = title_text.get_rect(center=(self.window_width//2, 120 - title_bounce))
        
        # Add glow effect to title
        glow_surface = style_manager.apply_glow_effect(title_text, title_color, 5)
        glow_rect = glow_surface.get_rect(center=title_rect.center)
        screen.blit(glow_surface, glow_rect)
        screen.blit(title_text, title_rect)
        
        # Animated menu options with slide-in effect
        start_y = 280
        for i, option in enumerate(self.menu_options):
            # Slide-in animation for each option
            slide_x = style_manager.animate_slide_in(f"option_{i}", 
                                                   -200, self.window_width//2, 
                                                   1.0 + i * 0.3)
            
            if i == self.selected_option:
                # Selected option styling
                color = style_manager.get_color('primary')
                pulse = style_manager.animate_pulse(f"selected_{i}", 0.3, 4.0)
                color = tuple(int(c * pulse) for c in color)
                
                # Animated selector with rotation
                selector_angle = style_manager.animate_rotate(f"selector_{i}", 2.0)
                selector_size = 8 + style_manager.animate_pulse(f"selector_size_{i}", 0.3, 3.0) * 4
                
                # Draw rotating selector
                center_x = slide_x - 60
                center_y = start_y + i * 60 + 12
                
                # Create diamond selector
                points = []
                for angle in range(0, 360, 90):
                    rad = math.radians(angle + selector_angle)
                    x = center_x + math.cos(rad) * selector_size
                    y = center_y + math.sin(rad) * selector_size
                    points.append((x, y))
                
                pygame.draw.polygon(screen, style_manager.get_color('primary'), points)
                
            else:
                # Unselected option styling with fade-in
                alpha = style_manager.animate_fade_in(f"option_fade_{i}", 2.0)
                color = tuple(int(c * alpha) for c in style_manager.get_color('light'))
                
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(slide_x, start_y + i * 60))
            
            # Add subtle glow to selected option
            if i == self.selected_option:
                glow = style_manager.apply_glow_effect(option_text, color, 3)
                glow_rect = glow.get_rect(center=option_rect.center)
                screen.blit(glow, glow_rect)
            
            screen.blit(option_text, option_rect)
        
        # Animated instructions with typewriter effect
        instruction_text = style_manager.animate_text_typewriter("instructions", 
                                                               "USE ARROW KEYS AND ENTER", 8)
        if instruction_text:
            pulse = style_manager.animate_pulse("instruction_pulse", 0.4, 2.0)
            color = tuple(int(c * pulse) for c in style_manager.get_color('info'))
            
            inst_surface = self.font_small.render(instruction_text, True, color)
            inst_rect = inst_surface.get_rect(center=(self.window_width//2, self.window_height - 100))
            screen.blit(inst_surface, inst_rect)
        
        # Floating particles effect
        self._draw_floating_particles(screen)
    
    def _draw_floating_particles(self, screen):
        """Draw floating Pac-Man dots as particles"""
        import random
        
        for i in range(10):
            # Create floating dots with random movement
            time_offset = i * 0.5
            x_float = math.sin(time.time() * 0.5 + time_offset) * 50
            y_float = math.cos(time.time() * 0.3 + time_offset) * 30
            
            base_x = 100 + (i % 3) * 200
            base_y = 200 + (i // 3) * 150
            
            particle_x = base_x + x_float
            particle_y = base_y + y_float
            
            # Ensure particles stay on screen
            if 0 <= particle_x <= self.window_width and 0 <= particle_y <= self.window_height:
                pulse = style_manager.animate_pulse(f"particle_{i}", 0.5, 2.0 + i * 0.1)
                size = int(3 + pulse * 2)
                alpha = int(128 + pulse * 127)
                
                color = (*style_manager.get_color('primary'), alpha)
                
                # Create temporary surface for alpha blending
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size, size), size)
                screen.blit(particle_surface, (particle_x - size, particle_y - size))
