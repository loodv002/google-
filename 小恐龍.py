import pygame
from random import randint
from time import sleep
pygame.init()

win = pygame.display.set_mode((1024,256))
pygame.display.set_caption('google 小恐龍')

dinoAppearence = [pygame.image.load('dino1.png'), pygame.image.load('dino2.png')]
oacAppearence = [pygame.image.load('oac1.png'), pygame.image.load('oac2.png')]
gndAppearence = pygame.image.load('gnd.png')

font1 = pygame.font.Font('freesansbold.ttf', 32)

clock=pygame.time.Clock()

class dino(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.appearenceNum = 0
        self.jumpCount = -9
        self.way = -1
        self.isJump = False
        self.score = 0

    def draw(self):
        self.appearenceNum += 1
        if self.appearenceNum >= len(dinoAppearence):
            self.appearenceNum = 0
            
        win.blit(dinoAppearence[self.appearenceNum], (self.x, self.y))

    
    def drawScore(self):
        self.score += 1
        scoreFont = font1.render('SCORE:' + '0' * (4 - len(str(self.score))) + str(self.score), True, (0, 0, 0), (255, 255, 255))

        win.blit(scoreFont, (800, 20))

class oac(object):
    def __init__(self, x, y, width, height, appearenceNum):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.vel = 10
        self.appearenceNum = appearenceNum

    def draw(self):
        self.x -= self.vel

        win.blit(oacAppearence[self.appearenceNum], (self.x, self.y))

gnd1_x=0; gnd2_x=1198; gnd_vel=10
def drawBackgound():
    global gnd1_x, gnd2_x, gnd_vel
    win.blit(gndAppearence, (gnd1_x, 244))
    win.blit(gndAppearence, (gnd2_x, 244))
    for i in range(gnd_vel):
        gnd1_x -= 1
        gnd2_x -= 1
        if gnd1_x <= -1198:
            gnd1_x = 1198

        if gnd2_x <= -1198:
            gnd2_x = 1198

def redrawWindow():
    win.fill((255, 255, 255))
    drawBackgound()
    dino1.draw()
    dino1.drawScore()
    for oacs in oacList:
        oacs.draw()
    pygame.display.update()
        
dino1=dino(50, 207, 40, 43)
run = True
oacColdDownCount = 0
oacList = []

while run:
    clock.tick(30)

    if oacColdDownCount != 0:
        oacColdDownCount += 1

    if oacColdDownCount > 50:
        oacColdDownCount = 0
    
    if (not (randint(0, 10))) and oacColdDownCount == 0 and len(oacList) <= 4:
        if randint(0,1):
            oacList.append(oac(1025, 203, 23, 46, 0))
        else:
            oacList.append(oac(1025, 203, 49, 46, 1))

        oacColdDownCount += 1

    for oacs in oacList:
        if oacs.x < 0 - oacs.width:
            oacList.pop(oacList.index(oacs))

        if dino1.y + dino1.height >= oacs.y and (oacs.x <= dino1.x + dino1.width <= oacs.x + oacs.width or oacs.x <= dino1.x <= oacs.x + oacs.width):
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        dino1.isJump =True
    if (dino1.isJump):
        dino1.jumpCount += 1

        if dino1.jumpCount > 0:
            dino1.way = 1
        else:
            dino1.way = -1

        dino1.y += dino1.jumpCount ** 2 * 0.5 * dino1.way

        if dino1.jumpCount == 8:
            dino1.isJump = False
            dino1.jumpCount = -9

    redrawWindow()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

sleep(3)
pygame.quit()
