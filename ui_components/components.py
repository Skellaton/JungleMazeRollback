import pygame

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

class MazeNodes:
    def __init__(self, x, y, maze_width, maze_height, cell_size, button_style, maze, parent_component):
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Parent component reference for linked movement
        self.parent_component = parent_component
        self.is_locked = False
        
        # Store initial relative position to parent
        self.relative_x = x - parent_component.x
        self.relative_y = y - parent_component.y
        
        # Maze properties
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = cell_size
        self.maze = maze
        
        # Component dimensions
        self.button_width = 40  # Width of buttons
        self.width = maze_width * cell_size
        self.height = maze_height * cell_size + self.button_width
        
        # Close button properties
        self.close_button_rect = pygame.Rect(
            x,  # Start at component's x
            y,  # Start at component's y
            self.button_width,
            self.button_width
        )
        self.close_button_hovered = False
        
        # Lock button properties
        self.lock_button_rect = pygame.Rect(
            x + self.button_width,  # Position after close button
            y,
            self.button_width,
            self.button_width
        )
        self.lock_button_hovered = False
        self.button_style = button_style
        
    def handle_event(self, event):
        # Handle close and lock buttons
        if event.type == pygame.MOUSEMOTION:
            self.close_button_hovered = self.close_button_rect.collidepoint(event.pos)
            self.lock_button_hovered = self.lock_button_rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.close_button_rect.collidepoint(event.pos):
                    return "close"
                elif self.lock_button_rect.collidepoint(event.pos):
                    self.is_locked = not self.is_locked
                    # Update relative position when locking
                    if self.is_locked:
                        self.relative_x = self.x - self.parent_component.x
                        self.relative_y = self.y - self.parent_component.y
                    return None
                
                mouse_x, mouse_y = event.pos
                # Check if click is in the component but not in the buttons
                if (self.x <= mouse_x <= self.x + self.width and 
                    self.y + self.button_width <= mouse_y <= self.y + self.height):
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
        
        return None
    
    def move_to(self, new_x, new_y):
        """Move the component to a new position and update all related positions."""
        self.x = new_x
        self.y = new_y
        # Update button positions
        self.close_button_rect.x = self.x
        self.close_button_rect.y = self.y
        self.lock_button_rect.x = self.x + self.button_width
        self.lock_button_rect.y = self.y
        
        # If locked, move parent component
        if self.is_locked:
            parent_new_x = self.x - self.relative_x
            parent_new_y = self.y - self.relative_y
            self.parent_component.move_to(parent_new_x, parent_new_y)
    
    def update_position_from_parent(self):
        """Update position based on parent's movement when locked."""
        if self.is_locked:
            new_x = self.parent_component.x + self.relative_x
            new_y = self.parent_component.y + self.relative_y
            self.move_to(new_x, new_y)
    
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
        
        # Draw lock button
        color = self.button_style.hover_color if self.lock_button_hovered else self.button_style.background_color
        if self.is_locked:
            color = self.button_style.hover_color  # Keep highlighted when locked
        pygame.draw.rect(screen, color, self.lock_button_rect)
        pygame.draw.rect(screen, self.button_style.border_color, self.lock_button_rect, self.button_style.border_width)
        
        # Draw lock symbol
        lock_margin = 10
        lock_color = self.button_style.text_color
        # Draw lock body
        lock_body = pygame.Rect(
            self.lock_button_rect.centerx - 8,
            self.lock_button_rect.centery - 2,
            16,
            14
        )
        pygame.draw.rect(screen, lock_color, lock_body, 2)
        # Draw lock shackle
        if self.is_locked:
            # Closed shackle
            pygame.draw.arc(screen, lock_color,
                          [self.lock_button_rect.centerx - 8,
                           self.lock_button_rect.centery - 12,
                           16, 16],
                          0, 3.14, 2)
        else:
            # Open shackle
            pygame.draw.arc(screen, lock_color,
                          [self.lock_button_rect.centerx - 4,
                           self.lock_button_rect.centery - 12,
                           16, 16],
                          -3.14/2, 3.14/2, 2) 