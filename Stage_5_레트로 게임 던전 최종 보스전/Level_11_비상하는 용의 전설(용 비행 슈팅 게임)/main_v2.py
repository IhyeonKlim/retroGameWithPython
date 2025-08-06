# ==========================
# 초기화 및 import
# ==========================
import pygame
from ticks_manager import TicksManager
from player import Player
from monster import Monster
from utils import draw_score_and_items, draw_lives
from meteo import Meteo
from boss import Boss
from scrolling_background import ScrollingBackground

# ==========================
# 게임 상수 설정
# ==========================
SCREEN_WIDTH = 540  # 게임 화면의 가로 크기(픽셀)
SCREEN_HEIGHT = 960  # 게임 화면의 세로 크기(픽셀)
WHITE = (255, 255, 255)  # 텍스트, UI 요소에 사용되는 흰색 RGB 값
BLACK = (0, 0, 0)  # 게임 배경색으로 사용되는 검은색 RGB 값
HEART_RED = (255, 0, 0)  # 플레이어의 생명력(하트)을 나타내는 빨간색 RGB 값
BLUE = (0, 0, 255)  # 플레이어 캐릭터의 색상으로 사용되는 파란색 RGB 값
MAX_FPS = 60  # 게임의 최대 프레임 속도를 60으로 제한 (부드러운 게임 플레이를 위함)

# ==========================
# Pygame 초기화 및 화면 설정
# ==========================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 설정된 크기로 게임 화면 생성
pygame.display.set_caption("용 비행 게임")  # 게임 창의 제목을 "용 비행 게임"으로 설정
clock = pygame.time.Clock()  # 게임의 프레임 속도(FPS)를 제어하기 위한 Clock 객체 생성

# ==========================
# 게임 상태 및 변수 관리
# ==========================
game_state = "intro"  # 게임의 현재 상태를 관리하는 변수 (intro, playing, stage_clear, game_over)
running = True  # 메인 게임 루프를 계속 실행할지 여부를 결정하는 불리언 변수
fps = 60  # 현재 게임의 프레임 속도

# 점수 및 게임 진행 관련 변수
score = [0]  # 현재 점수를 저장하는 리스트 (참조 타입으로 사용하기 위함)
coins = 0  # 플레이어가 획득한 코인의 총합
items_collected = 0  # 획득한 아이템의 총 개수
stage = 1  # 현재 진행 중인 게임 스테이지

# 거리 및 속도 관련 변수
distance = 0  # 플레이어가 이동한 누적 거리
current_distance = 0  # 스테이지 내에서 이동한 현재 거리 (100m마다 초기화)
distance_speed = 1  # 10ms마다 거리가 증가하는 속도 (실제 게임 속도와 연관)

# 특수 효과 관련 변수
slow_motion_start_time = None  # 슬로우 모션 효과가 시작된 시점의 시간
slow_motion_duration = 1000  # 슬로우 모션이 지속되는 시간 (1000ms = 1초)
stage_clear_screen_start_time = 0  # 스테이지 클리어 화면이 시작된 시점의 시간

# 시간 관리 객체 및 변수
ticks_manager = TicksManager()  # 게임 내 시간을 밀리초 단위로 관리하는 커스텀 객체
last_distance_update = ticks_manager.get_ticks()  # 마지막으로 거리를 업데이트한 시점의 시간
meteo_spawn_interval = 5000  # 운석이 생성되는 간격 (5000ms = 5초)
last_meteo_spawn_time = 3000  # 마지막 운석이 생성된 시점의 시간

# ==========================
# 게임 객체 관리
# ==========================
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

# 보스 객체 관련 변수
boss_image_path = "assets/boss_image.png"  # 보스 캐릭터 이미지 파일 경로
boss = None  # 보스 객체 인스턴스 (초기에는 존재하지 않음)
boss_active = False  # 보스가 현재 화면에 활성화되었는지 여부
boss_spawn_distance = 1000  # 보스가 등장하기 시작하는 거리 기준
boss_warning = False  # 보스 등장 예고 메시지를 표시할지 여부
boss_warning_start_time = None  # 보스 경고가 시작된 시점의 시간
boss_spawn_delay = 2000  # 보스 경고 후 실제 보스 등장까지의 지연 시간

