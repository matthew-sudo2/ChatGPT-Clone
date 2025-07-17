"""
Ghost entity class
"""
import pygame
import random
from game.components.position import Position

class Ghost:
    def __init__(self, x, y, color, name, tile_size):
        self.position = Position(x, y)
        self.color = color
        self.name = name
        self.tile_size = tile_size
        self.speed = 1
        self.direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.scared = False
        self.direction_timer = 0
        self.ai_mode = "chase"  # chase, scatter, frightened
        self.mode_timer = 0
        
    def update(self, game_manager):
        """Update ghost position and AI behavior"""
        self.direction_timer += 1
        self.mode_timer += 1
        
        # Update AI mode
        self._update_ai_mode(game_manager)
        
        # Get AI direction
        ai_direction = self._get_ai_direction(game_manager)
        if ai_direction:
            self.direction = ai_direction
            self.direction_timer = 0
        
        # Move ghost
        self._move(game_manager)
        
        # Handle tunnel effect
        self._handle_tunnel(game_manager)
    
    def _update_ai_mode(self, game_manager):
        """Update the ghost's AI mode based on game state"""
        if game_manager.power_mode and not self.scared:
            self.ai_mode = "frightened"
            self.scared = True
        elif not game_manager.power_mode and self.scared:
            self.ai_mode = "chase"
            self.scared = False
        elif self.mode_timer > 600:  # Switch between chase and scatter every 10 seconds
            if self.ai_mode == "chase":
                self.ai_mode = "scatter"
            elif self.ai_mode == "scatter":
                self.ai_mode = "chase"
            self.mode_timer = 0
    
    def _get_ai_direction(self, game_manager):
        """Get direction based on current AI mode"""
        if self.direction_timer < 30:  # Don't change direction too frequently
            return None
            
        possible_directions = self._get_possible_directions(game_manager)
        if not possible_directions:
            return None
        
        if self.ai_mode == "frightened":
            return self._frightened_behavior(game_manager, possible_directions)
        elif self.ai_mode == "chase":
            return self._chase_behavior(game_manager, possible_directions)
        elif self.ai_mode == "scatter":
            return self._scatter_behavior(game_manager, possible_directions)
        
        return random.choice(possible_directions)
    
    def _get_possible_directions(self, game_manager):
        """Get all valid directions the ghost can move"""
        possible_directions = []
        
        for direction in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
            next_x, next_y = self.position.x, self.position.y
            if direction == 'LEFT':
                next_x -= self.speed
            elif direction == 'RIGHT':
                next_x += self.speed
            elif direction == 'UP':
                next_y -= self.speed
            elif direction == 'DOWN':
                next_y += self.speed
            
            if self._can_move_to(next_x, next_y, game_manager):
                possible_directions.append(direction)
        
        return possible_directions
    
    def _frightened_behavior(self, game_manager, possible_directions):
        """AI behavior when ghost is scared"""
        pacman_pos = game_manager.pacman.position
        best_direction = None
        max_distance = -1
        
        for direction in possible_directions:
            next_x, next_y = self.position.x, self.position.y
            if direction == 'LEFT':
                next_x -= self.tile_size
            elif direction == 'RIGHT':
                next_x += self.tile_size
            elif direction == 'UP':
                next_y -= self.tile_size
            elif direction == 'DOWN':
                next_y += self.tile_size
            
            distance = abs(next_x - pacman_pos.x) + abs(next_y - pacman_pos.y)
            if distance > max_distance:
                max_distance = distance
                best_direction = direction
        
        return best_direction if best_direction else random.choice(possible_directions)
    
    def _chase_behavior(self, game_manager, possible_directions):
        """AI behavior when chasing Pac-Man"""
        if random.random() < 0.7:  # 70% chance to actively chase
            pacman_pos = game_manager.pacman.position
            best_direction = None
            min_distance = float('inf')
            
            for direction in possible_directions:
                next_x, next_y = self.position.x, self.position.y
                if direction == 'LEFT':
                    next_x -= self.tile_size
                elif direction == 'RIGHT':
                    next_x += self.tile_size
                elif direction == 'UP':
                    next_y -= self.tile_size
                elif direction == 'DOWN':
                    next_y += self.tile_size
                
                distance = abs(next_x - pacman_pos.x) + abs(next_y - pacman_pos.y)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction
            
            return best_direction if best_direction else random.choice(possible_directions)
        else:
            return random.choice(possible_directions)
    
    def _scatter_behavior(self, game_manager, possible_directions):
        """AI behavior when scattering (moving to corners)"""
        # Move towards corners based on ghost color
        target_x, target_y = self._get_scatter_target(game_manager)
        
        best_direction = None
        min_distance = float('inf')
        
        for direction in possible_directions:
            next_x, next_y = self.position.x, self.position.y
            if direction == 'LEFT':
                next_x -= self.tile_size
            elif direction == 'RIGHT':
                next_x += self.tile_size
            elif direction == 'UP':
                next_y -= self.tile_size
            elif direction == 'DOWN':
                next_y += self.tile_size
            
            distance = abs(next_x - target_x) + abs(next_y - target_y)
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        return best_direction if best_direction else random.choice(possible_directions)
    
    def _get_scatter_target(self, game_manager):
        """Get scatter target position based on ghost type"""
        maze_offset_x = game_manager.level_manager.maze_offset_x
        maze_offset_y = game_manager.level_manager.maze_offset_y
        maze_width = game_manager.level_manager.maze_width
        maze_height = game_manager.level_manager.maze_height
        
        if self.name == "blinky":  # Red ghost - top right
            return maze_offset_x + maze_width * self.tile_size, maze_offset_y
        elif self.name == "pinky":  # Pink ghost - top left
            return maze_offset_x, maze_offset_y
        elif self.name == "inky":  # Cyan ghost - bottom right
            return maze_offset_x + maze_width * self.tile_size, maze_offset_y + maze_height * self.tile_size
        else:  # Clyde - bottom left
            return maze_offset_x, maze_offset_y + maze_height * self.tile_size
    
    def _move(self, game_manager):
        """Move the ghost in current direction with improved collision detection"""
        next_x, next_y = self.position.x, self.position.y
        if self.direction == 'LEFT':
            next_x -= self.speed
        elif self.direction == 'RIGHT':
            next_x += self.speed
        elif self.direction == 'UP':
            next_y -= self.speed
        elif self.direction == 'DOWN':
            next_y += self.speed
        
        if self._can_move_to(next_x, next_y, game_manager):
            self.position.set_position(next_x, next_y)

    def _can_move_to(self, x, y, game_manager):
        """Check if ghost can move to the given position with improved collision detection"""
        # Check all four corners of the ghost's bounding box
        margin = 2  # Small margin to prevent getting stuck
        
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
        """Draw ghost sprite with enhanced visual effects"""
        from game.manager.spritemanager import sprite_manager
        from game.manager.stylemanager import style_manager
        
        # Determine which sprite to use
        if self.scared:
            frame = "1" if (pygame.time.get_ticks() // 200) % 2 == 0 else "2"
            sprite_name = f"ghost_scared_{frame}"
        else:
            frame = "1" if (pygame.time.get_ticks() // 200) % 2 == 0 else "2"
            color_name = self._get_color_name()
            sprite_name = f"ghost_{color_name}_{frame}"
        
        sprite = sprite_manager.get_sprite(sprite_name)
        
        if sprite:
            # Apply visual effects to sprite
            if self.scared:
                # Flashing blue effect when scared
                flash_alpha = int(abs(style_manager.animate_pulse(f"ghost_flash_{self.name}", 1.0, 6.0)) * 100 + 155)
                blue_overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                blue_overlay.fill((0, 0, 255, flash_alpha))
                sprite = sprite.copy()
                sprite.blit(blue_overlay, (0, 0))
                
                # Add trembling effect
                shake_x = int(style_manager.animate_shake(f"ghost_shake_x_{self.name}", 2, 8.0))
                shake_y = int(style_manager.animate_shake(f"ghost_shake_y_{self.name}", 2, 8.0))
            else:
                shake_x = shake_y = 0
                
                # Add subtle glow for each ghost color
                glow_surface = style_manager.apply_glow_effect(sprite, self.color, 2)
                glow_rect = glow_surface.get_rect(center=(
                    self.position.x + self.tile_size // 2,
                    self.position.y + self.tile_size // 2
                ))
                screen.blit(glow_surface, glow_rect)
            
            # Center the sprite on the tile with effects
            sprite_rect = sprite.get_rect()
            draw_x = self.position.x + (self.tile_size - sprite_rect.width) // 2 + shake_x
            draw_y = self.position.y + (self.tile_size - sprite_rect.height) // 2 + shake_y
            screen.blit(sprite, (draw_x, draw_y))
        else:
            # Enhanced fallback drawing with visual effects
            center_x = self.position.x + self.tile_size // 2
            center_y = self.position.y + self.tile_size // 2
            radius = self.tile_size // 2 - 2
            
            if self.scared:
                # Flashing blue with pulse effect
                pulse = style_manager.animate_pulse(f"ghost_pulse_{self.name}", 0.3, 6.0)
                flash_intensity = int(abs(pulse) * 100 + 155)
                color = (0, 0, flash_intensity)
                
                # Trembling effect
                shake_x = int(style_manager.animate_shake(f"ghost_shake_x_{self.name}", 2, 8.0))
                shake_y = int(style_manager.animate_shake(f"ghost_shake_y_{self.name}", 2, 8.0))
                center_x += shake_x
                center_y += shake_y
                
                # Draw glow effect for scared state
                for i in range(3):
                    glow_radius = radius + (i + 1) * 2
                    glow_alpha = 60 - i * 15
                    glow_color = (0, 0, 255, glow_alpha)
                    
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
                    screen.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
            else:
                color = self.color
                # Subtle floating animation
                float_offset = int(style_manager.animate_float(f"ghost_float_{self.name}", 2, 3.0))
                center_y += float_offset
            
            # Draw ghost body (circle top, rectangle bottom)
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            # Calculate body rectangle position
            body_x = center_x - (self.tile_size - 4) // 2
            body_y = center_y
            body_width = self.tile_size - 4
            body_height = self.tile_size // 2 - 2
            
            pygame.draw.rect(screen, color, (body_x, body_y, body_width, body_height))
            
            # Draw animated wavy bottom
            wave_offset = (pygame.time.get_ticks() // 100) % 10
            points = []
            for i in range(5):
                x_pos = body_x + i * body_width // 4
                wave_height = 4 if (i + wave_offset // 5) % 2 == 0 else 8
                y_pos = body_y + body_height - wave_height
                points.append((x_pos, y_pos))
            points.append((body_x + body_width, body_y + body_height))
            points.append((body_x, body_y + body_height))
            pygame.draw.polygon(screen, color, points)
            
            # Draw animated eyes
            eye_color = (255, 0, 0) if self.scared else (255, 255, 255)
            eye_blink = (pygame.time.get_ticks() // 2000) % 10 == 0  # Occasional blink
            if not eye_blink:
                pygame.draw.circle(screen, eye_color, (center_x - 6, center_y - 4), 2)
                pygame.draw.circle(screen, eye_color, (center_x + 6, center_y - 4), 2)

    def _get_color_name(self):
        """Get color name for sprite selection"""
        if self.color == (255, 0, 0):
            return "red"
        elif self.color == (255, 182, 193):
            return "pink"
        elif self.color == (0, 255, 255):
            return "cyan"
        elif self.color == (255, 165, 0):
            return "orange"
        else:
            return "red"  # Default

    def reset_position(self):
        """Reset ghost to starting position"""
        self.position.reset_to_start()
        self.scared = False
        self.ai_mode = "chase"
        self.mode_timer = 0
