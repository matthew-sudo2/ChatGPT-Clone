import pygame
import os

# This script creates simple pixel art sprites for the Pac-Man game
# Run this to generate PNG files for custom sprites

def create_pacman_sprite():
    """Create a simple Pac-Man sprite"""
    size = 20
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Yellow circle
    pygame.draw.circle(surface, (255, 255, 0), (size//2, size//2), size//2 - 1)
    
    # Mouth (black triangle)
    mouth_points = [
        (size//2, size//2),
        (size - 2, 4),
        (size - 2, size - 4)
    ]
    pygame.draw.polygon(surface, (0, 0, 0), mouth_points)
    
    return surface

def create_ghost_sprite(color):
    """Create a ghost sprite with the given color"""
    size = 20
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Ghost body (circle top, rectangle bottom)
    pygame.draw.circle(surface, color, (size//2, size//2), size//2 - 1)
    pygame.draw.rect(surface, color, (1, size//2, size - 2, size//2 - 1))
    
    # Wavy bottom
    points = []
    for i in range(5):
        x_pos = 1 + i * (size - 2) // 4
        y_pos = size - 1 if i % 2 == 0 else size - 5
        points.append((x_pos, y_pos))
    points.append((size - 1, size - 1))
    points.append((1, size - 1))
    pygame.draw.polygon(surface, color, points)
    
    # Eyes
    pygame.draw.circle(surface, (255, 255, 255), (6, 8), 2)
    pygame.draw.circle(surface, (255, 255, 255), (size - 6, 8), 2)
    pygame.draw.circle(surface, (0, 0, 0), (6, 8), 1)
    pygame.draw.circle(surface, (0, 0, 0), (size - 6, 8), 1)
    
    return surface

def create_dot_sprite():
    """Create a small dot sprite"""
    size = 20
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), 2)
    return surface

def create_power_pellet_sprite():
    """Create a power pellet sprite"""
    size = 20
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), 6)
    return surface

def create_wall_sprite():
    """Create a wall sprite"""
    size = 20
    surface = pygame.Surface((size, size))
    surface.fill((0, 0, 255))  # Blue wall
    return surface

def main():
    pygame.init()
    
    # Create assets directory if it doesn't exist
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Create and save sprites
    pacman = create_pacman_sprite()
    pygame.image.save(pacman, os.path.join(assets_dir, "pacman.png"))
    
    # Ghost sprites
    colors = {
        "red": (255, 0, 0),
        "pink": (255, 182, 193),
        "cyan": (0, 255, 255),
        "orange": (255, 165, 0)
    }
    
    for name, color in colors.items():
        ghost = create_ghost_sprite(color)
        pygame.image.save(ghost, os.path.join(assets_dir, f"ghost_{name}.png"))
    
    # Other sprites
    dot = create_dot_sprite()
    pygame.image.save(dot, os.path.join(assets_dir, "dot.png"))
    
    power_pellet = create_power_pellet_sprite()
    pygame.image.save(power_pellet, os.path.join(assets_dir, "power_pellet.png"))
    
    wall = create_wall_sprite()
    pygame.image.save(wall, os.path.join(assets_dir, "wall.png"))
    
    print("Sprites created successfully in the assets folder!")
    pygame.quit()

if __name__ == "__main__":
    main()
