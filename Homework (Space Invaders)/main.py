
import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900,500))

WIDTH = 900
HEIGHT = 500

greenTankHit = pygame.USEREVENT + 1
grayTankHit = pygame.USEREVENT + 2

GREEN = (0,255,0)
GRAY = (128,128,128)
BLACK = (0,0,0)
WHITE = (255,255,255)

BULLET_FIRE = pygame.mixer.Sound("Gun+Silencer.mp3")
BULLET_HIT = pygame.mixer.Sound("Grenade+1.mp3")
BULLET_VELOCITY = 5
VEL = 5
MAX_B = 3

TANK_W = 55
TANK_H = 40

HEALTH_F = pygame.font.SysFont("arial", 60)
WINNER_F = pygame.font.SysFont("calibri", 30)

FPS = 60

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg,(WIDTH, HEIGHT))

greenTank = pygame.image.load("tank1.png")
greenTank = pygame.transform.scale(greenTank,(TANK_W, TANK_H))

grayTank = pygame.image.load("tank2.png")
grayTank = pygame.transform.scale(grayTank, (TANK_W, TANK_H))

def draw(green, greenB, greenHealth, gray, grayB, grayHealth):
    screen.blit(bg, (0,0))
    pygame.draw.rect(screen, WHITE, BORDER)
    screen.blit(greenTank, (green.x, green.y))
    screen.blit(grayTank, (gray.x, gray.y))
    greenHealthT = HEALTH_F.render(f"health: {greenHealth}", 1, WHITE)
    grayHealthT = HEALTH_F.render(f"health: {grayHealth}", 1, WHITE)
    screen.blit(greenHealthT, (WIDTH - greenHealthT.get_width() - 10, 10))
    screen.blit(grayHealthT, (10, 10))
    for bullet in greenB:
        pygame.draw.rect(screen, GREEN, bullet)
    for bullet in grayB:
        pygame.draw.rect(screen, GRAY, bullet)

    pygame.display.update()

def grayMove(keysPressed, gray):
    if keysPressed[pygame.K_a] and gray.x - VEL > 0:
        gray.x -= VEL
    if keysPressed[pygame.K_d] and gray.x + VEL + gray.width < BORDER.x:
        gray.x += VEL
    if keysPressed[pygame.K_w] and gray.y - VEL > 0:
        gray.y -= VEL
    if keysPressed[pygame.K_s] and gray.y + VEL + gray.height < HEIGHT - 20:
        gray.y += VEL
    
    pygame.display.update()

def greenMove(keysPressed, green):
    if keysPressed[pygame.K_UP] and green.y - VEL > 0:
        green.y -= VEL
    if keysPressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT - 20:
        green.y += VEL
    if keysPressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width:
        green.x -= VEL
    if keysPressed[pygame.K_RIGHT] and green.x + VEL + green.width < WIDTH:
        green.x += VEL

    pygame.display.update()

def displayWinner(winnerT):
    winnerT = WINNER_F.render(winnerT, 1, WHITE)
    screen.blit(winnerT, (WIDTH//2 - winnerT.get_width()//2, HEIGHT//2 - winnerT.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def handleB(greenB, grayB, green, gray):
    for bullet in greenB:
        bullet.x -= BULLET_VELOCITY
        if gray.colliderect(bullet):
            pygame.event.post(pygame.event.Event(grayTankHit))
            greenB.remove(bullet)
        elif bullet.x > WIDTH:
            greenB.remove(bullet)
    for bullet in grayB:
        bullet.x += BULLET_VELOCITY
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(greenTankHit))
            grayB.remove(bullet)
        elif bullet.x < 0:
            grayB.remove(bullet)

def main():
    gray = pygame.Rect(100,300, TANK_W, TANK_H)
    green =  pygame.Rect(700,300, TANK_W, TANK_H)
    
    grayH = 100
    greenH = 100   
    
    grayB = []
    greenB = []

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(grayB) < MAX_B:
                    bullet = pygame.Rect(gray.x + gray.width//2, gray.y + gray.height//2, 10, 5)
                    grayB.append(bullet)
                    BULLET_FIRE.play()
                if event.key == pygame.K_RCTRL and len(greenB) < MAX_B:
                    bullet = pygame.Rect(green.x + green.width//2, green.y + green.height//2, 10, 5)
                    greenB.append(bullet)
                    BULLET_FIRE.play()
            if event.type == greenTankHit:
                greenH -= 10
                BULLET_HIT.play()
            if event.type == grayTankHit:
                grayH -= 10
                BULLET_HIT.play()
        draw(green, greenB, greenH, gray, grayB, grayH)
        winnerT = ""
        if greenH <= 0:
            winnerT = "Gray has won the Game!"
        if grayH <= 0:
            winnerT = "Green has won the Game!"
        if winnerT != "":
            displayWinner(winnerT)
        keysPressed = pygame.key.get_pressed()
        greenMove(keysPressed, green)
        grayMove(keysPressed, gray)
        handleB(greenB, grayB, green, gray)

main()