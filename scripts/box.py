# -*- coding: UTF-8 -*-
from Box2D import *
import pygame, sys, math, random
from pygame.locals import *
from picToMap import *

from enemyBehavior import enemyControl
from coreBehavior import coreControl

block_size = 10
gravity = 0

# set up pygame-box2d constants
bullet_size = int(block_size / 2)
player_size_x = int(block_size * 0.75)
player_size_y = int(block_size * 1.5)
player_density = 0.1

pygame_screen_x = 1400
pygame_screen_y = 400

camera_scale = 1

camera_1_x = pygame_screen_x - pygame_screen_x - 5
camera_1_y = pygame_screen_y - pygame_screen_y - 5

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y), FULLSCREEN)
pygame.display.set_caption("csproject 01 beta 1.0")
mode = "menu"

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (100, 200, 0) 
BLUE = (0, 0, 255)

# setup current stage (menu, game ..)
mode = "menu"

# set up menu assets
menu_time_delay = 0
menu_items = [u"Play 开始",u"Quit 退出"]
menu_focus = 0

def menuDisplay():
    # clean screen
    windowSurface.fill(BLUE)
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    y = 100
    # render text
    for text in menu_items:
        myfont = pygame.font.SysFont("SimHei", 30)
        if text == menu_items[menu_focus]:
            myfont = pygame.font.SysFont("SimHei", 40)
        label = myfont.render(text, 1, (255,255,0))
        windowSurface.blit(label, (100, y))
        y = y + 50
    pygame.display.flip()

def menuControl():
    global menu_focus
    global menu_time_delay
    global mode
    if menu_time_delay >= 20:
        keys = pygame.key.get_pressed()
        if keys[K_UP] == 1:
            menu_focus -= 1
            if menu_focus < 0:
                menu_focus = len(menu_items) - 1
            menu_time_delay = 0
        if keys[K_DOWN] == 1:
            menu_focus += 1
            if menu_focus >= len(menu_items):
                menu_focus = 0
            menu_time_delay = 0
        # if selected
        if keys[K_RETURN] == 1:
            if menu_focus == 0:
                mode = "game"
                core.__init__(100, 200, 100, 10, 100, 1)
                enemy.__init__(1200, 200, 100, 10, 100, 0)
            if menu_focus == 1:
                pygame.quit()
                sys.exit(0)
        if keys[K_TAB] == 1:
            mode = "game"
    if menu_time_delay >= 10000:
        menu_time_delay = 20
    menu_time_delay += 1
# menu setup end


# game set up start
# setup game assets

# produce map
mapArray = generateMap("..\\assets\\map\\map2.bmp")

# setup terrain list
terrainList = []
# set up  box2d world
world = b2World()
world.__SetGravity((0, -gravity))

# create player class
class player:
    # initialize method
    def __init__(self, x = 0, y = 0, life_value = 100, power_value = 0, jet_energy_value = 100, direction_value = 1):
        # life set to 100
        self.life = life_value
        self.direction = direction_value
        # jet pack energy set to 100
        self.jet_energy = jet_energy_value
        # power set to 10
        self.power = power_value
        # record the last fire time to for bullet time delay effect
        self.last_fire_time = 0
        # the body of the player
        self.body = create_player_body(x, y)
        # determine if the player should be rendered or not
        self.isDead = False
        # determine if the player should be drawn red
        self.isHurt = False
        try:
            for i in self.bullet_list:
                world.DestroyBody(i)
            self.bullet_list = []
        except:
            # list used to store bullets
            self.bullet_list = []

    def shoot(self):
        # fire ammo
        if self.last_fire_time > 10:
            if self.direction == 1:
                self.bullet = create_bullet(self.body.position[0] + block_size + 1, self.body.position[1])
                if self.bullet == None:
                    return
                self.bullet.linearVelocity.x = 1000 + self.body.linearVelocity.x
            elif self.direction == 0:
                self.bullet = create_bullet(self.body.position[0] - block_size - 1, self.body.position[1])
                if self.bullet == None:
                    return
                self.bullet.linearVelocity.x = -1000 + self.body.linearVelocity.x
            # print(self.bullet.linearVelocity.x)
            self.bullet.userData = "bullet"
            if len(self.bullet_list) <= 100:
                self.bullet_list.append(self.bullet)
            else:
                world.DestroyBody(self.bullet_list[0])
                self.bullet_list = self.bullet_list[1:]
                self.bullet_list.append(self.bullet)
            self.last_fire_time = 0

    # hited by enemy
    def hit(self, hitPower=0):
        self.life -= hitPower
        self.isHurt = True
        if self.life <= 0:
            self.dead()

    def dead(self):
        self.isDead = True
        world.DestroyBody(self.body)
# game assets setup end

