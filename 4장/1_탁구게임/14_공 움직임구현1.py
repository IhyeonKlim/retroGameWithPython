import sys
import pygame
import time
from pygame import QUIT, KEYDOWN, Rect

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("ping pong game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS 설정
fps_value = 60
clock = pygame.time.Clock()

# 테두리 및 여백 설정
border_thickness = 10
horizontal_padding = 60
vertical_padding = 40

# 플레이 구역 설정
play_area_x = border_thickness + horizontal_padding
play_area_y = border_thickness + vertical_padding
play_area_width = screen_width - 2 * (border_thickness + horizontal_padding)
play_area_height = screen_height - 2 * (border_thickness + vertical_padding)

# 공 클래스 정의
# 우선 Ball의 클래스를 정의(플레이어때와 구조는 같습니다)
class Ball:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 50, 50)  # 공의 크기 설정 (0.0 위치에 가로 50, 세로 50)
        self.rect.centerx = x  # 사각형 중심의 X 좌표 설정
        self.rect.centery = y  # 사각형 중심의 Y 좌표 설정
    def move(self):
		    self.rect.centerx -= 5 # 화면 왼쪽 상단이 0인 것을 기억하세요! x값이 -로 가면 왼쪽입니다.

# 플레이어 클래스 정의
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)
        self.rect.centerx = x
        self.rect.centery = y

    def move_up(self):
        self.rect.centery -= 5

    def move_down(self):
        self.rect.centery += 5

# 플레이어 객체 생성
player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

#공 객체 생성
ball = Ball(play_area_x + play_area_width // 2, play_area_y + play_area_height // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # 동시에 여러 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.rect.top > play_area_y:
        player1.move_up()
    if keys[pygame.K_s] and player1.rect.bottom < play_area_y + play_area_height:
        player1.move_down()
    if keys[pygame.K_UP] and player2.rect.top > play_area_y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.rect.bottom < play_area_y + play_area_height:
        player2.move_down()

    # 화면 그리기
    screen.fill(BLACK)

    # 테두리 그리기
    outer_rect_x = play_area_x - border_thickness
    outer_rect_y = play_area_y - border_thickness
    outer_rect_width = play_area_width + 2 * border_thickness
    outer_rect_height = play_area_height + 2 * border_thickness
    pygame.draw.rect(screen, WHITE, (outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height), border_thickness)

    # 중앙 점선 그리기
    mid_x = play_area_x + play_area_width // 2
    for y in range(play_area_y, play_area_y + play_area_height, 40):
        pygame.draw.line(screen, WHITE, (mid_x, y), (mid_x, y + 20), 5)

    # 플레이어 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 이동
    ball.move() # 공의 좌표값을 바꾸기 위해서 move 메서드 호출
    # 공 그리기
    pygame.draw.rect(screen, WHITE, ball.rect)

    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
