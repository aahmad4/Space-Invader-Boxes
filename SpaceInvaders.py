# Ali Ahmad
# Space Invader Boxes

# Importing needed libraries

import pygame
from pygame.locals import *
import sys
from random import shuffle


# Creating variables for each color I need in an RGB Format
#          (Red, Green, Blue)
Gray      = (100, 100, 100)
NavyBlue  = ( 60,  60, 100)
White     = (255, 255, 255)
Red       = (255,   0,   0)
Green     = (  0, 255,   0)
Blue      = (  0,   0, 255)
Yellow    = (255, 255,   0)
NearBlack = ( 19,  15,  48)
ComBlue   = (233, 232, 255)


# Creating constants for the player object

PlayerWidth = 40
PlayerHeight = 10
PlayerColor = ComBlue
Player1 = 'Player 1'
PlayerSpeed = 5
PlayerColor = Green

# Creating constants for the GUI

GameTitle = 'Space Invaders!'
DisplayWidth = 640
DisplayHeight = 480
bgColor = NearBlack
xMargin = 50
yMargin = 50

# Creating constants for the bullet

BulletWidth = 5
BulletHeight = 5
BulletOffSet = 700

# Creating constants for the enemies

enemyWidth = 25
enemyHeight = 25
enemyName = 'Enemy'
enemyGap = 20
arrayWidth = 10
arrayHeight = 4
MoveTime = 1000
movex = 10
movey = enemyHeight
timeOffset = 300

# Defining what each key does location wise in the GUI

DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}




# Creating the player object

class Player(pygame.sprite.Sprite):

    # Initializing player

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PlayerWidth
        self.height = PlayerHeight
        self.image = pygame.Surface((self.width, self.height))
        self.color = PlayerColor
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = Player1
        self.speed = PlayerSpeed
        self.vectorx = 0

    # Defining player movements based on keys hit

    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
                
        self.checkForSide()
        self.image.fill(self.color)

    # Making sure player does not go past the display on either end

    def checkForSide(self):
        if self.rect.right > DisplayWidth:
            self.rect.right = DisplayWidth
            self.vectorx = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vectorx = 0


# Creating the box object 