# function used to create bullets
def create_bullet(box_x_pos, box_y_pos):
    try:
        body = world.CreateDynamicBody(position=(box_x_pos, box_y_pos))
        box = body.CreatePolygonFixture(box=(bullet_size / 2.0, bullet_size / 2.0), density=0.001, friction=1)
        body.linearDamping = 0
    except:
        return None
    return body

# function used to instantiate enemy
def create_player_body(box_x_pos, box_y_pos):
    body = world.CreateDynamicBody(position=(box_x_pos, box_y_pos))
    body.fixedRotation = True
    body.__SetUserData(data="player")
    tex = body.CreatePolygonFixture(box=(player_size_x / 2.0, player_size_y / 2.0), density=100, friction=0.9)
    tex.fixedRotation = True
    return body

# game terrain setup
def generateBlockFromMap(map):
    for i in range(0, len(mapArray)):
        for j in range(0, len(mapArray[i])):
            if mapArray[i][j] != 255:
                block = world.CreateStaticBody(
                    position=(j * block_size, i * block_size),
                    shapes=b2PolygonShape(box=(block_size / 2, block_size / 2)),
                )
                block.__SetUserData(data="block")
                terrainList.append(block)

generateBlockFromMap(mapArray)
# game terrain setup end

# create main player core
core = player(100, 200, 100, 10, 100, 1)
# create enemy
enemy = player(400, 200, 100, 10, 100, 0)
# game setup end


# load image
# load bullet texture
bulletImage = pygame.image.load("..\\assets\\texture\\redbox.png").convert()
bulletTex = pygame.transform.scale(bulletImage, (bullet_size, bullet_size))

# load player texture
playerImage = pygame.image.load("..\\assets\\texture\\player.png").convert()
playerHurtImage = pygame.image.load("..\\assets\\texture\\playerHurt.png").convert()
playerTex = pygame.transform.scale(playerImage, (player_size_x, player_size_y))

# load dirt texture
dirtImage = pygame.image.load("..\\assets\\texture\\dirt.png").convert()
dirtTex = pygame.transform.scale(dirtImage, (int(block_size), int(block_size)))

# load grass texture
grassImage = pygame.image.load("..\\assets\\texture\\grass.png").convert()
grassTex = pygame.transform.scale(grassImage, (int(block_size), int(block_size)))

# load rock texture
rockImage = pygame.image.load("..\\assets\\texture\\rock.png").convert()
rockTex = pygame.transform.scale(rockImage, (int(block_size), int(block_size)))

# load brick texture
brickImage = pygame.image.load("..\\assets\\texture\\brick.png").convert()
brickTex = pygame.transform.scale(brickImage, (int(block_size), int(block_size)))

def gameControl():
    global mode
    keys = pygame.key.get_pressed()

    # exit to menu
    if keys[K_ESCAPE] == 1:
        mode = "menu"


def gamePhysics():
    # get the objects that are colliding
    contactList = world.__GetContactList_internal()
    # if there is objects colliding
    if contactList != None:
        # colliding object a and b
        bodyA = contactList.__GetFixtureA().__GetBody()
        bodyB = contactList.__GetFixtureB().__GetBody()
        # case that obj a is bullet
        if bodyA.__GetUserData() == "bullet":
            # destroy bullet
            world.DestroyBody(bodyA)
            # remove bullet from the bullet list in player
            try:
                core.bullet_list.remove(bodyA)
            except:
                enemy.bullet_list.remove(bodyA)
            # if another object is a player
            if bodyB == core.body:
                core.hit(enemy.power)
            elif bodyB == enemy.body:
                enemy.hit(core.power)
        # case that obj b is bullet
        elif bodyB.__GetUserData() == "bullet":
            # destroy bullet
            world.DestroyBody(bodyB)
            # remove bullet from the bullet list in player
            try:
                core.bullet_list.remove(bodyB)
            except:
                enemy.bullet_list.remove(bodyB)
            # if another object is a player
            if bodyA == core.body:
                core.hit(enemy.power)
            elif bodyA == enemy.body:
                enemy.hit(core.power)

    # get the camera coordinates as global variable
    global camera_1_y
    global camera_1_x
    
    # add gravity velocity
    if not core.isDead:
        core.body.__SetLinearVelocity((core.body.__GetLinearVelocity()[0], core.body.__GetLinearVelocity()[1] - 10))
    if not enemy.isDead:
        enemy.body.__SetLinearVelocity((enemy.body.__GetLinearVelocity()[0], enemy.body.__GetLinearVelocity()[1] - 10))

    # tick the time to perform physics effect        
    world.Step(timeStep, vel_iters, pos_iters)

def renderBullet(body, tex, size):
    texBox = pygame.transform.scale(bulletImage, (int(size), int(size)))
    rotatedTex = pygame.transform.rotozoom(texBox, math.degrees(body.angle), 1)
    rotatedTex.set_colorkey(0)
    windowSurface.blit(rotatedTex, (((body.position.x - camera_1_x)) - ((size / 2.0)), (pygame_screen_y - (body.position.y) - ((size / 2.0) - camera_1_y))))

