import random
from typing import List, Tuple, Set
from .base_solver import BaseMazeSolver

class MouseMazeSolver(BaseMazeSolver):
    """Maze solver using random movement like a mouse exploring."""
    
    def solve_step_by_step(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Solve the maze using random movement, yielding each step for animation.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Yields:
            Tuple[int, int]: Current cell being explored
            or
            List[Tuple[int, int]]: Final solution path when found
        """
        current = start
        visited = {start}
        path = [start]
        max_steps = self.width * self.height * 4  # Prevent infinite loops
        steps = 0
        
        while current != end and steps < max_steps:
            yield current
            
            neighbors = self._get_neighbors(current)
            unvisited = [n for n in neighbors if n not in visited]
            
            if unvisited:
                # If there are unvisited neighbors, randomly choose one
                next_cell = random.choice(unvisited)
                visited.add(next_cell)
                path.append(next_cell)
                current = next_cell
            elif path:
                # If no unvisited neighbors, backtrack
                path.pop()
                if path:
                    current = path[-1]
                else:
                    break
            else:
                break
                
            steps += 1
        
        if current == end:
            yield path
        else:
            yield []
            
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells.
        
        Args:
            pos (Tuple[int, int]): Current position coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: List of valid neighboring cell coordinates.
        """
        x, y = pos
        neighbors = []
        
        # Check all four directions in random order
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and 
                self.maze[new_y, new_x] == 0):
                neighbors.append((new_x, new_y))
                
        return neighbors

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze using random movement.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the solution path.
                                  Returns an empty list if no solution is found.
        """
        current = start
        visited = {start}
        path = [start]
        max_steps = self.width * self.height * 4  # Prevent infinite loops
        steps = 0
        
        while current != end and steps < max_steps:
            neighbors = self._get_neighbors(current)
            unvisited = [n for n in neighbors if n not in visited]
            
            if unvisited:
                # If there are unvisited neighbors, randomly choose one
                next_cell = random.choice(unvisited)
                visited.add(next_cell)
                path.append(next_cell)
                current = next_cell
            elif path:
                # If no unvisited neighbors, backtrack
                path.pop()
                if path:
                    current = path[-1]
                else:
                    break
            else:
                break
                
            steps += 1
        
        return path if current == end else [] 