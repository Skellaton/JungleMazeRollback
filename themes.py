from animation_themes import ThemeInterface, MatrixTheme, FireTheme, OceanTheme, finish_tracker
from typing import Optional

class ThemeFactory:
    """Factory for creating theme instances"""
    @staticmethod
    def create_theme(theme_name: str, maze_id: Optional[int] = None) -> ThemeInterface:
        theme_map = {
            "matrix": MatrixTheme,
            "fire": FireTheme,
            "ocean": OceanTheme,
            # Add more themes here
        }
        
        theme_class = theme_map.get(theme_name.lower())
        if theme_class:
            theme = theme_class()
            if maze_id is not None:
                theme.set_maze_id(maze_id)
            return theme
        return MatrixTheme()  # Default theme

    @staticmethod
    def reset_finish_order():
        """Reset the finish order tracker"""
        finish_tracker.reset() 