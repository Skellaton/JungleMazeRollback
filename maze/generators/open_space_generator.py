import numpy as np
import random
from .base_generator import BaseMazeGenerator

class OpenSpaceGenerator(BaseMazeGenerator):
    def generate(self):
        # Initialize maze with all paths (0)
        self.maze.fill(0)
        
        # Add outer walls
        self.maze[0, :] = 1
        self.maze[-1, :] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1
        
        # Create large open spaces
        self._create_open_spaces()
        
        # Add long walls between spaces
        self._add_long_walls()
        
        # Ensure connectivity
        self._ensure_connectivity()
        
        # Set start and end points
        self.start_pos = (1, 1)
        self.end_pos = (self.maze.shape[1] - 2, self.maze.shape[0] - 2)
        return self.maze
    
    def _create_open_spaces(self):
        """Create large open spaces in the maze."""
        # Determine number of spaces based on maze size
        num_spaces = max(2, min(5, self.width // 4))
        
        # Create spaces
        for _ in range(num_spaces):
            # Random size for the space
            space_width = random.randint(3, min(7, self.width - 2))
            space_height = random.randint(3, min(7, self.height - 2))
            
            # Random position for the space
            x = random.randint(1, self.width * 2 - space_width - 1)
            y = random.randint(1, self.height * 2 - space_height - 1)
            
            # Clear the space
            self.maze[y:y+space_height, x:x+space_width] = 0
    
    def _add_long_walls(self):
        """Add long walls between open spaces."""
        # Number of walls based on maze size
        num_walls = max(2, min(8, self.width // 3))
        
        for _ in range(num_walls):
            # Random wall length (increased minimum and maximum)
            wall_length = random.randint(4, min(15, max(self.width, self.height)))
            
            # Random position with bias towards edges
            if random.random() < 0.7:  # 70% chance to start from an edge
                if random.random() < 0.5:  # 50% chance for horizontal wall
                    x = 1 if random.random() < 0.5 else self.width * 2 - 2
                    y = random.randint(1, self.height * 2 - 2)
                    end_x = x + wall_length if x == 1 else x - wall_length
                    end_x = max(1, min(end_x, self.width * 2 - 2))
                    
                    # Create horizontal wall
                    if x < end_x:
                        self.maze[y, x:end_x] = 1
                    else:
                        self.maze[y, end_x:x] = 1
                    
                    # Add passage
                    passage_x = random.randint(min(x, end_x), max(x, end_x) - 1)
                    self.maze[y, passage_x] = 0
                else:  # Vertical wall
                    y = 1 if random.random() < 0.5 else self.height * 2 - 2
                    x = random.randint(1, self.width * 2 - 2)
                    end_y = y + wall_length if y == 1 else y - wall_length
                    end_y = max(1, min(end_y, self.height * 2 - 2))
                    
                    # Create vertical wall
                    if y < end_y:
                        self.maze[y:end_y, x] = 1
                    else:
                        self.maze[end_y:y, x] = 1
                    
                    # Add passage
                    passage_y = random.randint(min(y, end_y), max(y, end_y) - 1)
                    self.maze[passage_y, x] = 0
            else:  # 30% chance for internal wall
                # Random position
                x = random.randint(1, self.width * 2 - 2)
                y = random.randint(1, self.height * 2 - 2)
                
                # Random orientation (horizontal or vertical)
                if random.random() < 0.5:
                    # Horizontal wall
                    end_x = min(x + wall_length, self.width * 2 - 2)
                    if end_x > x:  # Only create wall if it has length
                        self.maze[y, x:end_x] = 1
                        # Add passage
                        passage_x = random.randint(x, end_x - 1)
                        self.maze[y, passage_x] = 0
                else:
                    # Vertical wall
                    end_y = min(y + wall_length, self.height * 2 - 2)
                    if end_y > y:  # Only create wall if it has length
                        self.maze[y:end_y, x] = 1
                        # Add passage
                        passage_y = random.randint(y, end_y - 1)
                        self.maze[passage_y, x] = 0
    
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
    
    def _flood_fill(self, maze, start_x, start_y):
        """Iterative flood fill to check connectivity."""
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack.pop()
            if (0 <= x < self.width * 2 and 0 <= y < self.height * 2 and 
                maze[y][x] == 0 and self.maze[y][x] == 0):
                maze[y][x] = 1
                stack.extend([
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1)
                ])
    
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