class Blocker(pygame.sprite.Sprite):

    # Initializing object

    def __init__(self, side, color, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = side
        self.height = side
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = 'blocker'
        self.row = row
        self.column = column


# Creating the bullet object

class Bullet(pygame.sprite.Sprite):

    # Initializing object

    def __init__(self, rect, color, vectory, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = BulletWidth
        self.height = BulletHeight
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = rect.bottom
        self.name = 'bullet'
        self.vectory = vectory
        self.speed = speed
    
    # Defining a kill

    def update(self, *args):
        self.oldLocation = (self.rect.x, self.rect.y)
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0:
            self.kill()

        elif self.rect.bottom > 500:
            self.kill()

        
# Creating the enemy object

class Enemy(pygame.sprite.Sprite):
    
    # Initializing object

    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = enemyWidth
        self.height = enemyHeight
        self.row = row
        self.column = column
        self.image = self.setImage()
        self.rect = self.image.get_rect()
        self.name = 'enemy'
        self.vectorx = 1
        self.moveNumber = 0
        self.MoveTime = MoveTime
        self.timeOffset = row * timeOffset
        self.timer = pygame.time.get_ticks() - self.timeOffset


    # Defining where each enemy goes

    def update(self, keys, currentTime):
        if currentTime - self.timer > self.MoveTime:
            if self.moveNumber < 6:
                self.rect.x += movex * self.vectorx
                self.moveNumber += 1
            elif self.moveNumber >= 6:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += movey
                if self.MoveTime > 100:
                    self.MoveTime -= 50
            self.timer = currentTime

    # Setting each alien image

    def setImage(self):
        if self.row == 0:
            image = pygame.image.load('scaryalien.png')
        elif self.row == 1:
            image = pygame.image.load('scarieralien.png')
        elif self.row == 2:
            image = pygame.image.load('scariestalien.png')
        else:
            image = pygame.image.load('scaryalien.png')
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image



class Text(object):
    def __init__(self, font, size, message, color, rect, surface):
        self.font = pygame.font.Font(font, size)
        self.message = message
        self.surface = self.font.render(self.message, True, color)
        self.rect = self.surface.get_rect()
        self.setRect(rect)

    def setRect(self, rect):
        self.rect.centerx, self.rect.centery = rect.centerx, rect.centery - 5


    def draw(self, surface):
        surface.blit(self.surface, self.rect)


# This is where the main code runs

class App(object):
    
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.gameStart = True
        self.gameOver = False
        self.beginGame = False
        self.laserSound = pygame.mixer.Sound('laser.ogg')
        self.startLaser = pygame.mixer.Sound('alienLaser.ogg')
        self.playIntroSound = True


    # Create login screen

    def resetGame(self):
        self.gameStart = True
        self.needToMakeEnemies = True
        
        self.introMessage1 = Text('orena.ttf', 25,
                                 'Welcome to Space Invaders!',
                                 Green, self.displayRect,
                                 self.displaySurf)
        self.introMessage2 = Text('orena.ttf', 20,
                                  'Press Any Key to Continue',
                                  Green, self.displayRect,
                                  self.displaySurf)
        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5

        self.gameOverMessage = Text('orena.ttf', 25,
                                    'GAME OVER', Green,
                                    self.displayRect, self.displaySurf)
        
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.GreenBullets = pygame.sprite.Group()
        self.blockerGroup1 = self.makeBlockers(0)
        self.blockerGroup2 = self.makeBlockers(1)
        self.blockerGroup3 = self.makeBlockers(2)
        self.blockerGroup4 = self.makeBlockers(3)
        self.allBlockers = pygame.sprite.Group(self.blockerGroup1, self.blockerGroup2,
                                               self.blockerGroup3, self.blockerGroup4)
        self.allSprites = pygame.sprite.Group(self.player, self.allBlockers)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.enemyMoves = 0
        self.enemyBulletTimer = pygame.time.get_ticks()
        self.gameOver = False
        self.gameOverTime = pygame.time.get_ticks()
        if self.playIntroSound:
            self.startLaser.play()
            self.playIntroSound = False
        


    def makeBlockers(self, number=1):
        blockerGroup = pygame.sprite.Group()
        
        for row in range(5):
            for column in range(7):
                blocker = Blocker(10, Green, row, column)
                blocker.rect.x = 50 + (150 * number) + (column * blocker.width)
                blocker.rect.y = 375 + (row * blocker.height)
                blockerGroup.add(blocker)

        for blocker in blockerGroup:
            if (blocker.column == 0 and blocker.row == 0
                or blocker.column == 6 and blocker.row == 0):
                blocker.kill()

        return blockerGroup



    def checkForEnemyBullets(self):
        RedBulletsGroup = pygame.sprite.Group()

        for bullet in self.bullets:
            if bullet.color == Red:
                RedBulletsGroup.add(bullet)

        for bullet in RedBulletsGroup:
            if pygame.sprite.collide_rect(bullet, self.player):
                if self.player.color == Green:
                    self.player.color = Yellow
                elif self.player.color == Yellow:
                    self.player.color = Red
                elif self.player.color == Red:
                    self.gameOver = True
                    self.gameOverTime = pygame.time.get_ticks()
                bullet.kill()



    def shootEnemyBullet(self, rect):
        if (pygame.time.get_ticks() - self.enemyBulletTimer) > BulletOffSet:
            self.bullets.add(Bullet(rect, Red, 1, 5))
            self.allSprites.add(self.bullets)
            self.enemyBulletTimer = pygame.time.get_ticks()



    def findEnemyShooter(self):
        columnList = []
        for enemy in self.enemies:
            columnList.append(enemy.column)

        columnSet = set(columnList)
        columnList = list(columnSet)
        shuffle(columnList)
        column = columnList[0]
        enemyList = []
        rowList = []

        for enemy in self.enemies:
            if enemy.column == column:
                rowList.append(enemy.row)

        row = max(rowList)

        for enemy in self.enemies:
            if enemy.column == column and enemy.row == row:
                self.shooter = enemy 

        
        
        
        
    

    def makeScreen(self):
        pygame.display.set_caption(GameTitle)
        displaySurf = pygame.display.set_mode((DisplayWidth, DisplayHeight))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(bgColor)
        displaySurf.convert()

        return displaySurf, displayRect



    def makePlayer(self):
        player = Player()
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player



    def makeEnemies(self):
        enemies = pygame.sprite.Group()
        
        for row in range(arrayHeight):
            for column in range(arrayWidth):
                enemy = Enemy(row, column)
                enemy.rect.x = xMargin + (column * (enemyWidth + enemyGap))
                enemy.rect.y = yMargin + (row * (enemyHeight + enemyGap))
                enemies.add(enemy)

        return enemies



    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.GreenBullets) < 1:
                    bullet = Bullet(self.player.rect, Green, -1, 20)
                    self.GreenBullets.add(bullet)
                    self.bullets.add(self.GreenBullets)
                    self.allSprites.add(self.bullets)
                    self.laserSound.play()
                elif event.key == K_ESCAPE:
                    self.terminate()


    def gameStartInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameOver = False
                self.gameStart = False
                self.beginGame = True


    def gameOverInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameStart = True
                self.beginGame = False
                self.gameOver = False
    

        


    def checkCollisions(self):
        self.checkForEnemyBullets()
        pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        pygame.sprite.groupcollide(self.enemies, self.allBlockers, False, True)
        self.collide_Green_blockers()
        self.collide_Red_blockers()
        

        
    def collide_Green_blockers(self):
        for bullet in self.GreenBullets:
            casting = Bullet(self.player.rect, Green, -1, 20)
            casting.rect = bullet.rect.copy()
            for pixel in range(bullet.speed):
                hit = pygame.sprite.spritecollideany(casting,self.allBlockers)
                if hit:
                    hit.kill()
                    bullet.kill()
                    break
                casting.rect.y -= 1


    def collide_Red_blockers(self):
        Reds = (shot for shot in self.bullets if shot.color == Red)
        Red_bullets = pygame.sprite.Group(Reds)
        pygame.sprite.groupcollide(Red_bullets, self.allBlockers, True, True)

    



    def checkGameOver(self):
        if len(self.enemies) == 0:
            self.gameOver = True
            self.gameStart = False
            self.beginGame = False
            self.gameOverTime = pygame.time.get_ticks()

        else:
            for enemy in self.enemies:
                if enemy.rect.bottom > DisplayHeight:
                    self.gameOver = True
                    self.gameStart = False
                    self.beginGame = False
                    self.gameOverTime = pygame.time.get_ticks()
       
        
                

    def terminate(self):
        pygame.quit()
        sys.exit()


    def mainLoop(self):
        while True:
            if self.gameStart:
                self.resetGame()
                self.gameOver = False
                self.displaySurf.fill(bgColor)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.gameStartInput()
                pygame.display.update()

            elif self.gameOver:
                self.playIntroSound = True
                self.displaySurf.fill(bgColor)
                self.gameOverMessage.draw(self.displaySurf)
                #prevent users from exiting the GAME OVER screen
                #too quickly
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                pygame.display.update()
                
            elif self.beginGame:
                if self.needToMakeEnemies:
                    
                    self.enemies = self.makeEnemies()
                    self.allSprites.add(self.enemies)
                    self.needToMakeEnemies = False
                    pygame.event.clear()
                    
                    
                        
                else:    
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(bgColor)
                    self.checkInput()
                    self.allSprites.update(self.keys, currentTime)
                    if len(self.enemies) > 0:
                        self.findEnemyShooter()
                        self.shootEnemyBullet(self.shooter.rect)
                    self.checkCollisions()
                    self.allSprites.draw(self.displaySurf)
                    self.blockerGroup1.draw(self.displaySurf)
                    pygame.display.update()
                    self.checkGameOver()
                    self.clock.tick(self.fps)
                    
            
            
    


if __name__ == '__main__':
    app = App()
    app.mainLoop()
