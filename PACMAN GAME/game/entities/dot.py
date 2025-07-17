"""
Dot entity class for pellets and power pellets
"""
import pygame
from game.components.position import Position

class Dot:
    def __init__(self, x, y, is_power_pellet=False):
        self.position = Position(x, y)
        self.is_power_pellet = is_power_pellet
        self.active = True
        self.points = 50 if is_power_pellet else 10
        self.animation_timer = 0
        
    def update(self):
        """Update dot animation"""
        self.animation_timer += 1
        
    def draw(self, screen, tile_size):
        """Draw the dot with enhanced visual effects"""
        if not self.active:
            return
        
        from game.manager.spritemanager import sprite_manager
        from game.manager.stylemanager import style_manager
        
        center_x = self.position.x + tile_size // 2
        center_y = self.position.y + tile_size // 2
        
        if self.is_power_pellet:
            sprite = sprite_manager.get_sprite("power_pellet")
            if not sprite:
                sprite = sprite_manager.get_sprite("map_power_pellet")  # Try map assets
            if sprite:
                # Apply pulsing animation to power pellet
                scale = style_manager.animate_scale(f"power_pellet_{self.position.x}_{self.position.y}", 0.3, 3.0)
                width = int(sprite.get_width() * scale)
                height = int(sprite.get_height() * scale)
                scaled_sprite = pygame.transform.scale(sprite, (width, height))
                
                # Add rainbow glow effect
                rainbow_color = style_manager.animate_rainbow(f"power_glow_{self.position.x}_{self.position.y}", 2.0)
                glow_surface = style_manager.apply_glow_effect(scaled_sprite, rainbow_color, 4)
                
                # Center the enhanced sprite
                sprite_rect = scaled_sprite.get_rect()
                draw_x = center_x - sprite_rect.width // 2
                draw_y = center_y - sprite_rect.height // 2
                
                glow_rect = glow_surface.get_rect(center=(center_x, center_y))
                screen.blit(glow_surface, glow_rect)
                screen.blit(scaled_sprite, (draw_x, draw_y))
            else:
                # Enhanced fallback with rainbow glow
                rainbow_color = style_manager.animate_rainbow(f"power_color_{self.position.x}_{self.position.y}", 2.0)
                pulse = style_manager.animate_pulse(f"power_pulse_{self.position.x}_{self.position.y}", 0.4, 3.0)
                base_radius = 6
                radius = int(base_radius * (1 + pulse))
                
                # Draw glow layers
                for i in range(4):
                    glow_radius = radius + (i + 1) * 2
                    glow_alpha = 120 - i * 25
                    glow_color = (*rainbow_color, glow_alpha)
                    
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
                    screen.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
                
                # Draw main power pellet
                pygame.draw.circle(screen, rainbow_color, (center_x, center_y), radius)
        else:
            sprite = sprite_manager.get_sprite("dot")
            if not sprite:
                sprite = sprite_manager.get_sprite("map_dot")  # Try map assets
            if sprite:
                # Add subtle glow to regular dots
                glow_surface = style_manager.apply_glow_effect(sprite, (255, 255, 100), 2)
                glow_rect = glow_surface.get_rect(center=(center_x, center_y))
                screen.blit(glow_surface, glow_rect)
                
                # Center the sprite on the tile
                sprite_rect = sprite.get_rect()
                draw_x = center_x - sprite_rect.width // 2
                draw_y = center_y - sprite_rect.height // 2
                screen.blit(sprite, (draw_x, draw_y))
            else:
                # Enhanced fallback with gentle pulse and glow
                pulse = style_manager.animate_pulse(f"dot_pulse_{self.position.x}_{self.position.y}", 0.1, 4.0)
                radius = int(3 * (1 + pulse))
                
                # Subtle glow effect
                glow_color = (255, 255, 150, 80)
                glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, glow_color, (radius * 2, radius * 2), radius * 2)
                screen.blit(glow_surface, (center_x - radius * 2, center_y - radius * 2))
                
                # Main dot with slight color variation
                dot_color = (255, 255, int(200 + pulse * 55))  # Subtle yellow variation
                pygame.draw.circle(screen, dot_color, (center_x, center_y), radius)
    
    def collect(self):
        """Collect the dot"""
        if self.active:
            self.active = False
            return self.points
        return 0
    
    def is_collected(self):
        """Check if dot has been collected"""
        return not self.active
