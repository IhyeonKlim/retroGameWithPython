import pygame
import random
import time

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cop Shooting Game")

# 색상 정의
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()


class Gun:
    """플레이어의 총 관리 클래스"""
    def __init__(self):
        self.MAX_BULLETS = 7
        self.bullets = self.MAX_BULLETS
        self.reload_speed = 0.7
        self.last_reload_time = None
        self.quick_reload_cooldown = 2.0  # 퀵 리로드 대기 시간 (초)
        self.last_quick_reload_time = time.time()

    def shoot(self):
        if self.bullets > 0:
            self.bullets -= 1
            print("Shot fired!")
            return True
        else:
            print("Out of bullets!")
            return False

    def reload(self):
        if self.bullets < self.MAX_BULLETS:
            current_time = time.time()
            if self.last_reload_time is None or current_time - self.last_reload_time >= self.reload_speed:
                self.bullets += 1
                self.last_reload_time = current_time

    def quick_reload(self):
        """퀵 리로드"""
        current_time = time.time()
        if current_time - self.last_quick_reload_time >= self.quick_reload_cooldown:
            if self.bullets < self.MAX_BULLETS:
                self.bullets += 1
                self.last_quick_reload_time = current_time
                print("Quick Reload!")

    def remaining_quick_reload_time(self):
        """퀵 리로드 남은 대기 시간"""
        current_time = time.time()
        remaining_time = self.quick_reload_cooldown - (current_time - self.last_quick_reload_time)
        return max(0, remaining_time)

    def draw_bullets(self):
        bullet_width, bullet_height = 20, 10
        for i in range(self.bullets):
            x = WIDTH - (bullet_width + 5) * (i + 1)
            y = HEIGHT - bullet_height - 10
            pygame.draw.rect(screen, YELLOW, (x, y, bullet_width, bullet_height))


class Player:
    """플레이어 상태 관리 클래스"""
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font(None, 36)

    def update_score(self, amount):
        self.score += amount

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            print("Game Over!")
            return False
        return True

    def draw(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))


class Crosshair:
    """조준 십자선 클래스"""
    def __init__(self):
        self.color = GREEN

    def draw(self, position):
        pygame.draw.line(screen, self.color, (position[0] - 20, position[1]), (position[0] + 20, position[1]), 2)
        pygame.draw.line(screen, self.color, (position[0], position[1] - 20), (position[0], position[1] + 20), 2)


# 기본 게임 루프
gun = Gun()
player = Player()
crosshair = Crosshair()
running = True
font = pygame.font.Font(None, 36)  # 텍스트 표시용 기본 폰트

# 피격 효과 관련 변수
hit_effect_time = None
hit_effect_duration = 300  # 피격 효과 지속 시간 (밀리초)

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                gun.shoot()
            elif event.button == 3:  # 오른쪽 클릭
                gun.quick_reload()

    # 화면 검은색으로 채우기
    screen.fill(BLACK)

    # 총기 동작
    gun.reload()
    gun.draw_bullets()

    # "Reload" 텍스트 표시
    if gun.bullets == 0:
        reload_text = font.render("Reload", True, YELLOW)
        reload_rect = reload_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(reload_text, reload_rect)

    # 퀵 리로드 대기 시간 표시
    quick_reload_time = gun.remaining_quick_reload_time()
    quick_reload_text = font.render(f"Quick Reload: {quick_reload_time:.1f}s", True, WHITE)
    screen.blit(quick_reload_text, (10, HEIGHT - 40))

    # 피격 효과
    if hit_effect_time and current_time - hit_effect_time < hit_effect_duration:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # 투명도 설정
        overlay.fill(RED)
        screen.blit(overlay, (0, 0))

    # 플레이어 상태 표시
    player.draw()

    # 십자선 그리기
    mouse_pos = pygame.mouse.get_pos()
    crosshair.draw(mouse_pos)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

