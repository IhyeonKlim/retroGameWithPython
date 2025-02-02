import sys
import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# 색상 정의
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 테두리 및 플레이 구역 설정
BORDER_THICKNESS = 10
HORIZONTAL_PADDING, VERTICAL_PADDING = 60, 40
PLAY_AREA_X = BORDER_THICKNESS + HORIZONTAL_PADDING
PLAY_AREA_Y = BORDER_THICKNESS + VERTICAL_PADDING
PLAY_AREA_WIDTH = SCREEN_WIDTH - 2 * (BORDER_THICKNESS + HORIZONTAL_PADDING)
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - 2 * (BORDER_THICKNESS + VERTICAL_PADDING)

# 폰트 설정
font = pygame.font.Font(None, 50)  # 스코어용
large_font = pygame.font.Font(None, 100)  # 타이틀용

# 스코어 변수
player1_score, player2_score = 0, 0

# 게임 상태 변수
game_started = game_over = False
winner = None


class Ball:
    """공 클래스"""

    def __init__(self, x, y):
        self.radius = 10
        self.x, self.y = x, y
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

    def _set_random_direction(self):
        """랜덤 방향 설정"""
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def move(self, player1, player2):
        global player1_score, player2_score, game_over, winner

        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        if self.left <= PLAY_AREA_X:
            player2_score += 1
            self._check_game_over("Player 2")

        if self.right >= PLAY_AREA_X + PLAY_AREA_WIDTH:
            player1_score += 1
            self._check_game_over("Player 1")

        if self.top <= PLAY_AREA_Y or self.bottom >= PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            self.direction_y *= -1
            self.increase_speed()

        if player1.rect.collidepoint(self.left, self.y):
            self.direction_x = 1
            self.x = player1.rect.right + self.radius

        elif player2.rect.collidepoint(self.right, self.y):
            self.direction_x = -1
            self.x = player2.rect.left - self.radius

    def _check_game_over(self, scoring_player):
        """게임 종료 확인"""
        if player1_score >= 11 or player2_score >= 11:
            global game_over, winner
            game_over, winner = True, scoring_player
        self.reset()

    def increase_speed(self):
        """속도 증가"""
        self.speed = min(self.speed * self.acceleration, self.max_speed)

    def reset(self):
        """공 초기화"""
        self.x = PLAY_AREA_X + PLAY_AREA_WIDTH // 2
        self.y = PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2
        self.speed = 4
        self._set_random_direction()
        self.enable = False


class Player:
    """플레이어 클래스"""

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 10, 80)
        self.rect.centerx = x
        self.rect.centery = y

    def move_up(self):
        self.rect.centery -= 7

    def move_down(self):
        self.rect.centery += 7


# 객체 생성
player1 = Player(PLAY_AREA_X + 20, PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
player2 = Player(PLAY_AREA_X + PLAY_AREA_WIDTH - 20, PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)
ball = Ball(PLAY_AREA_X + PLAY_AREA_WIDTH // 2, PLAY_AREA_Y + PLAY_AREA_HEIGHT // 2)


def draw_text(text, font, color, position):
    """텍스트를 화면에 그리는 함수"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def game_loop():
    """게임 루프"""
    global game_started, game_over, player1_score, player2_score, winner

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_TAB and not ball.enable:
                    ball.enable = True
                elif event.key == pygame.K_RETURN and not game_started and not game_over:
                    game_started = True
                    ball.enable = True
                elif event.key == pygame.K_r and game_over:
                    game_started = False
                    game_over = False
                    player1_score = player2_score = 0
                    winner = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.rect.top > PLAY_AREA_Y:
            player1.move_up()
        if keys[pygame.K_s] and player1.rect.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            player1.move_down()
        if keys[pygame.K_UP] and player2.rect.top > PLAY_AREA_Y:
            player2.move_up()
        if keys[pygame.K_DOWN] and player2.rect.bottom < PLAY_AREA_Y + PLAY_AREA_HEIGHT:
            player2.move_down()

        if ball.enable and game_started:
            ball.move(player1, player2)

        screen.fill(BLACK)

        pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y),
                         (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y), BORDER_THICKNESS)
        pygame.draw.line(screen, WHITE, (PLAY_AREA_X, PLAY_AREA_Y + PLAY_AREA_HEIGHT),
                         (PLAY_AREA_X + PLAY_AREA_WIDTH, PLAY_AREA_Y + PLAY_AREA_HEIGHT), BORDER_THICKNESS)

        for y in range(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_HEIGHT, 40):
            pygame.draw.line(screen, WHITE, (PLAY_AREA_X + PLAY_AREA_WIDTH // 2, y),
                             (PLAY_AREA_X + PLAY_AREA_WIDTH // 2, y + 20), 5)

        pygame.draw.rect(screen, WHITE, player1.rect)
        pygame.draw.rect(screen, WHITE, player2.rect)
        pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.radius)

        draw_text(f"{player1_score:02}", font, WHITE, (SCREEN_WIDTH // 4, 30))
        draw_text(f"{player2_score:02}", font, WHITE, (3 * SCREEN_WIDTH // 4, 30))

        if not game_started and not game_over:
            draw_text("PING PONG", large_font, WHITE, (SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 4))
            draw_text("Press Enter to Start", font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        if game_over:
            draw_text(f"{winner} Wins!", font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            draw_text("Press R to Restart Game", font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    game_loop()
