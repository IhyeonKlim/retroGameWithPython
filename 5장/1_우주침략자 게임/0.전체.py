import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP

class unit:
    def __init__(self, x, y, color):
        self.rect = Rect(0, 0, 22, 12)
        self.rect.centerx = x
        self.rect.centery = y
        self.character = []
        self.enable = True
        self.frame_index = 0
        self.color = color

    def draw(self):
        if self.frame_index >= len(self.character):
            self.frame_index = 0

        for y, line in enumerate(self.character[self.frame_index]):
            ry = self.rect.y + y
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + x
                pygame.draw.circle(screen, self.color, [rx, ry], 1)

        return True

    def move_left(self):
        self.rect.centerx -= 2
        self.frame_index = (self.frame_index + 1) % 2

        return True

    def move_right(self):
        self.rect.centerx += 2
        self.frame_index = (self.frame_index + 1) % 2

        return True

class enemy(unit):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                           [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                           [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]],
                          [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]]]
        self.delay = 10

    def move_down(self):
        self.rect.centery += 6

        return True

class ufo(enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]]
        self.delay = 5

class player(unit):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]]

class wall:
    def __init__(self, x, y, color):
        self.rect = Rect(0, 0, 45, 20)
        self.rect.centerx = x
        self.rect.centery = y
        self.body = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 0, 0, 0, 0, 0, 1, 1]]
        self.color = color

    def colliderect(self, bullet):
        for y, line in enumerate(self.body):
            ry = self.rect.y + (y * 5)
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + (x * 5)
                if Rect(rx, ry, 5, 5).colliderect(bullet.rect):
                    self.body[y][x] = 0
                    return True

        return False

    def draw(self):
        for y, line in enumerate(self.body):
            ry = self.rect.y + (y * 5)
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + (x * 5)
                pygame.draw.rect(screen, self.color, [rx, ry, 5, 5])

        return True

class bullet:
    def __init__(self):
        self.rect = Rect(0, 0, 3, 7)
        self.enable = False
        self.color = white

    def fire(self, x, y):
        if self.enable is True:
            return False

        self.rect.centerx = x
        self.rect.y = y - self.rect.height
        self.enable = True

        return True

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        return True

    def moveup(self):
        self.rect.centery -= 1

        if self.rect.centery < 0:
            self.enable = False
            return False

        return True

    def movedown(self):
        self.rect.centery += 1

        if self.rect.centery > screen.get_height():
            self.enable = False
            return False

        return True

def game_over():
    if life <= 0:
        return True

    for row in enemies:
        for enemy in row:
            if enemy.rect.centery > screen.get_height() - 70:
                return True

    return False

