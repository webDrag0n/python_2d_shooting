import pygame
from pygame.locals import *

# recieve a player target
def coreControl(core):
    keys = pygame.key.get_pressed()
    if not core.isDead:
        if core.body.linearVelocity.y <= 0:
            if core.jet_energy < 100:
                core.jet_energy += 0.2
        
        # left
        if keys[K_a] == 1:
            core.body.linearVelocity = (core.body.linearVelocity.x - 10, core.body.linearVelocity.y)
            core.direction = 0
        # right
        if keys[K_d] == 1:
            core.body.linearVelocity = (core.body.linearVelocity.x + 10, core.body.linearVelocity.y)
            core.direction = 1
        # up
        if keys[K_w] == 1:
            if core.jet_energy > 0:
                core.body.linearVelocity = (core.body.linearVelocity.x, core.body.linearVelocity.y + 50)
                core.jet_energy -= 1.2
        # down
        if keys[K_s] == 1:
            if core.jet_energy > 0:
                core.body.linearVelocity = (core.body.linearVelocity.x, core.body.linearVelocity.y - 25)
                core.jet_energy -= 0.3

        if keys[K_LSHIFT] == 1:
            core.body.linearVelocity = (core.body.linearVelocity.x, core.body.linearVelocity.y + 100)

        if keys[K_f] == 1:
            core.shoot()
        
        core.last_fire_time += 1