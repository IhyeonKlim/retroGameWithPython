import sys
import pygame
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
RED = (255, 0, 0)

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

# 꼭지점 좌표 계산
top_left = (play_area_x, play_area_y)
top_right = (play_area_x + play_area_width, play_area_y)
bottom_left = (play_area_x, play_area_y + play_area_height)
bottom_right = (play_area_x + play_area_width, play_area_y + play_area_height)

print("Top Left:", top_left)
print("Top Right:", top_right)
print("Bottom Left:", bottom_left)
print("Bottom Right:", bottom_right)

def draw_center_dashed_line(surface, color, start_x, start_y, height, dash_height, gap_height, line_width):
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y), (start_x, y + dash_height), line_width)

class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)
        self.rect.centerx = x
        self.rect.centery = y
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def update_position(self):
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def move_up(self):
        self.rect.centery -= 5
        self.update_position()

    def move_down(self):
        self.rect.centery += 5
        self.update_position()

player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

class Ball:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 50, 50)
        self.rect.centerx = x
        self.rect.centery = y

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

    if keys[pygame.K_w] and player1.top > play_area_y:
        player1.move_up()
    if keys[pygame.K_s] and player1.bottom < play_area_y + play_area_height:
        player1.move_down()
    if keys[pygame.K_UP] and player2.top > play_area_y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.bottom < play_area_y + play_area_height:
        player2.move_down()

    screen.fill(BLACK)

    outer_rect_x = play_area_x - border_thickness
    outer_rect_y = play_area_y - border_thickness
    outer_rect_width = play_area_width + 2 * border_thickness
    outer_rect_height = play_area_height + 2 * border_thickness
    pygame.draw.rect(screen, WHITE, (outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height), border_thickness)

    mid_x = play_area_x + play_area_width // 2
    draw_center_dashed_line(screen, WHITE, mid_x, play_area_y, play_area_height, 20, 20, 10)

    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)
    pygame.draw.rect(screen, WHITE, ball.rect)

    pygame.draw.circle(screen, RED, top_left, 5)
    pygame.draw.circle(screen, RED, top_right, 5)
    pygame.draw.circle(screen, RED, bottom_left, 5)
    pygame.draw.circle(screen, RED, bottom_right, 5)

    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
