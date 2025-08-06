import sys
import math
import random
import pygame
import configparser
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP

class Bullet:
    def __init__(self, cx, cy, degree, is_mine):
        self.rect = Rect(0, 0, 3, 3)

        self.is_mine = is_mine
        if self.is_mine:
            self.color = (255, 255, 255)
        else:
            self.color = (250, 237, 125)

        self.degree = degree
        self.theta = float(degree) * math.pi / 180
        self.step = 0
        self.cx = cx
        self.cy = cy

    def get_center_x(self):
        return self.rect.centerx

    def get_center_y(self):
        return self.rect.centery

    def move(self):
        self.rect.centerx = self.cx + self.step * math.cos(self.theta)
        self.rect.centery = self.cy + self.step * math.sin(self.theta)

        self.step += 4

    def draw(self):
        if self.is_mine:
            pygame.draw.line(screen, self.color, [self.rect.x - 10, self.rect.y - 10], [self.rect.x - 10, self.rect.y + 10], self.rect.width)
            pygame.draw.line(screen, self.color, [self.rect.x + 10, self.rect.y - 10], [self.rect.x + 10, self.rect.y + 10], self.rect.width)
        else:
            pygame.draw.circle(screen, self.color, [self.rect.x, self.rect.y], 4)
            pygame.draw.circle(screen, (255, 255, 255), [self.rect.x, self.rect.y], 4, 1)

class Unit:
    def __init__(self, file=None):
        self.image = None
        self.width = 50
        self.height = 50

        if file is not None:
            ini.read(file)
            config = ini['CONFIG']
            self.hp = int(config['HP'])
            self.sp = int(config['SP'])
            self.width = int(config['WIDTH'])
            self.height = int(config['HEIGHT'])
            self.no = int(config['NO'])
            self.is_boss = config['ISBOSS'] == 'True'
            self.image = pygame.image.load('./images/' + config['IMAGEFILE'])

        self.rect = Rect(0, 0, self.width, self.height)
        self.is_explosion = False
        self.exp_index = 0

    def get_center_x(self):
        return self.rect.centerx

    def get_center_y(self):
        return self.rect.centery

    def set_center_x(self, x):
        self.rect.centerx = x

    def set_center_y(self, y):
        self.rect.centery = y

    def explosion(self):
        self.image = pygame.image.load('./images/explosion.png')
        self.is_explosion = True
        self.exp_index = 0

    def draw(self):
        if not self.is_explosion:
            sprite = self.image.subsurface(self.no * self.width, 0, self.width, self.height)
        else:
            if int(self.exp_index / 1) * self.width >= self.image.get_width():
                return False

            sprite = self.image.subsurface(int(self.exp_index / 1) * self.width, 0, self.width, self.height)
            #sprite = pygame.transform.scale(sprite, (self.width, self.height))
            self.exp_index += 1

        screen.blit(sprite, self.rect)
        return True

class Player(Unit):
    def __init__(self, file):
        super().__init__(file)
        self.degree = -90

        x = screen.get_width() / 2
        y = screen.get_height() - 100
        self.set_center_x(x)
        self.set_center_y(y)

    def move_left(self):
        if self.get_center_x() <= 25:
            return
        self.set_center_x(self.get_center_x() - 3)

    def move_right(self):
        if self.get_center_x() >= screen.get_width() - 25:
            return
        self.set_center_x(self.get_center_x() + 3)

    def move_forward(self):
        if self.get_center_y() <= 25:
            return
        self.set_center_y(self.get_center_y() - 3)

    def move_backward(self):
        if self.get_center_y() >= screen.get_height() - 25:
            return
        self.set_center_y(self.get_center_y() + 3)

    def fire(self):
        cx = self.get_center_x()
        cy = self.get_center_y() - (self.height / 2)
        degree = self.degree

        bullet = Bullet(cx, cy, degree, True)

        return bullet

