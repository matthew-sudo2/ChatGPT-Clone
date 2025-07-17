"""
Pac-Man Game - Main Entry Point
A modular Pac-Man game implementation using pygame
"""

import pygame
import sys
from game.states.menu import MenuState
from game.states.play import PlayState
from game.states.gameover import GameOverState

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 20
FPS = 60

class PacManGame:
    def __init__(self):
        """Initialize the main game application"""
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pac-Man Game - Modular Edition")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.current_state = "menu"
        self.states = {}
        self._initialize_states()
        
        # Game running flag
        self.running = True
        
    def _initialize_states(self):
        """Initialize all game states"""
        self.states["menu"] = MenuState(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.states["play"] = PlayState(WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE)
        # GameOver state is created dynamically when needed
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Pass events to current state
            state_result = None
            if self.current_state in self.states:
                state_result = self.states[self.current_state].handle_input(event)
            
            # Handle state transitions
            self._handle_state_transition(state_result)
    
    def _handle_state_transition(self, state_result):
        """Handle transitions between game states"""
        if state_result is None:
            return
            
        if state_result == "start_game":
            self.current_state = "play"
            self.states["play"].reset()
            
        elif state_result == "menu":
            self.current_state = "menu"
            
        elif state_result == "exit" or state_result == "quit":
            self.running = False
            
        elif state_result == "restart":
            self.states["play"].reset()
            self.current_state = "play"
            
        elif state_result == "game_over":
            # Create game over state with current scores
            play_state = self.states["play"]
            final_score = play_state.game_manager.score_manager.get_score()
            high_score = play_state.game_manager.score_manager.get_high_score()
            
            self.states["game_over"] = GameOverState(WINDOW_WIDTH, WINDOW_HEIGHT, 
                                                   final_score, high_score)
            self.current_state = "game_over"
            
        elif state_result == "high_scores":
            # TODO: Implement high scores state
            pass
    
    def update(self):
        """Update current game state"""
        if self.current_state in self.states:
            self.states[self.current_state].update()
            
        # Check if play state transitioned to game over
        if (self.current_state == "play" and 
            self.states["play"].game_manager.game_state == "game_over"):
            self._handle_state_transition("game_over")
    
    def draw(self):
        """Draw current game state"""
        if self.current_state in self.states:
            self.states[self.current_state].draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        self.quit()
    
    def quit(self):
        """Clean up and quit the game"""
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        game = PacManGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
