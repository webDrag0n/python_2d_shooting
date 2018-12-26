import pygame
from pygame.locals import *

# recieve a player target
def enemyControl(enemy):
    keys = pygame.key.get_pressed()
    if not enemy.isDead:
        if enemy.body.__GetLinearVelocity().y <= 0:
            if enemy.jet_energy < 100:
                enemy.jet_energy += 0.2
        
        # left
        if keys[K_LEFT] == 1:
            enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity().x - 15, enemy.body.__GetLinearVelocity().y))
            enemy.direction = 0
        # right
        if keys[K_RIGHT] == 1:
            enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity().x + 15, enemy.body.__GetLinearVelocity().y))
            enemy.direction = 1
        # up
        if keys[K_UP] == 1:
            if enemy.jet_energy > 0:
                enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity().x, enemy.body.__GetLinearVelocity().y + 50))
                enemy.jet_energy -= 1.2
        # down
        if keys[K_DOWN] == 1:
            if enemy.jet_energy > 0:
                enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity().x, enemy.body.__GetLinearVelocity().y - 25))
                enemy.jet_energy -= 0.3

        if keys[K_RSHIFT] == 1:
            enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity().x, enemy.body.__GetLinearVelocity().y + 100))

        if keys[K_SLASH] == 1:
            enemy.shoot()
        
        enemy.last_fire_time += 1