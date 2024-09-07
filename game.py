import pygame
from pygame.constants import K_SPACE, SWSURFACE
import random
import sys

pygame.init()
pygame.mixer.init()

exitGame = False
gameOver = False
fps = 60
clock = pygame.time.Clock()

screenWidth = 640
screenHeight = 480
gameWindow = pygame.display.set_mode((screenWidth, screenHeight))

# Loading all images
spaceShip = pygame.image.load('ship.png').convert_alpha()
bullet = pygame.image.load('bullet.png').convert_alpha()
enemyShip = pygame.image.load('enemy.png').convert_alpha()
background = pygame.image.load('bg.jpg').convert_alpha()
# welcomeText = pygame.image.load('start.png').convert_alpha()

# Transforming images
spaceShip = pygame.transform.scale(spaceShip, (100, 100))
bullet = pygame.transform.scale(bullet, (32, 32))
enemyShip = pygame.transform.scale(enemyShip, (100, 87))
enemyShip = pygame.transform.rotate(enemyShip, 180)

# Initialize high score
high_score = 0

# Function to fire a bullet
def fire():
    global fired
    global bulletY
    global bulletX
    fired = True
    if bulletY > 0:
        bulletY -= 20
    else:
        bulletY = spaceshipY
        bulletX = spaceshipX + (spaceShip.get_width() / 2) - (bullet.get_width() / 2)
        fired = False

# Function to respawn enemy
def reSpawn():
    global enemyX
    global enemyY
    enemyY = 0 - enemyShip.get_height()
    enemyX = random.randint(0, screenWidth - enemyShip.get_width())

# Function to check collision
def isCollide(x1, y1, x2, y2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance < 50

# Function to display text on the screen
def text_screen(text, color, x, y, size):
    font = pygame.font.SysFont('consolas', size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to display centered text
def textScreencent(text, color, size):
    font = pygame.font.SysFont('consolas', size)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(screenWidth / 2, screenHeight / 2))
    gameWindow.blit(text, text_rect)

# Welcome screen function
def welcomeScreen():
    global exitGame
    gameWindow.fill((0, 0, 0))
    textScreencent("Spaceship Shooter! Press SPACE to Play", (255, 255, 255), 20)
    # textScreencent("Spaceship Shooter! Press SPACE to Play", (255, 255, 255), 40)
    pygame.display.update()
    while not exitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mainGame()

# Main game function
def mainGame():
    global bulletX, bulletY, spaceshipX, spaceshipY, exitGame, fired, enemyX, enemyY, gameOver, high_score
    # X and Y position of sprites
    spaceshipX = screenWidth / 2 - spaceShip.get_width() / 2
    spaceshipY = screenHeight - spaceShip.get_height() - 20
    bulletX = spaceshipX + spaceShip.get_width() / 2 - bullet.get_width() / 2
    bulletY = spaceshipY
    enemyX = random.randint(0, screenWidth - enemyShip.get_width())
    enemyY = 0 - enemyShip.get_height()
    bulletSound = pygame.mixer.Sound('bullet.wav')
    enemyVel = 2
    fired = False
    score = 0
    gameOver = False

    '''---------- Main Game Loop -----------'''
    while not exitGame:
        gameWindow.blit(background, (0, 0))
        gameWindow.blit(bullet, (bulletX, bulletY))
        gameWindow.blit(spaceShip, (spaceshipX, spaceshipY))
        gameWindow.blit(enemyShip, (enemyX, enemyY))
        text_screen(f'Score: {score}', (255, 255, 255), 10, 10, 30)
        text_screen(f'High Score: {high_score}', (255, 255, 255), 10, 50, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True

        keys = pygame.key.get_pressed()
        if not spaceshipX == 0:
            if keys[pygame.K_LEFT]:
                spaceshipX -= 5
                if not fired:
                    bulletX -= 5
        if not spaceshipX == screenWidth - spaceShip.get_width():
            if keys[pygame.K_RIGHT]:
                spaceshipX += 5
                if not fired:
                    bulletX += 5
        if keys[pygame.K_SPACE]:
            fire()
            if fired:
                bulletSound.play()

        if fired:
            fire()

        enemyY += enemyVel

        if enemyY > screenHeight - enemyShip.get_height():
            reSpawn()

        if isCollide(bulletX, bulletY, enemyX, enemyY):
            bulletY = spaceshipY
            bulletX = spaceshipX + (spaceShip.get_width() / 2) - (bullet.get_width() / 2)
            reSpawn()
            score += 1
            fired = False

        if isCollide(spaceshipX, spaceshipY, enemyX, enemyY):
            gameOver = True

        if gameOver:
            textScreencent("Game Over! Press R to Restart", (255, 0, 0), 30)
            pygame.display.update()
            # Update high score
            if score > high_score:
                high_score = score
            restart()

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Restart the game on key press
def restart():
    global gameOver, exitGame
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
                gameOver = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                gameOver = False
                mainGame()

# Run the game
if __name__ == "__main__":
    welcomeScreen()
    mainGame()
