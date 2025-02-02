import sys
import pygame
import random  # 랜덤 모듈 추가
from pygame import QUIT, KEYDOWN, K_TAB, K_r, Rect

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("Ping Pong Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS 설정
fps_value = 60  # 초당 60프레임
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

# 폰트 설정 (스코어 표시용)
font = pygame.font.Font(None, 50)  # 크기 50의 기본 폰트 사용

# 폰트 설정 (기본 폰트 크기 50 → 100으로 키움)
large_font = pygame.font.Font(None, 150)  # PING PONG 텍스트용 폰트

# 스코어 변수 초기화
player1_score = 0
player2_score = 0

# 게임 상태 변수
game_started = False
game_over = False
winner = None


# 공 클래스 정의 (원)
class Ball:
    def __init__(self, x, y):
        self.radius = 10  # 공의 반지름 설정
        self.x = x  # 공의 X축 중심 좌표
        self.y = y  # 공의 Y축 중심 좌표

        self.speed = 4  # 초기 속도 설정 (픽셀 단위)
        self.acceleration = 1.1  # 가속도 설정 (충돌 시 10% 속도 증가)
        self.max_speed = 8  # 최대 속도 제한
        self.enable = False  # 공 비활성화된 상태

        self._set_random_direction()  # 랜덤 방향 설정

    @property
    def left(self):
        """공의 왼쪽 경계"""
        return self.x - self.radius

    @property
    def right(self):
        """공의 오른쪽 경계"""
        return self.x + self.radius

    @property
    def top(self):
        """공의 위쪽 경계"""
        return self.y - self.radius

    @property
    def bottom(self):
        """공의 아래쪽 경계"""
        return self.y + self.radius

    def move(self, player1, player2):
        global player1_score, player2_score, game_over, winner

        # 공의 위치 업데이트
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # 왼쪽 경계를 벗어난 경우 player2 스코어 증가
        if self.left <= play_area_x:
            player2_score += 1
            self.reset()
            if player2_score >= 11:
                game_over = True
                winner = "Player 2"

        # 오른쪽 경계를 벗어난 경우 player1 스코어 증가
        if self.right >= play_area_x + play_area_width:
            player1_score += 1
            self.reset()
            if player1_score >= 11:
                game_over = True
                winner = "Player 1"

        # 위쪽 경계에 부딪힌 경우
        if self.top <= play_area_y:
            self.direction_y *= -1
            self.increase_speed()

        # 아래쪽 경계에 부딪힌 경우
        if self.bottom >= play_area_y + play_area_height:
            self.direction_y *= -1
            self.increase_speed()

        # 플레이어와의 충돌 처리
        if player1.rect.collidepoint(self.left, self.y):
            self.direction_x = 1  # 오른쪽으로 반사
            self.x = player1.rect.right + self.radius  # 공 위치 조정

        elif player2.rect.collidepoint(self.right, self.y):
            self.direction_x = -1  # 왼쪽으로 반사
            self.x = player2.rect.left - self.radius  # 공 위치 조정

    def increase_speed(self):
        """속도를 증가시키되 최대 속도를 초과하지 않도록 제한"""
        new_speed = self.speed * self.acceleration
        self.speed = min(new_speed, self.max_speed)

    def _set_random_direction(self):
        """공의 방향을 랜덤하게 설정하는 메서드"""
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def reset(self):
        """공을 중앙에 위치시키고 초기화하는 메서드"""
        self.x = play_area_x + play_area_width // 2
        self.y = play_area_y + play_area_height // 2
        self.speed = 4
        self._set_random_direction()
        self.enable = False

# 플레이어 클래스 정의
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 80)
        self.rect.centerx = x
        self.rect.centery = y

    def move_up(self):
        self.rect.centery -= 7

    def move_down(self):
        self.rect.centery += 7

# 플레이어 객체 생성
player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

# 공 객체 생성
ball = Ball(play_area_x + play_area_width // 2, play_area_y + play_area_height // 2)

# 게임 루프 시작
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_TAB and not ball.enable:
                ball.enable = True  # 공 활성화
            elif event.key == pygame.K_RETURN and not game_started and not game_over:
                game_started = True
                ball.enable = True
            elif event.key == K_r and game_over:
                game_started = False
                game_over = False
                player1_score = 0
                player2_score = 0
                winner = None

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

    # 공 이동 및 충돌 처리
    if ball.enable and game_started:
        ball.move(player1, player2)

    # 화면 그리기
    screen.fill(BLACK)

    # 위쪽 테두리 그리기
    pygame.draw.line(
        screen, WHITE,
        (play_area_x, play_area_y),
        (play_area_x + play_area_width, play_area_y),
        border_thickness
    )

    # 아래쪽 테두리 그리기
    pygame.draw.line(
        screen, WHITE,
        (play_area_x, play_area_y + play_area_height),
        (play_area_x + play_area_width, play_area_y + play_area_height),
        border_thickness
    )

    # 중앙 점선 그리기
    mid_x = play_area_x + play_area_width // 2
    for y in range(play_area_y, play_area_y + play_area_height, 40):
        pygame.draw.line(screen, WHITE, (mid_x, y), (mid_x, y + 20), 5)

    # 플레이어 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 그리기
    pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.radius)

    # 스코어 표시 (00 형식)
    player1_score_text = font.render(f"{player1_score:02}", True, WHITE)
    player2_score_text = font.render(f"{player2_score:02}", True, WHITE)\

    # 플레이어 1 스코어 위치 (왼쪽 1/4 지점, 테두리 위)
    player1_score_pos = (
        screen_width // 4 - player1_score_text.get_width() // 2,  # X 좌표 중앙 정렬
        10  # 화면 위쪽에 10px 간격
    )

    # 플레이어 2 스코어 위치 (오른쪽 3/4 지점, 테두리 위)
    player2_score_pos = (
        3 * (screen_width // 4) - player2_score_text.get_width() // 2,  # X 좌표 중앙 정렬
        10  # 화면 위쪽에 10px 간격
    )
    # 스코어 텍스트를 화면에 그리기
    screen.blit(player1_score_text, player1_score_pos)
    screen.blit(player2_score_text, player2_score_pos)

    # 게임 시작 전 메시지 표시
    if not game_started and not game_over:
        # "Press Enter to Start" 텍스트
        start_text = font.render("Press Enter to Start", True, WHITE)
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + 10))

        # "PING PONG" 텍스트 (크기 2배로 키우고 화면 하단에 표시)
        pong_text = large_font.render("PING PONG", True, WHITE)

        # PING PONG 텍스트 위치 조정 (화면 하단, 테두리 위에 배치)
        pong_text_pos = (
            screen_width // 2 - pong_text.get_width() // 2,  # X 좌표 중앙 정렬
            3 * (screen_height //4) - pong_text.get_height() // 2  # 테두리 위에 10px 여유 공간 확보
        )
        screen.blit(pong_text, pong_text_pos)

    if game_over:
        win_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 50))
        # 게임 오버시에 표시 다시시작하기 표시
        restart_text = font.render("Press R to Restart Game", True, WHITE)
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 10))

    # 화면 업데이트 및 FPS 유지
    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
