import sys
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect

# 게임 화면 크기
screen_size = {
    'width': 640,
    'height': 480
}

# 색상 정의
white = (255, 255, 255)
yellow = (255, 228, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("우주 침략자 게임")
pygame.key.set_repeat(5, 5) # 키입력을 빠르게.
clock = pygame.time.Clock()  # FPS 조절을 위한 클럭 객체 생성
time = 0  # 게임 시간 (프레임 기준)

#스코어 life
score = 0
life = 3

# Unit 클래스
class unit:
    def __init__(self, x, y, color):
        self.rect = Rect(0, 0, 22, 12)  # 기본 사각형 크기
        self.rect.centerx = x          # 중앙 X좌표 설정
        self.rect.centery = y          # 중앙 Y좌표 설정
        self.character = []            # ASCII 형태 이미지 (2D 배열)
        self.enable = True             # 활성화 여부
        self.frame_index = 0           # 애니메이션 프레임 인덱스
        self.color = color             # 색상 저장

    def draw(self):
        # 프레임 인덱스가 범위를 넘으면 리셋
        if self.frame_index >= len(self.character):
            self.frame_index = 0

        # 현재 프레임의 픽셀 정보 기반으로 도트 이미지 출력
        for y, line in enumerate(self.character[self.frame_index]):
            ry = self.rect.y + y  # Y좌표
            for x, pt in enumerate(line):
                if pt <= 0:  # 0이면 출력하지 않음
                    continue
                rx = self.rect.x + x  # X좌표
                pygame.draw.circle(screen, self.color, [rx, ry], 1)  # 작은 원으로 도트 그림

        return True

    def move_left(self):
        self.rect.centerx -= 2  # 왼쪽 이동
        self.frame_index = (self.frame_index + 1) % 2  # 프레임 변경 (깜빡이기용)
        return True

    def move_right(self):
        self.rect.centerx += 2  # 오른쪽 이동
        self.frame_index = (self.frame_index + 1) % 2  # 프레임 변경
        return True

# Player 클래스 (unit 상속)
class player(unit):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[  # 플레이어 도트 형태 (고정 프레임 하나)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]]

# ------------------------------
# 적 클래스 (unit 상속, 2프레임)
# ------------------------------
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
        self.delay = 10  # 움직임 딜레이 프레임
    def move_down(self):
        self.rect.centery += 6  # 아래로 이동
        return True

# 총알 구현
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

# 플레이어 생성
player = player(screen.get_width() / 2, screen.get_height() - 30, white)

# 총알 객체 생성
player_bullet = bullet() #클래스 명과 변수명이 같은 경우 callable error가 생길 수 있음. 변수명 변경
player_bullet.color = player.color

enemies = []  # 2차원 배열로 적 저장
marginx = (screen.get_width() - (40 * 11)) / 2  # 화면 가운데 정렬
for y in range(0, 5):  # 5줄의 적 생성
    row = []
    color = green if y <= 0 else blue if y < 3 else yellow  # 색상 다르게
    for x in range(0, 11):  # 각 줄에 11마리 적
        row.append(enemy(marginx + x * 40, 100 + y * 25, color))
    enemies.append(row)
is_move_right_enemy = 1  # 1이면 오른쪽으로 이동 중

enemy_bullets = []
fired_enemy_bullets = []
for i in range(0, 5):
    enemy_bullets.append(bullet())

# 벽 생성
walls = []
for i in range(0, 4):
    walls.append(wall(155 + i * 110, screen.get_height() - 70, red))


# 게임 루프
def update_game():
    global is_move_right_enemy, time, player_bullet, fired_enemy_bullets, enemy_bullets,  score, life

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move_left()
            elif event.key == K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE:
                if player_bullet.enable is True:
                    break
                if player.enable is False:
                    break
                player_bullet.fire(player.rect.centerx, player.rect.y)
    # 화면 초기화
    screen.fill(black)

    # 플레이어 그리기
    player.draw()

    # 적 이동 및 그리기
    for y, row in enumerate(enemies):
        for x, enemy in enumerate(row):
            if enemy.enable is True:
                if enemy.rect.colliderect(player_bullet.rect) and player_bullet.enable is True:
                    enemy.enable = False
                    player_bullet.enable = False
                    score +=100
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

    # 경계 충돌 시 방향 바꾸기
    is_change_direction = False

    for row in enemies:
        for enemy in row:
            if (is_move_right_enemy > 0 and enemy.rect.right >= screen.get_width()) or \
               (is_move_right_enemy <= 0 and enemy.rect.left <= 0):
                is_move_right_enemy = (is_move_right_enemy + 1) % 2  # 방향 전환
                is_change_direction = True
                break
        if is_change_direction:
            break

    # 방향 전환 시 아래로 이동
    for row in enemies:
        for enemy in row:
            if is_change_direction:
                enemy.delay = max(4, enemy.delay - 1)
                enemy.move_down()

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

    # 총알 그리기
    if player_bullet.enable is True:
        player_bullet.moveup()
        player_bullet.draw()

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

    for wall in walls:
        if player_bullet.enable is True:
            if wall.colliderect(player_bullet) is True:
                player_bullet.enable = False

        wall.draw()

    # 화면 업데이트
    pygame.display.update()
    clock.tick(60)
    time += 1

# 메인 루프
while True:
    update_game()  # 매 프레임 호출