# 게임 요소 리스트
meteo_list = []  # 화면에 존재하는 모든 운석 객체들을 저장하는 리스트
coin_list = []  # 화면에 존재하는 모든 코인 객체들을 저장하는 리스트
item_list = []  # 화면에 존재하는 모든 아이템 객체들을 저장하는 리스트

# UI 요소
font = pygame.font.SysFont(None, 36)  # UI 텍스트를 위한 기본 폰트
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 게임 화면에 덧씌울 반투명 오버레이
overlay.fill((0, 0, 0))  # 오버레이를 검정색으로 채움
overlay.set_alpha(100)  # 투명도 설정 (0: 투명, 255: 불투명)


# ==========================
# 게임 함수
# ==========================

def reset_game():
    """
    게임을 초기 상태로 완전히 초기화합니다.
    게임 오버 후 'R' 키를 눌렀을 때 호출됩니다.
    """
    global score, coins, items_collected, distance, current_distance, fps, slow_motion_start_time, stage, meteo_list, monster_row, boss, boss_active, boss_warning, coin_list, item_list, player, last_distance_update, meteo_spawn_interval, last_meteo_spawn_time, stage_clear_screen_start_time

    # 모든 게임 변수를 초기값으로 재설정
    score = [0]
    coins = 0
    items_collected = 0
    distance = 0
    current_distance = 0
    fps = MAX_FPS
    slow_motion_start_time = None
    stage = 1

    # 게임 요소 리스트 초기화
    meteo_list.clear()
    coin_list.clear()
    item_list.clear()

    # 보스 관련 변수 초기화
    boss = None
    boss_active = False
    boss_warning = False
    stage_clear_screen_start_time = 0

    # 플레이어 객체 재설정
    player = Player(
        x=SCREEN_WIDTH // 2 - 25, y=SCREEN_HEIGHT - 130,
        width=100, height=100, speed=5, color=BLUE,
        image_path="assets/player_image.png"
    )

    # 몬스터 행 재설정
    monster_row = Monster.create_row(
        screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
        image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png"
    )

    # 시간 관리 객체 재설정
    ticks_manager.reset_ticks()
    last_distance_update = ticks_manager.get_ticks()
    meteo_spawn_interval = 5000
    last_meteo_spawn_time = 3000


def reset_for_next_stage():
    """
    현재 스테이지 클리어 후 다음 스테이지를 위해 게임 요소를 초기화합니다.
    난이도를 점진적으로 상승시킵니다.
    """
    global stage, distance, distance_speed, meteo_spawn_interval, monster_row, boss, boss_active, boss_warning, slow_motion_start_time, stage_clear_screen_start_time

    # 스테이지 번호 증가 및 난이도 상승
    stage += 1
    distance_speed += 0.5
    meteo_spawn_interval = max(3000, meteo_spawn_interval - 500)  # 운석 생성 간격 감소

    # 게임 요소 초기화
    distance = 0
    meteo_list.clear()
    coin_list.clear()
    item_list.clear()

    # 다음 스테이지의 몬스터 행 생성
    monster_row = Monster.create_row(
        screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
        image_path="assets/normal_monster.png", special_image_path="assets/special_monster.png"
    )

    # 보스 관련 변수 초기화
    boss = None
    boss_active = False
    boss_warning = False
    slow_motion_start_time = None
    stage_clear_screen_start_time = 0


def handle_input(event):
    """
    게임 상태에 따라 키보드 및 마우스 입력을 처리합니다.
    """
    global running, game_state
    # 윈도우 닫기 버튼(X)을 눌렀을 때 게임 종료
    if event.type == pygame.QUIT:
        running = False

    # 게임 상태가 "intro"일 때, ENTER 키를 누르면 게임 시작
    if game_state == "intro":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state = "playing"

    # 게임 상태가 "game_over"일 때, R 키를 누르면 게임 재시작
    elif game_state == "game_over":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            game_state = "playing"


