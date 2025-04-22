import numpy as np
from typing import List, Tuple
from .base_solver import BaseMazeSolver

class DFSMazeSolver(BaseMazeSolver):
    """Depth-First Search algorithm for maze solving."""
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze using Depth-First Search.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the solution path.
        """
        visited = np.zeros(self.maze.shape, dtype=bool)
        path = []
        
        def dfs(x: int, y: int) -> bool:
            if (x, y) == end:
                path.append((x, y))
                return True
                
            if visited[y, x] or self.maze[y, x] == 1:
                return False
                
            visited[y, x] = True
            path.append((x, y))
            
            # Try all possible moves (up, right, down, left)
            moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    not visited[ny, nx] and self.maze[ny, nx] == 0):
                    if dfs(nx, ny):
                        return True
            
            path.pop()
            return False
        
        dfs(start[0], start[1])
        return path
    
    def solve_step_by_step(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Solve the maze step by step for animation.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Yields:
            Tuple[int, int]: The current cell being explored.
            List[Tuple[int, int]]: The solution path when found.
        """
        visited = np.zeros(self.maze.shape, dtype=bool)
        path = []
        
        def dfs(x: int, y: int):
            if (x, y) == end:
                path.append((x, y))
                yield path  # Yield the final path when exit is found
                return True
                
            if visited[y, x] or self.maze[y, x] == 1:
                return False
                
            visited[y, x] = True
            path.append((x, y))
            
            # Yield the current cell for animation
            yield (x, y)
            
            # Try all possible moves (up, right, down, left)
            moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    not visited[ny, nx] and self.maze[ny, nx] == 0):
                    for result in dfs(nx, ny):
                        if isinstance(result, list):  # If we got a path
                            yield result  # Yield the path
                            return True
                        yield result
            
            path.pop()
            return False
        
        for result in dfs(start[0], start[1]):
            if isinstance(result, list):  # If we got a path
                yield result  # Yield the path
                return
            yield result 