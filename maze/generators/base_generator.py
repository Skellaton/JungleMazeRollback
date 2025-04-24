from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple

class BaseMazeGenerator(ABC):
    """Abstract base class for maze generators."""
    
    def __init__(self, width: int, height: int):
        """Initialize the maze generator with dimensions.
        
        Args:
            width (int): The width of the maze (in cells).
            height (int): The height of the maze (in cells).
        """
        self.width = width
        self.height = height
        # Initialize maze with walls (1) and paths (0)
        self.maze = np.ones((height * 2 + 1, width * 2 + 1), dtype=np.int8)
        self.start_pos = None
        self.end_pos = None
    
    @abstractmethod
    def generate(self) -> np.ndarray:
        """Generate a new maze.
        
        Returns:
            np.ndarray: A 2D numpy array where 0 represents paths and 1 represents walls.
        """
        pass
    
    def get_start_end_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the start and end points of the maze.
        
        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the start and end coordinates.
        """
        if self.start_pos is None or self.end_pos is None:
            # Default start and end points if not set by the generator
            self.start_pos = (1, 1)
            self.end_pos = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)
        return self.start_pos, self.end_pos 