class Enemy(Unit):
    def __init__(self, file):
        super().__init__(file)
        self.degree_bullets = []

        ini.read(file)
        attack = ini['ATTACK']
        limit = int(attack['BulletCount'])
        for i in range(limit):
            degree = int(attack['Bullet' + str(i)])
            self.degree_bullets.append(degree)

        self.actions = []

        action = ini['ACTION']
        index = 0
        prev = ''
        while True:
            act = action[str(index)]
            if 'Repeat' in act:
                limit = int(act.split(',', 1)[1])
                for _ in range(limit):
                    self.actions.append(prev)
            else:
                self.actions.append(act)

            if act in {'Exit', 'Continue'}:
                break
            index += 1
            prev = act

        self.index = 0

    def move_left(self):
        self.set_center_x(self.get_center_x() - 3)

    def move_right(self):
        self.set_center_x(self.get_center_x() + 3)

    def move_forward(self):
        self.set_center_y(self.get_center_y() + 3)

    def move_backward(self):
        self.set_center_y(self.get_center_y() - 3)

    def fire(self):
        cx = self.get_center_x()
        cy = self.get_center_y() + (self.height / 2)
        bullets = []

        for degree in self.degree_bullets:
            bullet = Bullet(cx, cy, degree, False)
            bullets.append(bullet)

        return bullets

class ScenarioManager:
    def __init__(self, file, callback):
        self.scenarios = []
        self.file = file
        self.callback = callback
        self.index = 0

    def tick(self):
        ini.read(self.file)
        scenario = ini['SCENARIO']
        try:
            event = scenario[str(self.index)]

            org = event.split(',', 2)
            x = int(org[1])
            y = int(org[2])
            enemy = org[0]
            self.callback(enemy, x, y)
        except:
            pass

        self.index += 1

class Star:
    def __init__(self, level):
        self.size = level
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.step = level
        self.color = (50 + (level * 10), 50 + (level * 10), 50 + (level * 10))

    def move(self):
        self.rect.y += self.step

        if self.rect.y > screen.get_height():
            self.rect.y = 0

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

def key_input():
    global is_press_right, is_press_left, is_press_up, is_press_down, bomb_index

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_RIGHT:
                is_press_right = False
            elif event.key == pygame.K_LEFT:
                is_press_left = False
            elif event.key == pygame.K_UP:
                is_press_up = False
            elif event.key == pygame.K_DOWN:
                is_press_down = False
            elif event.key == pygame.K_SPACE:
                bullets.append(player.fire())
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                if player.sp >= 100 and player.hp > 0:
                    player.sp = 0
                    for i in range(30):
                        bomb = {
                            'bomb': Unit(),
                            'index': i * 3
                        }
                        bomb['bomb'].set_center_x(random.randint(100, screen.get_width() - 100))
                        bomb['bomb'].set_center_y(random.randint(100, screen.get_height() - 100))
                        bombs.append(bomb)

                    bullets.clear()

                    bomb_index = 0
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT:
                is_press_right = True
            elif event.key == pygame.K_LEFT:
                is_press_left = True
            elif event.key == pygame.K_UP:
                is_press_up = True
            elif event.key == pygame.K_DOWN:
                is_press_down = True

    if player.is_explosion:
        is_press_left = False
        is_press_up = False
        is_press_right = False
        is_press_down = False
        return

    if is_press_right:
        player.move_right()
    if is_press_left:
        player.move_left()
    if is_press_up:
        player.move_forward()
    if is_press_down:
        player.move_backward()

def bomb():
    global bomb_index

    if bomb_index < 0:
        return

    for bomb in bombs:
        if bomb['index'] == bomb_index:
            bomb['bomb'].explosion()
        if bomb['bomb'].is_explosion:
            if not bomb['bomb'].draw():
                bombs.remove(bomb)

    for enemy in enemies:
        enemy.hp = max(enemy.hp - 10, 0)
        enemy.explosion()

    bomb_index += 1

    if len(bombs) <= 0:
        bomb_index = -1

