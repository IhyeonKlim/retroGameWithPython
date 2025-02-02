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


class Enemy:
    """적 객체 관리 클래스"""
    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(50, HEIGHT // 2 - self.size),
            self.size, self.size
        )
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.outer_circle_size = 100
        self.inner_circle_size = 50
        self.outer_circle_thickness = 4
        self.inner_circle_thickness = 2

    def is_expired(self, current_time):
        return current_time - self.spawn_time > self.lifetime

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time
        circle_progress = max(0, 1 - elapsed_time / self.lifetime)
        outer_size = int(self.outer_circle_size * circle_progress)
        pygame.draw.circle(screen, RED, self.rect.center, outer_size, self.outer_circle_thickness)
        pygame.draw.circle(screen, YELLOW, self.rect.center, self.inner_circle_size, self.inner_circle_thickness)


class SpecialEnemy(Enemy):
    """스페셜 적 객체 관리 클래스"""
    def __init__(self):
        super().__init__()
        self.lifetime = 1500  # 스페셜 적의 빠른 공격
        self.outer_circle_size = 120
        self.inner_circle_size = 40

    def draw(self):
        """스페셜 적을 파란색으로 표시"""
        pygame.draw.rect(screen, BLUE, self.rect)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time
        circle_progress = max(0, 1 - elapsed_time / self.lifetime)
        outer_size = int(self.outer_circle_size * circle_progress)
        pygame.draw.circle(screen, BLUE, self.rect.center, outer_size, self.outer_circle_thickness)
        pygame.draw.circle(screen, YELLOW, self.rect.center, self.inner_circle_size, self.inner_circle_thickness)


# 기본 게임 루프
gun = Gun()
player = Player()
crosshair = Crosshair()
enemies = []
special_enemies = []
last_enemy_spawn_time = pygame.time.get_ticks()
last_special_enemy_spawn_time = pygame.time.get_ticks()
enemy_spawn_interval = 2000
special_enemy_spawn_interval = 10000

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gun.shoot():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for enemy in enemies[:]:
                    if enemy.rect.collidepoint(mouse_x, mouse_y):
                        enemies.remove(enemy)
                        player.update_score(10)
                for special_enemy in special_enemies[:]:
                    if special_enemy.rect.collidepoint(mouse_x, mouse_y):
                        special_enemies.remove(special_enemy)
                        player.update_score(50)

    # 화면 검은색으로 채우기
    screen.fill(BLACK)

    # 적 생성
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_interval:
        enemies.append(Enemy())
        last_enemy_spawn_time = current_time

    # 스페셜 적 생성
    if current_time - last_special_enemy_spawn_time > special_enemy_spawn_interval:
        special_enemies.append(SpecialEnemy())
        last_special_enemy_spawn_time = current_time

    # 적 업데이트 및 그리기
    for enemy in enemies[:]:
        if enemy.is_expired(current_time):
            enemies.remove(enemy)
        else:
            enemy.draw()

    # 스페셜 적 업데이트 및 그리기
    for special_enemy in special_enemies[:]:
        if special_enemy.is_expired(current_time):
            special_enemies.remove(special_enemy)
        else:
            special_enemy.draw()

    # 총기 동작
    gun.reload()
    gun.draw_bullets()

    # 플레이어 상태 표시
    player.draw()

    # 십자선 그리기
    mouse_pos = pygame.mouse.get_pos()
    crosshair.draw(mouse_pos)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

