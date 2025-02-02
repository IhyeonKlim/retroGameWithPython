import pygame
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
            self.bullets -= 1
            print("Shot fired!")
        else:
            print("Out of bullets!")

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


# 기본 게임 루프
gun = Gun()
player = Player()
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

    # 총기 동작
    gun.reload()
    gun.draw_bullets()

    # 플레이어 상태 표시
    player.draw()

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

