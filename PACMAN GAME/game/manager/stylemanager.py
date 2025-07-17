"""
Style Manager - CSS-like styling system for Pygame
Provides animations, transitions, and visual effects
"""
import pygame
import math
import time

class StyleManager:
    def __init__(self):
        self.animations = {}
        self.transitions = {}
        self.effects = {}
        self.start_time = time.time()
        
        # CSS-like color palette
        self.colors = {
            'primary': (255, 255, 0),      # Pac-Man Yellow
            'secondary': (33, 33, 255),    # Maze Blue
            'danger': (255, 0, 0),         # Red
            'success': (0, 255, 0),        # Green
            'warning': (255, 165, 0),      # Orange
            'info': (0, 255, 255),         # Cyan
            'light': (255, 255, 255),      # White
            'dark': (0, 0, 0),             # Black
            'muted': (128, 128, 128),      # Gray
            'ghost_red': (255, 0, 0),
            'ghost_pink': (255, 184, 255),
            'ghost_cyan': (0, 255, 255),
            'ghost_orange': (255, 165, 0),
        }
        
        # CSS-like font sizes
        self.font_sizes = {
            'xs': 12,
            'sm': 16,
            'md': 20,
            'lg': 24,
            'xl': 32,
            'xxl': 48
        }
        
    def get_color(self, color_name):
        """Get color by name like CSS"""
        return self.colors.get(color_name, (255, 255, 255))
    
    def get_font_size(self, size_name):
        """Get font size by name like CSS"""
        return self.font_sizes.get(size_name, 16)
    
    def animate_pulse(self, element_id, intensity=0.3, speed=2.0):
        """CSS-like pulse animation"""
        current_time = time.time() - self.start_time
        pulse = abs(math.sin(current_time * speed)) * intensity + (1 - intensity)
        return pulse
    
    def animate_bounce(self, element_id, height=10, speed=3.0):
        """CSS-like bounce animation"""
        current_time = time.time() - self.start_time
        bounce = abs(math.sin(current_time * speed)) * height
        return bounce
    
    def animate_fade_in(self, element_id, duration=1.0):
        """CSS-like fade-in animation"""
        if element_id not in self.animations:
            self.animations[element_id] = time.time()
        
        elapsed = time.time() - self.animations[element_id]
        alpha = min(elapsed / duration, 1.0)
        return alpha
    
    def animate_slide_in(self, element_id, start_x, end_x, duration=1.0):
        """CSS-like slide-in animation"""
        if element_id not in self.animations:
            self.animations[element_id] = time.time()
        
        elapsed = time.time() - self.animations[element_id]
        progress = min(elapsed / duration, 1.0)
        
        # Ease-out animation
        progress = 1 - (1 - progress) ** 3
        
        current_x = start_x + (end_x - start_x) * progress
        return current_x
    
    def animate_scale(self, element_id, scale_factor=0.2, speed=2.0):
        """CSS-like scale animation"""
        current_time = time.time() - self.start_time
        scale = 1 + math.sin(current_time * speed) * scale_factor
        return scale
    
    def animate_rotate(self, element_id, speed=1.0):
        """CSS-like rotation animation"""
        current_time = time.time() - self.start_time
        angle = (current_time * speed * 180) % 360
        return angle
    
    def animate_rainbow(self, element_id, speed=1.0):
        """Animated rainbow colors"""
        current_time = time.time() - self.start_time
        hue = (current_time * speed * 60) % 360
        
        # Convert HSV to RGB
        h = hue / 60
        c = 255
        x = c * (1 - abs((h % 2) - 1))
        
        if 0 <= h < 1:
            return (c, x, 0)
        elif 1 <= h < 2:
            return (x, c, 0)
        elif 2 <= h < 3:
            return (0, c, x)
        elif 3 <= h < 4:
            return (0, x, c)
        elif 4 <= h < 5:
            return (x, 0, c)
        else:
            return (c, 0, x)
    
    def create_gradient(self, surface, start_color, end_color, vertical=True):
        """Create CSS-like gradients"""
        w, h = surface.get_size()
        
        for i in range(h if vertical else w):
            ratio = i / (h if vertical else w)
            
            color = [
                int(start_color[j] + (end_color[j] - start_color[j]) * ratio)
                for j in range(3)
            ]
            
            if vertical:
                pygame.draw.line(surface, color, (0, i), (w, i))
            else:
                pygame.draw.line(surface, color, (i, 0), (i, h))
    
    def apply_glow_effect(self, surface, color, intensity=3):
        """CSS-like glow/box-shadow effect"""
        w, h = surface.get_size()
        glow_surface = pygame.Surface((w + intensity * 2, h + intensity * 2), pygame.SRCALPHA)
        
        for i in range(intensity):
            alpha = 255 // (i + 1)
            glow_color = (*color, alpha)
            pygame.draw.rect(glow_surface, glow_color, 
                           (intensity - i, intensity - i, w + i * 2, h + i * 2))
        
        return glow_surface
    
    def animate_text_typewriter(self, element_id, full_text, speed=10):
        """CSS-like typewriter animation"""
        if element_id not in self.animations:
            self.animations[element_id] = time.time()
        
        elapsed = time.time() - self.animations[element_id]
        chars_shown = int(elapsed * speed)
        
        return full_text[:min(chars_shown, len(full_text))]
    
    def reset_animation(self, element_id):
        """Reset animation for an element"""
        if element_id in self.animations:
            del self.animations[element_id]
    
    def animate_shake(self, element_id, intensity=2, speed=6.0):
        """Create shake/trembling animation effect"""
        import random
        current_time = time.time()
        
        # Use sine wave with random offset for shake effect
        base_shake = math.sin(current_time * speed) * intensity
        random_offset = (random.random() - 0.5) * intensity * 0.5
        
        return base_shake + random_offset
    
    def animate_float(self, element_id, amplitude=3, speed=2.0):
        """Create gentle floating animation effect"""
        current_time = time.time()
        
        # Use sine wave for smooth floating motion
        float_offset = math.sin(current_time * speed) * amplitude
        
        return float_offset

# Global style manager instance
style_manager = StyleManager()
