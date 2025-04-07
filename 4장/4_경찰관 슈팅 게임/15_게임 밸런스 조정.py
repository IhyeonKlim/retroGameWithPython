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
        self.reload_speed = 1  #  장전 속도 증가 (fullReloading 시 0.5)
        self.last_reload_time = None
        self.quick_reload_cooldown = 1.5  #  퀵 리로드 대기시간 감소 (2.0 → 1.5)
        self.last_quick_reload_time = time.time()
        self.last_shot_time = time.time()
        self.isFullReloading = False

    def shoot(self):
        if self.bullets > 0 and not self.isFullReloading:
            self.bullets -= 1
            self.last_shot_time = time.time()
            return True
        else:
            return False

    def reload(self):
        """자동 장전"""
        if self.bullets < self.MAX_BULLETS:
            current_time = time.time()
            if self.last_reload_time is None or current_time - self.last_reload_time >= self.reload_speed:
                self.bullets += 1
                self.last_reload_time = current_time
            if self.bullets == 0:
                self.isFullReloading = True
                self.reload_speed = 0.5
        if self.bullets == self.MAX_BULLETS:
            self.isFullReloading = False
            self.reload_speed = 1
        if self.isFullReloading and self.bullets == self.MAX_BULLETS:
            self.isFullReloading = False

    def quick_reload(self):
        """ 퀵 리로드 변경: 1초마다 1발 장전, 1.5초 대기"""
        current_time = time.time()
        if current_time - self.last_quick_reload_time >= self.quick_reload_cooldown:
            if self.bullets < self.MAX_BULLETS:
                self.bullets += 1
                self.last_quick_reload_time = current_time
                print("Quick Reload!")

    def remaining_quick_reload_time(self):
        """ 퀵 리로드 남은 대기 시간 반환 (소수점 1자리)"""
        current_time = time.time()
        remaining_time = self.quick_reload_cooldown - (current_time - self.last_quick_reload_time)
        return max(0, remaining_time)

    def draw_bullets(self):
        """ 총알 UI 위치 조정 (더 아래로 이동)"""
        bullet_width, bullet_height = 20, 10
        for i in range(self.bullets):
            x = WIDTH - (bullet_width + 5) * (i + 1)
            y = HEIGHT - bullet_height - 20  #  위치 변경 (기존보다 10px 아래)
            pygame.draw.rect(screen, YELLOW, (x, y, bullet_width, bullet_height))


class Player:
    """ 플레이어 상태 변경: 점수 시스템 및 생명 시스템 조정"""
    def __init__(self):
        self.score = 0
        self.lives = 5  #  생명 증가 (3 → 5)
        self.font = pygame.font.Font(None, 36)

    def update_score(self, amount):
        """점수 증가"""
        self.score += amount

    def lose_life(self):
        """생명 감소"""
        self.lives -= 1
        if self.lives <= 0:
            print(f"Game Over! Final Score: {self.score}")
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
    """ 적 객체 변경: 공격 완료 시간 및 크기 변경"""
    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(50, HEIGHT // 2 - self.size),
            self.size, self.size
        )
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000  #  적의 최대 생존 시간 (5초) 추가
        self.ATTACK_TIME = 2500  #  공격 완료 시간 변경 (3000 → 2500)
        self.outer_circle_size = 90  #  외곽 동심원 크기 조정 (100 → 90)
        self.inner_circle_size = 45  #  내부 동심원 크기 조정 (50 → 45)
        self.outer_circle_thickness = 4
        self.inner_circle_thickness = 2

    def is_expired(self, current_time):
        """ 제거 조건 변경: 더 빠르게 제거됨"""
        return current_time - self.spawn_time > self.ATTACK_TIME

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
        self.lifetime = 1500
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
    TEXT_DURATION = 1000  # 텍스트 표시 지속 시간 (1초)

    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size), random.randint(50, HEIGHT // 2 - self.size),
            self.size, self.size
        )
        self.spawn_time = pygame.time.get_ticks()
        self.hit_time = None  # 공격받은 시간
        self.text = "Don't shoot me!"  # 기본 텍스트
        self.text_color = GREEN  # 텍스트 색상
        self.hit = False  # 공격받았는지 여부

    def is_expired(self, current_time):
        """인질 유지 시간이 지나면 제거"""
        return current_time - self.spawn_time > self.HOSTAGE_LIFETIME

    def draw(self):
        """인질과 텍스트를 화면에 그리기"""
        pygame.draw.rect(screen, GREEN, self.rect)

        # 텍스트 표시
        current_time = pygame.time.get_ticks()
        if not self.hit and current_time - self.spawn_time > 500:
            # 처음 0.5초 이후 텍스트 표시
            self.text = "Don't shoot me!"
            self.text_color = GREEN
        elif self.hit:
            # 공격받은 경우, 일정 시간 후 텍스트 제거
            self.text = "Noooooo!!!!"
            self.text_color = RED

        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 30))
        screen.blit(text_surface, text_rect)

