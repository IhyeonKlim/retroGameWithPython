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
BLUE = (0, 0, 255)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# UI 설정
font = pygame.font.Font(None, 36)  # 텍스트 표시용 기본 폰트

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
        """총 발사"""
        if self.bullets > 0:
            self.bullets -= 1
            print("Shot fired!")
            return True
        else:
            print("Out of bullets!")
            return False

    def reload(self):
        """자동 장전"""
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
        self.font = pygame.font.Font(None, 36)

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
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.outer_circle_size = 100
        self.inner_circle_size = 50
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
special_enemies = []
hostages = []
last_enemy_spawn_time = pygame.time.get_ticks()
last_special_enemy_spawn_time = pygame.time.get_ticks()
last_hostage_spawn_time = pygame.time.get_ticks()
enemy_spawn_interval = 2000
special_enemy_spawn_interval = 10000
hostage_spawn_interval = 5000
hit_effect_time = None
hit_effect_duration = 300  # 피격 효과 지속 시간 (밀리초)

running = True
while running:
    current_time = pygame.time.get_ticks()
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
                # 인질 클릭 처리
                for hostage in hostages[:]:
                    if hostage.rect.collidepoint(mouse_x, mouse_y):
                        hostages.remove(hostage)
                        player.update_score(-50)
                        player.lose_life()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # 오른쪽 클릭
            gun.quick_reload()




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
            if enemy.attack_success(current_time):  # 동심원이 줄어들면 플레이어 생명 감소
                hit_effect_time = pygame.time.get_ticks()
                if not player.lose_life():
                    running = False
            enemies.remove(enemy)
        else:
            enemy.draw()

    # 스페셜 적 업데이트 및 그리기
    for special_enemy in special_enemies[:]:
        if special_enemy.is_expired(current_time):
            if special_enemy.attack_success(current_time):  # 동심원이 줄어들면 플레이어 생명 감소
                hit_effect_time = pygame.time.get_ticks()
                if not player.lose_life():
                    running = False
            special_enemies.remove(special_enemy)
        else:
            special_enemy.draw()

    # 피격 효과
    if hit_effect_time and current_time - hit_effect_time < hit_effect_duration:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # 투명도 설정
        overlay.fill(RED)
        screen.blit(overlay, (0, 0))

    # 인질 생성
    if current_time - last_hostage_spawn_time > hostage_spawn_interval:
        hostages.append(Hostage())
        last_hostage_spawn_time = current_time

    # 인질 업데이트 및 그리기
    for hostage in hostages[:]:
        if hostage.is_expired(current_time):
            hostages.remove(hostage)
        else:
            hostage.draw()

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

    # 플레이어 상태 표시
    player.draw()

    # 십자선 그리기
    mouse_pos = pygame.mouse.get_pos()
    crosshair.draw(mouse_pos)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

