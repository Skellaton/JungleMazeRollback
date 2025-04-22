from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple

class BaseMazeGenerator(ABC):
    """Abstract base class for maze generators."""
    
    @abstractmethod
    def generate(self) -> np.ndarray:
        """Generate a new maze.
        
        Returns:
            np.ndarray: A 2D numpy array where 0 represents paths and 1 represents walls.
        """
        pass
    
    @abstractmethod
    def get_start_end_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the start and end points of the maze.
        
        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the start and end coordinates.
        """
        pass 