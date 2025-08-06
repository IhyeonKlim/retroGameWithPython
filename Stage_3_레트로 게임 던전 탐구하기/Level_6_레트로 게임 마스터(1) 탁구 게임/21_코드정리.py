import sys
import random  # 무작위 방향 설정에 사용할 랜덤 모듈

import pygame
from pygame import QUIT, KEYDOWN, K_TAB, K_r, Rect  # 자주 쓰는 상수만 직접 import

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 창 제목 설정
pygame.display.set_caption("ping pong game")

# 색상 정의
BLACK = (0, 0, 0)      # 배경색
WHITE = (255, 255, 255)  # 테두리, 텍스트, 점선
RED = (255, 0, 0)      # 필요 시 강조용 (현재 사용 안 함)

# FPS 설정
FPS = 60  # 초당 프레임 수
clock = pygame.time.Clock()

# 테두리 및 여백
BORDER_THICKNESS = 10  # 상하 테두리 두께
HORIZONTAL_PADDING = 60  # 좌우 여백
VERTICAL_PADDING = 40    # 상하 여백

# 실제 플레이 가능한 영역 계산
PLAY_AREA_X = BORDER_THICKNESS + HORIZONTAL_PADDING
PLAY_AREA_Y = BORDER_THICKNESS + VERTICAL_PADDING
PLAY_AREA_WIDTH = SCREEN_WIDTH - 2 * (BORDER_THICKNESS + HORIZONTAL_PADDING)
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - 2 * (BORDER_THICKNESS + VERTICAL_PADDING)

# 중앙 점선 설정
DASH_WIDTH = 10
DASH_HEIGHT = 20
DASH_GAP = 20

# 각 꼭지점 좌표 (현재 사용되진 않지만 참고용)
top_left = (PLAY_AREA_X, PLAY_AREA_Y)
top_right = (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y)
bottom_left = (PLAY_AREA_X, PLAY_AREA_Y + PLAY_AREA_HEIGHT)
bottom_right = (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y + PLAY_AREA_HEIGHT)

# 키보드 누르고 있으면 반복 입력 가능하게 설정
pygame.key.set_repeat(5, 5)

# 중앙 점선을 화면에 그리는 함수
def draw_center_dashed_line(surface, color, start_x, start_y,
                            height, dash_height, gap_height, line_width):
    """중앙 수직 점선을 그리는 함수"""
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y),
                         (start_x, y + dash_height), line_width)

# 점수 표시용 폰트
font = pygame.font.Font(None, 50)  # 기본 크기 50
large_font = pygame.font.Font(None, 150)  # 큰 텍스트용 (PING PONG)

# 점수 및 게임 상태 변수
player1_score = 0
player2_score = 0
game_started = False  # 게임 시작 여부
game_over = False     # 게임 종료 여부
winner = None         # 승자 이름


# 공 클래스 정의
class Ball:
    def __init__(self, x, y):
        # 공의 속성 초기화
        self.radius = 10
        self.x = x
        self.y = y
        self.speed = 4
        self.acceleration = 1.1  # 충돌 시 가속도
        self.max_speed = 8
        self.enable = False  # 공 활성화 여부
        self._set_random_direction()  # 방향 무작위 설정

    # 경계 속성들 (충돌 체크용)
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

    # 공 움직임 및 충돌 처리
    def move(self, player1, player2):
        global player1_score, player2_score, game_over, winner

        # 위치 갱신
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # 왼쪽 벽에 닿으면 player2 점수 +1
        if self.left <= PLAY_AREA_X:
            player2_score += 1
            self.reset()
            if player2_score >= 11:
                game_over = True
                winner = "Player 2"

        # 오른쪽 벽에 닿으면 player1 점수 +1
        if self.right >= PLAY_AREA_X + PLAY_AREA_WIDTH:
            player1_score += 1
            self.reset()
            if player1_score >= 11:
                game_over = True
                winner = "Player 1"

        # 상단 벽 충돌 → 방향 반전
        if self.top <= PLAY_AREA_Y:
            self.direction_y *= -1
            self.increase_speed()

        # 하단 벽 충돌 → 방향 반전
        if self.bottom >= PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            self.direction_y *= -1
            self.increase_speed()

        # player1 라켓과 충돌
        if player1.rect.collidepoint(self.left, self.y):
            self.direction_x = 1  # 오른쪽 반사
            self.x = player1.rect.right + self.radius  # 튕긴 위치 조정

        # player2 라켓과 충돌
        elif player2.rect.collidepoint(self.right, self.y):
            self.direction_x = -1  # 왼쪽 반사
            self.x = player2.rect.left - self.radius

    def increase_speed(self):
        # 속도를 가속하되 최대 속도 초과하지 않도록 제한
        self.speed = min(self.speed * self.acceleration, self.max_speed)

    def _set_random_direction(self):
        # X, Y 방향 무작위 설정
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def reset(self):
        # 공을 중앙으로 재배치하고 속도 초기화
        self.x = PLAY_AREA_X + PLAY_AREA_WIDTH // 2
        self.y = PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2
        self.speed = 4
        self.enable = False
        self._set_random_direction()


