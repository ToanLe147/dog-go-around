"""Main menu UI for Pygame version."""

import pygame
from game import config


class Menu:
    """Main menu screen."""

    def __init__(self, screen):
        """Initialize menu."""
        self.screen = screen
        self.selected_option = 0
        self.options = ["Start Race", "Settings", "Quit"]

        # Fonts
        self.title_font = pygame.font.Font(None, 100)
        self.option_font = pygame.font.Font(None, 60)

    def handle_event(self, event):
        """Handle menu input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.options[self.selected_option] == "Start Race":
                    return "start"
                elif self.options[self.selected_option] == "Quit":
                    return "quit"
                elif self.options[self.selected_option] == "Settings":
                    return "settings"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(self.options):
                option_y = config.WINDOW_HEIGHT // 2 + i * 80
                option_rect = pygame.Rect(
                    config.WINDOW_WIDTH // 2 - 150, option_y - 30, 300, 60
                )
                if option_rect.collidepoint(mouse_pos):
                    if option == "Start Race":
                        return "start"
                    elif option == "Quit":
                        return "quit"
                    elif option == "Settings":
                        return "settings"

        return None

    def render(self):
        """Render the menu."""
        # Background
        self.screen.fill((20, 20, 40))

        # Title
        title = self.title_font.render("DOG GO AROUND", True, (255, 200, 0))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle = subtitle_font.render("Racing Game", True, config.COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(config.WINDOW_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)

        # Menu options
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(self.options):
            option_y = config.WINDOW_HEIGHT // 2 + i * 80
            option_rect = pygame.Rect(
                config.WINDOW_WIDTH // 2 - 150, option_y - 30, 300, 60
            )

            # Highlight/selection
            is_hovered = option_rect.collidepoint(mouse_pos)
            is_selected = i == self.selected_option

            bg_color = (60, 60, 100) if (is_hovered or is_selected) else (40, 40, 60)
            pygame.draw.rect(self.screen, bg_color, option_rect, border_radius=10)

            border_color = (
                (255, 200, 0) if (is_hovered or is_selected) else (100, 100, 120)
            )
            pygame.draw.rect(
                self.screen, border_color, option_rect, 3, border_radius=10
            )

            # Text
            color = (255, 255, 255) if (is_hovered or is_selected) else (180, 180, 180)
            text = self.option_font.render(option, True, color)
            text_rect = text.get_rect(center=option_rect.center)
            self.screen.blit(text, text_rect)

        # Controls hint
        hint_font = pygame.font.Font(None, 28)
        hint = hint_font.render(
            "Use Arrow Keys or Mouse to navigate", True, (150, 150, 150)
        )
        hint_rect = hint.get_rect(
            center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT - 50)
        )
        self.screen.blit(hint, hint_rect)
