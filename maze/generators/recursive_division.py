import numpy as np
import random
from .base_generator import BaseMazeGenerator

class RecursiveDivisionGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with all paths
        self.maze = np.zeros((self.height, self.width), dtype=np.int8)
        
        # Add outer walls
        self.maze[0, :] = 1
        self.maze[-1, :] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1
        
        # Start recursive division
        self._divide(1, 1, self.width - 2, self.height - 2)
        
        # Set start and end points
        self._set_start_end_points()
        return self.maze
    
    def _divide(self, x1, y1, x2, y2):
        """Recursively divide the maze."""
        width = x2 - x1 + 1
        height = y2 - y1 + 1
        
        # Base case: if region is too small
        if width < 3 or height < 3:
            return
        
        # Choose orientation based on region dimensions
        horizontal = True if width < height else False
        if width == height:
            horizontal = random.choice([True, False])
        
        # Calculate wall position (must be odd) and passage position (must be even)
        if horizontal:
            wall_y = random.randrange(y1 + 1, y2 - 1, 2)
            passage_x = random.randrange(x1, x2 + 1, 2)
            
            # Create horizontal wall with passage
            for x in range(x1, x2 + 1):
                if x != passage_x:
                    self.maze[wall_y, x] = 1
            
            # Add extra passages based on width
            if width > 10:
                num_extra_passages = width // 10
                possible_passages = list(range(x1, x2 + 1, 2))
                possible_passages.remove(passage_x)
                for _ in range(num_extra_passages):
                    if possible_passages:
                        extra_passage = random.choice(possible_passages)
                        possible_passages.remove(extra_passage)
                        self.maze[wall_y, extra_passage] = 0
            
            # Recursively divide sub-regions
            self._divide(x1, y1, x2, wall_y - 1)
            self._divide(x1, wall_y + 1, x2, y2)
        
        else:  # vertical
            wall_x = random.randrange(x1 + 1, x2 - 1, 2)
            passage_y = random.randrange(y1, y2 + 1, 2)
            
            # Create vertical wall with passage
            for y in range(y1, y2 + 1):
                if y != passage_y:
                    self.maze[y, wall_x] = 1
            
            # Add extra passages based on height
            if height > 10:
                num_extra_passages = height // 10
                possible_passages = list(range(y1, y2 + 1, 2))
                possible_passages.remove(passage_y)
                for _ in range(num_extra_passages):
                    if possible_passages:
                        extra_passage = random.choice(possible_passages)
                        possible_passages.remove(extra_passage)
                        self.maze[extra_passage, wall_x] = 0
            
            # Recursively divide sub-regions
            self._divide(x1, y1, wall_x - 1, y2)
            self._divide(wall_x + 1, y1, x2, y2) 