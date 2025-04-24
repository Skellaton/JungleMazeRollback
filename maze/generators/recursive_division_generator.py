import numpy as np
from .base_generator import BaseMazeGenerator
import random

class RecursiveDivisionGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with all paths (0)
        self.maze.fill(0)
        
        # Add outer walls
        self.maze[0, :] = 1
        self.maze[-1, :] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1
        
        # Start recursive division
        self._divide(1, 1, self.width * 2 - 1, self.height * 2 - 1)
        
        # Add extra passages for better connectivity
        self._add_extra_passages()
        
        # Ensure start and end points are connected
        self._ensure_connectivity()
        
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
            
            # Add extra passages for better connectivity
            if width > 4:  # Only add extra passages if the region is wide enough
                num_extra_passages = min(3, width // 4)  # Add up to 3 extra passages
                for _ in range(num_extra_passages):
                    extra_passage_x = x + random.randrange(0, width, 2)
                    if extra_passage_x != passage_x:  # Ensure it's a different position
                        self.maze[wall_y, extra_passage_x] = 0
            
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
            
            # Add extra passages for better connectivity
            if height > 4:  # Only add extra passages if the region is tall enough
                num_extra_passages = min(3, height // 4)  # Add up to 3 extra passages
                for _ in range(num_extra_passages):
                    extra_passage_y = y + random.randrange(0, height, 2)
                    if extra_passage_y != passage_y:  # Ensure it's a different position
                        self.maze[extra_passage_y, wall_x] = 0
            
            # Recursively divide chambers
            self._divide(x, y, wall_x - x, height)  # Left chamber
            self._divide(wall_x + 1, y, x + width - wall_x - 1, height)  # Right chamber
    
    def _add_extra_passages(self):
        """Add additional passages to improve connectivity."""
        # Add extra horizontal passages
        for y in range(2, self.height * 2 - 1, 2):
            for x in range(1, self.width * 2 - 1, 2):
                if (self.maze[y, x] == 1 and  # If it's a wall
                    self.maze[y-1, x] == 0 and  # And there's a path above
                    self.maze[y+1, x] == 0):  # And there's a path below
                    if random.random() < 0.5:  # 50% chance to add a passage
                        self.maze[y, x] = 0
        
        # Add extra vertical passages
        for x in range(2, self.width * 2 - 1, 2):
            for y in range(1, self.height * 2 - 1, 2):
                if (self.maze[y, x] == 1 and  # If it's a wall
                    self.maze[y, x-1] == 0 and  # And there's a path to the left
                    self.maze[y, x+1] == 0):  # And there's a path to the right
                    if random.random() < 0.5:  # 50% chance to add a passage
                        self.maze[y, x] = 0
    
    def _ensure_connectivity(self):
        """Ensure there's a path from start to end."""
        # Create a copy of the maze for flood fill
        flood_maze = np.copy(self.maze)
        
        # Flood fill from start position
        start_x, start_y = 1, 1
        end_x, end_y = self.maze.shape[1] - 2, self.maze.shape[0] - 2
        
        # Perform flood fill
        self._flood_fill(flood_maze, start_x, start_y)
        
        # If end point is not reachable, add passages until it is
        if flood_maze[end_y, end_x] != 2:  # 2 represents filled cells
            # Find the closest filled cell to the end point
            closest_filled = self._find_closest_filled(flood_maze, end_x, end_y)
            if closest_filled:
                # Create a path from the closest filled cell to the end point
                self._create_path(closest_filled, (end_x, end_y))
    
    def _flood_fill(self, maze, x, y):
        """Perform flood fill to check connectivity."""
        if (0 <= x < maze.shape[1] and 0 <= y < maze.shape[0] and 
            maze[y, x] == 0):  # If it's a path
            maze[y, x] = 2  # Mark as filled
            
            # Fill in all directions
            self._flood_fill(maze, x + 1, y)
            self._flood_fill(maze, x - 1, y)
            self._flood_fill(maze, x, y + 1)
            self._flood_fill(maze, x, y - 1)
    
    def _find_closest_filled(self, flood_maze, target_x, target_y):
        """Find the closest filled cell to the target position."""
        min_dist = float('inf')
        closest = None
        
        for y in range(flood_maze.shape[0]):
            for x in range(flood_maze.shape[1]):
                if flood_maze[y, x] == 2:  # If it's a filled cell
                    dist = abs(x - target_x) + abs(y - target_y)
                    if dist < min_dist:
                        min_dist = dist
                        closest = (x, y)
        
        return closest
    
    def _create_path(self, start, end):
        """Create a path between two points."""
        x1, y1 = start
        x2, y2 = end
        
        # Move horizontally first, then vertically
        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1
        
        # Create horizontal path
        x = x1
        while x != x2:
            self.maze[y1, x] = 0
            x += step_x
        
        # Create vertical path
        y = y1
        while y != y2:
            self.maze[y, x2] = 0
            y += step_y 