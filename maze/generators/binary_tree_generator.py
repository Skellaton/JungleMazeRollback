import numpy as np
from .base_generator import BaseMazeGenerator
import random

class BinaryTreeGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with walls (already done in base class)
        
        # Create a grid of cells (every other cell)
        for y in range(1, self.height * 2, 2):
            for x in range(1, self.width * 2, 2):
                self.maze[y, x] = 0
                
                # For each cell, carve a passage either north or east
                choices = []
                
                # Check if we can go north
                if y > 1 and self.maze[y-2, x] == 0:
                    choices.append('N')
                
                # Check if we can go east
                if x < self.width * 2 - 1 and self.maze[y, x+2] == 0:
                    choices.append('E')
                
                if choices:
                    # Choose randomly between available directions
                    direction = random.choice(choices)
                    
                    if direction == 'N':
                        self.maze[y-1, x] = 0  # Carve north
                    else:  # direction == 'E'
                        self.maze[y, x+1] = 0  # Carve east
        
        # Set start and end points
        self.start_pos = (1, 1)
        self.end_pos = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)
        return self.maze
    
    def _set_start_end_points(self):
        """Set start point at top-left and end point at bottom-right."""
        # Set start point near top-left
        self.start_pos = (1, 1)
        self.maze[1, 0] = 0  # Ensure entrance is accessible
        
        # Set end point near bottom-right
        end_y = self.height - 2 if self.height % 2 == 0 else self.height - 3
        end_x = self.width - 2 if self.width % 2 == 0 else self.width - 3
        self.end_pos = (end_x, end_y)
        self.maze[end_y, end_x + 1] = 0  # Ensure exit is accessible 