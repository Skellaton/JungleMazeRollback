import numpy as np
from .base_generator import BaseMazeGenerator
import random

class PrimsMazeGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with walls (already done in base class)
        
        # Start from a random cell
        start_y = random.randrange(1, self.height * 2, 2)
        start_x = random.randrange(1, self.width * 2, 2)
        self.maze[start_y, start_x] = 0
        
        # Initialize walls list with tuples of (wall_x, wall_y, cell_x, cell_y)
        # where cell_x, cell_y is the visited cell adjacent to the wall
        walls = []
        self._add_walls(start_x, start_y, walls)
        
        # While there are walls to process
        while walls:
            # Pick a random wall and its adjacent visited cell
            wall_info = random.choice(walls)
            walls.remove(wall_info)
            
            wall_x, wall_y, from_x, from_y = wall_info
            
            # Check if the cell on the opposite side of the wall is unvisited
            to_x, to_y = self._get_cell_beyond_wall(wall_x, wall_y, from_x, from_y)
            
            if (0 <= to_x < self.width * 2 + 1 and 
                0 <= to_y < self.height * 2 + 1 and 
                self.maze[to_y, to_x] == 1):
                # Carve through the wall and the cell beyond
                self.maze[wall_y, wall_x] = 0
                self.maze[to_y, to_x] = 0
                
                # Add new walls from the newly carved cell
                self._add_walls(to_x, to_y, walls)
        
        # Set start and end points
        self.start_pos = (1, 1)
        self.end_pos = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)
        return self.maze
    
    def _add_walls(self, x, y, walls):
        """Add adjacent walls to the walls list."""
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            new_x, new_y = x + dx, y + dy
            wall_x, wall_y = x + dx//2, y + dy//2
            
            if (0 <= new_x < self.width * 2 + 1 and 
                0 <= new_y < self.height * 2 + 1 and
                self.maze[wall_y, wall_x] == 1):
                # Store both wall coordinates and the current cell coordinates
                walls.append((wall_x, wall_y, x, y))
    
    def _get_cell_beyond_wall(self, wall_x, wall_y, from_x, from_y):
        """Get the coordinates of the unvisited cell on the opposite side of the wall."""
        # Calculate the direction from the visited cell to the wall
        dx = wall_x - from_x
        dy = wall_y - from_y
        
        # The cell beyond the wall is in the same direction
        return wall_x + dx, wall_y + dy 