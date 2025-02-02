import pygame
import random
import time
import os

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cop Shooting Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)         # Enemy 동심원의 큰 원 색상
YELLOW = (255, 255, 0)    # Enemy 동심원의 작은 원 색상
GREEN = (0, 255, 0)       # Hostage 색상
BLUE = (0, 0, 255)        # SpecialEnemy 큰 원 색상

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

class Gun:
    """플레이어의 총 관리 클래스"""
    def __init__(self):
        self.MAX_BULLETS = 7  # 최대 총알 수
        self.bullets = self.MAX_BULLETS  # 현재 총알 수
        self.reload_speed = 0.7  # 초당 장전 속도
        self.last_shot_time = time.time()  # 마지막 발사 시간
        self.last_reload_time = None  # 마지막 장전 시간
        self.reloading = False  # 자동 장전 여부
        self.last_quick_reload_time = 0  # 마지막 퀵 리로드 시간
        self.quick_reload_cooldown = 2.0  # 퀵 리로드 재사용 대기시간 (2초)

    def shoot(self):
        """총 발사"""
        if self.bullets > 0:
            self.bullets -= 1
            self.last_shot_time = time.time()
            if self.bullets > 0:
                self.reloading = False
                self.last_reload_time = None

    def reload(self):
        """자동 장전"""
        if self.bullets < self.MAX_BULLETS:
            current_time = time.time()
            if self.last_reload_time is None or current_time - self.last_reload_time >= self.reload_speed:
                self.bullets += 1
                self.last_reload_time = current_time
                if self.bullets == self.MAX_BULLETS:
                    self.reloading = False
                    self.last_reload_time = None

    def auto_reload(self):
        """자동 장전을 3초 간격으로 실행"""
        current_time = time.time()
        if self.bullets < self.MAX_BULLETS:
            if current_time - self.last_shot_time >= 3 and not self.reloading:
                self.reloading = True
                self.last_reload_time = current_time

    def draw_bullets(self):
        """총알 UI를 화면에 그리기"""
        bullet_width, bullet_height = 20, 10
        for i in range(self.bullets):
            x = WIDTH - (bullet_width + 5) * (i + 1)
            y = HEIGHT - bullet_height - 10
            pygame.draw.rect(screen, YELLOW, (x, y, bullet_width, bullet_height))

    def quick_reload(self):
        """퀵 리로드 (즉시 1발 장전, 2초 대기시간 적용)"""
        current_time = time.time()
        if current_time - self.last_quick_reload_time >= self.quick_reload_cooldown:  # 대기시간 체크
            if self.bullets < self.MAX_BULLETS:
                self.bullets += 1
                self.last_quick_reload_time = current_time

    def remaining_quick_reload_time(self):
        """퀵 리로드 남은 대기시간 계산"""
        current_time = time.time()
        remaining_time = self.quick_reload_cooldown - (current_time - self.last_quick_reload_time)
        return max(0, remaining_time)  # 음수가 되지 않도록 보장

class Enemy:
    """적 객체 관리"""
    def __init__(self):
        self.size = 100
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(100, 400 - self.size),
            self.size, self.size + 50) # 랜덤 위치 생성
        self.spawn_time = pygame.time.get_ticks()
        self.outer_size = max(WIDTH, HEIGHT) + 200 # 외부 동심원 크기
        self.inner_size = 50 # 내부 동심원 크기
        self.outer_circle_thickness = 20  # 큰 원 두께
        self.inner_circle_thickness = 4  # 작은 원 두께
        self.ATTACK_TIME = 3000 # 공격 완료 시간
        self.image = None
        self.circle_center =(self.rect.centerx, self.rect.centery-50)  # 동심원의 중심 좌표 (초기값: 사각형 중심)

        # Enemy 이미지를 로드
        image_path = "enemy.png"  # 이미지 파일 경로
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
            except pygame.error:
                print(f"Error loading image: '{image_path}'. Using default color.")
                self.image = None
        else:
            self.image = None  # 이미지가 없으면 None으로 설정
            print(f"Warning: '{image_path}' not found. Using default color.")

    def update(self, current_time):
        """동심원의 크기를 줄여 공격 완료 여부를 반환"""
        elapsed_time = current_time - self.spawn_time
        self.outer_size = max(WIDTH, HEIGHT) + 200 - (
                (max(WIDTH, HEIGHT) + 200 - self.inner_size) * (elapsed_time / self.ATTACK_TIME))
        return self.outer_size <= self.inner_size

    def draw(self):
        """적과 동심원을 화면에 그리기"""
        if self.image:
            # 이미지가 있으면 이미지를 그린다
            screen.blit(self.image, self.rect.topleft)
        else:
            # 이미지가 없으면 기본 빨간색 사각형
            pygame.draw.rect(screen, RED, self.rect)

        # 동심원
        pygame.draw.circle(screen, RED, self.circle_center, int(self.outer_size), self.outer_circle_thickness)  # 큰 원
        pygame.draw.circle(screen, YELLOW, self.circle_center, self.inner_size, self.inner_circle_thickness)  # 작은 원


class SpecialEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.ATTACK_TIME = 1500  # 동심원이 더 빠르게 줄어듭니다.
        self.outer_circle_thickness = 20
        self.inner_circle_thickness = 4

        # SpecialEnemy 이미지를 로드
        image_path = "special_enemy.png"  # 이미지 파일 경로
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None  # 이미지가 없으면 None으로 설정
            print(f"Warning: '{image_path}' not found. Using default color.")

    def draw(self):
        if self.image:
            # 이미지가 있으면 이미지를 그린다
            screen.blit(self.image, self.rect.topleft)
        else:
            # 이미지가 없으면 기본 파란색 사각형
            pygame.draw.rect(screen, BLUE, self.rect)

        pygame.draw.circle(screen, RED, self.circle_center, int(self.outer_size), self.outer_circle_thickness)  # 큰 원
        pygame.draw.circle(screen, YELLOW, self.circle_center, self.inner_size, self.inner_circle_thickness)  # 작은 원


class Hostage:
    HOSTAGE_LIFETIME = 3000  # 3초 유지
    TEXT_DURATION = 1000  # 텍스트 표시 지속 시간 (1초)

    def __init__(self):
        self.size = 100
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(100, 400 - self.size),
            self.size, self.size)
        self.spawn_time = pygame.time.get_ticks()
        self.hit_time = None  # 공격받은 시간
        self.text = "Hostage."  # 기본 텍스트
        self.text_color = GREEN  # 텍스트 색상
        self.hit = False  # 공격당했는지 여부
        self.removable = False  # 제거 가능 상태

        # Hostage 이미지 로드
        image_path = "hostage.png"
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
            except pygame.error:
                print(f"Error loading image: '{image_path}'. Using default color.")
                self.image = None
        else:
            self.image = None
            print(f"Warning: '{image_path}' not found. Using default color.")

    def update(self):
        """텍스트와 상태를 업데이트"""
        current_time = pygame.time.get_ticks()

        # 공격받지 않은 경우: 1초가 지나면 "Don't shoot me!"로 텍스트 변경
        if not self.hit and current_time - self.spawn_time > 500:
            self.text = "Don't shoot me!"
            self.text_color = GREEN

        # 공격받은 경우: 텍스트 표시 후 제거 가능 상태로 변경
        if self.hit and current_time - self.hit_time > self.TEXT_DURATION:
            self.removable = True

        # 지속 시간이 초과되면 제거 가능 상태로 변경
        if not self.hit and current_time - self.spawn_time > self.HOSTAGE_LIFETIME:
            self.removable = True

    def register_hit(self):
        """Hostage가 공격받았을 때 텍스트와 상태를 설정"""
        self.text = "life -1"
        self.text_color = RED
        self.hit_time = pygame.time.get_ticks()
        self.hit = True

    def draw(self):
        """Hostage와 텍스트를 화면에 표시"""
        # Hostage 이미지 또는 기본 초록색 사각형 표시
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, GREEN, self.rect)

        # 텍스트 표시
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 60))
        screen.blit(text_surface, text_rect)




class Player:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font(None, 36)

    def update_score(self, amount):
        self.score += amount

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            print(f"Game Over! Final Score: {self.score}")
            return False
        return True

    def draw(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))


class Crosshair:
    def __init__(self):
        self.color = GREEN

    def draw(self, position):
        pygame.draw.line(screen, self.color, (position[0] - 20, position[1]), (position[0] + 20, position[1]), 2)
        pygame.draw.line(screen, self.color, (position[0], position[1] - 20), (position[0], position[1] + 20), 2)


