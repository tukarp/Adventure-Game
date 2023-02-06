import pygame
from particles import AnimationPlayer
from random import choice, randint
from magic import MagicPlayer
from player import Player
from weapon import Weapon
from enemy import Enemy
from settings import *
from support import *
from tile import Tile
from ui import UI


class Level:
    # defining the level
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    # create the map
    def create_map(self):
        layout = {
            "boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("../map/map_Grass.csv"),
            "object": import_csv_layout("../map/map_Objects.csv"),
            "entities": import_csv_layout("../map/map_Entities.csv")
        }
        graphics = {
            "grass": import_folder("../graphics/grass"),
            "objects": import_folder("../graphics/objects")
        }
        # generating map
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], "grass", random_grass_image)
                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", surf)
                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                        (x, y),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic,
                                        self.destroy_magic)
                            else:
                                if col == "390": monster_name = "01"
                                elif col == "391": monster_name = "2"
                                elif col == "392": monster_name = "seg_fault"
                                else: monster_name = "python_error"
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_score)

    # create the attack
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    # destroy the attack
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # create the magic
    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == "flame":
            self.magic_player.flame(self.player, strength, cost, [self.visible_sprites, self.attack_sprites])

    # destroy the magic
    def destroy_magic(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # damage enemies and grass
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    # damage player
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    # create particles after entity death
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    # adding score
    def add_score(self, amount):
        self.player.score += amount

    # running the level
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

# camera
class YSortCameraGroup(pygame.sprite.Group):
    # defining camera
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 100)

        # creating the floor
        self.floor_surf = pygame.image.load("../graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    # draw things on the screen
    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    # updating enemy actions
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
