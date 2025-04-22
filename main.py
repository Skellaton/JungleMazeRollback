import pygame
import sys
from maze.generators import DFSMazeGenerator
from maze.solvers import AStarMazeSolver, BFSMazeSolver, RandomMazeSolver

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 15
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
    
    def __init__(self, theme_name="default"):
        self.themes = {
            "default": {
                "current_cell": (255, 215, 0),    # Gold
                "trail": (144, 238, 144)          # Light green
            },
            "neon": {
                "current_cell": (255, 0, 255),    # Magenta
                "trail": (0, 255, 255)            # Cyan
            },
            "fire": {
                "current_cell": (255, 69, 0),     # Red-Orange
                "trail": (255, 140, 0)            # Dark Orange
            },
            "ocean": {
                "current_cell": (0, 191, 255),    # Deep Sky Blue
                "trail": (0, 105, 148)            # Dark Blue
            },
            "sunset": {
                "current_cell": (255, 99, 71),    # Tomato Red
                "trail": (255, 182, 193)          # Light Pink
            },
            "matrix": {
                "current_cell": (0, 255, 0),      # Bright Green
                "trail": (0, 100, 0)              # Dark Green
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
    
    def set_theme(self, theme_name):
        """Set the current animation theme."""
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            self.current_cell = theme["current_cell"]
            self.trail = theme["trail"]
            self.current_theme = theme_name
    
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
        """Get the trail color, with special handling for rainbow theme."""
        if self.current_theme == "rainbow":
            return self.get_random_rainbow_color()
        return self.trail

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
            "dark": {
                "background": (0, 0, 0),        # Black
                "text": (255, 255, 255),       # White
                "border": (0, 0, 0),           # Black
                "accent": (50, 50, 50),        # Dark gray
                "button_hover": (70, 70, 70)
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

class ButtonStyle:
    """Class to define button styling properties."""
    
    def __init__(self, theme):
        # Colors
        self.background_color = theme.button_background
        self.hover_color = theme.button_hover
        self.border_color = theme.button_border
        self.text_color = theme.button_text
        
        # Font
        self.font = pygame.font.SysFont('consolas', 24)
        
        # Dimensions
        self.border_width = 2
        
    def get_background_color(self, is_hovered):
        """Get the appropriate background color based on hover state."""
        return self.hover_color if is_hovered else self.background_color

class Button:
    def __init__(self, x, y, width, height, text, action, style):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.style = style
        
    def draw(self, screen):
        # Draw button background
        color = self.style.get_background_color(self.is_hovered)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.style.border_color, self.rect, self.style.border_width)
        
        # Draw button text
        text_surface = self.style.font.render(self.text, True, self.style.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    return self.action
        return None

class Dropdown:
    def __init__(self, x, y, width, height, options, style):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = options[0]
        self.is_open = False
        self.style = style
        self.option_rects = []
    
    def draw(self, screen):
        # Draw main button
        color = self.style.get_background_color(self.is_open)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.style.border_color, self.rect, self.style.border_width)
        
        # Draw selected text
        text_surface = self.style.font.render(self.selected, True, self.style.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Draw dropdown arrow
        arrow_points = [
            (self.rect.right - 10, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery + 5),
            (self.rect.right - 5, self.rect.centery)
        ]
        pygame.draw.polygon(screen, self.style.text_color, arrow_points)
    
    def draw_options(self, screen):
        # Draw options if open
        if self.is_open:
            self.option_rects = []
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height * (i + 1),
                    self.rect.width,
                    self.rect.height
                )
                self.option_rects.append(option_rect)
                
                # Draw option background
                pygame.draw.rect(screen, self.style.background_color, option_rect)
                pygame.draw.rect(screen, self.style.border_color, option_rect, self.style.border_width)
                
                # Draw option text
                text_surface = self.style.font.render(option, True, self.style.text_color)
                text_rect = text_surface.get_rect(center=option_rect.center)
                screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    self.is_open = not self.is_open
                elif self.is_open:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = self.options[i]
                            self.is_open = False
                            return self.selected
        return None

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, label, style):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.style = style
        self.dragging = False
        self.font = pygame.font.SysFont('consolas', 16)
        
    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, self.style.background_color, self.rect)
        pygame.draw.rect(screen, self.style.border_color, self.rect, self.style.border_width)
        
        # Draw filled portion of track
        filled_width = (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(screen, self.style.hover_color, filled_rect)
        
        # Draw slider handle
        handle_x = self.rect.x + filled_width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, self.style.hover_color if self.dragging else self.style.background_color, handle_rect)
        pygame.draw.rect(screen, self.style.border_color, handle_rect, self.style.border_width)
        
        # Draw label and value
        label_text = f"{self.label}: {self.value}"
        label_surface = self.font.render(label_text, True, self.style.text_color)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 20))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                handle_x = self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width
                handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
                if handle_rect.collidepoint(event.pos):
                    self.dragging = True
                elif self.rect.collidepoint(event.pos):
                    # Click on track - move handle to click position
                    self.dragging = True
                    self.update_value(event.pos[0])
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])
        
        return self.value if self.dragging else None
    
    def update_value(self, mouse_x):
        # Calculate new value based on mouse position
        relative_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        self.value = int(self.min_value + (relative_x / self.rect.width) * (self.max_value - self.min_value))
        return self.value
    
    def update_style(self, new_style):
        """Update the slider's style."""
        self.style = new_style

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
        self.animation_theme = AnimationTheme()
        
        # Component dimensions
        button_width = 180
        button_height = 40
        button_spacing = 10
        self.close_button_width = 40  # Width of close button
        self.timer_width = 120  # Width of timer box
        self.width = max(maze_width * cell_size, 
                        self.close_button_width + button_spacing + 
                        button_width * 2 + button_spacing * 2 +
                        self.timer_width)
        self.height = maze_height * cell_size + button_height * 2 + button_spacing * 2
        
        # Timer properties
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_font = pygame.font.SysFont('consolas', 24)
        self.timer_rect = pygame.Rect(
            x + self.close_button_width + button_spacing + button_width * 2 + button_spacing * 2,
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
        
        # Create dropdowns
        self.algorithm_dropdown = Dropdown(
            x + self.close_button_width + button_spacing,  # Position after close button
            y,
            button_width,
            button_height,
            ["A*", "BFS", "Random"],
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
    
    def handle_event(self, event):
        # Handle dropdowns
        algorithm = self.algorithm_dropdown.handle_event(event)
        animation_theme = self.animation_theme_dropdown.handle_event(event)
        
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
                self.x = mouse_x - self.drag_offset_x
                self.y = mouse_y - self.drag_offset_y
                # Update positions
                self.close_button_rect.x = self.x
                self.close_button_rect.y = self.y
                self.algorithm_dropdown.rect.x = self.x + self.close_button_width + 10
                self.algorithm_dropdown.rect.y = self.y
                self.animation_theme_dropdown.rect.x = self.x + self.close_button_width + 10 + 180 + 10
                self.animation_theme_dropdown.rect.y = self.y
                self.timer_rect.x = self.x + self.close_button_width + 10 + 180 * 2 + 20
                self.timer_rect.y = self.y
        
        # Apply theme change if needed
        if animation_theme:
            self.animation_theme.set_theme(animation_theme.lower())
        
        return algorithm, animation_theme, None
    
    def draw(self, screen, app_theme, _):
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
        
        # Draw dropdowns
        self.algorithm_dropdown.draw(screen)
        self.animation_theme_dropdown.draw(screen)
        
        # Draw timer box
        pygame.draw.rect(screen, self.button_style.background_color, self.timer_rect)
        pygame.draw.rect(screen, self.button_style.border_color, self.timer_rect, self.button_style.border_width)
        
        # Draw timer text
        timer_text = f"{self.elapsed_time:.2f}s"
        timer_surface = self.timer_font.render(timer_text, True, self.button_style.text_color)
        timer_text_rect = timer_surface.get_rect(center=self.timer_rect.center)
        screen.blit(timer_surface, timer_text_rect)
        
        # Calculate maze position (centered horizontally in the component)
        maze_x = self.x + (self.width - self.maze_width * self.cell_size) // 2
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
                pygame.draw.rect(screen, self.animation_theme.get_trail_color(),
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
                    pygame.draw.rect(screen, app_theme.solution_color,
                                   (x * self.cell_size + maze_x,
                                    y * self.cell_size + maze_y,
                                    self.cell_size, self.cell_size))
        
        # Draw dropdown options on top of everything
        self.algorithm_dropdown.draw_options(screen)
        self.animation_theme_dropdown.draw_options(screen)

class Scoreboard:
    def __init__(self, x, y, width, height, theme):
        self.rect = pygame.Rect(x, y, width, height)
        self.scores = []  # List of (algorithm, time, theme) tuples
        self.theme = theme
        self.font = pygame.font.SysFont('consolas', 20)
        self.max_entries = 5  # Maximum number of scores to display
    
    def add_score(self, algorithm, time, animation_theme):
        """Add a new score to the scoreboard."""
        self.scores.append((algorithm, time, animation_theme))
        # Sort by time (ascending)
        self.scores.sort(key=lambda x: x[1])
        # Keep only the best scores
        if len(self.scores) > self.max_entries:
            self.scores = self.scores[:self.max_entries]
    
    def clear(self):
        """Clear all scores from the scoreboard."""
        self.scores = []
    
    def draw(self, screen):
        """Draw the scoreboard."""
        # Draw scores
        y_offset = 0  # Start from top since we removed the title
        for algorithm, time, theme in self.scores:
            # Create text with algorithm and time
            text = f"{algorithm}: {time:.2f}s"
            text_surface = self.font.render(text, True, theme.current_cell)
            screen.blit(text_surface, (self.rect.x, self.rect.y + y_offset))
            y_offset += 25

class MazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Generator and Solver")
        self.clock = pygame.time.Clock()
        
        # Load and scale logos
        self.logos = {
            "jungle": pygame.transform.scale(pygame.image.load("assets/logo_jungle.png"), (200, 200)),
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
            "Random": RandomMazeSolver
        }
        self.animation_themes = ["Default", "Neon", "Fire", "Ocean", "Sunset", "Matrix", "Candy", "Rainbow"]
        
        # Initialize maze components list
        self.maze_components = []
        
        # Initialize shared maze
        self.shared_maze = None
        self.maze_generator = DFSMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        
        # Create buttons and sliders
        button_width = 180
        button_height = 40
        button_spacing = 20
        button_y = 20
        
        # Calculate positions for sliders and buttons
        slider_width = 200
        slider_height = 10
        slider_spacing = 40
        slider_y = button_y + (button_height - slider_height) // 2  # Center vertically with buttons
        
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
            50,  # max width
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
            30,  # max height
            MAZE_HEIGHT,  # initial height
            "Height",
            self.button_style
        )
        
        # Add cell size slider
        self.cell_size_slider = Slider(
            slider_x,
            slider_y + slider_spacing * 2,
            slider_width,
            slider_height,
            10,  # min cell size
            30,  # max cell size
            CELL_SIZE,  # initial cell size
            "Cell Size",
            self.button_style
        )
        
        # Create buttons
        self.generate_button = Button(
            buttons_x,
            button_y,
            button_width,
            button_height,
            "Generate",
            self.generate_maze,
            self.button_style
        )
        
        self.solve_button = Button(
            buttons_x + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "Solve Maze",
            self.solve_maze,
            self.button_style
        )
        
        self.reset_button = Button(
            buttons_x + (button_width + button_spacing) * 2,
            button_y,
            button_width,
            button_height,
            "Reset",
            self.reset_solving,
            self.button_style
        )
        
        self.new_maze_button = Button(
            buttons_x + (button_width + button_spacing) * 3,
            button_y,
            button_width,
            button_height,
            "New Maze",
            self.create_new_maze,
            self.button_style
        )
        
        self.randomize_all_button = Button(
            buttons_x + (button_width + button_spacing) * 4,
            button_y,
            button_width,
            button_height,
            "Random",
            self.randomize_all_mazes,
            self.button_style
        )
        
        self.app_theme_dropdown = Dropdown(
            buttons_x + (button_width + button_spacing) * 5,
            button_y,
            button_width,
            button_height,
            ["Jungle", "Dark"],
            self.button_style
        )
        
        self.buttons = [self.generate_button, self.solve_button, self.reset_button, 
                       self.new_maze_button, self.randomize_all_button]
        
        # Initialize scoreboard
        self.scoreboard = Scoreboard(
            20,  # x position (next to logo)
            220,  # y position (below logo)
            200,  # width
            160,  # height (5 entries * 25px + padding)
            self.app_theme
        )
        
        # Create initial maze component and generate first maze
        self.create_new_maze()
        self.generate_maze()  # Generate initial maze
    
    def generate_maze(self):
        """Generate a new maze that will be shared across all components."""
        # Generate the maze
        self.shared_maze = self.maze_generator.generate()
        
        # Get start and end positions
        self.start_pos, self.end_pos = self.maze_generator.get_start_end_points()
        
        # Update all components with the new maze and positions
        for component in self.maze_components:
            component.set_maze(self.shared_maze, self.start_pos, self.end_pos)
    
    def create_new_maze(self):
        """Create a new maze component with random algorithm and theme."""
        # Calculate position for new maze component
        x = MAZE_OFFSET_X
        y = MAZE_OFFSET_Y + len(self.maze_components) * (MAZE_HEIGHT * self.cell_size_slider.value + MAZE_SPACING)
        
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
        self.scoreboard.clear()  # Clear scoreboard when solving starts
        for component in self.maze_components:
            component.start_solving(self.solvers[component.algorithm_dropdown.selected])
    
    def reset_solving(self):
        """Reset the solving animation for all maze components."""
        self.scoreboard.clear()  # Clear scoreboard when reset is pressed
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
        
        # Update logo
        self.current_logo = self.logos[theme_name]
    
    def randomize_all_mazes(self):
        """Randomize algorithm and theme for all maze components and reset any running mazes."""
        import random
        for component in self.maze_components:
            # Reset any running mazes
            component.reset_solving()
            
            # Randomly select new algorithm and theme
            random_algorithm = random.choice(list(self.solvers.keys()))
            random_theme = random.choice(self.animation_themes)
            
            # Update the component
            component.algorithm_dropdown.selected = random_algorithm
            component.animation_theme_dropdown.selected = random_theme
            component.animation_theme.set_theme(random_theme.lower())
    
    def update_solving(self):
        """Update solving animation for all components and check for completed mazes."""
        for component in self.maze_components:
            if component.solving:
                component.update_solving()
                # Check if maze is solved
                if not component.solving and component.solution is not None and component.elapsed_time > 0:
                    # Add to scoreboard
                    self.scoreboard.add_score(
                        component.algorithm_dropdown.selected,
                        component.elapsed_time,
                        component.animation_theme
                    )
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # Handle app theme dropdown
                selected_theme = self.app_theme_dropdown.handle_event(event)
                if selected_theme:
                    self.change_app_theme(selected_theme)
                
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
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def update_maze_dimensions(self):
        """Update maze dimensions and regenerate if needed."""
        new_width = self.width_slider.value
        new_height = self.height_slider.value
        new_cell_size = self.cell_size_slider.value
        
        # Update maze generator with new dimensions
        self.maze_generator = DFSMazeGenerator(new_width, new_height)
        
        # Update cell size for all components
        for component in self.maze_components:
            component.cell_size = new_cell_size
            # Recalculate component dimensions based on new cell size
            component.width = max(component.maze_width * new_cell_size, 
                                component.close_button_width + 10 + 
                                180 * 2 + 20 +
                                component.timer_width)
            component.height = component.maze_height * new_cell_size + 40 * 2 + 10 * 2
        
        # Regenerate maze with new dimensions
        self.generate_maze()
    
    def draw(self):
        """Draw the game screen."""
        self.screen.fill(self.app_theme.background)
        
        # Draw current theme's logo
        self.screen.blit(self.current_logo, (20, 10))
        
        # Draw scoreboard
        self.scoreboard.draw(self.screen)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw dimension sliders
        self.width_slider.draw(self.screen)
        self.height_slider.draw(self.screen)
        self.cell_size_slider.draw(self.screen)
        
        # Draw app theme dropdown and its options
        self.app_theme_dropdown.draw(self.screen)
        self.app_theme_dropdown.draw_options(self.screen)
        
        # Draw all maze components
        for component in self.maze_components:
            component.draw(self.screen, self.app_theme, None)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = MazeGame()
    game.run() 