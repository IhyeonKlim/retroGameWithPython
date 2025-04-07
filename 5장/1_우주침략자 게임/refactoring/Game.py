import pygame
import Config
import Unit
import Bullet
import sys
import random

from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_SPACE

# 게임 전체 로직을 관리하는 Game 클래스
class Game:
    def __init__(self):
        pygame.init()  # Pygame 시스템 초기화

        # 게임 화면 생성
        self.screen = pygame.display.set_mode(
            (Config.SCREEN_SIZE['width'], Config.SCREEN_SIZE['height'])
        )
        pygame.display.set_caption("우주 침략자 게임")  # 윈도우 타이틀 설정

        self.clock = pygame.time.Clock()  # 프레임 제한용 Clock 객체
        self.time = 0                     # 전체 게임 시간 (프레임 단위)
        self.score = 0                    # 플레이어 점수
        self.life = Config.LIFE           # 플레이어 생명 수
        self.is_move_right_enemy = 1      # 적 이동 방향 (1 = 오른쪽, -1 = 왼쪽)

        # 플레이어 생성 (중앙 하단 위치)
        self.player = Unit.Player(
            Config.SCREEN_SIZE['width'] // 2,
            Config.SCREEN_SIZE['height'] - 50,
            Config.WHITE
        )

        # 플레이어 총알 풀 생성 (최대 개수만큼 미리 생성)
        self.player_bullets = [Bullet.Bullet(self.player.color) for _ in range(Config.USER_BULLTES)]
        self.fired_player_bullets = []  # 현재 화면에 떠 있는 플레이어 총알

        # 적 총알 풀 및 발사된 총알
        self.enemy_bullets = [Bullet.Bullet(Config.YELLOW) for _ in range(Config.ENEMY_BULLETS)]
        self.fired_enemy_bullets = []

        # 적 유닛 생성 (2D 배열 형태)
        self.enemies = self.create_enemies()

        # 방어 벽 생성 (총 4개, 일정 간격으로 배치)
        self.walls = [
            Unit.Wall(155 + i * 110, self.screen.get_height() - 70, Config.RED)
            for i in range(4)
        ]

        # UFO 생성 (상단 가로 이동형 적)
        self.ufo = Unit.Ufo(0, 50, Config.WHITE)
        self.ufo.enable = False  # 기본 비활성화 상태

    # 적 유닛을 2차원 배열 형태로 생성
    def create_enemies(self):
        enemies = []
        margin_x = (self.screen.get_width() - (40 * Config.ENEMY_NUMBERS)) / 2  # 가운데 정렬 마진
        for y in range(Config.ENEMY_COLS):  # 줄 수만큼 반복
            row = []
            color = Config.GREEN if y <= 0 else Config.BLUE if y < 2 else Config.YELLOW if y < 5 else Config.RED
            for x in range(Config.ENEMY_NUMBERS):
                row.append(Unit.Enemy(margin_x + x * 40, 100 + y * 25, color))
            enemies.append(row)
        return enemies

    # 유닛(적, 플레이어, UFO) 출력
    def draw_unit(self, unit):
        if not unit.character:
            print(f"[WARN] character 정보 없음: {unit}")
            return

        unit = unit.get_draw_data()
        for y, row in enumerate(unit.character[unit.frame_index]):
            ry = unit.rect.y + y
            for x, val in enumerate(row):
                if val:
                    rx = unit.rect.x + x
                    pygame.draw.circle(self.screen, unit.color, [rx, ry], 1)

    # 방어벽 출력
    def draw_wall(self, wall):
        for y, line in enumerate(wall.body):
            ry = wall.rect.y + (y * 5)
            for x, pt in enumerate(line):
                if pt:
                    rx = wall.rect.x + (x * 5)
                    pygame.draw.rect(self.screen, wall.color, [rx, ry, 5, 5])

    # 충돌 처리: 총알과 적/벽/UFO/플레이어 간의 상호작용
    def handle_collisions(self):
        # 플레이어 총알 ↔ 적
        for bullet in list(self.fired_player_bullets):
            for row in self.enemies:
                for enemy in row:
                    if enemy.enable and bullet.rect.colliderect(enemy.rect):
                        enemy.enable = False
                        bullet.enabled = False
                        self.score += 100
            if not bullet.enabled:
                self.fired_player_bullets.remove(bullet)
                self.player_bullets.append(bullet)

        # 플레이어 총알 ↔ 벽
        for bullet in list(self.fired_player_bullets):
            for wall in self.walls:
                if wall.colliderect(bullet):
                    bullet.enabled = False
            if not bullet.enabled:
                self.fired_player_bullets.remove(bullet)
                self.player_bullets.append(bullet)

        # 플레이어 총알 ↔ UFO
        for bullet in list(self.fired_player_bullets):
            if self.ufo.enable and bullet.rect.colliderect(self.ufo.rect):
                self.ufo.enable = False
                bullet.enabled = False
                self.score += 1000
            if not bullet.enabled:
                self.fired_player_bullets.remove(bullet)
                self.player_bullets.append(bullet)

        # 적 총알 ↔ 벽 / 플레이어
        for bullet in list(self.fired_enemy_bullets):
            for wall in self.walls:
                if wall.colliderect(bullet):
                    bullet.enabled = False
            if bullet.enabled and self.player.rect.colliderect(bullet.rect):
                bullet.enabled = False
                self.life -= 1

            if not bullet.enabled:
                self.fired_enemy_bullets.remove(bullet)
                self.enemy_bullets.append(Bullet.Bullet(Config.YELLOW))

    # 키보드 입력 처리
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.player.move_left()
        if keys[K_RIGHT]:
            self.player.move_right()
        if keys[K_SPACE]:
            self.fire_bullet()

    # 적 이동 및 발사 로직 처리
    def update_enemies(self):
        is_change_direction = False
        for row in self.enemies:
            for enemy in row:
                if not enemy.enable:
                    continue

                if self.time % enemy.delay == 0:
                    if self.is_move_right_enemy > 0:
                        enemy.move_right()
                    else:
                        enemy.move_left()

                self.draw_unit(enemy)

                # 일정 확률로 총알 발사
                if random.randint(0, 999) < int(self.time / 1000):
                    enemy.fire(self.enemy_bullets, self.fired_enemy_bullets)

        # 경계 충돌 시 방향 전환 감지
        for row in self.enemies:
            for enemy in row:
                if (self.is_move_right_enemy > 0 and enemy.rect.right >= self.screen.get_width()) or \
                        (self.is_move_right_enemy <= 0 and enemy.rect.left <= 0):
                    self.is_move_right_enemy *= -1
                    is_change_direction = True
                    break
            if is_change_direction:
                break

        # 방향 전환 시 아래로 한 칸 이동 + 이동 속도 증가
        if is_change_direction:
            for row in self.enemies:
                for enemy in row:
                    enemy.delay = max(4, enemy.delay - 1)
                    enemy.move_down()

    # 적 총알 이동 및 화면 갱신
    def update_enemy_bullets(self):
        for bullet in list(self.fired_enemy_bullets):
            bullet.move_down(self.screen.get_height())
            if not bullet.enabled:
                self.fired_enemy_bullets.remove(bullet)
                self.enemy_bullets.append(Bullet.Bullet(Config.YELLOW))
                continue
            bullet.draw(self.screen)

    # 플레이어가 총알을 발사할 때 사용
    def fire_bullet(self):
        if self.player.enable and self.player_bullets:
            bullet = self.player_bullets.pop(0)
            if bullet.fire(self.player.rect.centerx, self.player.rect.top):
                self.fired_player_bullets.append(bullet)

    # 플레이어 총알 이동 및 그리기
    def update_player_bullets(self):
        for bullet in list(self.fired_player_bullets):
            bullet.move_up()
            if not bullet.enabled:
                self.fired_player_bullets.remove(bullet)
                self.player_bullets.append(bullet)
                continue
            bullet.draw(self.screen)

    # UFO 등장 및 이동 처리
    def update_ufo(self):
        if random.randint(0, 9) < 1 and not self.ufo.enable:
            self.ufo.enable = True
            self.ufo.rect.x = 0

        if self.ufo.enable:
            if self.ufo.rect.x + self.ufo.rect.width < self.screen.get_width():
                if self.time % self.ufo.delay == 0:
                    self.ufo.move_right()
                self.draw_unit(self.ufo)
            else:
                self.ufo.enable = False

    # 방어벽 출력
    def draw_walls(self):
        for wall in self.walls:
            self.draw_wall(wall)

    # 적이 모두 제거되었는지 확인
    def check_victory(self):
        for row in self.enemies:
            for enemy in row:
                if enemy.enable:
                    return False
        return True

    # 점수, 라이프, 게임 오버/승리 화면 출력
    def draw_ui(self):
        font = pygame.font.Font(None, 20)
        score_text = font.render(str(self.score), True, Config.WHITE)
        self.screen.blit(score_text, (10, 10))

        for i in range(self.life):
            pygame.draw.circle(
                self.screen, Config.RED,
                [self.screen.get_width() - (i * 10) - 15, 20],
                5
            )

        if self.life <= 0:
            self.player.enable = False
            font = pygame.font.Font(None, 40)
            text = font.render('GAME OVER', True, Config.RED)
            rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(text, rect)

        elif self.check_victory():
            self.player.enable = False
            font = pygame.font.Font(None, 40)
            text = font.render('YOU WIN!', True, Config.GREEN)
            rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(text, rect)

    # 매 프레임마다 게임 상태 갱신
    def update(self):
        self.handle_input()              # 입력 처리
        self.screen.fill(Config.BLACK)  # 배경 초기화

        if self.player.enable:
            self.draw_unit(self.player) # 플레이어 그리기

        self.draw_walls()               # 벽 그리기
        self.update_enemies()          # 적 움직임
        self.update_enemy_bullets()    # 적 총알 이동
        self.update_player_bullets()   # 플레이어 총알 이동
        self.update_ufo()              # UFO 움직임
        self.draw_ui()                 # UI 렌더링

        self.handle_collisions()       # 충돌 처리

        pygame.display.update()        # 화면 업데이트
        self.clock.tick(Config.FPS)    # FPS 유지
        self.time += 1                 # 게임 시간 누적

    # 게임 루프 실행
    def run(self):
        while True:
            self.update()
