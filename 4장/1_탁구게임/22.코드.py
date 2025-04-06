import sys
import random  # 랜덤 모듈 추가

import pygame
from pygame import QUIT, KEYDOWN, K_TAB, K_r, Rect

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 타이틀 설정
pygame.display.set_caption("ping pong game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 테두리 및 여백 설정
BORDER_THICKNESS = 10
HORIZONTAL_PADDING = 60
VERTICAL_PADDING = 40

# 플레이 구역 설정
PLAY_AREA_X = BORDER_THICKNESS + HORIZONTAL_PADDING
PLAY_AREA_Y = BORDER_THICKNESS + VERTICAL_PADDING
PLAY_AREA_WIDTH = SCREEN_WIDTH - 2 * (BORDER_THICKNESS + HORIZONTAL_PADDING)
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - 2 * (BORDER_THICKNESS + VERTICAL_PADDING)

# 점선 설정
DASH_WIDTH = 10
DASH_HEIGHT = 20
DASH_GAP = 20

# 꼭지점 좌표
top_left = (PLAY_AREA_X, PLAY_AREA_Y)
top_right = (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y)
bottom_left = (PLAY_AREA_X, PLAY_AREA_Y + PLAY_AREA_HEIGHT)
bottom_right = (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y + PLAY_AREA_HEIGHT)

# 키보드 반복 입력 허용
pygame.key.set_repeat(5, 5)

# 폰트 설정
font = pygame.font.Font(None, 50)
large_font = pygame.font.Font(None, 150)

# 스코어 변수
player1_score = 0
player2_score = 0

# 게임 상태
game_started = False
game_over = False
winner = None


def draw_center_dashed_line(surface, color, start_x, start_y,
                            height, dash_height, gap_height, line_width):
    """중앙 수직 점선 그리기 함수"""
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y),
                         (start_x, y + dash_height), line_width)


class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.speed = 4
        self.acceleration = 1.1
        self.max_speed = 8
        self.enable = False
        self._set_random_direction()

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    def move(self, player1, player2):
        global player1_score, player2_score, game_over, winner

        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        if self.left <= PLAY_AREA_X:
            player2_score += 1
            self.reset()
            if player2_score >= 11:
                game_over = True
                winner = "Player 2"

        if self.right >= PLAY_AREA_X + PLAY_AREA_WIDTH:
            player1_score += 1
            self.reset()
            if player1_score >= 11:
                game_over = True
                winner = "Player 1"

        if self.top <= PLAY_AREA_Y:
            self.direction_y *= -1
            self.increase_speed()

        if self.bottom >= PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            self.direction_y *= -1
            self.increase_speed()

        if player1.rect.collidepoint(self.left, self.y):
            self.direction_x = 1
            self.x = player1.rect.right + self.radius

        elif player2.rect.collidepoint(self.right, self.y):
            self.direction_x = -1
            self.x = player2.rect.left - self.radius

    def increase_speed(self):
        self.speed = min(self.speed * self.acceleration, self.max_speed)

    def _set_random_direction(self):
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def reset(self):
        self.x = PLAY_AREA_X + PLAY_AREA_WIDTH // 2
        self.y = PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2
        self.speed = 4
        self.enable = False
        self._set_random_direction()


class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 80)
        self.rect.centerx = x
        self.rect.centery = y
        self.update_position()

    def update_position(self):
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def move_up(self):
        self.rect.centery -= 7
        self.update_position()

    def move_down(self):
        self.rect.centery += 7
        self.update_position()


player1 = Player(PLAY_AREA_X + 20, PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
player2 = Player(PLAY_AREA_X + PLAY_AREA_WIDTH - 20,
                 PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
ball = Ball(PLAY_AREA_X + PLAY_AREA_WIDTH // 2,
            PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_TAB and not ball.enable:
                ball.enable = True
            elif event.key == pygame.K_RETURN and not game_started and not game_over:
                game_started = True
                ball.enable = True
            elif event.key == K_r and game_over:
                game_started = False
                game_over = False
                player1_score = 0
                player2_score = 0
                winner = None

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player1.top > PLAY_AREA_Y:
        player1.move_up()
    if keys[pygame.K_s] and player1.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
        player1.move_down()
    if keys[pygame.K_UP] and player2.top > PLAY_AREA_Y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
        player2.move_down()

    screen.fill(BLACK)

    # 위쪽, 아래쪽 테두리
    pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y),
                     (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y), BORDER_THICKNESS)
    pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y + PLAY_AREA_HEIGHT),
                     (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y + PLAY_AREA_HEIGHT), BORDER_THICKNESS)

    # 중앙 점선
    mid_x = PLAY_AREA_X + PLAY_AREA_WIDTH // 2
    for y in range(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_HEIGHT, DASH_HEIGHT + DASH_GAP):
        pygame.draw.line(screen, WHITE, (mid_x, y), (mid_x, y + DASH_HEIGHT), 5)

    # 라켓
    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 이동
    if ball.enable:
        ball.move(player1, player2)

    # 공 그리기
    pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.radius)

    # 스코어
    p1_text = font.render(f"{player1_score:02}", True, WHITE)
    p2_text = font.render(f"{player2_score:02}", True, WHITE)

    screen.blit(p1_text, (SCREEN_WIDTH // 4 - p1_text.get_width() // 2, 10))
    screen.blit(p2_text, (3 * (SCREEN_WIDTH // 4) - p2_text.get_width() // 2, 10))

    # 게임 시작 전 메시지
    if not game_started and not game_over:
        start_text = font.render("Press Enter to Start", True, WHITE)
        pong_text = large_font.render("PING PONG", True, WHITE)

        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 + 10))
        screen.blit(pong_text, (SCREEN_WIDTH // 2 - pong_text.get_width() // 2,
                                3 * (SCREEN_HEIGHT // 4) - pong_text.get_height() // 2))

    # 게임 오버 메시지
    if game_over:
        win_text = font.render(f"{winner} Wins!", True, WHITE)
        restart_text = font.render("Press R to Restart Game", True, WHITE)

        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
