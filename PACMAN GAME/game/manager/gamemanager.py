"""
Game Manager - Main game logic coordinator
"""
import pygame
from game.entities.pacman import Pacman
from game.entities.ghost import Ghost
from game.manager.scoremanager import ScoreManager
from game.manager.levelmanager import LevelManager

class GameManager:
    def __init__(self, window_width, window_height, tile_size):
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = tile_size
        
        # Initialize sprite manager with fallback sprites
        from game.manager.spritemanager import sprite_manager
        sprite_manager.create_fallback_sprites(tile_size)
        
        # Initialize managers
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager(tile_size, window_width, window_height)
        
        # Game state
        self.game_state = "playing"  # playing, paused, game_over, won
        self.power_mode = False
        self.power_timer = 0
        self.power_duration = 300  # 5 seconds at 60 FPS
        
        # Initialize entities
        self._create_entities()
        
    def _create_entities(self):
        """Create game entities"""
        # Create Pac-Man - try a position we know is safe (center of bottom corridor)
        start_x = 13 * self.tile_size + self.level_manager.maze_offset_x
        start_y = 24 * self.tile_size + self.level_manager.maze_offset_y  # Changed from 23 to 24
        
        # Check if starting position is valid
        if self.level_manager.is_wall(start_x, start_y):
            # Try alternative position
            start_y = 20 * self.tile_size + self.level_manager.maze_offset_y
        
        self.pacman = Pacman(start_x, start_y, self.tile_size)
        
        # Create ghosts
        self.ghosts = [
            Ghost(13 * self.tile_size + self.level_manager.maze_offset_x, 
                  11 * self.tile_size + self.level_manager.maze_offset_y, 
                  (255, 0, 0), "blinky", self.tile_size),
            Ghost(13 * self.tile_size + self.level_manager.maze_offset_x, 
                  13 * self.tile_size + self.level_manager.maze_offset_y, 
                  (255, 182, 193), "pinky", self.tile_size),
            Ghost(12 * self.tile_size + self.level_manager.maze_offset_x, 
                  13 * self.tile_size + self.level_manager.maze_offset_y, 
                  (0, 255, 255), "inky", self.tile_size),
            Ghost(14 * self.tile_size + self.level_manager.maze_offset_x, 
                  13 * self.tile_size + self.level_manager.maze_offset_y, 
                  (255, 165, 0), "clyde", self.tile_size)
        ]
    
    def update(self):
        """Update game logic"""
        if self.game_state != "playing":
            return
        
        # Update power mode timer
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for ghost in self.ghosts:
                    ghost.scared = False
        
        # Update entities
        self.pacman.update(self)
        for ghost in self.ghosts:
            ghost.update(self)
        
        # Update dots
        self.level_manager.update_dots()
        
        # Check collisions
        self._check_dot_collisions()
        self._check_ghost_collisions()
        
        # Check win/lose conditions
        self._check_win_condition()
    
    def _check_dot_collisions(self):
        """Check and handle dot collisions"""
        points, collected_dots = self.level_manager.check_dot_collision(self.pacman.position)
        
        for dot in collected_dots:
            if dot.is_power_pellet:
                self.score_manager.add_power_pellet_score()
                self._activate_power_mode()
            else:
                self.score_manager.add_dot_score()
    
    def _check_ghost_collisions(self):
        """Check and handle ghost collisions"""
        for ghost in self.ghosts:
            if (abs(self.pacman.position.x - ghost.position.x) < self.tile_size and 
                abs(self.pacman.position.y - ghost.position.y) < self.tile_size):
                
                if ghost.scared:
                    # Eat the ghost
                    points = self.score_manager.add_ghost_score()
                    ghost.reset_position()
                    ghost.scared = False
                else:
                    # Pac-Man dies
                    game_over = self.score_manager.lose_life()
                    if game_over:
                        self.game_state = "game_over"
                    else:
                        self.pacman.reset_position()
                        # Reset ghosts
                        for g in self.ghosts:
                            g.reset_position()
    
    def _check_win_condition(self):
        """Check if level is completed"""
        if self.level_manager.all_dots_collected():
            self.score_manager.next_level()
            self.level_manager.reset_level()
            self._reset_entities_for_new_level()
    
    def _activate_power_mode(self):
        """Activate power mode"""
        self.power_mode = True
        self.power_timer = self.power_duration
        
        # Make all ghosts scared
        for ghost in self.ghosts:
            ghost.scared = True
            ghost.ai_mode = "frightened"
    
    def _reset_entities_for_new_level(self):
        """Reset entities for new level"""
        self.pacman.reset_position()
        for ghost in self.ghosts:
            ghost.reset_position()
        self.power_mode = False
        self.power_timer = 0
    
    def handle_input(self, event):
        """Handle game input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if self.game_state == "playing":
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    self.game_state = "playing"
            elif event.key == pygame.K_r and self.game_state == "game_over":
                self.restart_game()
            elif event.key == pygame.K_q and self.game_state == "game_over":
                return "quit"
        return None
    
    def restart_game(self):
        """Restart the game"""
        self.score_manager.reset_game()
        self.level_manager.reset_level()
        self._reset_entities_for_new_level()
        self.game_state = "playing"
    
    def draw(self, screen):
        """Draw all game elements"""
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw maze and dots
        self.level_manager.draw_maze(screen)
        self.level_manager.draw_dots(screen)
        
        # Draw entities
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
        
        # Draw UI
        self._draw_ui(screen)
        
        # Draw game state overlays
        if self.game_state == "paused":
            self._draw_pause_screen(screen)
        elif self.game_state == "game_over":
            self._draw_game_over_screen(screen)
    
    def _draw_ui(self, screen):
        """Draw game UI - removed to only use Press Start 2P font"""
        # UI is now handled by the play state with Press Start 2P font
        pass
    
    def _draw_pause_screen(self, screen):
        """Draw pause overlay - removed to only use Press Start 2P font"""
        # Pause indication removed since it doesn't use Press Start 2P font
        pass
    
    def _draw_game_over_screen(self, screen):
        """Draw game over overlay - removed to only use Press Start 2P font"""
        # Game over screen is now handled by GameOverState with Press Start 2P font
        pass
