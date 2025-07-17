"""
Test script to verify collision detection improvements
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.manager.levelmanager import LevelManager

def test_collision_detection():
    """Test the collision detection system"""
    print("Testing collision detection...")
    
    # Create a level manager
    level_manager = LevelManager(20, 800, 600)
    
    # Test some wall positions
    wall_x = level_manager.maze_offset_x
    wall_y = level_manager.maze_offset_y
    
    print(f"Testing wall at ({wall_x}, {wall_y}): {level_manager.is_wall(wall_x, wall_y)}")
    
    # Test some non-wall positions
    open_x = level_manager.maze_offset_x + 20
    open_y = level_manager.maze_offset_y + 20
    
    print(f"Testing open space at ({open_x}, {open_y}): {level_manager.is_wall(open_x, open_y)}")
    
    # Test bounds
    print(f"Testing negative coordinates: {level_manager.is_wall(-10, -10)}")
    print(f"Testing out of bounds: {level_manager.is_wall(9999, 9999)}")
    
    print("Collision detection test completed!")

if __name__ == "__main__":
    test_collision_detection()
