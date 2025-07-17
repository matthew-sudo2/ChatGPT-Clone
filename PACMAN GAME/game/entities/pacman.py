"""
Pac-Man entity class
"""
import pygame
import math
import time
from game.components.position import Position

class Pacman:
    def __init__(self, x, y, tile_size):
        self.position = Position(x, y)
        self.tile_size = tile_size
        self.speed = 2
        self.direction = None
        self.next_direction = None
        self.color = (255, 255, 0)  # Yellow
        self.mouth_animation = 0
        self.power_mode = False
        self.power_timer = 0
        
    def update(self, game_manager):
        """Update Pac-Man's position and state"""
        keys = pygame.key.get_pressed()
        
        # Set next direction based on input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = 'LEFT'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = 'RIGHT'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = 'UP'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = 'DOWN'

        # Try to change direction if possible
        if self.next_direction:
            next_x, next_y = self.position.x, self.position.y
            if self.next_direction == 'LEFT':
                next_x -= self.speed
            elif self.next_direction == 'RIGHT':
                next_x += self.speed
            elif self.next_direction == 'UP':
                next_y -= self.speed
            elif self.next_direction == 'DOWN':
                next_y += self.speed
            
            can_move = self._can_move_to(next_x, next_y, game_manager)
            
            if can_move:
                self.direction = self.next_direction
                self.next_direction = None

        # Move in current direction
        if self.direction:
            next_x, next_y = self.position.x, self.position.y
            if self.direction == 'LEFT':
                next_x -= self.speed
            elif self.direction == 'RIGHT':
                next_x += self.speed
            elif self.direction == 'UP':
                next_y -= self.speed
            elif self.direction == 'DOWN':
                next_y += self.speed
            
            can_move = self._can_move_to(next_x, next_y, game_manager)
            
            if can_move:
                self.position.set_position(next_x, next_y)
            else:
                self.direction = None

        # Handle tunnel effect
        self._handle_tunnel(game_manager)
        
        # Update mouth animation
        self.mouth_animation = (self.mouth_animation + 1) % 20

    def _can_move_to(self, x, y, game_manager):
        """Check if Pac-Man can move to the given position with improved collision detection"""
        # Simplified collision detection - just check center point for now
        center_x = x + self.tile_size // 2
        center_y = y + self.tile_size // 2
        
        # Check if center point is in a wall
        if game_manager.level_manager.is_wall(center_x, center_y):
            return False
        
        # Also check the four corners with a smaller margin
        margin = 1  # Reduced margin
        corners = [
            (x + margin, y + margin),  # Top-left
            (x + self.tile_size - margin, y + margin),  # Top-right
            (x + margin, y + self.tile_size - margin),  # Bottom-left
            (x + self.tile_size - margin, y + self.tile_size - margin)  # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            if game_manager.level_manager.is_wall(corner_x, corner_y):
                return False
        
        return True

    def _handle_tunnel(self, game_manager):
        """Handle screen wrapping tunnels"""
        maze_offset_x = game_manager.level_manager.maze_offset_x
        maze_width = game_manager.level_manager.maze_width
        
        if self.position.x < maze_offset_x:
            self.position.x = maze_offset_x + (maze_width - 1) * self.tile_size
        elif self.position.x > maze_offset_x + (maze_width - 1) * self.tile_size:
            self.position.x = maze_offset_x

    def draw(self, screen):
        """Draw Pac-Man with enhanced visual effects"""
        from game.manager.spritemanager import sprite_manager
        from game.manager.stylemanager import style_manager
        
        # Determine which sprite to use based on direction and animation
        sprite_name = "pacman_right_1"  # Default
        
        if self.direction:
            frame = "1" if self.mouth_animation < 10 else "2"
            sprite_name = f"pacman_{self.direction.lower()}_{frame}"
        
        sprite = sprite_manager.get_sprite(sprite_name)
        
        if sprite:
            # Apply power mode effects to sprite
            if self.power_mode:
                # Create rainbow effect for power mode
                rainbow_color = style_manager.animate_rainbow("pacman_power", 3.0)
                colored_sprite = sprite.copy()
                colored_sprite.fill(rainbow_color, special_flags=pygame.BLEND_MULT)
                sprite = colored_sprite
                
                # Add pulsing scale effect
                scale = style_manager.animate_scale("pacman_scale", 0.2, 4.0)
                width = int(sprite.get_width() * scale)
                height = int(sprite.get_height() * scale)
                sprite = pygame.transform.scale(sprite, (width, height))
                
                # Add glow effect
                glow_surface = style_manager.apply_glow_effect(sprite, rainbow_color, 3)
                glow_rect = glow_surface.get_rect(center=(
                    self.position.x + self.tile_size // 2,
                    self.position.y + self.tile_size // 2
                ))
                screen.blit(glow_surface, glow_rect)
            
            # Center the sprite on the tile
            sprite_rect = sprite.get_rect()
            draw_x = self.position.x + (self.tile_size - sprite_rect.width) // 2
            draw_y = self.position.y + (self.tile_size - sprite_rect.height) // 2
            screen.blit(sprite, (draw_x, draw_y))
        else:
            # Enhanced fallback drawing with visual effects
            center_x = self.position.x + self.tile_size // 2
            center_y = self.position.y + self.tile_size // 2
            radius = self.tile_size // 2 - 2
            
            # Power mode effects
            if self.power_mode:
                # Rainbow color cycling
                color = style_manager.animate_rainbow("pacman_color", 2.0)
                
                # Pulsing size effect
                pulse = style_manager.animate_pulse("pacman_pulse", 0.3, 4.0)
                radius = int(radius * (0.8 + pulse * 0.4))
                
                # Add glow effect
                for i in range(3):
                    glow_radius = radius + (i + 1) * 2
                    glow_alpha = 80 - i * 25
                    glow_color = (*color, glow_alpha)
                    
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
                    screen.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
            else:
                color = self.color
            
            # Draw main circle
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            # Draw animated mouth based on direction
            if self.mouth_animation < 10:  # Mouth open
                if self.direction == 'RIGHT':
                    pygame.draw.polygon(screen, (0, 0, 0), [
                        (center_x, center_y),
                        (self.position.x + self.tile_size - 2, self.position.y + 4),
                        (self.position.x + self.tile_size - 2, self.position.y + self.tile_size - 4)
                    ])
                elif self.direction == 'LEFT':
                    pygame.draw.polygon(screen, (0, 0, 0), [
                        (center_x, center_y),
                        (self.position.x + 2, self.position.y + 4),
                        (self.position.x + 2, self.position.y + self.tile_size - 4)
                    ])
                elif self.direction == 'UP':
                    pygame.draw.polygon(screen, (0, 0, 0), [
                        (center_x, center_y),
                        (self.position.x + 4, self.position.y + 2),
                        (self.position.x + self.tile_size - 4, self.position.y + 2)
                    ])
                elif self.direction == 'DOWN':
                    pygame.draw.polygon(screen, (0, 0, 0), [
                        (center_x, center_y),
                        (self.position.x + 4, self.position.y + self.tile_size - 2),
                        (self.position.x + self.tile_size - 4, self.position.y + self.tile_size - 2)
                    ])

    def reset_position(self):
        """Reset Pac-Man to starting position"""
        self.position.reset_to_start()
        self.direction = None
        self.next_direction = None
