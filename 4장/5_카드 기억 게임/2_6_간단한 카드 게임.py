import sys
import pygame
import random
import math
import time

screenSize = {
    'width': 762,
    'height': 538
}

pygame.init()
screen = pygame.display.set_mode((screenSize['width'], screenSize['height']));
pygame.display.set_caption("MOMORIES GAME")

fullImage = pygame.image.load("cards.png");

rows = 4
cols = 8
cards = []
opend = {}

margin = 10
cardSize = {
    'width': 167,
    'height': 244
}

score = [0, 0]
turn = 0

def Init():
    for y in range(0, rows):
        row = []
        for x in range(0, cols):
            row.append({ 'x': math.ceil((x - 1) / 2), 'y': y, 'visible': False, 'enable': True})

        cards.append(row)

def openAllorNot(visible):
    for y in range(0, rows):
        for x in range(0, cols):
            cards[y][x]['visible'] = visible

def suffle(shake):
    for n in range(0, shake):
        ox = random.randint(0, cols - 1)
        oy = random.randint(0, rows - 1)

        tx = random.randint(0, cols - 1)
        ty = random.randint(0, rows - 1)

        temp = cards[oy][ox]
        cards[oy][ox] = cards[ty][tx]
        cards[ty][tx] = temp

def updateGame():
    screen.fill((255, 255, 255))

    for y in range(0, rows):
        for x in range(0, cols):
            card = cards[y][x]

            if card['enable'] == False:
                continue

            spriteImage = fullImage.subsurface(cardSize['width'] * 2, cardSize['height'] * 4, cardSize['width'], cardSize['height']);

            if card['visible'] == True:
                spriteImage = fullImage.subsurface(cardSize['width'] * card['x'], cardSize['height'] * card['y'], cardSize['width'], cardSize['height']);
                pygame.draw.rect(screen, (0, 0, 0),
                                 [cardSize['width'] / 2 * x + x * margin + margin,
                                  cardSize['height'] / 2 * y + y * margin + margin,
                                  cardSize['width'] / 2, cardSize['height'] / 2], 1)

            spriteImage = pygame.transform.scale(spriteImage, (cardSize['width'] / 2, cardSize['height'] / 2));
            screen.blit(spriteImage, [cardSize['width'] / 2 * x + x * margin + margin, cardSize['height'] / 2 * y + y * margin + margin])

    font = pygame.font.Font(None, 20)
    text = font.render(str(score[0]), False, (0, 0, 0))
    width = text.get_width()
    screen.blit(text, (margin, margin))

    text = font.render(str(score[1]), False, (0, 0, 0))
    width = text.get_width()
    screen.blit(text, (screenSize['width'] - margin - width, margin))

    pygame.display.update()

def open(pos):
    global trying
    global opend
    global turn

    x = math.ceil((pos[0] - margin) / (cardSize['width'] / 2 + margin)) - 1
    y = math.ceil((pos[1] - margin) / (cardSize['height'] / 2 + margin)) - 1

    card = cards[y][x]
    card['visible'] = True

    if trying % 2 <= 0:
        opend = cards[y][x]
        updateGame()
    else:
        updateGame()
        time.sleep(1)

        if opend['x'] == card['x'] and opend['y'] == card['y']:
            opend['enable'] = False
            card['enable'] = False

            score[turn % 2] = score[turn % 2] + 100
        else:
            opend['visible'] = False
            card['visible'] = False

        turn = turn + 1
        updateGame()

    trying = (trying + 1) % 2

Init()
openAllorNot(True)
suffle(99)
updateGame()
time.sleep(2)
openAllorNot(False)
updateGame()

trying = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            open(pygame.mouse.get_pos())
pygame.quit()