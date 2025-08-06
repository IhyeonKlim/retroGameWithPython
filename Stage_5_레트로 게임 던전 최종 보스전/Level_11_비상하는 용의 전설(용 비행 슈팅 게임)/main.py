# ==============================================================================
# 초기화 및 import
# ==============================================================================
import pygame
from ticks_manager import TicksManager
from player import Player
from monster import Monster
from utils import draw_score_and_items, draw_lives
from meteo import Meteo
from boss import Boss
from scrolling_background import ScrollingBackground

# ==============================================================================
# 게임 상수 설정
# ==============================================================================
SCREEN_WIDTH = 540  # 화면의 가로 크기
SCREEN_HEIGHT = 960  # 화면의 세로 크기
WHITE = (255, 255, 255)  # 흰색 RGB 값 (텍스트 및 UI 요소에 사용)
BLACK = (0, 0, 0)  # 검은색 RGB 값 (기본 배경색)
HEART_RED = (255, 0, 0)  # 빨간색 RGB 값 (플레이어 생명 표시)
BLUE = (0, 0, 255)  # 파란색 RGB 값 (플레이어 색상)
MAX_FPS = 60  # 게임의 최대 프레임 속도 제한

# ==============================================================================
# Pygame 초기화 및 화면 설정
# ==============================================================================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 게임 화면 생성
pygame.display.set_caption("용 비행 게임")  # 게임 창의 제목 설정
clock = pygame.time.Clock()  # FPS 제어를 위한 Clock 객체 생성

# ==============================================================================
# 게임 상태 및 변수 관리
# ==============================================================================
# 게임 상태를 나타내는 단일 변수. "intro", "playing", "stage_clear", "game_over" 중 하나
game_state = "intro"
running = True  # 메인 게임 루프의 실행 여부
fps = 60  # 현재 게임의 프레임 속도

# 점수 및 게임 진행 관련 변수
score = [0]  # 현재 점수
coins = 0  # 플레이어가 획득한 코인 수
items_collected = 0  # 수집한 아이템 수
stage = 1  # 현재 게임 스테이지

# 거리 및 속도 관련 변수
distance = 0  # 누적 이동 거리
current_distance = 0  # 현재 스테이지 이동 거리 (100m 단위로 리셋)
distance_speed = 1  # 거리가 증가하는 속도 (10ms 당 1 증가)

# 특수 효과 관련 변수
slow_motion_start_time = None  # 슬로우 모션 효과가 시작된 시간
slow_motion_duration = 1000  # 슬로우 모션 지속 시간 (밀리초)

# 시간 관리 객체 및 변수
ticks_manager = TicksManager()  # 게임 내 시간을 관리하는 객체
last_distance_update = ticks_manager.get_ticks()  # 마지막으로 거리가 업데이트된 시간
meteo_spawn_interval = 5000  # 운석이 생성되는 간격 (5초)
last_meteo_spawn_time = 3000  # 마지막 운석 생성 시간
stage_clear_screen_start_time = 0 # 스테이지 클리어 화면이 시작된 시간

# ==============================================================================
# 게임 객체 관리
# ==============================================================================
# 플레이어 객체
player = Player(
    x=SCREEN_WIDTH // 2 - 25, y=SCREEN_HEIGHT - 130,
    width=100, height=100, speed=5, color=BLUE,
    image_path="assets/player_image.png"
)

# 배경 스크롤 객체
background = ScrollingBackground(
    SCREEN_WIDTH, SCREEN_HEIGHT, "assets/background.png", speed=5
)

# 몬스터 객체
monster_row = Monster.create_row(
    screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
    image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png"
)

# 보스 객체
boss_image_path = "assets/boss_image.png"  # 보스 이미지 경로
boss = None  # 보스 객체 인스턴스 (초기값은 None)
boss_active = False  # 보스가 활성화되었는지 여부
boss_spawn_distance = 1000  # 보스가 등장할 거리
boss_warning = False  # 보스 등장 경고 상태
boss_warning_start_time = None  # 보스 경고 시작 시간
boss_spawn_delay = 3000  # 보스가 실제로 등장하기까지의 지연 시간

