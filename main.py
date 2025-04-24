import pygame
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 2)
from maze.generators import DFSMazeGenerator, PrimsMazeGenerator, BinaryTreeGenerator, RecursiveDivisionGenerator, OpenSpaceGenerator
from maze.solvers import AStarMazeSolver, BFSMazeSolver, MouseMazeSolver, DijkstraMazeSolver, DFSMazeSolver
from ui_components.components import ButtonStyle, Button, Dropdown, Slider, MazeNodes

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 10
MAZE_WIDTH = 35
MAZE_HEIGHT = 12  # Reduced from 18 to 12
BUTTON_HEIGHT = 80
MAZE_SPACING = 20  # Space between mazes

# Calculate the centered position for the mazes
MAZE_OFFSET_X = (1920 - (MAZE_WIDTH * CELL_SIZE)) // 2  # Center horizontally
MAZE_OFFSET_Y = ((1080 - BUTTON_HEIGHT - (MAZE_HEIGHT * CELL_SIZE * 3 + MAZE_SPACING * 2)) // 2) + BUTTON_HEIGHT  # Center vertically below buttons

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

class AnimationTheme:
    """Class to define animation color themes."""
    
    def __init__(self, theme_name="matrix"):
        self.themes = {
            "default": {
                "current_cell": (255, 215, 0),    # Gold
                "trail": (144, 238, 144),         # Light green
                "solution": {
                    "base": (0, 0, 255),          # Blue
                    "sparkle": None
                }
            },
            "neon": {
                "current_cell": (255, 0, 255),    # Magenta
                "trail": (0, 255, 255),           # Cyan
                "solution": {
                    "base": (0, 0, 255),          # Blue
                    "sparkle": None
                }
            },
            "fire": {
                "current_cell": (255, 0, 0),      # Bright Red
                "trail": (50, 0, 0),              # Very Dark Red
                "flame_colors": [
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
                ],
                "solution": {
                    "base": (0, 0, 255),          # Blue
                    "sparkle": None
                }
            },
            "gold": {
                "current_cell": (255, 215, 0),    # Gold
                "trail": (255, 215, 0),           # Gold
                "solution": {
                    "base": (255, 215, 0),        # Gold
                    "sparkle": [
                        (255, 255, 0),    # Yellow
                        (255, 215, 0),    # Gold
                        (255, 255, 200),  # Light Gold
                        (255, 200, 0)     # Dark Gold
                    ]
                }
            },
            "silver": {
                "current_cell": (192, 192, 192),  # Silver
                "trail": (192, 192, 192),         # Silver
                "solution": {
                    "base": (192, 192, 192),      # Silver
                    "sparkle": [
                        (255, 255, 255),  # White
                        (192, 192, 192),  # Silver
                        (220, 220, 220),  # Light Silver
                        (160, 160, 160)   # Dark Silver
                    ]
                }
            },
            "bronze": {
                "current_cell": (205, 127, 50),   # Bronze
                "trail": (205, 127, 50),          # Bronze
                "solution": {
                    "base": (205, 127, 50),       # Bronze
                    "sparkle": [
                        (218, 165, 32),   # Goldenrod
                        (205, 127, 50),   # Bronze
                        (222, 184, 135),  # Burlywood
                        (184, 115, 51)    # Dark Bronze
                    ]
                }
            },
            "metal": {
                "current_cell": (100, 100, 100),  # Darker Gray
                "trail": (100, 100, 100),         # Darker Gray
                "solution": {
                    "base": (100, 100, 100),      # Darker Gray
                    "sparkle": [
                        (150, 150, 150),  # Medium Gray
                        (100, 100, 100),  # Darker Gray
                        (120, 120, 120),  # Slightly Lighter Gray
                        (80, 80, 80)      # Very Dark Gray
                    ]
                }
            },
            "ocean": {
                "current_cell": (0, 0, 255),      # Bright Blue
                "trail": (0, 0, 50),              # Very Dark Blue
                "ocean_colors": [
                    (0, 0, 20),     # Very Dark Blue
                    (0, 0, 30),     # Dark Blue
                    (0, 0, 40),     # Slightly Lighter Dark Blue
                    (0, 0, 25),     # Medium Dark Blue
                    (0, 0, 35),     # Another Dark Blue
                    (0, 0, 45),     # Lighter Dark Blue
                    (0, 0, 15)      # Darkest Blue
                ],
                "solution": {
                    "base": (0, 0, 255),          # Blue
                    "sparkle": None
                }
            },
            "sunset": {
                "current_cell": (255, 99, 71),    # Tomato Red
                "trail": (255, 182, 193)          # Light Pink
            },
            "matrix": {
                "current_cell": (0, 255, 0),      # Bright Green
                "trail": (0, 50, 0),              # Very Dark Green
                "matrix_colors": [
                    (0, 20, 0),     # Very Dark Green
                    (0, 30, 0),     # Dark Green
                    (0, 40, 0),     # Slightly Lighter Dark Green
                    (0, 25, 0),     # Medium Dark Green
                    (0, 35, 0),     # Another Dark Green
                    (0, 45, 0),     # Lighter Dark Green
                    (0, 15, 0)      # Darkest Green
                ],
                "solution": {
                    "base": (0, 0, 255),          # Blue
                    "sparkle": None
                }
            },
            "candy": {
                "current_cell": (255, 105, 180),  # Hot Pink
                "trail": (255, 182, 193)          # Light Pink
            },
            "rainbow": {
                "current_cell": (148, 0, 211),    # Purple
                "trail": None                     # Will be random rainbow colors
            }
        }
        self.set_theme(theme_name)
        self.flame_timer = 0
        self.FLAME_CHANGE_INTERVAL = 50
        self.cell_colors = {}
        self.solution_colors = {}  # Dictionary to store solution cell colors
        self.solution_timer = 0
        self.SOLUTION_CHANGE_INTERVAL = 50
        import random
        self.random = random
        self.original_theme = None  # Store the original theme name
    
    def set_theme(self, theme_name):
        """Set the current animation theme."""
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            self.current_cell = theme["current_cell"]
            self.trail = theme["trail"]
            self.current_theme = theme_name
            self.original_theme = theme_name  # Store the original theme
            self.flame_colors = theme.get("flame_colors", None)
            self.ocean_colors = theme.get("ocean_colors", None)
            self.matrix_colors = theme.get("matrix_colors", None)
            self.solution_colors = {}  # Reset solution colors when theme changes
            self.solution_sparkle = theme.get("solution", {}).get("sparkle", None)
            self.solution_base = theme.get("solution", {}).get("base", (0, 0, 255))
            self.cell_colors = {}  # Reset cell colors when theme changes
    
    def get_random_rainbow_color(self):
        """Generate a random rainbow color."""
        import random
        rainbow_colors = [
            (255, 0, 0),      # Red
            (255, 127, 0),    # Orange
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (75, 0, 130),     # Indigo
            (148, 0, 211)     # Violet
        ]
        return random.choice(rainbow_colors)
    
    def get_trail_color(self):
        """Get the trail color, with special handling for rainbow and fire themes."""
        if self.current_theme == "rainbow":
            return self.get_random_rainbow_color()
        elif self.current_theme == "fire":
            current_time = pygame.time.get_ticks()
            if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
                self.flame_timer = current_time
                # Update colors for all cells
                for cell in self.cell_colors:
                    if self.random.random() < 0.7:  # 70% chance to change color for more natural flickering
                        self.cell_colors[cell] = self.random.choice(self.flame_colors)
            return self.trail
        return self.trail
    
    def get_cell_color(self, cell):
        """Get the color for a specific cell in fire theme."""
        if self.current_theme == "fire":
            if cell not in self.cell_colors:
                self.cell_colors[cell] = self.random.choice(self.flame_colors)
            return self.cell_colors[cell]
        elif self.current_theme == "ocean":
            current_time = pygame.time.get_ticks()
            if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
                self.flame_timer = current_time
                # Update colors for all cells
                for c in self.cell_colors:
                    if self.random.random() < 0.7:  # 70% chance to change color for more natural flickering
                        self.cell_colors[c] = self.random.choice(self.ocean_colors)
            
            if cell not in self.cell_colors:
                self.cell_colors[cell] = self.random.choice(self.ocean_colors)
            return self.cell_colors[cell]
        elif self.current_theme == "matrix":
            current_time = pygame.time.get_ticks()
            if current_time - self.flame_timer > self.FLAME_CHANGE_INTERVAL:
                self.flame_timer = current_time
                # Update colors for all cells
                for c in self.cell_colors:
                    if self.random.random() < 0.7:  # 70% chance to change color for more natural flickering
                        self.cell_colors[c] = self.random.choice(self.matrix_colors)
            
            if cell not in self.cell_colors:
                self.cell_colors[cell] = self.random.choice(self.matrix_colors)
            return self.cell_colors[cell]
        return self.get_trail_color()
    
    def get_solution_color(self, cell):
        """Get the color for a specific cell in the solution path."""
        if self.solution_sparkle:
            current_time = pygame.time.get_ticks()
            if current_time - self.solution_timer > self.SOLUTION_CHANGE_INTERVAL:
                self.solution_timer = current_time
                # Update colors for all solution cells
                for c in self.solution_colors:
                    if self.random.random() < 0.7:  # 70% chance to change color
                        self.solution_colors[c] = self.random.choice(self.solution_sparkle)
            
            if cell not in self.solution_colors:
                self.solution_colors[cell] = self.random.choice(self.solution_sparkle)
            return self.solution_colors[cell]
        return self.solution_base

class Theme:
    """Class to define the application's color theme."""
    
    def __init__(self, theme_name="jungle"):
        self.themes = {
            "jungle": {
                "background": (207, 208, 173),  # #cfd0ad
                "text": (29, 68, 42),          # #1d442a
                "border": (29, 68, 42),        # #1d442a
                "accent": (160, 180, 127),     # #a0b47f
                "button_hover": (170, 190, 137)
            },
            "dark jungle": {
                "background": (29, 68, 42),    # Dark green background
                "text": (29, 68, 42),          # Same as Jungle theme
                "border": (29, 68, 42),        # Same as Jungle theme
                "accent": (160, 180, 127),     # Same as Jungle theme
                "button_hover": (170, 190, 137)  # Same as Jungle theme
            },
            "dark": {
                "background": (0, 0, 0),        # Black
                "text": (200, 200, 200),       # Light gray
                "border": (0, 0, 0),           # Black
                "accent": (40, 40, 40),        # Brighter dark gray
                "button_hover": (60, 60, 60)   # Even brighter gray for hover
            }
        }
        self.set_theme(theme_name)
        
    def set_theme(self, theme_name):
        """Set the current theme."""
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            self.background = theme["background"]
            self.text = theme["text"]
            self.border = theme["border"]
            self.accent = theme["accent"]
            self.button_hover = theme["button_hover"]
            
            # Button colors
            self.button_background = self.accent
            self.button_border = self.border
            self.button_text = self.text
            
            # Special colors (same for all themes)
            self.start_color = (0, 255, 0)          # Green
            self.end_color = (255, 0, 0)            # Red
            self.solution_color = (0, 0, 255)       # Blue

class MazeComponent:
    def __init__(self, x, y, maze_width, maze_height, cell_size, button_style, maze_generator):
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Maze properties
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = cell_size
        self.maze_generator = maze_generator
        
        # Create own animation theme instance
        self.animation_theme = AnimationTheme("matrix")
        
        # Component dimensions
        button_width = 180
        button_height = 40
        button_spacing = 10
        self.close_button_width = 40  # Width of close button
        self.timer_width = 120  # Width of timer box
        self.width = max(maze_width * cell_size, 
                        self.close_button_width + button_spacing + 
                        button_width * 3 + button_spacing * 3 +
                        self.timer_width)
        self.height = maze_height * cell_size + button_height * 2 + button_spacing * 2
        
        # Timer properties
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_font = pygame.font.SysFont('consolas', 24)
        self.timer_rect = pygame.Rect(
            x + self.close_button_width + button_spacing + button_width * 3 + button_spacing * 3,
            y,
            self.timer_width,
            button_height
        )
        
        # Close button properties
        self.close_button_rect = pygame.Rect(
            x,  # Start at component's x
            y,  # Start at component's y
            self.close_button_width,
            button_height  # Same height as dropdowns
        )
        self.close_button_hovered = False
        self.button_style = button_style
        
        # Create dropdowns and nodes button
        self.algorithm_dropdown = Dropdown(
            x + self.close_button_width + button_spacing,  # Position after close button
            y,
            button_width,
            button_height,
            ["A*", "BFS", "DFS", "Dijkstra", "Mouse"],
            button_style
        )
        
        self.animation_theme_dropdown = Dropdown(
            x + self.close_button_width + button_spacing + button_width + button_spacing,  # Position after algorithm dropdown
            y,
            button_width,
            button_height,
            ["Default", "Neon", "Fire", "Ocean", "Sunset", "Matrix", "Candy", "Rainbow"],
            button_style
        )
        
        self.nodes_button = Button(
            x + self.close_button_width + button_spacing + button_width * 2 + button_spacing * 2,  # Position after animation theme dropdown
            y,
            button_width,
            button_height,
            "Nodes",
            self.show_nodes,
            button_style
        )
        
        # Initialize maze state
        self.maze = None
        self.solution = None
        self.solving = False
        self.current_cell = None
        self.explored_cells = set()
        self.solver = None
        self.solver_generator = None
        self.start_pos = None
        self.end_pos = None
        
        # Add z-index tracking
        self.dropdowns_open = False
        
        # Nodes component
        self.nodes_component = None
    
    def move_to(self, new_x, new_y):
        """Move the component to a new position and update all related positions."""
        try:
            # Calculate the offset from the old position
            dx = new_x - self.x
            dy = new_y - self.y
            
            # Update main component position
            self.x = new_x
            self.y = new_y
            
            # Update all component positions using the offset
            if hasattr(self, 'close_button_rect'):
                self.close_button_rect.x += dx
                self.close_button_rect.y += dy
            
            if hasattr(self, 'algorithm_dropdown'):
                self.algorithm_dropdown.rect.x += dx
                self.algorithm_dropdown.rect.y += dy
                
                # Update dropdown option positions if they're open
                if self.algorithm_dropdown.is_open and hasattr(self.algorithm_dropdown, 'option_rects'):
                    for rect in self.algorithm_dropdown.option_rects:
                        rect.x += dx
                        rect.y += dy
            
            if hasattr(self, 'animation_theme_dropdown'):
                self.animation_theme_dropdown.rect.x += dx
                self.animation_theme_dropdown.rect.y += dy
                
                # Update dropdown option positions if they're open
                if self.animation_theme_dropdown.is_open and hasattr(self.animation_theme_dropdown, 'option_rects'):
                    for rect in self.animation_theme_dropdown.option_rects:
                        rect.x += dx
                        rect.y += dy
            
            if hasattr(self, 'nodes_button'):
                self.nodes_button.rect.x += dx
                self.nodes_button.rect.y += dy
            
            if hasattr(self, 'timer_rect'):
                self.timer_rect.x += dx
                self.timer_rect.y += dy
            
            # Update nodes component position if it exists and is locked
            if hasattr(self, 'nodes_component') and self.nodes_component is not None:
                if hasattr(self.nodes_component, 'is_locked') and self.nodes_component.is_locked:
                    self.nodes_component.update_position_from_parent()
        except Exception as e:
            print(f"Error in move_to: {e}")  # Print error for debugging
            # Don't crash, just return
            return
    
    def show_nodes(self):
        """Create and show the nodes visualization component."""
        if self.maze is not None:
            # Calculate position for nodes component (slightly offset from main component)
            nodes_x = self.x + self.width + 20
            nodes_y = self.y
            self.nodes_component = MazeNodes(
                nodes_x,
                nodes_y,
                self.maze_width,
                self.maze_height,
                self.cell_size,
                self.button_style,
                self.maze,
                self  # Pass self as parent component
            )
        
    def handle_event(self, event):
        # Handle dropdowns and nodes button
        algorithm = self.algorithm_dropdown.handle_event(event)
        animation_theme = self.animation_theme_dropdown.handle_event(event)
        nodes_action = self.nodes_button.handle_event(event)
        
        # Update z-index tracking
        self.dropdowns_open = self.algorithm_dropdown.is_open or self.animation_theme_dropdown.is_open
        
        # Handle close button
        if event.type == pygame.MOUSEMOTION:
            self.close_button_hovered = self.close_button_rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.close_button_rect.collidepoint(event.pos):
                    return algorithm, animation_theme, "close"
                
                mouse_x, mouse_y = event.pos
                # Check if click is in the component but not in the dropdowns
                if (self.x <= mouse_x <= self.x + self.width and 
                    self.y + 50 <= mouse_y <= self.y + self.height and
                    not self.dropdowns_open):  # Don't allow dragging when dropdowns are open
                    self.dragging = True
                    self.drag_offset_x = mouse_x - self.x
                    self.drag_offset_y = mouse_y - self.y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                new_x = mouse_x - self.drag_offset_x
                new_y = mouse_y - self.drag_offset_y
                self.move_to(new_x, new_y)
        
        # Apply theme change if needed
        if animation_theme:
            self.animation_theme.set_theme(animation_theme.lower())
        
        # Handle nodes button
        if nodes_action:
            nodes_action()
        
        return algorithm, animation_theme, None
    
    def draw(self, screen, app_theme, _, event=None):
        """Draw the maze component. The third parameter is ignored since we use our own animation theme."""
        # Draw background for the entire component
        component_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, app_theme.accent, component_rect)
        pygame.draw.rect(screen, app_theme.border, component_rect, 2)
        
        # Draw close button
        color = self.button_style.hover_color if self.close_button_hovered else self.button_style.background_color
        pygame.draw.rect(screen, color, self.close_button_rect)
        pygame.draw.rect(screen, self.button_style.border_color, self.close_button_rect, self.button_style.border_width)
        
        # Draw X symbol
        x_margin = 12
        x_color = self.button_style.text_color
        pygame.draw.line(screen, x_color, 
                        (self.close_button_rect.left + x_margin, self.close_button_rect.centery - x_margin + 2),
                        (self.close_button_rect.right - x_margin, self.close_button_rect.centery + x_margin - 2), 2)
        pygame.draw.line(screen, x_color,
                        (self.close_button_rect.left + x_margin, self.close_button_rect.centery + x_margin - 2),
                        (self.close_button_rect.right - x_margin, self.close_button_rect.centery - x_margin + 2), 2)
        
        # Draw dropdowns and nodes button
        self.algorithm_dropdown.draw(screen)
        self.animation_theme_dropdown.draw(screen)
        self.nodes_button.draw(screen)
        
        # Draw timer box
        pygame.draw.rect(screen, self.button_style.background_color, self.timer_rect)
        pygame.draw.rect(screen, self.button_style.border_color, self.timer_rect, self.button_style.border_width)
        
        # Draw timer text
        timer_text = f"{self.elapsed_time:.2f}s"
        timer_surface = self.timer_font.render(timer_text, True, self.button_style.text_color)
        timer_text_rect = timer_surface.get_rect(center=self.timer_rect.center)
        screen.blit(timer_surface, timer_text_rect)
        
        # Calculate maze position (aligned to left side of component)
        maze_x = self.x + self.close_button_width + 10 - 30  # Start after close button and move left 30 pixels
        maze_y = self.y + 50  # Below dropdowns
        
        # Draw maze
        for y in range(self.maze.shape[0]):
            for x in range(self.maze.shape[1]):
                rect = pygame.Rect(
                    x * self.cell_size + maze_x,
                    y * self.cell_size + maze_y,
                    self.cell_size,
                    self.cell_size
                )
                if self.maze[y, x] == 1:  # Wall
                    pygame.draw.rect(screen, app_theme.border, rect)
                else:  # Path
                    pygame.draw.rect(screen, app_theme.accent, rect)
        
        # Draw start and end points if they exist
        if self.start_pos is not None and self.end_pos is not None:
            start_x, start_y = self.start_pos
            end_x, end_y = self.end_pos
            
            pygame.draw.rect(screen, app_theme.start_color,
                           (start_x * self.cell_size + maze_x,
                            start_y * self.cell_size + maze_y,
                            self.cell_size, self.cell_size))
            pygame.draw.rect(screen, app_theme.end_color,
                           (end_x * self.cell_size + maze_x,
                            end_y * self.cell_size + maze_y,
                            self.cell_size, self.cell_size))
        
        # Draw explored cells
        for x, y in self.explored_cells:
            if (x, y) != self.start_pos and (x, y) != self.end_pos:
                pygame.draw.rect(screen, self.animation_theme.get_cell_color((x, y)),
                               (x * self.cell_size + maze_x,
                                y * self.cell_size + maze_y,
                                self.cell_size, self.cell_size))
        
        # Draw current cell
        if self.current_cell:
            x, y = self.current_cell
            if (x, y) != self.start_pos and (x, y) != self.end_pos:
                pygame.draw.rect(screen, self.animation_theme.current_cell,
                               (x * self.cell_size + maze_x,
                                y * self.cell_size + maze_y,
                                self.cell_size, self.cell_size))
        
        # Draw solution path
        if self.solution:
            for x, y in self.solution:
                if (x, y) != self.start_pos and (x, y) != self.end_pos:
                    pygame.draw.rect(screen, self.animation_theme.get_solution_color((x, y)),
                                   (x * self.cell_size + maze_x,
                                    y * self.cell_size + maze_y,
                                    self.cell_size, self.cell_size))
        
        # Draw dropdown options on top of everything
        self.algorithm_dropdown.draw_options(screen)
        self.animation_theme_dropdown.draw_options(screen)
        
        # Draw nodes component if it exists
        if self.nodes_component:
            self.nodes_component.draw(screen, app_theme)
            if event:
                result = self.nodes_component.handle_event(event)
                if result == "close":
                    self.nodes_component = None

    def set_maze(self, maze, start_pos, end_pos):
        """Set the maze for this component."""
        self.maze = maze
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.solution = None
        self.solving = False
        self.current_cell = None
        self.explored_cells = set()
        self.elapsed_time = 0
    
    def start_solving(self, solver_class):
        if self.maze is not None and not self.solving and self.start_pos is not None and self.end_pos is not None:
            self.solving = True
            self.solution = None
            self.current_cell = None
            self.explored_cells = set()
            self.start_time = pygame.time.get_ticks()
            self.elapsed_time = 0
            self.solver = solver_class(self.maze)
            self.solver_generator = self.solver.solve_step_by_step(self.start_pos, self.end_pos)
    
    def update_solving(self):
        if self.solving:
            # Update elapsed time
            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.start_time) / 1000  # Convert to seconds
            
            try:
                result = next(self.solver_generator)
                if isinstance(result, tuple):
                    self.current_cell = result
                    self.explored_cells.add(result)
                elif isinstance(result, list):
                    self.solution = result
                    self.solving = False
            except StopIteration:
                self.solving = False
    
    def reset_solving(self):
        """Reset the solving animation state."""
        self.solution = None
        self.solving = False
        self.current_cell = None
        self.explored_cells = set()
        self.solver = None
        self.solver_generator = None
        self.elapsed_time = 0

class MazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Generator and Solver")
        self.clock = pygame.time.Clock()
        
        # Load and scale logos
        self.logos = {
            "jungle": pygame.transform.scale(pygame.image.load("assets/logo_jungle.png"), (200, 200)),
            "dark jungle": pygame.transform.scale(pygame.image.load("assets/logo_jungle.png"), (200, 200)),
            "dark": pygame.transform.scale(pygame.image.load("assets/logo_dark.png"), (200, 200))
        }
        self.current_logo = None
        
        # Initialize themes
        self.app_theme = Theme()
        self.button_style = ButtonStyle(self.app_theme)
        
        # Set initial logo based on default theme
        self.current_logo = self.logos["jungle"]
        
        # Initialize solvers and themes
        self.solvers = {
            "A*": AStarMazeSolver,
            "BFS": BFSMazeSolver,
            "DFS": DFSMazeSolver,
            "Dijkstra": DijkstraMazeSolver,
            "Mouse": MouseMazeSolver
        }
        
        # Initialize maze generators
        self.generators = {
            "DFS": DFSMazeGenerator,
            "Prim's": PrimsMazeGenerator,
            "Binary Tree": BinaryTreeGenerator,
            "Recursive Division": RecursiveDivisionGenerator,
            "Open Space": OpenSpaceGenerator
        }
        
        self.animation_themes = ["Default", "Neon", "Fire", "Ocean", "Sunset", "Matrix", "Candy", "Rainbow"]
        
        # Initialize maze components list
        self.maze_components = []
        
        # Initialize maze generator and shared maze
        self.maze_generator = DFSMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.shared_maze = None
        self.start_pos = None
        self.end_pos = None
        
        # Add pause state
        self.is_paused = False
        
        # Create buttons and sliders
        button_width = 180
        button_height = 40
        button_spacing = 10
        
        # Calculate positions for sliders and buttons
        slider_width = 200
        slider_height = 10
        slider_spacing = 40
        slider_y = 20
        
        # Position sliders to the left of buttons
        slider_x = 250
        buttons_x = slider_x + slider_width + 40  # Add some spacing between sliders and buttons
        
        # Create dimension sliders
        self.width_slider = Slider(
            slider_x,
            slider_y,
            slider_width,
            slider_height,
            5,  # min width
            90,  # max width
            MAZE_WIDTH,  # initial width
            "Width",
            self.button_style
        )
        
        self.height_slider = Slider(
            slider_x,
            slider_y + slider_spacing,
            slider_width,
            slider_height,
            5,  # min height
            50,  # max height
            MAZE_HEIGHT,  # initial height
            "Height",
            self.button_style
        )
        
        self.cell_size_slider = Slider(
            slider_x,
            slider_y + slider_spacing * 2,
            slider_width,
            slider_height,
            10,  # min cell size
            30,  # max cell size
            10,  # initial cell size
            "Cell Size",
            self.button_style
        )
        
        # Create maze generator dropdown
        self.generator_dropdown = Dropdown(
            buttons_x,
            slider_y,
            button_width,
            button_height,
            list(self.generators.keys()),
            self.button_style
        )
        
        # Create buttons
        self.generate_button = Button(
            buttons_x + button_width + button_spacing,
            slider_y,
            button_width,
            button_height,
            "Generate",
            self.generate_maze,
            self.button_style
        )
        
        self.solve_button = Button(
            buttons_x + (button_width + button_spacing) * 2,
            slider_y,
            button_width,
            button_height,
            "Solve Maze",
            self.solve_maze,
            self.button_style
        )
        
        self.reset_button = Button(
            buttons_x + (button_width + button_spacing) * 3,
            slider_y,
            button_width,
            button_height,
            "Reset",
            self.reset_solving,
            self.button_style
        )
        
        # Add pause button under reset button
        self.pause_button = Button(
            buttons_x + (button_width + button_spacing) * 3,  # Same x as reset button
            slider_y + button_height + 5,  # Position below reset button with small gap
            button_width,
            button_height,
            "Pause",
            self.toggle_pause,
            self.button_style
        )
        
        self.new_maze_button = Button(
            buttons_x + (button_width + button_spacing) * 4,
            slider_y,
            button_width,
            button_height,
            "New Maze",
            self.create_new_maze,
            self.button_style
        )
        
        self.randomize_all_button = Button(
            buttons_x + (button_width + button_spacing) * 5,
            slider_y,
            button_width,
            button_height,
            "Random",
            self.randomize_all_mazes,
            self.button_style
        )
        
        self.app_theme_dropdown = Dropdown(
            buttons_x + (button_width + button_spacing) * 6,
            slider_y,
            button_width,
            button_height,
            ["Jungle", "Dark Jungle", "Dark"],
            self.button_style
        )
        
        # Create buttons list with all buttons
        self.buttons = [
            self.generate_button,
            self.solve_button,
            self.reset_button,
            self.pause_button,
            self.new_maze_button,
            self.randomize_all_button
        ]
        
        # Track solved mazes
        self.solved_mazes = []
        
        # Create initial maze component and generate first maze
        self.create_new_maze()
        self.generate_maze()  # Generate initial maze
    
    def generate_maze(self):
        """Generate a new maze that will be shared across all components."""
        # Get the selected generator class
        generator_name = self.generator_dropdown.selected
        generator_class = self.generators.get(generator_name, DFSMazeGenerator)
        self.maze_generator = generator_class(MAZE_WIDTH, MAZE_HEIGHT)
        
        # Generate the maze
        self.shared_maze = self.maze_generator.generate()
        
        # Get start and end positions
        self.start_pos, self.end_pos = self.maze_generator.get_start_end_points()
        
        # Reset solved mazes list
        self.solved_mazes = []
        
        # Update all components with the new maze and positions
        for component in self.maze_components:
            component.set_maze(self.shared_maze, self.start_pos, self.end_pos)
    
    def create_new_maze(self):
        """Create a new maze component with random algorithm and theme."""
        # Calculate position for new maze component
        # Center the maze horizontally
        maze_width = MAZE_WIDTH * self.cell_size_slider.value
        x = (WINDOW_WIDTH - maze_width) // 2
        
        # Position vertically based on number of existing mazes
        y = (WINDOW_HEIGHT) // 2
        
        # Create new maze component
        new_component = MazeComponent(
            x,
            y,
            MAZE_WIDTH,
            MAZE_HEIGHT,
            self.cell_size_slider.value,  # Use current cell size from slider
            self.button_style,
            self.maze_generator
        )
        
        # Randomly select algorithm and theme
        import random
        random_algorithm = random.choice(list(self.solvers.keys()))
        random_theme = random.choice(self.animation_themes)
        
        # Set the random selections
        new_component.algorithm_dropdown.selected = random_algorithm
        new_component.animation_theme_dropdown.selected = random_theme
        # Apply the theme change to the component's own animation theme
        new_component.animation_theme.set_theme(random_theme.lower())
        
        # If there's a shared maze, set it for the new component
        if self.shared_maze is not None:
            new_component.set_maze(self.shared_maze, self.start_pos, self.end_pos)
        
        # Add to list of components
        self.maze_components.append(new_component)
    
    def solve_maze(self):
        """Solve all maze components simultaneously."""
        # Reset all mazes and clear solved list
        self.solved_mazes = []
        for component in self.maze_components:
            component.reset_solving()
        
        # Start solving all mazes
        for component in self.maze_components:
            component.start_solving(self.solvers[component.algorithm_dropdown.selected])
    
    def reset_solving(self):
        """Reset the solving animation for all maze components."""
        self.solved_mazes = []  # Clear solved mazes list
        for component in self.maze_components:
            component.reset_solving()
    
    def change_app_theme(self, theme_name):
        """Change the current app theme and logo."""
        theme_name = theme_name.lower()
        self.app_theme.set_theme(theme_name)
        self.button_style = ButtonStyle(self.app_theme)
        
        # Update all buttons and dropdowns
        for button in self.buttons:
            button.style = self.button_style
        self.app_theme_dropdown.style = self.button_style
        
        # Update sliders
        self.width_slider.update_style(self.button_style)
        self.height_slider.update_style(self.button_style)
        self.cell_size_slider.update_style(self.button_style)
        
        # Update all components
        for component in self.maze_components:
            component.button_style = self.button_style
            component.algorithm_dropdown.style = self.button_style
            component.animation_theme_dropdown.style = self.button_style
            component.nodes_button.style = self.button_style  # Update nodes button style
            # Update nodes component if it exists
            if component.nodes_component:
                component.nodes_component.button_style = self.button_style
        
        # Update logo
        self.current_logo = self.logos[theme_name]
    
    def randomize_all_mazes(self):
        """Randomize algorithm and theme for all maze components and reset any running mazes."""
        import random
        
        # Reset solved mazes list
        self.solved_mazes = []
        
        # Get lists of available algorithms and themes
        available_algorithms = list(self.solvers.keys())
        available_themes = self.animation_themes.copy()
        
        # Shuffle the lists to randomize the order
        random.shuffle(available_algorithms)
        random.shuffle(available_themes)
        
        # Reset any running mazes
        for component in self.maze_components:
            component.reset_solving()
            
            # Try to get a unique algorithm and theme
            if available_algorithms:
                algorithm = available_algorithms.pop()
            else:
                # If we ran out of unique algorithms, pick a random one
                algorithm = random.choice(list(self.solvers.keys()))
                
            if available_themes:
                theme = available_themes.pop()
            else:
                # If we ran out of unique themes, pick a random one
                theme = random.choice(self.animation_themes)
            
            # Update the component
            component.algorithm_dropdown.selected = algorithm
            component.animation_theme_dropdown.selected = theme
            component.animation_theme.set_theme(theme.lower())
    
    def toggle_pause(self):
        """Toggle the pause state and update the button text."""
        self.is_paused = not self.is_paused
        self.pause_button.text = "Resume" if self.is_paused else "Pause"
    
    def update_solving(self):
        """Update solving animation for all components and check for completed mazes."""
        # Skip updates if paused
        if self.is_paused:
            return
            
        # First, check for newly solved mazes
        for component in self.maze_components:
            if component.solving:
                component.update_solving()
                # Check if maze is solved
                if not component.solving and component.solution is not None and component.elapsed_time > 0:
                    # Only process if this maze hasn't been solved yet
                    if component not in self.solved_mazes:
                        self.solved_mazes.append(component)
        
        # Then, update themes for all solved mazes in order
        for i, component in enumerate(self.solved_mazes):
            # Assign theme based on completion order
            if i == 0:  # First to finish
                solution_theme = AnimationTheme("gold")
            elif i == 1:  # Second to finish
                solution_theme = AnimationTheme("silver")
            elif i == 2:  # Third to finish
                solution_theme = AnimationTheme("bronze")
            else:  # All others
                solution_theme = AnimationTheme("metal")
            
            # Only set the solution color, keeping other colors the same
            component.animation_theme.solution_base = solution_theme.solution_base
            component.animation_theme.solution_sparkle = solution_theme.solution_sparkle
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            current_event = None
            for event in pygame.event.get():
                current_event = event
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # Handle app theme dropdown
                selected_theme = self.app_theme_dropdown.handle_event(event)
                if selected_theme:
                    self.change_app_theme(selected_theme)
                
                # Handle maze generator dropdown
                selected_generator = self.generator_dropdown.handle_event(event)
                if selected_generator:
                    self.generate_maze()  # Regenerate maze with new generator
                
                # Handle dimension sliders
                new_width = self.width_slider.handle_event(event)
                new_height = self.height_slider.handle_event(event)
                new_cell_size = self.cell_size_slider.handle_event(event)
                
                # If dimensions changed, update maze
                if new_width is not None or new_height is not None or new_cell_size is not None:
                    self.update_maze_dimensions()
                
                # Handle maze component events
                for i, component in enumerate(self.maze_components):
                    algorithm, animation_theme, close = component.handle_event(event)
                    if close == "close":
                        self.maze_components.pop(i)
                        break
                
                # Handle button events
                for button in self.buttons:
                    action = button.handle_event(event)
                    if action:
                        action()
            
            # Update solving animation and check for completed mazes
            self.update_solving()
            
            self.draw(current_event)
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
        
    def update_maze_dimensions(self):
        """Update maze dimensions and regenerate if needed."""
        new_width = self.width_slider.value
        new_height = self.height_slider.value
        new_cell_size = self.cell_size_slider.value
        
        # Update MAZE_WIDTH and MAZE_HEIGHT constants
        global MAZE_WIDTH, MAZE_HEIGHT
        MAZE_WIDTH = new_width
        MAZE_HEIGHT = new_height
        
        # Get the selected generator class
        generator_name = self.generator_dropdown.selected
        generator_class = self.generators.get(generator_name, DFSMazeGenerator)
        
        # Update maze generator with new dimensions
        self.maze_generator = generator_class(new_width, new_height)
        
        # Update cell size for all components
        for component in self.maze_components:
            component.cell_size = new_cell_size
            component.maze_width = new_width
            component.maze_height = new_height
            
            # Recalculate component dimensions based on new cell size
            component.width = max(new_width * new_cell_size, 
                                component.close_button_width + 10 + 
                                180 * 2 + 20 +
                                component.timer_width)
            component.height = new_height * new_cell_size + 40 * 2 + 10 * 2
        
        # Regenerate maze with new dimensions
        self.generate_maze()
    
    def draw(self, event=None):
        """Draw the game screen."""
        self.screen.fill(self.app_theme.background)
        
        # Draw current theme's logo
        self.screen.blit(self.current_logo, (20, 10))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw dimension sliders
        self.width_slider.draw(self.screen)
        self.height_slider.draw(self.screen)
        self.cell_size_slider.draw(self.screen)
        
        # Draw dropdowns and their options
        self.generator_dropdown.draw(self.screen)
        self.generator_dropdown.draw_options(self.screen)
        self.app_theme_dropdown.draw(self.screen)
        self.app_theme_dropdown.draw_options(self.screen)
        
        # Draw all maze components
        for component in self.maze_components:
            component.draw(self.screen, self.app_theme, None, event)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = MazeGame()
    game.run() 