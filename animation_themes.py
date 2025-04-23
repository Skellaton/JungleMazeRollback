import pygame
import random
from abc import ABC, abstractmethod
from typing import List, Optional

class FinishOrderTracker:
    """Tracks the order in which mazes finish"""
    def __init__(self):
        self.finish_order: List[int] = []
        self.theme_assignments: List[Optional[str]] = [None, None, None]  # gold, silver, bronze

    def add_finish(self, maze_id: int):
        """Add a maze to the finish order if not already present"""
        if maze_id not in self.finish_order:
            self.finish_order.append(maze_id)
            self._update_theme_assignments()

    def reset(self):
        """Reset the finish order and theme assignments"""
        self.finish_order.clear()
        self.theme_assignments = [None, None, None]

    def _update_theme_assignments(self):
        """Update theme assignments based on finish order"""
        if len(self.finish_order) >= 1:
            self.theme_assignments[0] = "gold"  # First to finish
        if len(self.finish_order) >= 2:
            self.theme_assignments[1] = "silver"  # Second to finish
        if len(self.finish_order) >= 3:
            self.theme_assignments[2] = "bronze"  # Third to finish

    def get_theme_for_maze(self, maze_id: int) -> Optional[str]:
        """Get the theme for a specific maze based on its finish order"""
        if maze_id in self.finish_order:
            position = self.finish_order.index(maze_id)
            if position < len(self.theme_assignments):
                return self.theme_assignments[position]
        return None

# Create a global instance of the tracker
finish_tracker = FinishOrderTracker()

class ThemeInterface(ABC):
    """Interface for all theme types"""
    @abstractmethod
    def get_cell_color(self, cell):
        """Get the color for a specific cell"""
        pass
    
    @abstractmethod
    def get_solution_color(self, cell):
        """Get the color for a solution cell"""
        pass
    
    @abstractmethod
    def get_trail_color(self):
        """Get the color for the trail"""
        pass

class AnimationTheme(ThemeInterface):
    """Base class for animation themes"""
    def __init__(self):
        self.cell_colors = {}
        self.solution_colors = {}
        self.flame_timer = 0
        self.solution_timer = 0
        self.FLAME_CHANGE_INTERVAL = 50
        self.SOLUTION_CHANGE_INTERVAL = 50
        self.random = random.Random()
        self.maze_id: Optional[int] = None

    def set_maze_id(self, maze_id: int):
        """Set the maze ID for this theme instance"""
        self.maze_id = maze_id

    def get_metal_theme(self) -> Optional[str]:
        """Get the metal theme for this maze based on finish order"""
        if self.maze_id is not None:
            return finish_tracker.get_theme_for_maze(self.maze_id)
        return None

class MatrixTheme(AnimationTheme):
    """Matrix-style theme with green colors"""
    def __init__(self):
        super().__init__()
        self.current_cell = (0, 255, 0)      # Bright Green
        self.trail = (0, 50, 0)              # Very Dark Green
        self.matrix_colors = [
            (0, 20, 0),     # Very Dark Green
            (0, 30, 0),     # Dark Green
            (0, 40, 0),     # Slightly Lighter Dark Green
            (0, 25, 0),     # Medium Dark Green
            (0, 35, 0),     # Another Dark Green
            (0, 45, 0),     # Lighter Dark Green
            (0, 15, 0)      # Darkest Green
        ]
        self.solution_base = (0, 0, 255)     # Blue
        self.solution_sparkle = None

    def get_cell_color(self, cell):
        current_time = pygame.time.get_ticks()
        if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
            self.flame_timer = current_time
            for c in self.cell_colors:
                if self.random.random() < 0.7:
                    self.cell_colors[c] = self.random.choice(self.matrix_colors)
        
        if cell not in self.cell_colors:
            self.cell_colors[cell] = self.random.choice(self.matrix_colors)
        return self.cell_colors[cell]

    def get_solution_color(self, cell):
        return self.solution_base

    def get_trail_color(self):
        return self.trail

class FireTheme(AnimationTheme):
    """Fire-style theme with red and orange colors"""
    def __init__(self):
        super().__init__()
        self.current_cell = (255, 0, 0)      # Bright Red
        self.trail = (50, 0, 0)              # Very Dark Red
        self.flame_colors = [
            (20, 0, 0),     # Very Dark Red
            (30, 0, 0),     # Dark Red
            (40, 0, 0),     # Slightly Lighter Dark Red
            (25, 0, 0),     # Medium Dark Red
            (35, 0, 0),     # Another Dark Red
            (45, 0, 0),     # Lighter Dark Red
            (15, 0, 0),     # Darkest Red
            (255, 69, 0),   # Red-Orange
            (255, 140, 0),  # Dark Orange
            (255, 165, 0),  # Orange
            (255, 215, 0),  # Gold
            (255, 99, 71),  # Tomato Red
            (255, 50, 0),   # Bright Red
            (255, 180, 0)   # Light Orange
        ]
        self.solution_base = (0, 0, 255)     # Blue
        self.solution_sparkle = None

    def get_cell_color(self, cell):
        current_time = pygame.time.get_ticks()
        if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
            self.flame_timer = current_time
            for c in self.cell_colors:
                if self.random.random() < 0.7:
                    self.cell_colors[c] = self.random.choice(self.flame_colors)
        
        if cell not in self.cell_colors:
            self.cell_colors[cell] = self.random.choice(self.flame_colors)
        return self.cell_colors[cell]

    def get_solution_color(self, cell):
        return self.solution_base

    def get_trail_color(self):
        return self.trail

class OceanTheme(AnimationTheme):
    """Ocean-style theme with blue colors"""
    def __init__(self):
        super().__init__()
        self.current_cell = (0, 0, 255)      # Bright Blue
        self.trail = (0, 0, 50)              # Very Dark Blue
        self.ocean_colors = [
            (0, 0, 20),     # Very Dark Blue
            (0, 0, 30),     # Dark Blue
            (0, 0, 40),     # Slightly Lighter Dark Blue
            (0, 0, 25),     # Medium Dark Blue
            (0, 0, 35),     # Another Dark Blue
            (0, 0, 45),     # Lighter Dark Blue
            (0, 0, 15)      # Darkest Blue
        ]
        self.solution_base = (0, 0, 255)     # Blue
        self.solution_sparkle = None

    def get_cell_color(self, cell):
        current_time = pygame.time.get_ticks()
        if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
            self.flame_timer = current_time
            for c in self.cell_colors:
                if self.random.random() < 0.7:
                    self.cell_colors[c] = self.random.choice(self.ocean_colors)
        
        if cell not in self.cell_colors:
            self.cell_colors[cell] = self.random.choice(self.ocean_colors)
        return self.cell_colors[cell]

    def get_solution_color(self, cell):
        return self.solution_base

    def get_trail_color(self):
        return self.trail 