def update_game():
    screen.fill((0, 0, 0))

    for star in stars:
        star.move()
        star.draw()

    for bullet in bullets:
        bullet.move()
        bullet.draw()

        if (bullet.get_center_y() <= -3 or bullet.get_center_y() >= screen.get_height() + 3) or \
                (bullet.get_center_x() <= -3 or bullet.get_center_x() >= screen.get_width() + 3):
            bullets.remove(bullet)

        if bullet.is_mine:
            rect = Rect(bullet.rect.x - 10, bullet.rect.y - 10, 20, 20)
            for enemy in enemies:
                if not enemy.is_explosion and rect.colliderect(enemy.rect):
                    enemy.hp = max(enemy.hp - 10, 0)

                    try:
                        bullets.remove(bullet)
                    except:
                        pass

                    if enemy.hp <= 0:
                        enemy.explosion()
                        snd_bomb.play()

                    player.sp = min(player.sp + 10, 100)
                    break
        else:
            if not player.is_explosion and bullet.rect.colliderect(player.rect):
                player.hp = max(player.hp - 10, 0)
                bullets.remove(bullet)
                if player.hp <= 0:
                    player.explosion()
                    snd_bomb.play()

    key_input()
    if not player.draw():
        pygame.quit()
        sys.exit()

    if len(enemies) <= 0:
        pygame.display.update()
        return

    bomb()

    for enemy in enemies:
        if len(enemy.actions) == enemy.index:
            enemies.remove(enemy)
            continue

        if enemy.rect.colliderect(player.rect):
            player_hp = player.hp
            player.hp = max(player.hp - enemy.hp, 0)
            enemy.hp = max(enemy.hp - player_hp, 0)

            if enemy.hp <= 0:
                enemy.explosion()
                snd_bomb.play()
            if not player.is_explosion and player.hp <= 0:
                player.explosion()
                snd_bomb.play()

        act = enemy.actions[enemy.index]

        if not enemy.is_explosion and act == 'Continue':
            enemy.index = 0
            continue
        elif not enemy.is_explosion and act == 'MoveRight':
            enemy.move_right()
        elif not enemy.is_explosion and act == 'MoveLeft':
            enemy.move_left()
        elif not enemy.is_explosion and act == 'MoveForward':
            enemy.move_forward()
        elif not enemy.is_explosion and act == 'MoveBackward':
            enemy.move_backward()
        elif not enemy.is_explosion and act == 'Fire':
            if len(bombs) <= 0:
                enemy_bullets = enemy.fire()
                for eb in enemy_bullets:
                    bullets.append(eb)
        elif not enemy.is_explosion and act == 'Exit':
            enemies.remove(enemy)

        if not enemy.draw():
            enemies.remove(enemy)
            if enemy.is_boss:
                pygame.quit()
                sys.exit()

        enemy.index += 1

    font = pygame.font.SysFont('arial', 16)

    text = font.render('HP', True, (255, 255, 255))
    screen.blit(text, (10, screen.get_height() - 60))
    pygame.draw.rect(screen, (255, 0, 0), Rect(40, screen.get_height() - 60, player.hp, 16))
    pygame.draw.rect(screen, (255, 255, 255), Rect(40, screen.get_height() - 60, 100, 16), 1)

    text = font.render('SP', True, (255, 255, 255))
    screen.blit(text, (10, screen.get_height() - 40))
    pygame.draw.rect(screen, (0, 0, 255), Rect(40, screen.get_height() - 40, player.sp, 16))
    pygame.draw.rect(screen, (255, 255, 255), Rect(40, screen.get_height() - 40, 100, 16), 1)

    pygame.display.update()

def on_appear_enemies(config, x, y):
    enemy = Enemy('./units/' + config + '.ini')
    enemy.set_center_x(x)
    enemy.set_center_y(y)

    enemies.append(enemy)

screen_size = {
    'width': 1024,
    'height': 768
}

pygame.init()
pygame.key.set_repeat(5, 5)
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()
fps = 64
ini = configparser.ConfigParser()

bullets = []
enemies = []
player = Player('./units/player.ini')

is_press_left = False
is_press_up = False
is_press_right = False
is_press_down = False

stars = []
for i in range(100):
    level = random.randint(1, 5)
    star = Star(level)
    stars.append(star)

bombs = []
bomb_index = -1
scenario_manager = ScenarioManager('./scenarios/scenario.ini', on_appear_enemies)
snd_bomb = pygame.mixer.Sound(".\\sounds\\bomb.wav")

scenario_manager.index = 0
screen.fill((0, 0, 0))

while True:
    clock.tick(fps)

    scenario_manager.tick()
    update_game()