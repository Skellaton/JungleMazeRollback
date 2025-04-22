import numpy as np
from typing import List, Tuple
import heapq
from .base_solver import BaseMazeSolver

class DijkstraMazeSolver(BaseMazeSolver):
    """Dijkstra's algorithm for maze solving."""
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze using Dijkstra's algorithm.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the solution path.
        """
        # Initialize distances and previous nodes
        distances = np.full(self.maze.shape, float('inf'))
        previous = np.full(self.maze.shape, None, dtype=object)
        visited = np.zeros(self.maze.shape, dtype=bool)
        
        # Priority queue: (distance, x, y)
        heap = [(0, start[0], start[1])]
        distances[start[1], start[0]] = 0
        
        # Define possible moves (up, right, down, left)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        while heap:
            current_dist, x, y = heapq.heappop(heap)
            
            # Skip if we've already found a better path to this node
            if visited[y, x]:
                continue
                
            visited[y, x] = True
            
            # Check if we've reached the end
            if (x, y) == end:
                break
            
            # Explore neighbors
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                
                # Check if the neighbor is valid and not a wall
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.maze[ny, nx] == 0 and not visited[ny, nx]):
                    
                    # Calculate new distance (all moves cost 1)
                    new_dist = current_dist + 1
                    
                    # Update if we found a shorter path
                    if new_dist < distances[ny, nx]:
                        distances[ny, nx] = new_dist
                        previous[ny, nx] = (x, y)
                        heapq.heappush(heap, (new_dist, nx, ny))
        
        # Reconstruct the path
        path = []
        current = end
        while current is not None:
            path.append(current)
            if current == start:
                break
            current = previous[current[1], current[0]]
        
        return list(reversed(path))
    
    def solve_step_by_step(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Solve the maze step by step for animation.
        
        Args:
            start (Tuple[int, int]): The starting coordinates (x, y).
            end (Tuple[int, int]): The ending coordinates (x, y).
            
        Yields:
            Tuple[int, int]: The current cell being explored.
            List[Tuple[int, int]]: The solution path when found.
        """
        # Initialize distances and previous nodes
        distances = np.full(self.maze.shape, float('inf'))
        previous = np.full(self.maze.shape, None, dtype=object)
        visited = np.zeros(self.maze.shape, dtype=bool)
        
        # Priority queue: (distance, x, y)
        heap = [(0, start[0], start[1])]
        distances[start[1], start[0]] = 0
        
        # Define possible moves (up, right, down, left)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        while heap:
            current_dist, x, y = heapq.heappop(heap)
            
            # Skip if we've already found a better path to this node
            if visited[y, x]:
                continue
                
            visited[y, x] = True
            
            # Yield the current cell for animation
            yield (x, y)
            
            # Check if we've reached the end
            if (x, y) == end:
                # Reconstruct the path
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    if current == start:
                        break
                    current = previous[current[1], current[0]]
                yield list(reversed(path))  # Yield the final path
                return
            
            # Explore neighbors
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                
                # Check if the neighbor is valid and not a wall
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.maze[ny, nx] == 0 and not visited[ny, nx]):
                    
                    # Calculate new distance (all moves cost 1)
                    new_dist = current_dist + 1
                    
                    # Update if we found a shorter path
                    if new_dist < distances[ny, nx]:
                        distances[ny, nx] = new_dist
                        previous[ny, nx] = (x, y)
                        heapq.heappush(heap, (new_dist, nx, ny))
        
        yield []  # No path found 