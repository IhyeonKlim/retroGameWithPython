import pygame
from ticks_manager import TicksManager
from player import Player
from monster import Monster
from utils import draw_score_and_items, draw_game_over, draw_lives, draw_intro
from meteo import Meteo
from boss import Boss
from scrolling_background import ScrollingBackground

# 상수 설정
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEART_RED = (255, 0, 0)
BLUE = (0, 0, 255)
MAX_FPS = 60

# 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("용 비행 게임")

# Clock 객체와 게임 변수 초기화
clock = pygame.time.Clock()
score = [0]  # 점수는 리스트로 전달하여 참조형으로 사용
coins = 0
items_collected = 0  # 수집한 아이템 수
distance = 0
current_distance = 0
distance_speed = 1  # 10ms마다 1씩 증가하여 1초당 100m로 설정
game_over = False
running = True
fps = 60
slow_motion_start_time = None  # FPS 느려지는 효과의 시작 시간
slow_motion_duration = 1000  # 느려지는 효과 지속 시간 (밀리초)
stage = 1

# 인트로 상태 변수
intro = True

# 운석 리스트
meteo_list = []

# 시간 체크 변수
ticks_manager = TicksManager()
last_distance_update = ticks_manager.get_ticks()
meteo_spawn_interval = 5000  # 5초마다 운석 생성
last_meteo_spawn_time = 3000  # 마지막 운석 생성시점

