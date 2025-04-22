import numpy as np
from typing import List, Tuple, Set, Dict
from heapq import heappush, heappop

class MazeSolver:
    def __init__(self, maze: np.ndarray):
        self.maze = maze
        self.height, self.width = maze.shape
        
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Solve the maze using A* algorithm."""
        # Priority queue for open nodes
        open_set = []
        # Set of visited nodes
        closed_set = set()
        # Dictionary to store the path
        came_from = {}
        # Dictionary to store g scores (cost from start to current)
        g_score = {start: 0}
        # Dictionary to store f scores (g_score + heuristic)
        f_score = {start: self._heuristic(start, end)}
        
        heappush(open_set, (f_score[start], start))
        
        while open_set:
            current = heappop(open_set)[1]
            
            if current == end:
                return self._reconstruct_path(came_from, current)
                
            closed_set.add(current)
            
            for neighbor in self._get_neighbors(current):
                if neighbor in closed_set:
                    continue
                    
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, end)
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # No path found
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Calculate the Manhattan distance between two points."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells."""
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
        """Reconstruct the path from start to end."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path 