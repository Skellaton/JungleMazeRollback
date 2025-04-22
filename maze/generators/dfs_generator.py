import numpy as np
import random
from typing import Set, Tuple
from .base_generator import BaseMazeGenerator

class DFSMazeGenerator(BaseMazeGenerator):
    """Maze generator using Depth-First Search algorithm."""
    
    def __init__(self, width: int, height: int):
        """Initialize the DFS maze generator.
        
        Args:
            width (int): The width of the maze (in cells).
            height (int): The height of the maze (in cells).
        """
        self.width = width
        self.height = height
        self.maze = np.zeros((height * 2 + 1, width * 2 + 1), dtype=int)
        self.visited = set()
        
    def generate(self) -> np.ndarray:
        """Generate a new maze using Depth-First Search algorithm.
        
        Returns:
            np.ndarray: A 2D numpy array where 0 represents paths and 1 represents walls.
        """
        # Initialize maze with walls
        self.maze.fill(1)
        self.visited.clear()
        
        # Start from a random cell
        start_x = random.randrange(0, self.width) * 2 + 1
        start_y = random.randrange(0, self.height) * 2 + 1
        self.maze[start_y, start_x] = 0
        
        # Start DFS from the initial cell
        self._dfs(start_x, start_y)
        
        # Set start and end points
        self.maze[1, 1] = 0  # Start point
        self.maze[-2, -2] = 0  # End point
        
        return self.maze
    
    def _dfs(self, x: int, y: int) -> None:
        """Perform Depth-First Search to generate the maze.
        
        Args:
            x (int): Current x coordinate.
            y (int): Current y coordinate.
        """
        self.visited.add((x, y))
        
        # Define possible directions (right, down, left, up)
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check if the new position is valid and not visited
            if (0 < new_x < self.width * 2 and 
                0 < new_y < self.height * 2 and 
                (new_x, new_y) not in self.visited):
                
                # Remove wall between current and new cell
                wall_x = x + dx // 2
                wall_y = y + dy // 2
                self.maze[wall_y, wall_x] = 0
                self.maze[new_y, new_x] = 0
                
                self._dfs(new_x, new_y)
    
    def get_start_end_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the start and end points of the maze.
        
        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the start and end coordinates.
        """
        return ((1, 1), (self.maze.shape[1] - 2, self.maze.shape[0] - 2)) 