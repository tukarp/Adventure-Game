import pygame
import sys
from level import Level
from settings import *


class Game:
    # defining game class
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Adventure Game")
        self.clock = pygame.time.Clock()
        self.level = Level()

        # font
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # sound
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.02)
        main_sound.play(loops=-1)

    # draw text
    def draw_text(self, text, font, color, surface, x, y):
        text = self.font.render(text, 1, color)
        text_rect = text.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text, text_rect)

    # main menu
    def menu(self):
        self.screen.fill("black")
        self.draw_text("Made by Tomasz Wnuk", self.font, MENU_TEXT_COLOR, self.screen, 900, 650)
        self.draw_text("...and some online tutorials", self.font, MENU_TEXT_COLOR, self.screen, 830, 670)
        self.draw_text("WSAD to move", self.font, MENU_TEXT_COLOR, self.screen, 20, 20)
        self.draw_text("ARROWS to attack", self.font, MENU_TEXT_COLOR, self.screen, 20, 40)
        self.draw_text("Q / E to switch weapons", self.font, MENU_TEXT_COLOR, self.screen, 20, 60)
        self.draw_text("CTRL to switch weapons / magic", self.font, MENU_TEXT_COLOR, self.screen, 20, 80)
        pygame.display.update()
        pygame.time.wait(8000)

    # running the game
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


# game loop
if __name__ == '__main__':
    game = Game()
    game.menu()
    game.run()
