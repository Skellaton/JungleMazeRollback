import random
from typing import List, Tuple, Set
from dataclasses import dataclass

@dataclass
class Cell:
    """Represents a cell in the maze"""
    x: int
    y: int
    walls: List[bool]  # [top, right, bottom, left]
    visited: bool = False

class MazeGenerator:
    """Handles maze generation using Depth-First Search"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y, [True, True, True, True]) for x in range(width)] for y in range(height)]
        self.stack = []
        self.current = self.grid[0][0]
        self.current.visited = True
        self.stack.append(self.current)

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Get all unvisited neighbors of a cell"""
        neighbors = []
        x, y = cell.x, cell.y
        
        # Check top neighbor
        if y > 0 and not self.grid[y-1][x].visited:
            neighbors.append(self.grid[y-1][x])
        # Check right neighbor
        if x < self.width-1 and not self.grid[y][x+1].visited:
            neighbors.append(self.grid[y][x+1])
        # Check bottom neighbor
        if y < self.height-1 and not self.grid[y+1][x].visited:
            neighbors.append(self.grid[y+1][x])
        # Check left neighbor
        if x > 0 and not self.grid[y][x-1].visited:
            neighbors.append(self.grid[y][x-1])
            
        return neighbors

    def remove_wall(self, current: Cell, next_cell: Cell):
        """Remove the wall between two cells"""
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y
        
        if dx == 1:  # Next cell is to the right
            current.walls[1] = False
            next_cell.walls[3] = False
        elif dx == -1:  # Next cell is to the left
            current.walls[3] = False
            next_cell.walls[1] = False
        elif dy == 1:  # Next cell is below
            current.walls[2] = False
            next_cell.walls[0] = False
        elif dy == -1:  # Next cell is above
            current.walls[0] = False
            next_cell.walls[2] = False

    def generate(self):
        """Generate the maze using Depth-First Search"""
        while self.stack:
            neighbors = self.get_unvisited_neighbors(self.current)
            
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(self.current, next_cell)
                next_cell.visited = True
                self.stack.append(next_cell)
                self.current = next_cell
            else:
                self.current = self.stack.pop()
                
        return self.grid

class MazeSolver:
    """Handles maze solving using Breadth-First Search"""
    def __init__(self, grid: List[List[Cell]]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.visited = set()
        self.parent = {}
        self.queue = []
        self.solution = []

    def get_valid_neighbors(self, cell: Cell) -> List[Cell]:
        """Get all valid neighbors of a cell (no walls in between)"""
        neighbors = []
        x, y = cell.x, cell.y
        
        # Check top neighbor
        if y > 0 and not cell.walls[0]:
            neighbors.append(self.grid[y-1][x])
        # Check right neighbor
        if x < self.width-1 and not cell.walls[1]:
            neighbors.append(self.grid[y][x+1])
        # Check bottom neighbor
        if y < self.height-1 and not cell.walls[2]:
            neighbors.append(self.grid[y+1][x])
        # Check left neighbor
        if x > 0 and not cell.walls[3]:
            neighbors.append(self.grid[y][x-1])
            
        return neighbors

    def solve(self, start: Cell, end: Cell) -> List[Cell]:
        """Solve the maze using Breadth-First Search"""
        self.visited.clear()
        self.parent.clear()
        self.queue.clear()
        self.solution.clear()
        
        self.queue.append(start)
        self.visited.add((start.x, start.y))
        
        while self.queue:
            current = self.queue.pop(0)
            
            if current == end:
                # Reconstruct path
                while current != start:
                    self.solution.append(current)
                    current = self.parent[current]
                self.solution.append(start)
                self.solution.reverse()
                return self.solution
                
            for neighbor in self.get_valid_neighbors(current):
                if (neighbor.x, neighbor.y) not in self.visited:
                    self.visited.add((neighbor.x, neighbor.y))
                    self.parent[neighbor] = current
                    self.queue.append(neighbor)
                    
        return []  # No solution found 