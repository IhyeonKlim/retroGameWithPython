import sys
import pygame
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
# 적 클래스 (unit 상속)
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
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]]]
        self.delay = 10
    def move_down(self):
        self.rect.centery += 6  # 아래로 이동
        return True

# 플레이어 생성
player = player(screen.get_width() / 2, screen.get_height() - 30, white)
enemies = []  # 2차원 배열로 적 저장
marginx = (screen.get_width() - (40 * 11)) / 2  # 화면 가운데 정렬
for y in range(0, 5):  # 5줄의 적 생성
    row = []
    color = green if y <= 0 else blue if y < 3 else yellow  # 색상 다르게
    for x in range(0, 11):  # 각 줄에 11마리 적
        row.append(enemy(marginx + x * 40, 100 + y * 25, color))
    enemies.append(row)
is_move_right_enemy = 1  # 1이면 오른쪽으로 이동 중

# 게임 루프
def update_game():
    global is_move_right_enemy, time
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move_left()
            elif event.key == K_RIGHT:
                player.move_right()

    # 화면 초기화
    screen.fill(black)

    # 플레이어 그리기
    player.draw()

    # 적 그리기
    for y, row in enumerate(enemies):
        for x, enemy in enumerate(row):
            enemy.draw()



    # 화면 업데이트 및 FPS 유지
    pygame.display.update()
    clock.tick(60)
    time += 1

# 메인 루프
while True:
    update_game()  # 매 프레임 호출
