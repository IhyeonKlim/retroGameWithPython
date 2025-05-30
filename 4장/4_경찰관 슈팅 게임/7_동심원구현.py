import pygame
import time
import random

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

# FPS 설정
FPS = 60
clock = pygame.time.Clock()


class Gun:
    """플레이어의 총 관리 클래스"""
    def __init__(self):
        self.MAX_BULLETS = 7  # 최대 총알 수
        self.bullets = self.MAX_BULLETS  # 현재 총알 수
        self.reload_speed = 0.7  # 초당 장전 속도
        self.last_reload_time = None  # 마지막 장전 시간

    def shoot(self):
        """총 발사"""
        if self.bullets > 0:
            self.bullets -= 1  # 총알 수 감소
            print("Shot fired!")  # 발사 확인 메시지
        else:
            print("Out of bullets!")  # 총알 부족 메시지

    def reload(self):
        """자동 장전"""
        if self.bullets < self.MAX_BULLETS:
            current_time = time.time()
            if self.last_reload_time is None or current_time - self.last_reload_time >= self.reload_speed:
                self.bullets += 1
                self.last_reload_time = current_time

    def draw_bullets(self):
        """총알 UI를 화면에 그리기"""
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
        self.font = pygame.font.Font(None, 36)  # 기본 폰트 크기 36

    def update_score(self, amount):
        """점수 증가"""
        self.score += amount

    def lose_life(self):
        """생명 감소"""
        self.lives -= 1
        if self.lives <= 0:
            print("Game Over!")
            return False
        return True

    def draw(self):
        """화면에 점수와 생명 표시"""
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
        self.spawn_time = pygame.time.get_ticks()  # 적이 생성된 시간
        self.lifetime = 3000  # 적이 유지되는 시간 (밀리초)
        self.outer_circle_size = 100  # 동심원의 초기 크기
        self.inner_circle_size = 50  # 동심원의 최소 크기
        self.outer_circle_thickness = 4
        self.inner_circle_thickness = 2

    def is_expired(self, current_time):
        """적이 일정 시간이 지나면 사라지도록 설정"""
        return current_time - self.spawn_time > self.lifetime

    def attack_success(self, current_time):
        """동심원이 완전히 줄어들면 공격 성공"""
        elapsed_time = current_time - self.spawn_time
        return elapsed_time >= self.lifetime

    def draw(self):
        """적과 동심원을 화면에 그리기"""
        pygame.draw.rect(screen, RED, self.rect)

        # 동심원의 크기 업데이트
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time
        circle_progress = max(0, 1 - elapsed_time / self.lifetime)
        outer_size = int(self.outer_circle_size * circle_progress)

        # 동심원 그리기
        pygame.draw.circle(screen, RED, self.rect.center, outer_size, self.outer_circle_thickness)
        pygame.draw.circle(screen, YELLOW, self.rect.center, self.inner_circle_size, self.inner_circle_thickness)


class Hostage:
    """인질 객체 관리 클래스"""
    HOSTAGE_LIFETIME = 3000

    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(50, HEIGHT // 2 - self.size),
            self.size, self.size
        )
        self.spawn_time = pygame.time.get_ticks()  # 생성 시간
        self.text = "Hostage"  # 기본 텍스트

    def is_expired(self, current_time):
        """인질 유지 시간이 지나면 제거"""
        return current_time - self.spawn_time > self.HOSTAGE_LIFETIME

    def draw(self):
        """인질과 텍스트를 화면에 그리기"""
        pygame.draw.rect(screen, GREEN, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


# 기본 게임 루프
gun = Gun()
player = Player()
crosshair = Crosshair()
enemies = []
hostages = []
last_enemy_spawn_time = pygame.time.get_ticks()
last_hostage_spawn_time = pygame.time.get_ticks()
enemy_spawn_interval = 2000
hostage_spawn_interval = 5000

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임 종료 이벤트
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 왼쪽 클릭
            gun.shoot()
            player.update_score(10)  # 클릭 시 점수 증가

    # 화면 검은색으로 채우기
    screen.fill(BLACK)

    # 적 생성
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_interval:
        enemies.append(Enemy())
        last_enemy_spawn_time = current_time

    # 인질 생성
    if current_time - last_hostage_spawn_time > hostage_spawn_interval:
        hostages.append(Hostage())
        last_hostage_spawn_time = current_time

    # 적 업데이트 및 그리기
    for enemy in enemies[:]:
        if enemy.is_expired(current_time):
            if enemy.attack_success(current_time):  # 동심원이 줄어들면 플레이어 생명 감소
                if not player.lose_life():
                    running = False
            enemies.remove(enemy)
        else:
            enemy.draw()

    # 인질 업데이트 및 그리기
    for hostage in hostages[:]:
        if hostage.is_expired(current_time):
            hostages.remove(hostage)
        else:
            hostage.draw()

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