def update_game():
    global bullet, time, is_move_right_enemy, enemy_bullets, fired_enemy_bullets, score, life

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                if bullet.enable is True:
                    break
                if player.enable is False:
                    break

                bullet.fire(player.rect.centerx, player.rect.y)
            elif event.key == pygame.K_RIGHT:
                if player.enable is False:
                    break
                if player.rect.x + player.rect.width >= screen.get_width():
                    break

                player.move_right()
            elif event.key == pygame.K_LEFT:
                if player.enable is False:
                    break
                if player.rect.x <= 0:
                    break

                player.move_left()

    screen.fill(black)

    if bullet.enable is True:
        bullet.moveup()
        bullet.draw()

    if player.enable is True:
        player.draw()

    is_change_direction = False
    for row in enemies:
        for enemy in row:
            if (is_move_right_enemy > 0 and enemy.rect.x + enemy.rect.width >= screen.get_width()) or \
                    (is_move_right_enemy <= 0 and enemy.rect.x <= 0):
                is_move_right_enemy = (is_move_right_enemy + 1) % 2
                is_change_direction = True
                break
        if is_change_direction is True:
            break

    for row in enemies:
        for enemy in row:
            if is_change_direction is True:
                enemy.delay -= 1 if enemy.delay > 4 else 0
                enemy.move_down()

    for wall in walls:
        if bullet.enable is True:
            if wall.colliderect(bullet) is True:
                bullet.enable = False

        wall.draw()

    for y, row in enumerate(enemies):
        for x, enemy in enumerate(row):
            if enemy.enable is True:
                if enemy.rect.colliderect(bullet.rect) and bullet.enable is True:
                    enemy.enable = False
                    bullet.enable = False
                    score += 100
                    break

                if time % enemy.delay == 0:
                    if is_move_right_enemy > 0:
                        enemy.move_right()
                    else:
                        enemy.move_left()

                enemy.draw()

                if random.randint(0, 9999) < int(time / 1000) and len(enemy_bullets) > 0:
                    enemy_bullet = enemy_bullets.pop(0)
                    enemy_bullet.color = enemy.color
                    fired_enemy_bullets.append(enemy_bullet)
                    fired_enemy_bullets[len(fired_enemy_bullets) - 1].fire(enemy.rect.centerx, enemy.rect.y + enemy.rect.height)

    for i, emeny_bullet in enumerate(fired_enemy_bullets):
        if emeny_bullet.movedown() is False:
            enemy_bullets.append(fired_enemy_bullets.pop(i))

        if emeny_bullet.enable is True:
            for wall in walls:
                if wall.colliderect(emeny_bullet) is True:
                    emeny_bullet.enable = False
                    enemy_bullets.append(fired_enemy_bullets.pop(i))
                    continue

            if player.rect.colliderect(emeny_bullet.rect):
                emeny_bullet.enable = False
                enemy_bullets.append(fired_enemy_bullets.pop(i))
                life -= 1
                continue

            emeny_bullet.draw()


    if random.randint(0, 99) < 1 and ufo.enable is False:
        ufo.enable = True
        ufo.rect.x = 0

    if ufo.enable is True:
        if ufo.rect.x + ufo.rect.width < screen.get_width():
            if time % ufo.delay == 0:
                ufo.move_right()
            ufo.draw()
        else:
            ufo.enable = False

        if ufo.rect.colliderect(bullet.rect):
            score += 1000
            ufo.enable = False


    font = pygame.font.Font(None, 20)
    text = font.render(str(score), False, white)
    screen.blit(text, (10, 10))

    for l in range(0, life):
        pygame.draw.circle(screen, red, [screen.get_width() - (l * 10) - 15, 20], 5)

    if game_over() is True:
        player.enable = False

        font = pygame.font.Font(None, 40)
        text = font.render('GAME OVER', False, red)
        width = text.get_width()
        height = text.get_height()
        screen.blit(text, ((screen.get_width() / 2) - (width / 2), (screen.get_height() / 2) - (height / 2)))

    pygame.display.update()
    time += 1

    return True

screen_size = {
    'width': 640,
    'height': 480
}

white = (255, 255, 255)
yellow = (255, 228, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']));
pygame.key.set_repeat(5, 5)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

enemies = []
marginx = (screen.get_width() - (40 * 11)) / 2
for y in range(0, 5):
    row = []
    color = green if y <= 0 else blue if y < 3 else yellow
    for x in range(0, 11):
        row.append(enemy(marginx + x * 40, 100 + y * 25, color))
    enemies.append(row)
is_move_right_enemy = 1
enemy_bullets = []
fired_enemy_bullets = []
for i in range(0, 5):
    enemy_bullets.append(bullet())

player = player(screen.get_width() / 2, screen.get_height() - 30, white)
bullet = bullet()
bullet.color = player.color

ufo = ufo(0, 50, white)
ufo.enable = False

walls = []
for i in range(0, 4):
    walls.append(wall(155 + i * 110, screen.get_height() - 70, red))

life = 3
score = 0
time = 0
fps = 300
while True:
    update_game()
    clock.tick(fps)