import pygame
from settings import *

class UI:
    # defining ui
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(10, 34, MANA_BAR_WIDTH, BAR_HEIGHT)

    # handling ui bar
    def show_bar(self, current, max_amount, background_rect, color):
        # drawing bar background
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, background_rect)

        # converting statistics to pixels
        ratio = current / max_amount
        current_width = background_rect.width * ratio
        current_rect = background_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, background_rect, 3)

    # showing actual score
    def show_score(self, score):
        text_surface = self.font.render(str(int(score)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

        # converting weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # converting magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic["graphic"]
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    # showing actual used weapon / magic
    def selection_box(self, left, top, has_switched):
        background_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, background_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, background_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, background_rect, 3)
        return background_rect

    # showing weapon icon
    def weapon_overlay(self, weapon_index, has_switched):
        background_rect = self.selection_box(10, 630, has_switched)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = background_rect.center)

        self.display_surface.blit(weapon_surface, weapon_rect)

    # showing magic icon
    def magic_overlay(self, magic_index, has_switched):
        background_rect = self.selection_box(80, 635, has_switched)
        magic_surface = self.magic_graphics[magic_index]
        magic_rect = magic_surface.get_rect(center = background_rect.center)

        self.display_surface.blit(magic_surface, magic_rect)

    # displaying UI
    def display(self, player):
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats["mana"], self.mana_bar_rect, MANA_COLOR)

        self.show_score(player.score)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
