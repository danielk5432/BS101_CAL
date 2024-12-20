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

        self.money_text = ""


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

        elif self.state == "GAMEOVER":
            self.screen.blit(self.end_text, (self.width // 2 - 250, self.height // 2))

        elif self.state == "MONEY":
            text = self.font.render(self.money_text, True, (255, 255, 255))
            self.screen.blit(text, (self.width // 2 - 250, self.height // 2))
        else:
            self.draw_ui_panel()

    def print_draw_area(self, draw, shape):
        area = draw.area()
        intersect_area = draw.intersect_area(shape)
        if self.state_obj.state != "CHECK":
            draw.intersection.draw(self.screen, (255,0,0), fill=True) # for test
        text = self.font.render(f'Area: %d'%area, True, (255, 255, 255))
        self.screen.blit(text, (20 , 5))
        text = self.font.render(f'Intersect Area: %d'%intersect_area, True, (255, 255, 255))
        self.screen.blit(text, (20 , 50))
        percent = intersect_area / area * 100
        text = self.font.render(f'Intersect Percent: %.2f %%'%percent, True, (255, 255, 255))
        self.screen.blit(text, (20 ,95))

    def state_update(self):
        self.state = self.state_obj.get_state()

    def draw_ui_panel(self):
        text_space = 20
        # Display score
        score_text = self.font.render(f"Score: {self.state_obj.money}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.game_width + text_space, 20))

        # Display round
        round_text = self.font.render(f"Round: {self.state_obj.round}", True, (255, 255, 255))
        self.screen.blit(round_text, (self.game_width + text_space, 60))

        state_text = self.font.render("State", True, (255, 255, 255))
        self.screen.blit(state_text, (self.game_width + text_space, 100))

        state_text = self.font.render(self.state, True, (255, 255, 255))
        self.screen.blit(state_text, (self.game_width + text_space, 140))

        if self.state == "CHECK":
            check_left_text = self.font.render("Check Left", True, (255, 255, 255))
            self.screen.blit(check_left_text, (self.game_width + text_space, 180))

            check_left_text = self.font.render(str(self.state_obj.check_left()), True, (255, 255, 255))
            self.screen.blit(check_left_text, (self.game_width + text_space, 220))

        """
        # Display scoring multipliers
        multiplier_text = self.font.render("Multipliers:", True, (255, 255, 255))
        self.screen.blit(multiplier_text, (self.game_width + 20, 120))

        
    
        shapes = ["Square", "Rectangle", "Circle", "Triangle", "Star"]
        multipliers = [1, 2, 3, 5, 10]

        for i, (shape, multiplier) in enumerate(zip(shapes, multipliers)):
            shape_text = self.font.render(f"{shape}: x{multiplier}", True, (255, 255, 255))
            self.screen.blit(shape_text, (self.game_width + 20, 160 + i * 40))
"""

    def increment_score(self, points):
        self.score += points

    def next_round(self):
        self.round += 1

    def reset_game(self):
        self.score = 1000
        self.round = 1
