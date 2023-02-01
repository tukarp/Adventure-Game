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
        pygame.display.set_caption("Roguelike")
        self.clock = pygame.time.Clock()
        self.level = Level()

        # font
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # sound
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.15)
        main_sound.play(loops=-1)

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
    game.run()
