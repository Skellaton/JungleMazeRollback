from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple

class BaseMazeSolver(ABC):
    """Abstract base class for maze solvers."""
    
    def __init__(self, maze: np.ndarray):
        """Initialize the maze solver.
        
        Args:
            maze (np.ndarray): A 2D numpy array representing the maze.
        """
        self.maze = maze
        self.height, self.width = maze.shape
    
    @abstractmethod
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze from start to end.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the solution path.
                                  Returns an empty list if no solution is found.
        """
        pass 