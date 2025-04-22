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
        self.current_solver = "A*"
        
        # Initialize maze generators and solvers for all three mazes
        self.maze_generators = [DFSMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)]
        self.mazes = [None]
        self.solutions = [None]
        self.solving = [False]
        self.current_cells = [None]
        self.explored_cells = [set()]
        self.generate_all_mazes()
        
        # Create buttons and dropdowns
        button_width = 180
        button_height = 40
        button_spacing = 30
        button_y = 20
        
        # Adjust button positions to account for logo
        buttons_start_x = 250  # Start buttons after the logo
        
        # Create main buttons
        self.generate_button = Button(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2,
            button_y,
            button_width,
            button_height,
            "Generate",
            self.generate_all_mazes,
            self.button_style
        )
        
        self.solve_button = Button(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2 + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "Solve Maze",
            self.solve_all_mazes,
            self.button_style
        )
        
        # Create theme dropdowns
        self.app_theme_dropdown = Dropdown(
            buttons_start_x + (WINDOW_WIDTH - buttons_start_x - button_width * 3 - button_spacing * 2) // 2 + (button_width + button_spacing) * 2,
            button_y,
            button_width,
            button_height,
            ["Jungle", "Dark"],
            self.button_style
        )
        
        # Create algorithm and animation theme dropdowns on the left
        left_dropdown_x = MAZE_OFFSET_X - button_width - 20
        
        self.algorithm_dropdown = Dropdown(
            left_dropdown_x,
            MAZE_OFFSET_Y,
            button_width,
            button_height,
            list(self.solvers.keys()),
            self.button_style
        )
        
        self.animation_theme_dropdown = Dropdown(
            left_dropdown_x,
            MAZE_OFFSET_Y + button_height + 10,
            button_width,
            button_height,
            ["Default", "Neon", "Fire", "Ocean", "Sunset", "Matrix", "Candy", "Rainbow"],
            self.button_style
        )
        
        self.buttons = [self.generate_button, self.solve_button]
    
    def generate_all_mazes(self):
        """Generate new maze."""
        self.mazes[0] = self.maze_generators[0].generate()
        self.solutions[0] = None
    
    def solve_all_mazes(self):
        """Start solving all mazes."""
        for i in range(1):
            if self.mazes[i] is not None and not self.solving[i]:
                self.solving[i] = True
                self.solutions[i] = None
                self.current_cells[i] = None
                self.explored_cells[i] = set()
                start, end = self.maze_generators[i].get_start_end_points()
                solver_class = self.solvers[self.current_solver]
                self.solver = solver_class(self.mazes[i])
                self.solver_generator = self.solver.solve_step_by_step(start, end)
                self.update_solving(i)
    
    def update_solving(self, maze_index):
        """Update the solving animation state for a specific maze."""
        if self.solving[maze_index]:
            try:
                result = next(self.solver_generator)
                if isinstance(result, tuple):
                    # Current cell being explored
                    self.current_cells[maze_index] = result
                    self.explored_cells[maze_index].add(result)
                elif isinstance(result, list):
                    # Final solution path
                    self.solutions[maze_index] = result
                    self.solving[maze_index] = False
            except StopIteration:
                self.solving[maze_index] = False
    
    def change_app_theme(self, theme_name):
        """Change the current app theme and logo."""
        theme_name = theme_name.lower()
        self.app_theme.set_theme(theme_name)
        self.button_style = ButtonStyle(self.app_theme)
        for button in self.buttons:
            button.style = self.button_style
        self.app_theme_dropdown.style = self.button_style
        self.algorithm_dropdown.style = self.button_style
        self.animation_theme_dropdown.style = self.button_style
        self.current_logo = self.logos[theme_name]
    
    def change_animation_theme(self, theme_name):
        """Change the current animation theme."""
        self.animation_theme.set_theme(theme_name.lower())
    
    def change_algorithm(self, algorithm_name):
        """Change the current solving algorithm."""
        if algorithm_name in self.solvers:
            self.current_solver = algorithm_name
    
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
                
                # Handle algorithm dropdown
                selected_algorithm = self.algorithm_dropdown.handle_event(event)
                if selected_algorithm:
                    self.change_algorithm(selected_algorithm)
                
                # Handle animation theme dropdown
                selected_animation_theme = self.animation_theme_dropdown.handle_event(event)
                if selected_animation_theme:
                    self.change_animation_theme(selected_animation_theme)
                
                # Handle button events
                for button in self.buttons:
                    action = button.handle_event(event)
                    if action:
                        action()
            
            # Update solving animation for all mazes
            for i in range(1):
                if self.solving[i]:
                    self.update_solving(i)
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
        
    def draw(self):
        """Draw the maze and its solution."""
        self.screen.fill(self.app_theme.background)
        
        # Draw current theme's logo
        self.screen.blit(self.current_logo, (20, 10))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw dropdowns
        self.app_theme_dropdown.draw(self.screen)
        self.algorithm_dropdown.draw(self.screen)
        self.animation_theme_dropdown.draw(self.screen)
        
        # Draw the maze
        maze_index = 0
        maze_offset_y = MAZE_OFFSET_Y
        
        # Draw maze
        for y in range(self.mazes[maze_index].shape[0]):
            for x in range(self.mazes[maze_index].shape[1]):
                rect = pygame.Rect(
                    x * CELL_SIZE + MAZE_OFFSET_X,
                    y * CELL_SIZE + maze_offset_y,
                    CELL_SIZE,
                    CELL_SIZE
                )
                if self.mazes[maze_index][y, x] == 1:  # Wall
                    pygame.draw.rect(self.screen, self.app_theme.border, rect)
                else:  # Path
                    pygame.draw.rect(self.screen, self.app_theme.accent, rect)
        
        # Draw start and end points
        start, end = self.maze_generators[maze_index].get_start_end_points()
        pygame.draw.rect(self.screen, self.app_theme.start_color,
                       (start[0] * CELL_SIZE + MAZE_OFFSET_X,
                        start[1] * CELL_SIZE + maze_offset_y,
                        CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, self.app_theme.end_color,
                       (end[0] * CELL_SIZE + MAZE_OFFSET_X,
                        end[1] * CELL_SIZE + maze_offset_y,
                        CELL_SIZE, CELL_SIZE))
        
        # Draw explored cells
        for x, y in self.explored_cells[maze_index]:
            if (x, y) != start and (x, y) != end:
                pygame.draw.rect(self.screen, self.animation_theme.get_trail_color(),
                               (x * CELL_SIZE + MAZE_OFFSET_X,
                                y * CELL_SIZE + maze_offset_y,
                                CELL_SIZE, CELL_SIZE))
        
        # Draw current cell
        if self.current_cells[maze_index]:
            x, y = self.current_cells[maze_index]
            if (x, y) != start and (x, y) != end:
                pygame.draw.rect(self.screen, self.animation_theme.current_cell,
                               (x * CELL_SIZE + MAZE_OFFSET_X,
                                y * CELL_SIZE + maze_offset_y,
                                CELL_SIZE, CELL_SIZE))
        
        # Draw solution path
        if self.solutions[maze_index]:
            for x, y in self.solutions[maze_index]:
                if (x, y) != start and (x, y) != end:
                    pygame.draw.rect(self.screen, self.app_theme.solution_color,
                                   (x * CELL_SIZE + MAZE_OFFSET_X,
                                    y * CELL_SIZE + maze_offset_y,
                                    CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = MazeGame()
    game.run() 