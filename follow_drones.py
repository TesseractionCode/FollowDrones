import pygame
import math
from pygame import Vector2
from random import randint

from time import time


'''A circle that can move'''
class Entity:

    entities = []

    def __init__(self, pos: Vector2, color, radius):
        self.pos = pos
        self.vel = Vector2(0, 0)
        self.accel = Vector2(0, 0)
        self.color = color
        self.radius = radius

        Entity.entities.append(self)

    @staticmethod
    def updateAll(dT):
        for entity in Entity.entities:
            entity.update(dT)

    @staticmethod
    def renderAll(screen):
        for entity in Entity.entities:
            entity.render(screen)

    def update(self, dT):
        self.vel += self.accel * dT
        self.pos += self.vel * dT

    def render(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.pos.x, self.pos.y), self.radius)


class Drone(Entity):

    def __init__(self, pos: Vector2, max_speed, rest_dist, attractor: Entity):
        super().__init__(pos, color=(255, 0, 0), radius=10)
        self.max_speed = max_speed
        self.rest_dist = rest_dist
        self.attractor = attractor

    def update(self, dT):
        '''Calculate the new acceleration of the drone based off of its distance from the attractor.'''
        follow_direction = Vector2.normalize(self.attractor.pos - self.pos)
        follow_dist = self.pos.distance_to(self.attractor.pos)
        self.accel = follow_direction * \
            math.sqrt(abs(follow_dist - self.rest_dist)) * self.max_speed * \
            (abs(follow_dist - self.rest_dist)/(follow_dist - self.rest_dist))
        return super().update(dT)


'''Setup the screen'''
resolution = (800, 600)
screen = pygame.display.set_mode(resolution)

# Create an entity for the player
player = Entity(Vector2(resolution[0]/2, resolution[1]/2), (255, 255, 255), 16)

# Generate some drones at random positions with the player as their attractor
for _ in range(20):
    ex = randint(0, resolution[0])
    ey = randint(0, resolution[1])
    Drone(Vector2(ex, ey), max_speed=4, rest_dist=60, attractor=player)

moveSpeed = 100  # Move speed for the player

dT = 0
running = True
'''Game loop'''
while running:
    start_time = time()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Messily get the controls for the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.vel.y = -moveSpeed
            if event.key == pygame.K_a:
                player.vel.x = -moveSpeed
            if event.key == pygame.K_s:
                player.vel.y = moveSpeed
            if event.key == pygame.K_d:
                player.vel.x = moveSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.vel.y = 0
            if event.key == pygame.K_a:
                player.vel.x = 0
            if event.key == pygame.K_s:
                player.vel.y = 0
            if event.key == pygame.K_d:
                player.vel.x = 0

    # Update
    Entity.updateAll(dT)
    # Render
    Entity.renderAll(screen)
    # Display
    pygame.display.update()
    screen.fill((0, 0, 0))

    dT = time() - start_time