# 플레이어 클래스 정의 (라켓)
class Player:
    def __init__(self, x, y):
        # 라켓 Rect 객체 생성
        self.rect = Rect(0, 0, 10, 80)
        self.rect.centerx = x
        self.rect.centery = y
        self.update_position()

    def update_position(self):
        # 현재 rect 기준 top/bottom 업데이트
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def move_up(self):
        self.rect.centery -= 7
        self.update_position()

    def move_down(self):
        self.rect.centery += 7
        self.update_position()


# 플레이어 및 공 생성
player1 = Player(PLAY_AREA_X + 20, PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
player2 = Player(PLAY_AREA_X + PLAY_AREA_WIDTH - 20,
                 PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
ball = Ball(PLAY_AREA_X + PLAY_AREA_WIDTH // 2,
            PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)

# 메인 게임 루프 시작
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False  # 창 닫으면 종료
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_TAB and not ball.enable and not game_over:
                ball.enable = True  # Tab 키로 공 활성화
            elif event.key == pygame.K_RETURN and not game_started and not game_over:
                game_started = True
                ball.enable = True  # Enter로 게임 시작
            elif event.key == K_r and game_over:
                # R 키로 리셋
                game_started = False
                game_over = False
                player1_score = 0
                player2_score = 0
                winner = None

    # 키보드 실시간 입력 처리
    keys = pygame.key.get_pressed()

    # 각 플레이어 키 조작
    if keys[pygame.K_w] and player1.top > PLAY_AREA_Y:
        player1.move_up()
    if keys[pygame.K_s] and player1.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
        player1.move_down()
    if keys[pygame.K_UP] and player2.top > PLAY_AREA_Y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
        player2.move_down()

    # 배경 지우기
    screen.fill(BLACK)

    # 상단/하단 테두리 그리기
    pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y),
                     (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y), BORDER_THICKNESS)
    pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y + PLAY_AREA_HEIGHT),
                     (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y + PLAY_AREA_HEIGHT), BORDER_THICKNESS)

    # 중앙 점선 그리기
    mid_x = PLAY_AREA_X + PLAY_AREA_WIDTH // 2
    for y in range(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_HEIGHT, DASH_HEIGHT + DASH_GAP):
        pygame.draw.line(screen, WHITE, (mid_x, y), (mid_x, y + DASH_HEIGHT), 5)

    # 라켓 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 이동
    if ball.enable:
        ball.move(player1, player2)

    # 공 그리기
    pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.radius)

    # 점수 텍스트 렌더링
    p1_text = font.render(f"{player1_score:02}", True, WHITE)
    p2_text = font.render(f"{player2_score:02}", True, WHITE)

    # 점수 위치 설정
    screen.blit(p1_text, (SCREEN_WIDTH // 4 - p1_text.get_width() // 2, 10))
    screen.blit(p2_text, (3 * (SCREEN_WIDTH // 4) - p2_text.get_width() // 2, 10))

    # 게임 시작 전 메시지 표시
    if not game_started and not game_over:
        start_text = font.render("Press Enter to Start", True, WHITE)
        pong_text = large_font.render("PING PONG", True, WHITE)

        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 + 10))
        screen.blit(pong_text, (SCREEN_WIDTH // 2 - pong_text.get_width() // 2,
                                3 * (SCREEN_HEIGHT // 4) - pong_text.get_height() // 2))

    # 게임 오버 시 메시지 표시
    if game_over:
        win_text = font.render(f"{winner} Wins!", True, WHITE)
        restart_text = font.render("Press R to Restart Game", True, WHITE)

        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 10))

    # 화면 갱신 및 FPS 유지
    pygame.display.update()
    clock.tick(FPS)

# 종료 처리
pygame.quit()
sys.exit()
