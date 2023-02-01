import pygame
from support import import_folder
from entity import Entity
from settings import *


class Player(Entity):
    # defining player
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, destroy_magic):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        # player graphics setup
        self.import_player_assets()
        self.status = "down"

        # player movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # player weapons
        self.player_chosen_attack = "weapon"
        self.player_ui_box_select = False
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # player magic
        self.create_magic = create_magic
        self.destroy_magic = destroy_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # player stats
        self.stats = {"health": 100, "mana": 60, "attack": 10, "magic": 4, "speed": 8}
        self.stats = {"health": 300, "mana": 140, "attack": 20, "magic": 10, "speed": 10}
        self.upgrade_cost = {"health": 100, "mana": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]
        self.mana = self.stats["mana"]
        self.speed = self.stats["speed"]
        self.score = 0

        # player getting damaged
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # sound
        self.weapon_attack_sound = pygame.mixer.Sound("../audio/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)


    # import player assets
    def import_player_assets(self):
        player_path = "../graphics/player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
            "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []
        }
        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    # player input
    def input(self):
        if not self.attacking:
            # get input
            keys = pygame.key.get_pressed()

            # player moving up and down
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            # player moving left and right
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # switching between magic and weapon
            if keys[pygame.K_LCTRL]:
                if self.player_chosen_attack == "weapon":
                    self.magic_switch_time = pygame.time.get_ticks()
                    self.player_chosen_attack = "magic"
                    self.can_switch_magic = False
                else:
                    self.weapon_switch_time = pygame.time.get_ticks()
                    self.player_chosen_attack = "weapon"
                    self.can_switch_weapon = False

            # player attack input
            # attacking up
            if keys[pygame.K_UP] and self.player_chosen_attack == "weapon":
                self.direction.y = -1
                self.status = "up"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            # attacking down
            elif keys[pygame.K_DOWN] and self.player_chosen_attack == "weapon":
                self.direction.y = 1
                self.status = "down"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            # attacking to the left
            elif keys[pygame.K_LEFT] and self.player_chosen_attack == "weapon":
                self.direction.x = -1
                self.status = "left"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            # attacking to the right
            elif keys[pygame.K_RIGHT] and self.player_chosen_attack == "weapon":
                self.direction.x = 1
                self.status = "right"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # player magic input
            # magic up
            if keys[pygame.K_UP] and self.player_chosen_attack == "magic":
                self.direction.y = -1
                self.status = "up"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)
            # magic down
            elif keys[pygame.K_DOWN] and self.player_chosen_attack == "magic":
                self.direction.y = 1
                self.status = "down"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)
            # magic to the left
            elif keys[pygame.K_LEFT] and self.player_chosen_attack == "magic":
                self.direction.x = -1
                self.status = "left"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)
            # magic to the right
            elif keys[pygame.K_RIGHT] and self.player_chosen_attack == "magic":
                self.direction.x = 1
                self.status = "right"
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)

            # player switching weapons
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                # checking for index out of range error
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # player switching magic
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                # checking for index out of range error
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    # managing players statuses
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    # overwrite idle
                    self.status = self.status.replace("idle", "attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    # player cooldowns
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    # player animations
    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # getting damage
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # player full weapon damage
    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    # player full magic damage
    def full_magic_damage(self):
        base_damage = self.stats["magic"]
        magic_damage = magic_data[self.magic]["strength"]
        return base_damage + magic_damage

    # player recovering mana over time
    def mana_recovery(self):
        if self.mana < self.stats["mana"]:
            self.mana += 0.05 * self.stats["magic"]
        else:
            self.mana = self.stats["mana"]

    # player recovering health after killing enemy
    def health_recovery(self):
        if self.health + 25 < self.stats["health"]:
            self.health += 25
        else:
            self.health = self.stats["health"]

    # player death
    #def player_death(self):
        # if self.health <= 0:
            # pygame.display.

    # player update
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.mana_recovery()
