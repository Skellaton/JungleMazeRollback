from collections import deque
from typing import List, Tuple, Dict
from .base_solver import BaseMazeSolver

class BFSMazeSolver(BaseMazeSolver):
    """Maze solver using Breadth-First Search algorithm."""
    
    def solve_step_by_step(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Solve the maze using BFS algorithm, yielding each step for animation.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Yields:
            Tuple[int, int]: Current cell being explored
            or
            List[Tuple[int, int]]: Final solution path when found
        """
        # Queue for BFS
        queue = deque([start])
        # Set of visited nodes
        visited = {start}
        # Dictionary to store the path
        came_from = {}
        
        while queue:
            current = queue.popleft()
            yield current  # Yield current cell for animation
            
            if current == end:
                path = self._reconstruct_path(came_from, current)
                yield path  # Yield the final path
                return
            
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        yield []  # No path found
    
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells.
        
        Args:
            pos (Tuple[int, int]): Current position coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: List of valid neighboring cell coordinates.
        """
        x, y = pos
        neighbors = []
        
        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and 
                self.maze[new_y, new_x] == 0):
                neighbors.append((new_x, new_y))
                
        return neighbors
    
    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                         current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct the path from start to end.
        
        Args:
            came_from (Dict[Tuple[int, int], Tuple[int, int]]): Dictionary mapping each cell to its predecessor.
            current (Tuple[int, int]): The end point coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: The complete path from start to end.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze using BFS algorithm.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the solution path.
                                  Returns an empty list if no solution is found.
        """
        # Queue for BFS
        queue = deque([start])
        # Set of visited nodes
        visited = {start}
        # Dictionary to store the path
        came_from = {}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return []  # No path found 