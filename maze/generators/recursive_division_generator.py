import numpy as np
from .base_generator import BaseMazeGenerator
import random

class RecursiveDivisionGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with walls (already done in base class)
        
        # Start recursive division
        self._divide(1, 1, self.width * 2 - 1, self.height * 2 - 1)
        
        # Set start and end points
        self.start_pos = (1, 1)
        self.end_pos = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)
        return self.maze
    
    def _divide(self, x, y, width, height):
        """Recursively divide the maze into chambers."""
        # Base case: if the chamber is too small
        if width < 2 or height < 2:
            return
        
        # Choose orientation based on chamber dimensions
        horizontal = True if width < height else False
        if width == height:
            horizontal = random.choice([True, False])
        
        # Calculate wall position and passage position
        if horizontal:
            # Horizontal wall
            wall_y = y + random.randrange(0, height, 2)
            passage_x = x + random.randrange(0, width, 2)
            
            # Create wall with passage
            for wx in range(x, x + width):
                if wx != passage_x:
                    self.maze[wall_y, wx] = 1
            
            # Recursively divide chambers
            self._divide(x, y, width, wall_y - y)  # Upper chamber
            self._divide(x, wall_y + 1, width, y + height - wall_y - 1)  # Lower chamber
        
        else:
            # Vertical wall
            wall_x = x + random.randrange(0, width, 2)
            passage_y = y + random.randrange(0, height, 2)
            
            # Create wall with passage
            for wy in range(y, y + height):
                if wy != passage_y:
                    self.maze[wy, wall_x] = 1
            
            # Recursively divide chambers
            self._divide(x, y, wall_x - x, height)  # Left chamber
            self._divide(wall_x + 1, y, x + width - wall_x - 1, height)  # Right chamber
    
    def _set_start_end_points(self):
        """Override to ensure start and end points are accessible."""
        # Find a valid start point (left side)
        for y in range(1, self.height - 1):
            if self.maze[y, 1] == 0:
                self.start_pos = (1, y)
                break
        
        # Find a valid end point (right side)
        for y in range(self.height - 2, 0, -1):
            if self.maze[y, self.width - 2] == 0:
                self.end_pos = (self.width - 2, y)
                break
        
        # Clear any walls blocking the start and end
        if self.start_pos:
            self.maze[self.start_pos[1], self.start_pos[0] - 1] = 0
        if self.end_pos:
            self.maze[self.end_pos[1], self.end_pos[0] + 1] = 0 