class Game:
    """게임의 메인 클래스"""
    def __init__(self):
        # 초기화 단계에서 필요한 변수들 선언
        self.gun = Gun()  # 총기 객체 생성
        self.player = Player()  # 플레이어 객체 생성
        self.crosshair = Crosshair()  # 십자선 객체 생성
        self.font = pygame.font.Font(None, 74)  # 텍스트 폰트 설정
        self.enemies = []  # 적 리스트
        self.hostages = []  # 인질 리스트
        self.last_spawn_time = pygame.time.get_ticks()  # 마지막 적 생성 시간
        self.enemy_spawn_interval = 4000  # 적 생성 간격 (밀리초)
        self.minimum_enemy_spawn_interval = 1000  # 최소 적 생성 간격
        self.special_enemy_spawn_interval = 10000  # 스페셜 적 생성 간격
        self.hostage_spawn_interval = 5000  # 인질 생성 간격
        self.last_special_enemy_spawn_time = pygame.time.get_ticks()  # 마지막 스페셜 적 생성 시간
        self.spawn_reduction_rate = 1  # 난이도 증가율
        self.last_hostage_spawn_time = pygame.time.get_ticks()  # 마지막 인질 생성 시간
        self.running = True  # 게임 실행 여부
        self.hit_effect_time = None  # 피격 효과 시작 시간
        self.hit_duration = 300  # 빨간 화면 지속 시간 (밀리초)
        self.hit_image = pygame.image.load("hit_effect.png")  # 피격 이미지
        self.hit_image = pygame.transform.scale(self.hit_image, (800, 600))  # 크기 조정
        self.state = "intro"  # 게임 상태, 기본값: intro

        # 배경 이미지 로드
        image_path = "background.png"
        if os.path.exists(image_path):
            try:
                self.background_image = pygame.image.load(image_path)
                self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
            except pygame.error:
                print(f"Error loading image: '{image_path}'. Using default black background.")
                self.background_image = None
        else:
            self.background_image = None
            print(f"Warning: '{image_path}' not found. Using default black background.")

    def draw_background(self):
        """게임 상태에 따라 배경을 그립니다."""
        if self.state == "playing" and self.background_image:
            screen.blit(self.background_image, (0, 0))  # 배경 이미지 그리기
        else:
            screen.fill(BLACK)  # 기본 검은색 배경

    def spawn_enemy(self):
        self.enemies.append(Enemy())

    def spawn_special_enemy(self):
        self.enemies.append(SpecialEnemy())

    def spawn_hostage(self):
        """새로운 Hostage 생성"""
        new_hostage = Hostage()
        self.hostages.append(new_hostage)

    def update_hostages(self):
        """Hostage 상태를 업데이트하고 만료된 Hostage 제거"""
        current_time = pygame.time.get_ticks()

        # Hostage 생성
        if current_time - self.last_hostage_spawn_time > self.hostage_spawn_interval:
            self.spawn_hostage()
            self.last_hostage_spawn_time = current_time

        # Hostage 상태 업데이트 및 제거
        for hostage in self.hostages[:]:
            hostage.update()
            if hostage.removable:  # 제거 가능 상태 확인
                self.hostages.remove(hostage)

    def handle_shooting(self):
        if self.gun.bullets > 0:
            self.gun.shoot()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for enemy in self.enemies[:]:
                if enemy.rect.collidepoint(mouse_x, mouse_y):
                    self.enemies.remove(enemy)
                    self.player.update_score(10)
            for hostage in self.hostages:
                if hostage.rect.collidepoint(mouse_x, mouse_y):
                    hostage.register_hit()  # 상태를 변경 (즉시 제거하지 않음)
                    self.player.update_score(-100)
                    self.player.lose_life()

    def update_enemy_spawn_interval(self):
        """적 생성 간격을 감소시키고, 최소 간격을 유지"""
        if self.enemy_spawn_interval > self.minimum_enemy_spawn_interval:
            self.enemy_spawn_interval -= self.spawn_reduction_rate

    def reset_enemy_spawn_interval(self):
        """life가 감소하면 적 생성 간격을 초기화"""
        self.enemy_spawn_interval = 4000

    def draw_text_with_outline(self, text, position):
        """텍스트를 테두리와 함께 화면에 표시"""
        outline_surface = self.font.render(text, True, BLACK)
        text_surface = self.font.render(text, True, YELLOW)
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(outline_surface, (position[0] + dx, position[1] + dy))
        screen.blit(text_surface, position)

    def draw_quick_reload_cooldown(self):
        """퀵 리로드 남은 대기시간을 생명 아래에 표시"""
        remaining_time = self.gun.remaining_quick_reload_time()
        cooldown_text = self.font.render(f"Quick Reload: {remaining_time:.1f}s", True, WHITE)
        screen.blit(cooldown_text, (10, 550))  # 생명 아래 위치

    def draw_quick_reload_text(self):
        """퀵 리로드 텍스트를 화면 중앙에 표시"""
        if self.gun.remaining_quick_reload_time() > 0:  # 대기 중일 때만 표시
            quick_reload_text = self.font.render("Quick Reload", True, YELLOW)
            quick_reload_rect = quick_reload_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(quick_reload_text, quick_reload_rect)

    def update_enemies(self):
        """적의 상태를 업데이트하고 공격 성공 시 피격 효과를 트리거."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = current_time

        if current_time - self.last_special_enemy_spawn_time > self.special_enemy_spawn_interval:
            self.spawn_special_enemy()
            self.last_special_enemy_spawn_time = current_time

        for enemy in self.enemies[:]:
            if enemy.update(current_time):
                # 동심원의 중심을 적의 사각형 중심으로 동기화
                self.enemies.remove(enemy)
                if not self.player.lose_life():
                    self.state = "game_over"
                else:
                    self.hit_effect_time = current_time  # 피격 효과 트리거
                    self.reset_enemy_spawn_interval()  # life가 감소하면 생성 간격 초기화

    def draw_reload_text(self):
        """장전 중일 때 화면에 텍스트 표시"""
        if self.gun.bullets == 0 or self.gun.reloading:
            # 텍스트 렌더링
            text_surface = self.font.render("Reload", True, YELLOW)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 화면의 정중앙에 배치

            # 테두리가 있는 텍스트 표시
            self.draw_text_with_outline("Reload", (text_rect.x, text_rect.y))

    def display_hit_effect(self):
        """피격 효과를 화면에 표시."""
        current_time = pygame.time.get_ticks()
        if self.hit_effect_time and current_time - self.hit_effect_time < self.hit_duration:
            # 빨간 화면 덮기
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)  # 투명도 설정
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))

            # 화면 중앙에 피격 이미지 표시
            image_rect = self.hit_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(self.hit_image, image_rect)
        else:
            self.hit_effect_time = None  # 효과 종료

    def show_intro(self):
        """인트로 화면 표시"""
        self.draw_background()
        intro_text = self.font.render("Left-click to start", True, WHITE)
        intro_rect = intro_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(intro_text, intro_rect)
        pygame.display.flip()

    def show_game_over(self):
        """게임 오버 화면 표시"""
        self.draw_background()
        game_over_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def reset_game(self):
        """게임 상태 초기화"""
        self.gun = Gun()
        self.player = Player()
        self.enemies = []
        self.hostages = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.last_hostage_spawn_time = pygame.time.get_ticks()
        self.state = "playing"

    def run(self):
        """게임 메인 루프"""
        while self.running:
            self.draw_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "game_over" and event.key == pygame.K_r:
                        self.reset_game()  # 게임 재시작
                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "intro":
                    if event.button == 1:  # 왼쪽 버튼
                        self.reset_game()  # 게임 시작
                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "playing":
                    if event.button == 1:  # 왼쪽 버튼
                        self.handle_shooting()
                    elif event.button == 3:  # 오른쪽 버튼
                        self.gun.quick_reload()  # 수동 장전
                #elif event.type == pygame.MOUSEMOTION:
                    # 마우스 이동 좌표 출력
                    #print(f"Mouse moved to: {event.pos}")

            if self.state == "intro":
                self.show_intro()
            elif self.state == "playing":
                self.draw_background()
                self.update_enemies()
                self.update_hostages()
                self.gun.auto_reload()
                self.draw_quick_reload_cooldown()  # 퀵 리로드 대기시간 표시
                if self.gun.reloading:
                    self.gun.reload()

                # Reload 텍스트 및 퀵 리로드 텍스트 표시
                self.draw_reload_text()
                self.draw_quick_reload_text()

                # 그리기
                self.player.draw()
                self.gun.draw_bullets()
                mouse_pos = pygame.mouse.get_pos()

                # 적 표시
                for enemy in self.enemies:
                    enemy.draw()
                # 인질 표시
                for hostage in self.hostages:
                    hostage.draw()

                # Reload 텍스트 및 십자가 커서 그리기 (상단 우선 순서)
                self.draw_reload_text()
                self.crosshair.draw(mouse_pos)

                # 피격 효과 표시
                self.display_hit_effect()
                pygame.display.flip()

                # 난이도 증가 및 생명 체크
                self.update_enemy_spawn_interval()
                if self.player.lives <= 0 :
                    self.state ="game_over"  # 게임 오버 상태로 변경

            elif self.state == "game_over":
                self.show_game_over() # 게임 오버 화면 표시


            clock.tick(FPS)



if __name__ == "__main__":
    Game().run()