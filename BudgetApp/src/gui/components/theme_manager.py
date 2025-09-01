"""
Theme management for the application.
Handles dark/light mode switching and consistent styling.
"""

import customtkinter as ctk
from typing import Dict, Tuple


class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self):
        self._current_mode = "dark"  # Default to dark mode
        self._themes = self._load_themes()
        
    def _load_themes(self) -> Dict[str, Dict]:
        """Load theme configurations."""
        return {
            "light": {
                "appearance_mode": "light",
                "color_theme": "blue",
                "colors": {
                    "primary": "#1f538d",
                    "secondary": "#14375e",
                    "success": "#28a745",
                    "warning": "#ffc107",
                    "danger": "#dc3545",
                    "info": "#17a2b8",
                    "background": "#ffffff",
                    "surface": "#f8f9fa",
                    "text": "#212529",
                    "text_secondary": "#6c757d"
                }
            },
            "dark": {
                "appearance_mode": "dark",
                "color_theme": "blue",
                "colors": {
                    "primary": "#3b82f6",
                    "secondary": "#1e40af",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "danger": "#ef4444",
                    "info": "#06b6d4",
                    "background": "#1a1a1a",
                    "surface": "#2a2a2a",
                    "text": "#ffffff",
                    "text_secondary": "#9ca3af"
                }
            }
        }
    
    def apply_theme(self, mode: str = None):
        """Apply the specified theme mode."""
        if mode:
            self._current_mode = mode
        
        theme = self._themes[self._current_mode]
        
        # Set CustomTkinter appearance mode
        ctk.set_appearance_mode(theme["appearance_mode"])
        ctk.set_default_color_theme(theme["color_theme"])
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_mode = "light" if self._current_mode == "dark" else "dark"
        self.apply_theme(new_mode)
    
    def get_current_mode(self) -> str:
        """Get the current theme mode."""
        return self._current_mode
    
    def is_dark_mode(self) -> bool:
        """Check if currently in dark mode."""
        return self._current_mode == "dark"
    
    def get_color(self, color_name: str) -> str:
        """Get a color value from the current theme."""
        theme = self._themes[self._current_mode]
        return theme["colors"].get(color_name, "#000000")
    
    def get_colors(self) -> Dict[str, str]:
        """Get all colors from the current theme."""
        theme = self._themes[self._current_mode]
        return theme["colors"]
    
    def get_button_style(self, variant: str = "primary") -> Dict:
        """Get button styling for the current theme."""
        colors = self.get_colors()
        
        styles = {
            "primary": {
                "fg_color": colors["primary"],
                "hover_color": colors["secondary"],
                "text_color": "white",
                "corner_radius": 8
            },
            "secondary": {
                "fg_color": "transparent",
                "hover_color": colors["surface"],
                "text_color": colors["text"],
                "border_width": 1,
                "border_color": colors["text_secondary"],
                "corner_radius": 8
            },
            "success": {
                "fg_color": colors["success"],
                "hover_color": self._darken_color(colors["success"]),
                "text_color": "white",
                "corner_radius": 8
            },
            "warning": {
                "fg_color": colors["warning"],
                "hover_color": self._darken_color(colors["warning"]),
                "text_color": "black",
                "corner_radius": 8
            },
            "danger": {
                "fg_color": colors["danger"],
                "hover_color": self._darken_color(colors["danger"]),
                "text_color": "white",
                "corner_radius": 8
            }
        }
        
        return styles.get(variant, styles["primary"])
    
    def get_card_style(self) -> Dict:
        """Get card/frame styling for the current theme."""
        colors = self.get_colors()
        return {
            "fg_color": colors["surface"],
            "corner_radius": 12,
            "border_width": 1,
            "border_color": colors["text_secondary"] if self.is_dark_mode() else "#e9ecef"
        }
    
    def get_input_style(self) -> Dict:
        """Get input field styling for the current theme."""
        colors = self.get_colors()
        return {
            "fg_color": colors["background"],
            "border_color": colors["text_secondary"],
            "text_color": colors["text"],
            "corner_radius": 6
        }
    
    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Darken a hex color by the specified factor."""
        # Simple color darkening - could be enhanced
        if color.startswith('#'):
            color = color[1:]
        
        try:
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(int(c * factor) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        except (ValueError, IndexError):
            return color  # Return original if parsing fails
    
    @staticmethod
    def get_status_colors() -> Dict[str, str]:
        """Get status colors that work in both themes."""
        return {
            "success": "#10b981",
            "warning": "#f59e0b", 
            "error": "#ef4444",
            "info": "#06b6d4"
        }


# Global theme manager instance
theme_manager = ThemeManager()