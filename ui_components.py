import pygame

class MazeNodes:
    def __init__(self, x, y, maze_width, maze_height, cell_size, button_style, maze):
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Maze properties
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = cell_size
        self.maze = maze
        
        # Component dimensions
        button_width = 40  # Width of close button
        self.width = maze_width * cell_size
        self.height = maze_height * cell_size + button_width
        
        # Close button properties
        self.close_button_rect = pygame.Rect(
            x,  # Start at component's x
            y,  # Start at component's y
            button_width,
            button_width
        )
        self.close_button_hovered = False
        self.button_style = button_style
        
    def handle_event(self, event):
        # Handle close button
        if event.type == pygame.MOUSEMOTION:
            self.close_button_hovered = self.close_button_rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.close_button_rect.collidepoint(event.pos):
                    return "close"
                
                mouse_x, mouse_y = event.pos
                # Check if click is in the component but not in the close button
                if (self.x <= mouse_x <= self.x + self.width and 
                    self.y + self.close_button_rect.height <= mouse_y <= self.y + self.height):
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
                # Update close button position
                self.close_button_rect.x = self.x
                self.close_button_rect.y = self.y
        
        return None
    
    def draw(self, screen, app_theme):
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