# 플레이어 생성
player = Player(x=SCREEN_WIDTH // 2 - 25, y=SCREEN_HEIGHT - 130, width=100, height=100, speed=5, color=BLUE, image_path="player_image.png")

# 몬스터 생성
monster_row = Monster.create_row(screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage, image_path="normal_monster.png", special_image_path="special_monster.png")

boss_image_path = "boss_image.png"

# Boss 관련 변수
boss = None
boss_active = False
boss_spawn_distance = 1000  # 보스가 등장할 거리
stage_cleared = False  # 스테이지 완료 상태
boss_warning = False  # 보스 경고 상태
boss_warning_start_time = None  # 경고 시작 시간
boss_spawn_delay = 2000  # 2초 (밀리초)

# 코인 및 아이템 리스트
coin_list = []
item_list = []

# font for meteo
font = pygame.font.SysFont(None, 36)


# ScrollingBackground 객체 생성
background = ScrollingBackground(SCREEN_WIDTH, SCREEN_HEIGHT, "background.png", speed=5)

# 어두운 필터 추가
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 크기와 동일한 Surface 생성
overlay.fill((0, 0, 0))  # 검정색으로 채우기
overlay.set_alpha(100)  # 투명도 설정 (0-255)


# 게임 루프
while running:

    if intro:
        draw_intro(screen, BLACK, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter 키로 시작
                intro = False
        continue

    # 게임 오버 상태 확인
    if player.lives <= 0:
        game_over = True

    # 게임 오버 화면 표시
    if game_over:
        draw_game_over(screen, BLACK, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # R 키로 게임 재시작
                # 게임 상태 초기화
                player.lives = 3
                score = [0]
                coins = 0
                items_collected = 0
                distance = 0  # 거리 초기화
                current_distance = 0
                meteo_list.clear()  # 운석 리스트 초기화
                coin_list.clear()  # 코인 리스트 초기화
                item_list.clear()  # 아이템 리스트 초기화
                monster_row = Monster.create_row(screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
                                                 image_path="normal_monster.png",
                                                 special_image_path="special_monster.png")
                player = Player(x=SCREEN_WIDTH // 2 - 25, y=SCREEN_HEIGHT - 130, width=50, height=50, speed=5,
                                color=BLUE)  # 플레이어 초기화
                ticks_manager.reset_ticks()  # 시간 초기화
                last_distance_update = ticks_manager.get_ticks()  # 거리 업데이트 시간 초기화
                game_stage_complete = False  # 스테이지 상태 초기화
                boss = None  # 보스 초기화
                boss_active = False
                boss_warning = False  # 보스 경고 상태 초기화
                game_over = False
                fps = MAX_FPS
                slow_motion_start_time = None  # 느려지는 효과 초기화
        continue
    # 배경 업데이트 및 그리기
    background.update()
    background.draw(screen)
    # 화면에 배경 그린 후 필터 추가
    background.draw(screen)
    screen.blit(overlay, (0, 0))  # 필터를 화면 위에 덧씌우기
    #screen.fill(WHITE)
    current_time = ticks_manager.get_ticks()

    # 거리 측정 및 업데이트
    if current_time - last_distance_update >= 10:
        current_distance += distance_speed
        if current_distance >= 100:
            current_distance = 0
        distance += distance_speed
        last_distance_update = current_time
        score[0] += distance_speed

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 플레이어 관련 업데이트
    player.auto_shoot()
    player.update_bullet_effect(ticks_manager)
    player.move(keys, SCREEN_WIDTH)
    player.draw(screen)
    player.update_bullets(screen)
    player.update_magnet(
        ticks_manager=ticks_manager,
        coin_list=coin_list,
        item_list=item_list,
        coins=coins
    )

    # 운석 생성
    if current_time - last_meteo_spawn_time > meteo_spawn_interval:
        meteo_list.append(Meteo.create_random(SCREEN_WIDTH, "meteo_image.png"))
        last_meteo_spawn_time = current_time

    # 운석 이동 및 충돌 처리
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

    # 몬스터 관련 업데이트
    for monster in monster_row[:]:
        monster.move()
        if monster.y > SCREEN_HEIGHT:
            monster_row.remove(monster)
        else:
            monster.draw(screen)

    if not boss_active:
        Monster.handle_collision(
            monsters=monster_row,
            bullets=player.bullets,
            score=score,
            coin_list=coin_list,
            item_list=item_list
        )

    if player.is_hyper_flight_active():
        Monster.handle_hyper_flight_collision(
            monsters=monster_row,
            mid_screen_height=SCREEN_HEIGHT // 2,
            score=score,
            coin_list=coin_list,
            item_list=item_list,
            item_spawn_chance=30,
        )

    for monster in monster_row[:]:
        if player.rect.colliderect(monster.rect) and not player.is_hyper_flight_active():
            player.lives -= 1
            slow_motion_start_time = ticks_manager.get_ticks()
            monster_row.remove(monster)

    if not monster_row and not boss_active and not boss_warning:
        monster_row = Monster.create_row(screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
                                         image_path="normal_monster.png", special_image_path="special_monster.png")

    # 아이템 및 코인 이동 및 충돌 처리
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
                player.increase_bullet_count()
            elif item.type == 'magnet':
                player.activate_magnet(ticks_manager, duration=5000)
            elif item.type == 'hyper_flight':
                player.activate_hyper_flight(ticks_manager, duration=5000)
                distance += 1000
                monster_row.clear()
            item_list.remove(item)

    if player.is_hyper_flight_active():
        fps = 600
        distance += distance_speed * 10
    else:
        fps = max(fps - 10, MAX_FPS)

    player.update_hyper_flight(ticks_manager)

    draw_score_and_items(
        surface=screen,
        score=score[0],
        coins=coins,
        distance=distance,
        color=WHITE,
        bullet_effect_time_left=None,
        hyper_flight_time_left=None,
        hyper_flight_message=player.get_hyper_flight_message(),
        magnet_time_left=player.get_magnet_time_left(ticks_manager),
        bullet_level=player.get_bullet_level(),
    )
    draw_lives(screen, player.lives, HEART_RED)

    if slow_motion_start_time is not None:
        elapsed_time = ticks_manager.get_ticks() - slow_motion_start_time
        if elapsed_time < slow_motion_duration:
            fps = 10
        else:
            slow_motion_start_time = None
            fps = MAX_FPS
    else:
        if fps < MAX_FPS:
            fps = min(fps + 3, MAX_FPS)

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

        for bullet in player.bullets[:]:
            if bullet.rect.colliderect(boss.rect):
                boss.take_damage(10)
                player.bullets.remove(bullet)

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
            stage_cleared = True
            score[0] += 100000

    if stage_cleared:
        screen.fill(WHITE)
        stage_text = font.render("{} STAGE CLEAR!".format(stage), True, (0, 255, 0))
        text_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(stage_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        stage += 1
        stage_cleared = False

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
