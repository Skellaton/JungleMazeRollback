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