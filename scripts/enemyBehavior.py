import pygame
from pygame.locals import *

# recieve a player target
def enemyControl(enemy):
    keys = pygame.key.get_pressed()
    if not enemy.isDead:
        if enemy.body.linearVelocity.y <= 0:
            if enemy.jet_energy < 100:
                enemy.jet_energy += 0.2
        
        # left
        if keys[K_LEFT] == 1:
            enemy.body.linearVelocity = (enemy.body.linearVelocity.x - 15, enemy.body.linearVelocity.y)
            enemy.direction = 0
        # right
        if keys[K_RIGHT] == 1:
            enemy.body.linearVelocity = (enemy.body.linearVelocity.x + 15, enemy.body.linearVelocity.y)
            enemy.direction = 1
        # up
        if keys[K_UP] == 1:
            if enemy.jet_energy > 0:
                enemy.body.linearVelocity = (enemy.body.linearVelocity.x, enemy.body.linearVelocity.y + 50)
                enemy.jet_energy -= 1.2
        # down
        if keys[K_DOWN] == 1:
            if enemy.jet_energy > 0:
                enemy.body.linearVelocity = (enemy.body.linearVelocity.x, enemy.body.linearVelocity.y - 25)
                enemy.jet_energy -= 0.3

        if keys[K_RSHIFT] == 1:
            enemy.body.linearVelocity = (enemy.body.linearVelocity.x, enemy.body.linearVelocity.y + 100)

        if keys[K_SLASH] == 1:
            enemy.shoot()
        
        enemy.last_fire_time += 1