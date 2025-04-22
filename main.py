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
        self.maze_generator = maze_generator  # Store reference to maze generator
        
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
        
        # Add z-index tracking
        self.dropdowns_open = False
    
    def set_maze(self, maze):
        """Set the maze for this component."""
        self.maze = maze
        self.solution = None
        self.solving = False
        self.current_cell = None
        self.explored_cells = set()
        self.elapsed_time = 0
    
    def start_solving(self, solver_class):
        if self.maze is not None and not self.solving:
            self.solving = True
            self.solution = None
            self.current_cell = None
            self.explored_cells = set()
            self.start_time = pygame.time.get_ticks()
            start, end = self.maze_generator.get_start_end_points()
            self.solver = solver_class(self.maze)
            self.solver_generator = self.solver.solve_step_by_step(start, end)
    
    def update_solving(self):
        if self.solving:
            try:
                result = next(self.solver_generator)
                if isinstance(result, tuple):
                    self.current_cell = result
                    self.explored_cells.add(result)
                elif isinstance(result, list):
                    self.solution = result
                    self.solving = False
                    self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            except StopIteration:
                self.solving = False
                self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
    
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
        
        return algorithm, animation_theme, None
    
    def draw(self, screen, app_theme, animation_theme):
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
        
        # Draw start and end points
        start, end = self.maze_generator.get_start_end_points()
        pygame.draw.rect(screen, app_theme.start_color,
                       (start[0] * self.cell_size + maze_x,
                        start[1] * self.cell_size + maze_y,
                        self.cell_size, self.cell_size))
        pygame.draw.rect(screen, app_theme.end_color,
                       (end[0] * self.cell_size + maze_x,
                        end[1] * self.cell_size + maze_y,
                        self.cell_size, self.cell_size))
        
        # Draw explored cells
        for x, y in self.explored_cells:
            if (x, y) != start and (x, y) != end:
                pygame.draw.rect(screen, animation_theme.get_trail_color(),
                               (x * self.cell_size + maze_x,
                                y * self.cell_size + maze_y,
                                self.cell_size, self.cell_size))
        
        # Draw current cell
        if self.current_cell:
            x, y = self.current_cell
            if (x, y) != start and (x, y) != end:
                pygame.draw.rect(screen, animation_theme.current_cell,
                               (x * self.cell_size + maze_x,
                                y * self.cell_size + maze_y,
                                self.cell_size, self.cell_size))
        
        # Draw solution path
        if self.solution:
            for x, y in self.solution:
                if (x, y) != start and (x, y) != end:
                    pygame.draw.rect(screen, app_theme.solution_color,
                                   (x * self.cell_size + maze_x,
                                    y * self.cell_size + maze_y,
                                    self.cell_size, self.cell_size))
        
        # Draw dropdown options on top of everything
        self.algorithm_dropdown.draw_options(screen)
        self.animation_theme_dropdown.draw_options(screen)

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
        self.animation_theme = AnimationTheme()
        self.button_style = ButtonStyle(self.app_theme)
        
        # Set initial logo based on default theme
        self.current_logo = self.logos["jungle"]
        
        # Initialize solvers
        self.solvers = {
            "A*": AStarMazeSolver,
            "BFS": BFSMazeSolver,
            "Random": RandomMazeSolver
        }
        
        # Initialize maze components list
        self.maze_components = []
        
        # Initialize shared maze
        self.shared_maze = None
        self.maze_generator = DFSMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        
        # Create buttons
        button_width = 180
        button_height = 40
        button_spacing = 30
        button_y = 20
        buttons_start_x = 250
        
        self.generate_button = Button(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2,
            button_y,
            button_width,
            button_height,
            "Generate",
            self.generate_maze,
            self.button_style
        )
        
        self.solve_button = Button(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2 + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "Solve Maze",
            self.solve_maze,
            self.button_style
        )
        
        self.new_maze_button = Button(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2 + (button_width + button_spacing) * 2,
            button_y,
            button_width,
            button_height,
            "New Maze",
            self.create_new_maze,
            self.button_style
        )
        
        self.app_theme_dropdown = Dropdown(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2 + (button_width + button_spacing) * 3,
            button_y,
            button_width,
            button_height,
            ["Jungle", "Dark"],
            self.button_style
        )
        
        self.buttons = [self.generate_button, self.solve_button, self.new_maze_button]
        
        # Create initial maze component and generate first maze
        self.create_new_maze()
        self.generate_maze()  # Generate initial maze
    
    def generate_maze(self):
        """Generate a new maze that will be shared across all components."""
        self.shared_maze = self.maze_generator.generate()
        # Update all components with the new maze
        for component in self.maze_components:
            component.set_maze(self.shared_maze)
    
    def create_new_maze(self):
        """Create a new maze component."""
        # Calculate position for new maze component
        x = MAZE_OFFSET_X
        y = MAZE_OFFSET_Y + len(self.maze_components) * (MAZE_HEIGHT * CELL_SIZE + MAZE_SPACING)
        
        # Create new maze component
        new_component = MazeComponent(
            x,
            y,
            MAZE_WIDTH,
            MAZE_HEIGHT,
            CELL_SIZE,
            self.button_style,
            self.maze_generator  # Pass the maze generator
        )
        
        # If there's a shared maze, set it for the new component
        if self.shared_maze is not None:
            new_component.set_maze(self.shared_maze)
        
        # Add to list of components
        self.maze_components.append(new_component)
    
    def solve_maze(self):
        """Solve the most recently created maze."""
        if self.maze_components:
            self.maze_components[-1].start_solving(self.solvers[self.maze_components[-1].algorithm_dropdown.selected])
    
    def change_app_theme(self, theme_name):
        """Change the current app theme and logo."""
        theme_name = theme_name.lower()
        self.app_theme.set_theme(theme_name)
        self.button_style = ButtonStyle(self.app_theme)
        for button in self.buttons:
            button.style = self.button_style
        self.app_theme_dropdown.style = self.button_style
        for component in self.maze_components:
            component.algorithm_dropdown.style = self.button_style
            component.animation_theme_dropdown.style = self.button_style
        self.current_logo = self.logos[theme_name]
    
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
                
                # Handle maze component events
                for i, component in enumerate(self.maze_components):
                    algorithm, animation_theme, close = component.handle_event(event)
                    if animation_theme:
                        self.animation_theme.set_theme(animation_theme.lower())
                    if close == "close":
                        self.maze_components.pop(i)
                        break
                
                # Handle button events
                for button in self.buttons:
                    action = button.handle_event(event)
                    if action:
                        action()
            
            # Update solving animation for all components
            for component in self.maze_components:
                if component.solving:
                    component.update_solving()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def draw(self):
        """Draw the game screen."""
        self.screen.fill(self.app_theme.background)
        
        # Draw current theme's logo
        self.screen.blit(self.current_logo, (20, 10))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw app theme dropdown
        self.app_theme_dropdown.draw(self.screen)
        
        # Draw all maze components
        for component in self.maze_components:
            component.draw(self.screen, self.app_theme, self.animation_theme)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = MazeGame()
    game.run() 