# 게임 요소 리스트
meteo_list = []  # 운석 객체를 담는 리스트
coin_list = []  # 코인 객체를 담는 리스트
item_list = []  # 아이템 객체를 담는 리스트

# UI 요소
font = pygame.font.SysFont(None, 36) # 일반 텍스트용 폰트
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 전체에 덮을 어두운 필터
overlay.fill((0, 0, 0))
overlay.set_alpha(100)

# ==============================================================================
# 게임 함수
# ==============================================================================

def reset_game():
    """
    게임을 초기화하여 처음 상태로 되돌립니다.
    """
    global score, coins, items_collected, distance, current_distance, fps, slow_motion_start_time, stage, meteo_list, monster_row, boss, boss_active, boss_warning, coin_list, item_list, player, last_distance_update, meteo_spawn_interval, last_meteo_spawn_time, stage_clear_screen_start_time

    score = [0]
    coins = 0
    items_collected = 0
    distance = 0
    current_distance = 0
    fps = MAX_FPS
    slow_motion_start_time = None
    stage = 1
    meteo_list.clear()
    coin_list.clear()
    item_list.clear()
    boss = None
    boss_active = False
    boss_warning = False
    stage_clear_screen_start_time = 0

    player = Player(
        x=SCREEN_WIDTH // 2 - 25, y=SCREEN_HEIGHT - 130,
        width=100, height=100, speed=5, color=BLUE,
        image_path="assets/player_image.png"
    )
    monster_row = Monster.create_row(
        screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
        image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png"
    )

    ticks_manager.reset_ticks()
    last_distance_update = ticks_manager.get_ticks()
    meteo_spawn_interval = 5000
    last_meteo_spawn_time = 3000


def reset_for_next_stage():
    """
    다음 스테이지를 위해 게임을 초기화합니다. 난이도가 상승합니다.
    """
    global stage, distance, distance_speed, meteo_spawn_interval, monster_row, boss, boss_active, boss_warning, slow_motion_start_time, stage_clear_screen_start_time

    stage += 1
    distance_speed += 0.5
    meteo_spawn_interval = max(3000, meteo_spawn_interval - 500)

    distance = 0
    meteo_list.clear()
    coin_list.clear()
    item_list.clear()

    monster_row = Monster.create_row(
        screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
        image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png"
    )

    boss = None
    boss_active = False
    boss_warning = False
    slow_motion_start_time = None
    stage_clear_screen_start_time = 0


def handle_input(event):
    """
    게임 상태에 따른 키보드 및 마우스 입력을 처리합니다.
    """
    global running, game_state, intro
    if event.type == pygame.QUIT:
        running = False
    if game_state == "intro":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state = "playing"
    elif game_state == "game_over":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            game_state = "playing"


def draw_intro_screen(surface, background_color, text_color):
    """
    인트로 화면을 그립니다.
    """
    surface.fill(background_color)
    font_large = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 30)
    title_text = font_large.render("Dragon flying game", True, text_color)
    start_text = font_small.render("Press Enter to start", True, text_color)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(title_text, title_rect)
    surface.blit(start_text, start_rect)


def draw_game_over_screen(surface, background_color, text_color):
    """
    게임 오버 화면을 그립니다.
    """
    surface.fill(background_color)
    font_large = pygame.font.SysFont(None, 60)
    font_medium = pygame.font.SysFont(None, 40)
    font_small = pygame.font.SysFont(None, 30)
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"score: {score[0]}", True, text_color)
    restart_text = font_small.render("press R to restart", True, text_color)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    surface.blit(game_over_text, game_over_rect)
    surface.blit(score_text, score_rect)
    surface.blit(restart_text, restart_rect)


