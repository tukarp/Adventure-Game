import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    # defining player
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    # input
    def input(self):
        key = pygame.key.get_pressed()

        # moving up and down
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.direction.y = -1
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # moving left and right
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.direction.x = -1
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    # moving
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center


    # collisions
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    # update
    def update(self):
        self.input()
        self.move(self.speed)
