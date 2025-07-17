"""
Sprite Manager - handles loading and managing sprites from sprite sheets
"""
import pygame
import os

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.sprite_sheet = None
        self.map_assets = None
        self._load_sprite_sheets()
        self._extract_sprites()
        self.extract_map_sprites()
    
    def _load_sprite_sheets(self):
        """Load the sprite sheets"""
        # Load general sprites (Pac-Man, ghosts, etc.)
        general_sprite_path = os.path.join("assets", "sprites", "general_sprites.png")
        if os.path.exists(general_sprite_path):
            self.sprite_sheet = pygame.image.load(general_sprite_path).convert_alpha()
        else:
            # Fallback to old location
            sprite_path = os.path.join("assets", "images", "pacman_sprites.png")
            if os.path.exists(sprite_path):
                self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            else:
                self.sprite_sheet = None
        
        # Load map assets
        map_assets_path = os.path.join("assets", "sprites", "map_assets.png")
        if os.path.exists(map_assets_path):
            self.map_assets = pygame.image.load(map_assets_path).convert_alpha()
        else:
            self.map_assets = None
    
    def _extract_sprites(self):
        """Extract individual sprites from the sprite sheet"""
        if not self.sprite_sheet:
            return
        
        # Define sprite locations on the sheet (these are approximate, adjust as needed)
        sprite_definitions = {
            # Pac-Man sprites (facing different directions)
            "pacman_right_1": (456, 0, 13, 13),
            "pacman_right_2": (472, 0, 13, 13),
            "pacman_left_1": (456, 16, 13, 13),
            "pacman_left_2": (472, 16, 13, 13),
            "pacman_up_1": (456, 32, 13, 13),
            "pacman_up_2": (472, 32, 13, 13),
            "pacman_down_1": (456, 48, 13, 13),
            "pacman_down_2": (472, 48, 13, 13),
            
            # Ghost sprites
            "ghost_red_1": (456, 64, 14, 14),
            "ghost_red_2": (472, 64, 14, 14),
            "ghost_pink_1": (456, 80, 14, 14),
            "ghost_pink_2": (472, 80, 14, 14),
            "ghost_cyan_1": (456, 96, 14, 14),
            "ghost_cyan_2": (472, 96, 14, 14),
            "ghost_orange_1": (456, 112, 14, 14),
            "ghost_orange_2": (472, 112, 14, 14),
            "ghost_scared_1": (456, 128, 14, 14),
            "ghost_scared_2": (472, 128, 14, 14),
            
            # Maze elements - better coordinates for small dots
            "dot": (520, 8, 3, 3),  # Small white dot
            "power_pellet": (488, 0, 8, 8),  # Power pellet
        }
        
        for name, (x, y, width, height) in sprite_definitions.items():
            sprite_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite_surface.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            # Scale sprites to be smaller - reduced from 2x to 1.5x for character sprites
            if "pacman" in name or "ghost" in name:
                scaled_sprite = pygame.transform.scale(sprite_surface, (int(width * 1.5), int(height * 1.5)))
            else:
                # Keep dots and other elements at normal size
                scaled_sprite = pygame.transform.scale(sprite_surface, (width * 2, height * 2))
            self.sprites[name] = scaled_sprite
    
    def extract_map_sprites(self):
        """Extract map elements from the map assets"""
        if not self.map_assets:
            return
        
        # Define map sprite locations (these will need to be adjusted based on the actual sprite sheet)
        map_sprite_definitions = {
            # Wall pieces - these coordinates are examples, adjust based on actual sprite sheet
            "wall_horizontal": (0, 0, 8, 8),
            "wall_vertical": (8, 0, 8, 8),
            "wall_corner_tl": (16, 0, 8, 8),  # top-left corner
            "wall_corner_tr": (24, 0, 8, 8),  # top-right corner
            "wall_corner_bl": (32, 0, 8, 8),  # bottom-left corner
            "wall_corner_br": (40, 0, 8, 8),  # bottom-right corner
            "wall_junction_t": (48, 0, 8, 8),  # T-junction
            "wall_junction_cross": (56, 0, 8, 8),  # cross junction
            
            # Dots and pellets from map assets
            "map_dot": (188, 180, 2, 2),  # Small dot from map assets
            "map_power_pellet": (200, 180, 8, 8),  # Power pellet from map assets
            
            # Ghost house elements
            "ghost_house_door": (16, 8, 16, 8),
        }
        
        for name, (x, y, width, height) in map_sprite_definitions.items():
            sprite_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite_surface.blit(self.map_assets, (0, 0), (x, y, width, height))
            # Scale up for visibility
            scaled_sprite = pygame.transform.scale(sprite_surface, (width * 2, height * 2))
            self.sprites[name] = scaled_sprite
    
    def get_sprite(self, name):
        """Get a sprite by name"""
        return self.sprites.get(name, None)
    
    def create_fallback_sprites(self, tile_size):
        """Create fallback sprites if sprite sheet is not available"""
        if self.sprite_sheet:
            return  # We have the sprite sheet, no need for fallbacks
        
        # Create simple colored rectangles as fallbacks
        self.sprites = {}
        
        # Pac-Man (yellow circle)
        pacman_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(pacman_surface, (255, 255, 0), (tile_size//2, tile_size//2), tile_size//2 - 2)
        
        for direction in ["right", "left", "up", "down"]:
            for frame in ["1", "2"]:
                self.sprites[f"pacman_{direction}_{frame}"] = pacman_surface.copy()
        
        # Ghosts
        ghost_colors = {
            "red": (255, 0, 0),
            "pink": (255, 182, 193),
            "cyan": (0, 255, 255),
            "orange": (255, 165, 0)
        }
        
        for color_name, color in ghost_colors.items():
            ghost_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            pygame.draw.circle(ghost_surface, color, (tile_size//2, tile_size//2), tile_size//2 - 2)
            for frame in ["1", "2"]:
                self.sprites[f"ghost_{color_name}_{frame}"] = ghost_surface
        
        # Scared ghost
        scared_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(scared_surface, (0, 0, 255), (tile_size//2, tile_size//2), tile_size//2 - 2)
        for frame in ["1", "2"]:
            self.sprites[f"ghost_scared_{frame}"] = scared_surface
        
        # Dots
        dot_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(dot_surface, (255, 255, 255), (tile_size//2, tile_size//2), 2)
        self.sprites["dot"] = dot_surface
        
        # Power pellet
        power_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(power_surface, (255, 255, 255), (tile_size//2, tile_size//2), 6)
        self.sprites["power_pellet"] = power_surface

# Global sprite manager instance
sprite_manager = SpriteManager()
