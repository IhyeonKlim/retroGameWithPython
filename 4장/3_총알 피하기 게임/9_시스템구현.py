import pygame
import random
import math
import sys
import os

# Pygame 초기화
pygame.init()

# 색상 정의 (RGB)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 화면 설정 (가로, 세로 크기 설정)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")

# FPS 설정 (게임 속도 조절)
FPS = 60
clock = pygame.time.Clock()

# 폰트 설정 (게임 화면에 사용할 텍스트 스타일)
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 60)

# 플레이어 클래스 정의
class Player:
    """플레이어 클래스"""
    def __init__(self):
        self.size = 20  # 플레이어 크기 설정
        self.speed = 4  # 플레이어 속도 설정
        # 플레이어 위치 초기화 (화면 중앙에서 시작)
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.size, self.size)

    def move(self, keys):
        # 키보드 입력에 따라 플레이어의 위치 이동
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        # 플레이어 그리기 (파란색 사각형)
        pygame.draw.rect(screen, BLUE, self.rect)

# 일반 총알 클래스 정의
# 플레이어를 향해 이동하며 충돌을 감지하는 역할

class Bullet:
    """일반 총알 클래스"""
    def __init__(self, player, bullets):
        # 총알을 화면 가장자리에서 생성
        self.x, self.y = self._spawn_on_border(bullets)
        self.radius = 3  # 총알 크기 설정
        self.speed = random.uniform(1, 2)  # 총알 속도 설정 (임의 속도)

        # 플레이어를 목표로 각도 계산
        self.target_x = player.rect.centerx
        self.target_y = player.rect.centery
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def _spawn_on_border(self, bullets):
        """기존 총알과 최소 거리가 필요한 위치에 총알 생성"""
        while True:
            side = random.choice(['left', 'right', 'top', 'bottom'])
            if side == 'left':
                x, y = 0, random.randint(0, SCREEN_HEIGHT)
            elif side == 'right':
                x, y = SCREEN_WIDTH - 1, random.randint(0, SCREEN_HEIGHT)
            elif side == 'top':
                x, y = random.randint(0, SCREEN_WIDTH), 0
            else:
                x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 1

            # 기존 총알과 최소 거리(30픽셀)를 확보한 위치에서 생성
            if all(math.hypot(b.x - x, b.y - y) > 30 for b in bullets):
                return x, y

    def move(self):
        # 각도에 따라 총알 이동
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        # 총알 그리기 (노란색 원)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def is_on_border(self):
        # 총알이 화면 밖으로 나갔는지 확인
        return self.x <= 0 or self.x >= SCREEN_WIDTH - 1 or self.y <= 0 or self.y >= SCREEN_HEIGHT - 1

    def check_collision(self, player):
        # 총알과 플레이어 사이의 충돌 여부 확인
        return check_collision_with_player(self, player)

# 특별 총알 (Comet) 클래스 정의
# 일반 총알보다 크고 빠른 속도로 이동

class Comet(Bullet):
    """특별 총알 (Comet) 클래스"""
    def __init__(self, player, bullets):
        super().__init__(player, bullets)
        self.radius = 6  # 일반 총알보다 큰 반지름
        self.speed *= 1.5  # 일반 총알보다 빠른 속도

    def draw(self):
        # 특별 총알 그리기 (빨간색 원)
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# 충돌 감지 함수 정의
def check_collision_with_player(bullet, player):
    """총알과 플레이어 사이의 충돌 여부를 반환하는 함수."""
    distance = math.hypot(player.rect.centerx - bullet.x, player.rect.centery - bullet.y)
    return distance < bullet.radius + player.size / 2

# 게임 클래스 정의
# 게임의 전체적인 흐름을 제어

class Game:
    """게임 클래스"""
    def __init__(self):
        self.player = None
        self.score = 0
        self.game_state = "intro"  # 게임 상태: intro, playing, game_over
        self.reset_game()

    def reset_game(self):
        """게임을 초기화합니다."""
        self.player = Player()
        self.bullets = [Bullet(self.player, []) for _ in range(60)]  # 총알 60개 생성
        self.score = 0

    def run(self):
        # 메인 게임 루프 (게임을 실행하는 동안 지속)
        running = True

        while running:
            screen.fill(BLACK)  # 화면 배경을 검정색으로 채우기

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 창 닫기 버튼 클릭 시 게임 종료
                    pygame.quit()
                    sys.exit()

            if self.game_state == "intro":
                self.display_intro_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.game_state = "playing"

            elif self.game_state == "playing":
                self.play_game()

            elif self.game_state == "game_over":
                self.display_game_over_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset_game()
                    self.game_state = "intro"

            pygame.display.flip()
            clock.tick(FPS)

    def play_game(self):
        """게임을 플레이합니다."""
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw()

        # 총알 이동 및 그리기
        for bullet in self.bullets:
            bullet.move()  # 총알 이동
            bullet.draw()  # 총알 그리기

            if bullet.check_collision(self.player):
                self.game_state = "game_over"
            if bullet.is_on_border():
                # 총알이 화면 밖으로 나갔을 때 새로 생성
                self.bullets.remove(bullet)
                self.bullets.append(Bullet(self.player, self.bullets))

        # 점수 증가 및 표시
        self.score += 1
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 총알 개수 표시
        bullet_count_text = font.render(f"Bullets: {len(self.bullets)}", True, WHITE)
        screen.blit(bullet_count_text, (SCREEN_WIDTH // 2 - bullet_count_text.get_width() // 2, 10))

        # 특정 점수마다 특별 총알 생성
        if self.score > 0 and self.score % 100 == 0:
            self.bullets.append(Comet(self.player, self.bullets))

    def display_intro_screen(self):
        """게임 시작 전 화면을 표시합니다."""
        intro_text = font.render("Press Enter to Start", True, WHITE)
        screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def display_game_over_screen(self):
        """게임 오버 화면을 표시합니다."""
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

# 게임 실행
if __name__ == "__main__":
    game = Game()
    game.run()