def renderPlayer(player):
    # rotate and draw player core
    if player.isDead:
        return

    # rotate and draw bullet
    for bullet in player.bullet_list:
        renderBullet(bullet, bulletTex, bullet_size)

    # if hited by bullet, turns red
    if player.isHurt:
        playerTex = pygame.transform.scale(playerHurtImage, (player_size_x, player_size_y))
        player.isHurt = False
    else:
        playerTex = pygame.transform.scale(playerImage, (player_size_x, player_size_y))

    # find the direction of player
    if player.direction == 0:
        renderTex = pygame.transform.flip(playerTex, True, False)
    else:
        renderTex = pygame.transform.flip(playerTex, False, False)
    # render player to the screen
    windowSurface.blit(renderTex, (((player.body.position.x - camera_1_x)) - ((player_size_x / 2.0)), (pygame_screen_y - (player.body.position.y) - ((player_size_y / 2.0) - camera_1_y))))
    
    # draw player's life bar
    pygame.draw.rect(windowSurface, RED, (player.body.position.x - camera_1_x - 10, 460 - bPos2pPos(player.body.position.x, player.body.position.y)[1] + camera_1_y - 10, player.life / 5, 2))
    # draw player's jet bar
    pygame.draw.rect(windowSurface, WHITE, (player.body.position.x - camera_1_x - 10, 460 - bPos2pPos(player.body.position.x, player.body.position.y)[1] + camera_1_y - 13, player.jet_energy / 5, 2))


def bPos2pPos(bPos_x, bPos_y):
    return [bPos_x, bPos_y + 70]
def pPos2bPos(pPos_x, pPos_y):
    return [pPos_x, pPos_y - 70]

def renderUI():
    # draw ui
    # draw jet bar
    if core.isDead:
        # draw gameover if core died
        gameOverFont = pygame.font.SysFont("consolas", 150)
        gameOverLabel = gameOverFont.render("PLAYER 2 WINS", int(pygame_screen_x / 2), (255,0,0))
        windowSurface.blit(gameOverLabel, (100, 150))
    if enemy.isDead:
        # draw gameover if core died
        gameOverFont = pygame.font.SysFont("consolas", 150)
        gameOverLabel = gameOverFont.render("PLAYER 1 WINS", int(pygame_screen_x / 2), (255,0,0))
        windowSurface.blit(gameOverLabel, (100, 150))
 
def gameDisplay(playerImage):
    global gunTex_01

    # clean screen
    windowSurface.fill(BLUE)

    # draw ground
    for i in range(0, len(mapArray)):
        for j in range(0, len(mapArray[i])):
            # render grass
            if mapArray[i][j] == 0:
                windowSurface.blit(grassTex, (bPos2pPos(j * block_size, i * block_size)[0] - 5 - camera_1_x, 465 - bPos2pPos(j * block_size, i * block_size)[1] + camera_1_y))
            # render rock
            if mapArray[i][j] == 128:
                windowSurface.blit(rockTex, (bPos2pPos(j * block_size, i * block_size)[0] - 5 - camera_1_x, 465 - bPos2pPos(j * block_size, i * block_size)[1] + camera_1_y))
            # render dirt
            if mapArray[i][j] == 192:
                windowSurface.blit(dirtTex, (bPos2pPos(j * block_size, i * block_size)[0] - 5 - camera_1_x, 465 - bPos2pPos(j * block_size, i * block_size)[1] + camera_1_y))
            # render brick
            if mapArray[i][j] == 64:
                windowSurface.blit(brickTex, (bPos2pPos(j * block_size, i * block_size)[0] - 5 - camera_1_x, 465 - bPos2pPos(j * block_size, i * block_size)[1] + camera_1_y))

    if not core.isDead:
        renderPlayer(core)
    if not enemy.isDead:
        renderPlayer(enemy)

    # draw ui on top
    renderUI()
    # refresh screen
    pygame.display.flip()

def pyg():
    time_passed = clock.tick(100)
    if mode == "game":
        gameControl()
        coreControl(core)
        enemyControl(enemy)
        gameDisplay(playerImage)
    elif mode == "menu":
        menuControl()
        menuDisplay()

# Prepare for simulation. Typically we use a time step of 1/100 of a
# second (100Hz) and 6 velocity/2 position iterations. This provides a
# high quality simulation in most game scenarios.
timeStep = 1.0 / 100
vel_iters, pos_iters = 6, 2

# This is our little animation loop.
clock = pygame.time.Clock()
ev = pygame.event.poll()
while ev.type != pygame.QUIT:
    
    ev = pygame.event.poll()
    pyg()
    if mode == "game":
        gamePhysics()
pygame.quit()