def draw_stage_clear_screen(surface, current_stage):
    """
    스테이지 클리어 화면을 그립니다.
    """
    surface.fill(WHITE)
    font_large = pygame.font.SysFont(None, 60)
    stage_text = font_large.render(f"STAGE {current_stage} CLEAR!", True, (0, 255, 0))
    text_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(stage_text, text_rect)


# ==============================================================================
# 메인 게임 루프
# ==============================================================================
while running:
    # --- 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_input(event)

    # --- 게임 상태 업데이트 및 그리기 ---
    if game_state == "intro":
        draw_intro_screen(screen, BLACK, WHITE)

    elif game_state == "stage_clear":
        draw_stage_clear_screen(screen, stage)
        if stage_clear_screen_start_time == 0:
            stage_clear_screen_start_time = ticks_manager.get_ticks()
        if ticks_manager.get_ticks() - stage_clear_screen_start_time >= 3000:
            reset_for_next_stage()
            game_state = "playing"

    elif game_state == "game_over":
        draw_game_over_screen(screen, BLACK, WHITE)

    elif game_state == "playing":
        # --- 배경 및 UI 그리기 ---
        background.update()
        background.draw(screen)
        screen.blit(overlay, (0, 0))
        current_time = ticks_manager.get_ticks()

        # --- 점수 및 거리 업데이트 ---
        if current_time - last_distance_update >= 10:
            current_distance += distance_speed
            if current_distance >= 100:
                current_distance = 0
            distance += distance_speed
            last_distance_update = current_time
            score[0] += distance_speed

        keys = pygame.key.get_pressed()

        # --- 플레이어 관련 로직 ---
        if not player.is_hyper_flight_active():
            # 하이퍼 플라이트 시 사격 중지
            player.auto_shoot()
        player.update_bullet_effect(ticks_manager)
        player.move(keys, SCREEN_WIDTH)
        player.draw(screen)
        player.update_bullets(screen)
        player.update_magnet(ticks_manager=ticks_manager, coin_list=coin_list, item_list=item_list, coins=coins)

        # --- 운석 관련 로직 ---
        if current_time - last_meteo_spawn_time > meteo_spawn_interval:
            meteo_list.append(Meteo.create_random(SCREEN_WIDTH, "assets/meteo_image.png"))
            last_meteo_spawn_time = current_time
        for meteo in meteo_list[:]:
            meteo.update_state()
            if meteo.state == "warning":
                meteo.draw_warning(screen, font)
                meteo.draw_guide_line(screen, SCREEN_HEIGHT)
            elif meteo.state == "falling":
                meteo.move()
                meteo.draw(screen)
            if meteo.y > SCREEN_HEIGHT:
                meteo_list.remove(meteo)
            if meteo.state == "falling" and player.rect.colliderect(meteo.rect) and not player.is_hyper_flight_active():
                player.lives -= 1
                slow_motion_start_time = ticks_manager.get_ticks()
                meteo_list.remove(meteo)

        # --- 몬스터 관련 로직 ---
        for monster in monster_row[:]:
            monster.move()
            if monster.y > SCREEN_HEIGHT:
                monster_row.remove(monster)
            else:
                monster.draw(screen)
        if not boss_active:
            Monster.handle_collision(monsters=monster_row, bullets=player.bullets, score=score, coin_list=coin_list, item_list=item_list)
        if player.is_hyper_flight_active():
            Monster.handle_hyper_flight_collision(monsters=monster_row, mid_screen_height=SCREEN_HEIGHT // 6, score=score, coin_list=coin_list, item_list=item_list, item_spawn_chance=10)
        for monster in monster_row[:]:
            if player.rect.colliderect(monster.rect) and not player.is_hyper_flight_active():
                player.lives -= 1
                slow_motion_start_time = ticks_manager.get_ticks()
                monster_row.remove(monster)
        if not monster_row and not boss_active and not boss_warning:
            monster_row = Monster.create_row(screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage, image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png")

        # --- 아이템 및 코인 관련 로직 ---
        for item in item_list[:]:
            item.move()
            if item.y > SCREEN_HEIGHT:
                item_list.remove(item)
            else:
                item.draw(screen)
        for coin in coin_list[:]:
            coin.move()
            if coin.y > SCREEN_HEIGHT:
                coin_list.remove(coin)
            else:
                coin.draw(screen)
            if player.rect.colliderect(coin.rect):
                coins += coin.value
                coin_list.remove(coin)
        for item in item_list[:]:
            if player.rect.colliderect(item.rect):
                if item.type == 'bullet':
                    player.increase_bullet_power()
                elif item.type == 'magnet':
                    player.activate_magnet(ticks_manager, duration=5000)
                elif item.type == 'hyper_flight':
                    player.activate_hyper_flight(ticks_manager, duration=5000)
                    distance += 1000
                    monster_row.clear()
                item_list.remove(item)

        # --- FPS 및 효과 업데이트 ---
        if player.is_hyper_flight_active():
            fps = MAX_FPS*3  # MAX_FPS(60)으로 고정
            # 고속 이동은 distance_speed를 조절하는 방식으로 구현하는 것이 더 좋음
            distance += distance_speed * 3  # 속도를 높여도 FPS는 유지
        else:
            # 하이퍼플라이트가 끝나면 FPS를 원래대로 복구
            fps = MAX_FPS

        player.update_hyper_flight(ticks_manager)
        draw_score_and_items(surface=screen, score=score[0], coins=coins, distance=distance, color=WHITE, hyper_flight_time_left=None, hyper_flight_message=player.get_hyper_flight_message(), magnet_time_left=player.get_magnet_time_left(ticks_manager), bullet_level=player.get_bullet_level())
        draw_lives(screen, player.lives, HEART_RED)

        # --- 플레이어 피격시 슬로우모션 ---
        if slow_motion_start_time is not None:
            elapsed_time = ticks_manager.get_ticks() - slow_motion_start_time
            if elapsed_time < slow_motion_duration:
                fps = 10
            else:
                slow_motion_start_time = None
                fps = MAX_FPS

        player.update_hyper_flight(ticks_manager)  # 이 부분이 정상적으로 호출되도록 함

        # --- 보스 관련 로직 ---
        if boss_warning:
            if boss_warning_start_time is None:
                boss_warning_start_time = ticks_manager.get_ticks()
            warning_text = font.render("Boss is Coming!", True, (255, 0, 0))
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(warning_text, warning_rect)
            if ticks_manager.get_ticks() - boss_warning_start_time > boss_spawn_delay:
                boss_active = True
                boss_warning = False
                boss = Boss(x=SCREEN_WIDTH // 2 - 400 // 2, y=0, stage=stage, image_path=boss_image_path)
        if distance >= boss_spawn_distance and not boss_active and not boss_warning and not player.is_hyper_flight_active():
            boss_warning = True
            boss_warning_start_time = None
        if boss_active and not player.is_hyper_flight_active():
            boss.draw(screen)
            if boss.y < 120:
                boss.y += 1
            else:
                boss.move(SCREEN_WIDTH)
            for Bullet in player.bullets[:]:
                if Bullet.rect.colliderect(boss.rect):
                    boss.take_damage(player.bullet_damage)
                    player.bullets.remove(Bullet)
            if boss.rect.colliderect(player.rect):
                player.lives -= 3
                if player.lives > 0:
                    boss.y += boss.height
            if boss.is_time_up():
                boss.y += boss.speed
                if boss.y > SCREEN_HEIGHT:
                    boss_active = False
                    boss = None
                    print("Boss escaped!")
            if boss.health <= 0:
                boss_active = False
                boss = None
                game_state = "stage_clear"
                score[0] += 100000

        # --- 게임 오버 조건 확인 ---
        if player.lives <= 0:
            game_state = "game_over"

    # --- 화면 갱신 및 FPS 제어 ---
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()