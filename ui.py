import pygame
import numpy as np
import state as State

class UI:
    def __init__(self, screen, font, width, height, state):
        self.state_obj = state
        self.state = state.get_state()
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

        # UI Panel Dimensions
        self.ui_width = 200
        self.ui_height = height
        self.game_width = width - self.ui_width

        # Predefined text surfaces
        self.start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        self.end_text = font.render("GAME OVER! Press SPACE to Restart", True, (255, 255, 255))

        # Score and Round
        self.score = 1000
        self.round = 1

    def update(self):
        self.state_update()
        
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Game Area (Left Panel)
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.game_width, self.height))

        # UI Panel (Right Panel)
        pygame.draw.rect(self.screen, (100, 100, 100), (self.game_width, 0, self.ui_width, self.ui_height))
        
        # Render based on state
        if self.state == "START":
            self.screen.blit(self.start_text, (self.width // 2 - 150, self.height // 2))

        elif self.state == "CHECK":
            self.draw_ui_panel()

        elif self.state == "GAMEOVER":
            self.screen.blit(self.end_text, (self.width // 2 - 250, self.height // 2))

    def state_update(self):
        self.state = self.state_obj.get_state()

    def draw_ui_panel(self):
        # Display score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.game_width + 20, 20))

        # Display round
        round_text = self.font.render(f"Round: {self.round}", True, (255, 255, 255))
        self.screen.blit(round_text, (self.game_width + 20, 60))

        # Display scoring multipliers
        multiplier_text = self.font.render("Multipliers:", True, (255, 255, 255))
        self.screen.blit(multiplier_text, (self.game_width + 20, 120))

        shapes = ["Square", "Rectangle", "Circle", "Triangle", "Star"]
        multipliers = [1, 2, 3, 5, 10]

        for i, (shape, multiplier) in enumerate(zip(shapes, multipliers)):
            shape_text = self.font.render(f"{shape}: x{multiplier}", True, (255, 255, 255))
            self.screen.blit(shape_text, (self.game_width + 20, 160 + i * 40))

    def increment_score(self, points):
        self.score += points

    def next_round(self):
        self.round += 1

    def reset_game(self):
        self.score = 1000
        self.round = 1