def draw_intro_screen(surface, background_color, text_color):
    """
    게임 시작 전 인트로 화면을 그립니다.
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
    플레이어의 생명력이 0이 되었을 때 표시되는 게임 오버 화면을 그립니다.
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
    스테이지를 성공적으로 클리어했을 때 표시되는 화면을 그립니다.
    """
    surface.fill(WHITE)
    font_large = pygame.font.SysFont(None, 60)
    stage_text = font_large.render(f"STAGE {current_stage} CLEAR!", True, (0, 255, 0))
    text_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(stage_text, text_rect)


# ==========================
# 메인 게임 루프
# ==========================
while running:
    # --- 이벤트 처리 ---
    # Pygame 이벤트 큐에서 모든 이벤트를 가져와 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 윈도우 종료 이벤트 발생 시 게임 루프 종료
        handle_input(event)  # 현재 게임 상태에 따른 키보드 입력 처리

    # --- 게임 상태 업데이트 및 그리기 ---
    if game_state == "intro":
        # 인트로 상태일 경우, 인트로 화면만 그리기
        draw_intro_screen(screen, BLACK, WHITE)

    elif game_state == "stage_clear":
        # 스테이지 클리어 상태일 경우
        draw_stage_clear_screen(screen, stage)  # 클리어 화면 그리기

        # 타이머를 시작하여 3초 동안 화면 유지
        if stage_clear_screen_start_time == 0:
            stage_clear_screen_start_time = ticks_manager.get_ticks()
        if ticks_manager.get_ticks() - stage_clear_screen_start_time >= 3000:
            reset_for_next_stage()  # 3초가 지나면 다음 스테이지로 게임 초기화
            game_state = "playing"  # 게임 플레이 상태로 전환

    elif game_state == "game_over":
        # 게임 오버 상태일 경우, 게임 오버 화면만 그리기
        draw_game_over_screen(screen, BLACK, WHITE)

    elif game_state == "playing":
        # 게임 플레이 상태일 경우, 모든 게임 로직을 실행

        # --- 배경 및 UI 그리기 ---
        background.update()  # 배경 스크롤 업데이트
        background.draw(screen)  # 배경 그리기
        screen.blit(overlay, (0, 0))  # 화면에 어두운 오버레이 덧씌우기
        current_time = ticks_manager.get_ticks()

        # --- 점수 및 거리 업데이트 ---
        # 10ms마다 거리를 업데이트하여 부드럽게 증가하도록 함
        if current_time - last_distance_update >= 10:
            current_distance += distance_speed
            if current_distance >= 100:  # 100m마다 거리 초기화 (스테이지 진행용)
                current_distance = 0
            distance += distance_speed  # 총 누적 거리 증가
            last_distance_update = current_time
            score[0] += distance_speed  # 점수도 거리에 비례하여 증가

        keys = pygame.key.get_pressed()

        # --- 플레이어 관련 로직 ---
        player.auto_shoot()  # 플레이어의 자동 발사 기능
        player.update_bullet_effect(ticks_manager)  # 총알 강화 효과 시간 업데이트
        player.move(keys, SCREEN_WIDTH)  # 키 입력에 따라 플레이어 이동
        player.draw(screen)  # 플레이어 그리기
        player.update_bullets(screen)  # 플레이어가 발사한 총알 업데이트 및 그리기
        player.update_magnet(ticks_manager=ticks_manager, coin_list=coin_list, item_list=item_list,
                             coins=coins)  # 자석 효과 처리

        # --- 운석 관련 로직 ---
        # 설정된 간격마다 운석 생성
        if current_time - last_meteo_spawn_time > meteo_spawn_interval:
            meteo_list.append(Meteo.create_random(SCREEN_WIDTH, "assets/meteo_image.png"))
            last_meteo_spawn_time = current_time

        # 모든 운석 객체에 대한 처리
        for meteo in meteo_list[:]:
            meteo.update_state()  # 운석 상태(경고, 낙하) 업데이트
            if meteo.state == "warning":
                meteo.draw_warning(screen, font)  # 경고 메시지 그리기
                meteo.draw_guide_line(screen, SCREEN_HEIGHT)  # 운석 낙하 가이드라인 그리기
            elif meteo.state == "falling":
                meteo.move()  # 낙하 중인 운석 이동
                meteo.draw(screen)  # 낙하 중인 운석 그리기

            # 화면 아래로 벗어난 운석 제거
            if meteo.y > SCREEN_HEIGHT:
                meteo_list.remove(meteo)

            # 플레이어와 운석 충돌 처리 (하이퍼 플라이트 중에는 무적)
            if meteo.state == "falling" and player.rect.colliderect(meteo.rect) and not player.is_hyper_flight_active():
                player.lives -= 1  # 생명력 감소
                slow_motion_start_time = ticks_manager.get_ticks()  # 슬로우 모션 효과 시작
                meteo_list.remove(meteo)

        # --- 몬스터 관련 로직 ---
        # 몬스터 행의 모든 몬스터 객체에 대한 처리
        for monster in monster_row[:]:
            monster.move()  # 몬스터 이동
            if monster.y > SCREEN_HEIGHT:  # 화면 밖으로 나간 몬스터 제거
                monster_row.remove(monster)
            else:
                monster.draw(screen)  # 몬스터 그리기

        # 몬스터와 플레이어 총알 간의 충돌 처리 (보스가 없을 때만)
        if not boss_active:
            Monster.handle_collision(monsters=monster_row, bullets=player.bullets, score=score, coin_list=coin_list,
                                     item_list=item_list)

        # 하이퍼 플라이트 중일 때 몬스터 자동 제거
        if player.is_hyper_flight_active():
            Monster.handle_hyper_flight_collision(monsters=monster_row, mid_screen_height=SCREEN_HEIGHT // 2,
                                                  score=score, coin_list=coin_list, item_list=item_list,
                                                  item_spawn_chance=30)

        # 몬스터와 플레이어 충돌 처리 (하이퍼 플라이트 중에는 무적)
        for monster in monster_row[:]:
            if player.rect.colliderect(monster.rect) and not player.is_hyper_flight_active():
                player.lives -= 1
                slow_motion_start_time = ticks_manager.get_ticks()
                monster_row.remove(monster)

        # 몬스터 행이 비어있으면 새로운 행 생성
        if not monster_row and not boss_active and not boss_warning:
            monster_row = Monster.create_row(screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
                                             image_path="assets/normal_monster.png",
                                             special_image_path="assets/special_monster.png")

        # --- 아이템 및 코인 관련 로직 ---
        # 화면에 있는 모든 아이템 처리
        for item in item_list[:]:
            item.move()
            if item.y > SCREEN_HEIGHT:
                item_list.remove(item)
            else:
                item.draw(screen)

        # 화면에 있는 모든 코인 처리
        for coin in coin_list[:]:
            coin.move()
            if coin.y > SCREEN_HEIGHT:
                coin_list.remove(coin)
            else:
                coin.draw(screen)
            # 플레이어가 코인을 획득했을 경우
            if player.rect.colliderect(coin.rect):
                coins += coin.value
                coin_list.remove(coin)

        # 플레이어가 아이템을 획득했을 경우
        for item in item_list[:]:
            if player.rect.colliderect(item.rect):
                if item.type == 'bullet':
                    player.increase_bullet_count()
                elif item.type == 'magnet':
                    player.activate_magnet(ticks_manager, duration=5000)
                elif item.type == 'hyper_flight':
                    player.activate_hyper_flight(ticks_manager, duration=5000)
                    distance += 1000
                    monster_row.clear()
                item_list.remove(item)

        # --- FPS 및 효과 업데이트 ---
        # 하이퍼 플라이트 중일 때는 FPS를 높여 속도를 빠르게 함
        if player.is_hyper_flight_active():
            fps = 600
            distance += distance_speed * 10
        else:
            # 하이퍼 플라이트가 끝나면 FPS를 점진적으로 원래대로 복구
            fps = max(fps - 10, MAX_FPS)
        player.update_hyper_flight(ticks_manager)  # 하이퍼 플라이트 효과 시간 업데이트

        # 점수, 코인, 거리, 아이템 효과 등 UI 정보 그리기
        draw_score_and_items(surface=screen, score=score[0], coins=coins, distance=distance, color=WHITE,
                             bullet_effect_time_left=None, hyper_flight_time_left=None,
                             hyper_flight_message=player.get_hyper_flight_message(),
                             magnet_time_left=player.get_magnet_time_left(ticks_manager),
                             bullet_level=player.get_bullet_level())

        # 플레이어의 남은 생명력(하트) 그리기
        draw_lives(screen, player.lives, HEART_RED)

        # 슬로우 모션 효과 처리
        if slow_motion_start_time is not None:
            elapsed_time = ticks_manager.get_ticks() - slow_motion_start_time
            if elapsed_time < slow_motion_duration:
                fps = 10  # 슬로우 모션 지속 시간 동안 FPS를 낮춤
            else:
                slow_motion_start_time = None
                fps = MAX_FPS  # 효과가 끝나면 FPS 복구
        else:
            if fps < MAX_FPS:
                fps = min(fps + 3, MAX_FPS)  # FPS를 점진적으로 원래대로 복구

        # --- 보스 관련 로직 ---
        # 보스 등장 거리 조건 충족 및 보스가 없을 때
        if distance >= boss_spawn_distance and not boss_active and not boss_warning and not player.is_hyper_flight_active():
            boss_warning = True  # 보스 경고 상태로 전환
            boss_warning_start_time = None

        # 보스 경고 상태일 경우
        if boss_warning:
            if boss_warning_start_time is None:
                boss_warning_start_time = ticks_manager.get_ticks()
            warning_text = font.render("Boss is Coming!", True, (255, 0, 0))
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(warning_text, warning_rect)
            # 경고 딜레이 시간(2초)이 지나면 보스 활성화
            if ticks_manager.get_ticks() - boss_warning_start_time > boss_spawn_delay:
                boss_active = True
                boss_warning = False
                boss = Boss(x=SCREEN_WIDTH // 2 - 400 // 2, y=0, stage=stage, image_path=boss_image_path)

        # 보스 활성화 상태일 경우
        if boss_active and not player.is_hyper_flight_active():
            boss.draw(screen)  # 보스 그리기
            if boss.y < 120:
                boss.y += 1  # 보스가 화면 상단에 도달할 때까지 아래로 이동
            else:
                boss.move(SCREEN_WIDTH)  # 보스 이동 패턴 시작

            # 플레이어 총알과 보스 충돌 처리
            for Bullet in player.bullets[:]:
                if Bullet.rect.colliderect(boss.rect):
                    boss.take_damage(10)
                    player.bullets.remove(Bullet)

            # 플레이어와 보스 충돌 처리
            if boss.rect.colliderect(player.rect):
                player.lives -= 3  # 생명력 크게 감소
                if player.lives > 0:
                    boss.y += boss.height  # 보스를 화면 밖으로 잠시 밀어냄

            # 보스 시간 제한 처리
            if boss.is_time_up():
                boss.y += boss.speed  # 시간 초과 시 보스가 화면 아래로 도망감
                if boss.y > SCREEN_HEIGHT:
                    boss_active = False  # 화면 밖으로 나가면 보스 비활성화
                    boss = None
                    print("Boss escaped!")

            # 보스 체력이 0 이하가 되면 스테이지 클리어
            if boss.health <= 0:
                boss_active = False
                boss = None
                game_state = "stage_clear"
                score[0] += 100000  # 보스 처치 보너스 점수

        # --- 게임 오버 조건 확인 ---
        if player.lives <= 0:
            game_state = "game_over"  # 생명력이 0이 되면 게임 오버 상태로 전환

    # --- 화면 갱신 및 FPS 제어 ---
    pygame.display.flip()  # 모든 요소를 화면에 업데이트
    clock.tick(fps)  # 설정된 FPS에 맞춰 루프 속도 제어

pygame.quit()