class Game:
    """게임 관리 클래스"""
    def __init__(self):
        self.gun = Gun()
        self.player = Player()
        self.crosshair = Crosshair()
        self.enemies = []
        self.special_enemies = []
        self.hostages = []

        # 적/인질 스폰 타이머
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.last_special_enemy_spawn_time = pygame.time.get_ticks()
        self.last_hostage_spawn_time = pygame.time.get_ticks()

        # 스폰 간격 설정
        self.enemy_spawn_interval = 3000  #  적 생성 간격 증가 (2000 → 3000)
        self.hostage_spawn_interval = 4500  #  인질 생성 간격 감소 (5000 → 4500)
        self.special_enemy_spawn_interval = 9000  #  스페셜 적 생성 간격 감소 (10000 → 9000)

        # 피격 효과
        self.hit_effect_time = None
        self.hit_effect_duration = 300  # 300ms 지속

        self.running = True  # 게임 실행 여부
        self.state = "intro"  # 초기 상태를 'intro'로 설정

    def spawn_enemy(self):
        """일반 적 생성"""
        self.enemies.append(Enemy())

    def spawn_special_enemy(self):
        """스페셜 적 생성"""
        self.special_enemies.append(SpecialEnemy())

    def spawn_hostage(self):
        """인질 생성"""
        self.hostages.append(Hostage())

    def handle_shooting(self, mouse_x, mouse_y):
        """총을 쐈을 때의 처리"""
        if self.gun.shoot():
            for enemy in self.enemies[:]:
                if enemy.rect.collidepoint(mouse_x, mouse_y):
                    self.enemies.remove(enemy)
                    self.player.update_score(10)
                    if self.enemy_spawn_interval >= 2000:
                        self.enemy_spawn_interval = self.enemy_spawn_interval - 300
            for special_enemy in self.special_enemies[:]:
                if special_enemy.rect.collidepoint(mouse_x, mouse_y):
                    self.special_enemies.remove(special_enemy)
                    self.player.update_score(50)
                    if self.special_enemy_spawn_interval >= 3000:
                        self.special_enemy_spawn_interval = self.special_enemy_spawn_interval - 500
            for hostage in self.hostages[:]:
                if hostage.rect.collidepoint(mouse_x, mouse_y):
                    hostage.hit = True
                    self.player.update_score(-50)
                    self.player.lose_life()


    def update_objects(self):
        """게임 오브젝트 업데이트"""
        current_time = pygame.time.get_ticks()

        # 총알 관리
        self.gun.reload()

        # 적 스폰 관리
        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time
        if current_time - self.last_special_enemy_spawn_time > self.special_enemy_spawn_interval:
            self.spawn_special_enemy()
            self.last_special_enemy_spawn_time = current_time

        # 적 제거
        for enemy in self.enemies[:]:
            if enemy.is_expired(current_time):
                if self.player.lose_life():
                    self.hit_effect_time = pygame.time.get_ticks()
                self.enemies.remove(enemy)

        # 스페셜 적 제거
        for special_enemy in self.special_enemies[:]:
            if special_enemy.is_expired(current_time):
                if self.player.lose_life():
                    self.hit_effect_time = pygame.time.get_ticks()
                self.special_enemies.remove(special_enemy)

        # 인질 제거
        for hostage in self.hostages[:]:
            if hostage.is_expired(current_time):
                self.hostages.remove(hostage)

        # 인질 스폰 관리
        if current_time - self.last_hostage_spawn_time > self.hostage_spawn_interval:
            self.spawn_hostage()
            self.last_hostage_spawn_time = current_time

        # 게임오버 여부 확인
        self.check_game_over()


    def draw_objects(self):
        """화면에 모든 오브젝트를 그림"""
        screen.fill(BLACK)

        for enemy in self.enemies:
            enemy.draw()
        for special_enemy in self.special_enemies:
            special_enemy.draw()
        for hostage in self.hostages:
            hostage.draw()

        self.gun.draw_bullets()
        self.player.draw()

        # 십자선 그리기
        mouse_pos = pygame.mouse.get_pos()
        self.crosshair.draw(mouse_pos)

        # "Reload" 텍스트 표시
        if self.gun.bullets == 0 or self.gun.isFullReloading:
            font = pygame.font.Font(None, 42)
            reload_text = font.render("Reloading(can not shoot)", True, YELLOW)
            reload_rect = reload_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(reload_text, reload_rect)
            self.gun.reload()

        # 퀵 리로드 대기 시간 표시
        quick_reload_time = self.gun.remaining_quick_reload_time()
        font = pygame.font.Font(None, 36)
        quick_reload_text = font.render(f"Quick Reload: {quick_reload_time:.1f}s", True, WHITE)
        screen.blit(quick_reload_text, (10, HEIGHT - 40))

        # 피격 효과
        if self.hit_effect_time and pygame.time.get_ticks() - self.hit_effect_time < self.hit_effect_duration:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()  # 화면 업데이트

    def show_intro(self):
        """인트로 화면 표시"""
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("Click to Start", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

    def show_game_over(self):
        """게임 오버 화면 표시"""
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def check_game_over(self):
        """플레이어의 생명이 0이 되면 게임 오버 상태로 전환"""
        if self.player.lives == 0:
            self.hit_effect_time = pygame.time.get_ticks()
            self.state = "game_over"
        if self.player.lives <= 3: # 라이프가 3까지 감소시 적 스폰 시간 증가
            self.enemy_spawn_interval = 2500
            self.special_enemy_spawn_interval = 7000

    def reset_game(self):
        """게임 상태 초기화"""
        self.__init__()  # 게임을 처음 상태로 리셋
        self.state = "playing"  # 바로 게임 시작

    def run(self):
        """게임 루프 실행"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "intro":
                        self.state = "playing"
                        screen.fill(BLACK)  # 화면 초기화
                        pygame.display.flip()  # 인트로 텍스트 제거
                    elif self.state == "playing":
                        if event.button == 1:  # 왼쪽 클릭
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            self.handle_shooting(mouse_x, mouse_y)
                        elif event.button == 3:  # 오른쪽 클릭 (퀵 리로드)
                            self.gun.quick_reload()

                elif event.type == pygame.KEYDOWN and self.state == "game_over":
                    if event.key == pygame.K_r:  # 'R' 키를 누르면 게임 재시작
                        self.reset_game()

            if self.state == "intro":
                self.show_intro()
            elif self.state == "playing":
                self.update_objects()
                self.draw_objects()
            elif self.state == "game_over":
                self.show_game_over()

            clock.tick(FPS)

# 게임 실행
if __name__ == "__main__":
    Game().run()