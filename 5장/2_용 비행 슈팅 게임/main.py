# 초기화 및 상수 설정
import pygame
from ticks_manager import TicksManager
from player import Player
from monster import Monster
from utils import draw_score_and_items, draw_game_over, draw_lives, draw_intro
from meteo import Meteo
from boss import Boss
from scrolling_background import ScrollingBackground

# 상수 설정
SCREEN_WIDTH = 540  # 화면 가로 크기
SCREEN_HEIGHT = 960  # 화면 세로 크기
WHITE = (255, 255, 255)  # 흰색 (텍스트 및 UI 요소)
BLACK = (0, 0, 0)  # 검은색 (기본 배경)
HEART_RED = (255, 0, 0)  # 빨간색 (플레이어 생명 표시)
BLUE = (0, 0, 255)  # 파란색 (플레이어 색상)
MAX_FPS = 60  # 최대 프레임 속도 (게임의 FPS를 제한)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 생성
pygame.display.set_caption("용 비행 게임")  # 창 제목 설정

# 게임 변수 초기화
clock = pygame.time.Clock()  # FPS 제어를 위한 Clock 객체 생성
score = [0]  # 점수 저장 (리스트로 선언해 참조형으로 활용 가능)
coins = 0  # 플레이어가 획득한 코인 수
items_collected = 0  # 수집한 아이템 수
distance = 0  # 누적 이동 거리
current_distance = 0  # 현재 이동 거리 (100m 단위로 리셋됨)
distance_speed = 1  # 10ms마다 1씩 증가 (1초당 100m 이동)
game_over = False  # 게임 오버 상태
running = True  # 게임 루프 실행 여부
fps = 60  # 현재 FPS
slow_motion_start_time = None  # 슬로우 모션 효과의 시작 시간
slow_motion_duration = 1000  # 슬로우 모션 지속 시간 (밀리초)
stage = 1  # 현재 스테이지 번호

# 인트로 상태 변수
intro = True  # 인트로 화면 활성화 여부

# 운석 리스트
meteo_list = []  # 운석 객체를 저장하는 리스트

# 시간 관리 객체 초기화
ticks_manager = TicksManager()  # 게임 내 시간 관리를 위한 TicksManager 객체 생성
last_distance_update = ticks_manager.get_ticks()  # 거리 업데이트를 위한 마지막 시간 저장
meteo_spawn_interval = 5000  # 운석 생성 간격 (5초)
last_meteo_spawn_time = 3000  # 마지막 운석 생성 시점 (초기값)

# 플레이어 객체 생성
player = Player(
    x=SCREEN_WIDTH // 2 - 25,  # 화면 중앙에 위치
    y=SCREEN_HEIGHT - 130,  # 화면 아래쪽에 위치
    width=100, height=100,  # 플레이어의 크기 설정
    speed=5,  # 이동 속도
    color=BLUE,  # 기본 색상
    image_path="player_image.png"  # 플레이어 이미지 경로
)

# 몬스터 생성 (한 줄)
monster_row = Monster.create_row(
    screen_width=SCREEN_WIDTH,  # 화면 크기에 맞는 몬스터 행 생성
    y=-80,  # 초기 y 좌표 (화면 위쪽 밖에서 시작)
    count=5,  # 한 줄에 등장하는 몬스터 수
    margin=20,  # 화면 양쪽의 여백
    stage=stage,  # 현재 스테이지
    image_path="normal_monster.png",  # 일반 몬스터 이미지 경로
    special_image_path="special_monster.png"  # 특별 몬스터 이미지 경로
)

# 보스 관련 변수 초기화
boss_image_path = "boss_image.png"  # 보스 이미지 경로
boss = None  # 보스 객체 (초기값은 None)
boss_active = False  # 보스 활성화 여부
boss_spawn_distance = 1000  # 보스가 등장할 거리
stage_cleared = False  # 스테이지 클리어 여부
boss_warning = False  # 보스 경고 상태
boss_warning_start_time = None  # 보스 경고 시작 시간
boss_spawn_delay = 2000  # 보스가 등장하기까지의 딜레이 (2초)

# 코인 및 아이템 리스트 초기화
coin_list = []  # 코인 객체 리스트
item_list = []  # 아이템 객체 리스트

# 운석 경고 메시지용 폰트 설정
font = pygame.font.SysFont(None, 36)  # 기본 폰트 크기 36 설정

# 스크롤 배경 생성
background = ScrollingBackground(
    SCREEN_WIDTH, SCREEN_HEIGHT, "background.png", speed=5  # 배경 스크롤 속도 설정
)

# 어두운 필터 추가 (화면 전체의 투명 필터 효과)
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 크기에 맞는 Surface 생성
overlay.fill((0, 0, 0))  # 검정색으로 채우기
overlay.set_alpha(100)  # 투명도 설정 (0-255)

# 게임 루프
while running:
    # 인트로 화면 처리
    if intro:
        draw_intro(screen, BLACK, WHITE)  # 인트로 화면 출력
        pygame.display.flip()  # 화면 업데이트 (인트로 화면 출력)

        # 이벤트 처리 (인트로에서 게임 시작을 기다림)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                running = False  # 게임 종료
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter 키 입력 시
                intro = False  # 인트로 종료
        continue  # 인트로 상태 유지

    # 게임 오버 상태 확인
    if player.lives <= 0:  # 플레이어 생명이 0 이하인 경우
        game_over = True  # 게임 오버 상태로 전환

    # 게임 오버 화면 표시
    if game_over:
        draw_game_over(screen, BLACK, WHITE)  # 게임 오버 화면을 그리기
        pygame.display.flip()  # 화면 업데이트
        for event in pygame.event.get():  # 이벤트 처리 루프
            if event.type == pygame.QUIT:  # 창을 닫는 이벤트가 발생한 경우
                running = False  # 게임 종료
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # R 키를 누르면 게임 재시작
                # 게임 상태 초기화
                player.lives = 3  # 플레이어 생명 초기화
                score = [0]  # 점수 초기화
                coins = 0  # 코인 수 초기화
                items_collected = 0  # 수집한 아이템 수 초기화
                distance = 0  # 이동 거리 초기화
                current_distance = 0  # 현재 이동 거리 초기화
                meteo_list.clear()  # 운석 리스트 초기화
                coin_list.clear()  # 코인 리스트 초기화
                item_list.clear()  # 아이템 리스트 초기화
                monster_row = Monster.create_row(  # 새로운 몬스터 줄 생성
                    screen_width=SCREEN_WIDTH, y=-80, count=5, margin=20, stage=stage,
                    image_path="normal_monster.png", special_image_path="special_monster.png"
                )
                player = Player(
                    x=SCREEN_WIDTH // 2 - 25,  # 화면 중앙에 위치
                    y=SCREEN_HEIGHT - 130,  # 화면 아래쪽에 위치
                    width=100, height=100,  # 플레이어의 크기 설정
                    speed=5,  # 이동 속도
                    color=BLUE,  # 기본 색상
                    image_path="player_image.png"  # 플레이어 이미지 경로
                )
                ticks_manager.reset_ticks()  # 시간 초기화
                last_distance_update = ticks_manager.get_ticks()  # 거리 업데이트 초기화
                game_stage_complete = False  # 스테이지 상태 초기화
                boss = None  # 보스 객체 초기화
                boss_active = False  # 보스 활성화 상태 초기화
                boss_warning = False  # 보스 경고 상태 초기화
                game_over = False  # 게임 오버 상태 초기화
                fps = MAX_FPS  # FPS 초기화
                slow_motion_start_time = None  # 슬로우 모션 초기화
        continue  # 루프 재시작

    # 배경 업데이트 및 그리기
    background.update()  # 배경 업데이트
    background.draw(screen)  # 배경 그리기
    # 화면에 배경 그린 후 필터 추가
    background.draw(screen)  # 배경을 다시 그리기
    screen.blit(overlay, (0, 0))  # 어두운 필터를 화면 위에 덧씌우기
    #screen.fill(WHITE)  # 디버깅용 배경 흰색 설정 (주석 처리된 상태)
    current_time = ticks_manager.get_ticks()  # 현재 시간 갱신

    # 거리 측정 및 업데이트
    if current_time - last_distance_update >= 10:  # 마지막 업데이트 이후 10ms 경과 시
        current_distance += distance_speed  # 현재 이동 거리 증가
        if current_distance >= 100:  # 100m에 도달하면
            current_distance = 0  # 현재 이동 거리 리셋
        distance += distance_speed  # 누적 거리 증가
        last_distance_update = current_time  # 마지막 업데이트 시간 갱신
        score[0] += distance_speed  # 점수 증가

    # 이벤트 처리
    for event in pygame.event.get():  # 이벤트 큐에서 이벤트를 가져옴
        if event.type == pygame.QUIT:  # 창 닫기 이벤트 발생
            running = False  # 게임 종료

    keys = pygame.key.get_pressed()  # 현재 키 입력 상태 확인

    # 플레이어 관련 업데이트
    player.auto_shoot()  # 자동 발사 기능
    player.update_bullet_effect(ticks_manager)  # 탄환 효과 업데이트
    player.move(keys, SCREEN_WIDTH)  # 플레이어 이동
    player.draw(screen)  # 플레이어 그리기
    player.update_bullets(screen)  # 플레이어의 탄환 업데이트
    player.update_magnet(  # 자석 효과 업데이트
        ticks_manager=ticks_manager,
        coin_list=coin_list,
        item_list=item_list,
        coins=coins
    )

    # 운석 생성
    if current_time - last_meteo_spawn_time > meteo_spawn_interval:  # 마지막 운석 생성 이후 지정된 간격 초과 시
        meteo_list.append(Meteo.create_random(SCREEN_WIDTH, "meteo_image.png"))  # 랜덤 위치에 운석 생성
        last_meteo_spawn_time = current_time  # 마지막 운석 생성 시간 갱신

    # 운석 이동 및 충돌 처리
    for meteo in meteo_list[:]:  # 운석 리스트 복사본을 순회
        meteo.update_state()  # 운석 상태 업데이트

        if meteo.state == "warning":  # 운석이 경고 상태일 때
            meteo.draw_warning(screen, font)  # 경고 메시지 그리기
            meteo.draw_guide_line(screen, SCREEN_HEIGHT)  # 유도선 그리기
        elif meteo.state == "falling":  # 운석이 낙하 상태일 때
            meteo.move()  # 운석 이동
            meteo.draw(screen)  # 운석 그리기

        if meteo.y > SCREEN_HEIGHT:  # 운석이 화면 아래로 벗어나면
            meteo_list.remove(meteo)  # 운석 제거

        if meteo.state == "falling" and player.rect.colliderect(meteo.rect) and not player.is_hyper_flight_active():
            # 운석이 낙하 중이고, 플레이어와 충돌했으며, 하이퍼 플라이트 상태가 아닐 때
            player.lives -= 1  # 플레이어 생명 감소
            slow_motion_start_time = ticks_manager.get_ticks()  # 슬로우 모션 시작 시간 기록
            meteo_list.remove(meteo)  # 충돌한 운석 제거

    # 몬스터 관련 업데이트
    for monster in monster_row[:]:  # 현재 화면의 몬스터 리스트를 순회
        monster.move()  # 몬스터 이동
        if monster.y > SCREEN_HEIGHT:  # 몬스터가 화면 아래로 벗어난 경우
            monster_row.remove(monster)  # 몬스터 리스트에서 제거
        else:
            monster.draw(screen)  # 화면에 몬스터를 그리기

    if not boss_active:  # 보스가 활성화되지 않은 경우에만 몬스터 충돌 처리
        Monster.handle_collision(
            monsters=monster_row,  # 현재 몬스터 리스트
            bullets=player.bullets,  # 플레이어의 탄환 리스트
            score=score,  # 점수 업데이트
            coin_list=coin_list,  # 충돌로 생성된 코인 리스트
            item_list=item_list  # 충돌로 생성된 아이템 리스트
        )

    if player.is_hyper_flight_active():  # 플레이어가 하이퍼 플라이트 상태일 때
        Monster.handle_hyper_flight_collision(
            monsters=monster_row,  # 현재 몬스터 리스트
            mid_screen_height=SCREEN_HEIGHT // 2,  # 화면 중간 높이를 기준으로 충돌 처리
            score=score,  # 점수 업데이트
            coin_list=coin_list,  # 생성된 코인 리스트
            item_list=item_list,  # 생성된 아이템 리스트
            item_spawn_chance=30,  # 아이템 생성 확률 (30%)
        )

    for monster in monster_row[:]:  # 현재 몬스터 리스트 순회
        if player.rect.colliderect(monster.rect) and not player.is_hyper_flight_active():
            # 몬스터와 플레이어가 충돌하고 하이퍼 플라이트 상태가 아닌 경우
            player.lives -= 1  # 플레이어의 생명 감소
            slow_motion_start_time = ticks_manager.get_ticks()  # 슬로우 모션 시작 시간 기록
            monster_row.remove(monster)  # 충돌한 몬스터 제거

    if not monster_row and not boss_active and not boss_warning:
        # 모든 몬스터가 제거되었고 보스가 없으며 보스 경고 상태가 아닌 경우
        monster_row = Monster.create_row(  # 새로운 몬스터 행 생성
            screen_width=SCREEN_WIDTH,  # 화면 크기에 맞게 배치
            y=-80,  # 초기 y 위치 (화면 밖에서 시작)
            count=5,  # 몬스터 수
            margin=20,  # 가장자리 간격
            stage=stage,  # 현재 스테이지
            image_path="normal_monster.png",  # 일반 몬스터 이미지 경로
            special_image_path="special_monster.png"  # 특별 몬스터 이미지 경로
        )

    # 아이템 및 코인 이동 및 충돌 처리
    for item in item_list[:]:  # 아이템 리스트 순회
        item.move()  # 아이템 이동
        if item.y > SCREEN_HEIGHT:  # 아이템이 화면 아래로 벗어난 경우
            item_list.remove(item)  # 아이템 제거
        else:
            item.draw(screen)  # 아이템 화면에 그리기

    for coin in coin_list[:]:  # 코인 리스트 순회
        coin.move()  # 코인 이동
        if coin.y > SCREEN_HEIGHT:  # 코인이 화면 아래로 벗어난 경우
            coin_list.remove(coin)  # 코인 제거
        else:
            coin.draw(screen)  # 코인 화면에 그리기

        if player.rect.colliderect(coin.rect):  # 플레이어와 코인이 충돌한 경우
            coins += coin.value  # 플레이어의 코인 개수 증가
            coin_list.remove(coin)  # 충돌한 코인 제거

    for item in item_list[:]:  # 아이템 리스트 순회
        if player.rect.colliderect(item.rect):  # 플레이어와 아이템이 충돌한 경우
            if item.type == 'bullet':  # 탄환 증가 아이템인 경우
                player.increase_bullet_count()  # 플레이어의 탄환 수 증가
            elif item.type == 'magnet':  # 자석 아이템인 경우
                player.activate_magnet(ticks_manager, duration=5000)  # 자석 효과 활성화 (5초 지속)
            elif item.type == 'hyper_flight':  # 하이퍼 플라이트 아이템인 경우
                player.activate_hyper_flight(ticks_manager, duration=5000)  # 하이퍼 플라이트 활성화
                distance += 1000  # 추가 거리 보상
                monster_row.clear()  # 화면의 몬스터 제거
            item_list.remove(item)  # 충돌한 아이템 제거

    if player.is_hyper_flight_active():  # 플레이어가 하이퍼 플라이트 상태일 때
        fps = 600  # FPS를 600으로 증가 (고속 비행 효과 제공)
        distance += distance_speed * 10  # 거리 증가 속도 10배
    else:
        fps = max(fps - 10, MAX_FPS)  # FPS를 천천히 기본 값으로 복구

    player.update_hyper_flight(ticks_manager)  # 하이퍼 플라이트 상태 업데이트

    draw_score_and_items(  # 화면에 점수 및 아이템 상태 표시
        surface=screen,
        score=score[0],  # 현재 점수
        coins=coins,  # 획득한 코인 수
        distance=distance,  # 이동 거리
        color=WHITE,  # 글자 색상
        bullet_effect_time_left=None,  # 탄환 효과 남은 시간 (현재는 None)
        hyper_flight_time_left=None,  # 하이퍼 플라이트 남은 시간 (현재는 None)
        hyper_flight_message=player.get_hyper_flight_message(),  # 하이퍼 플라이트 메시지
        magnet_time_left=player.get_magnet_time_left(ticks_manager),  # 자석 효과 남은 시간
        bullet_level=player.get_bullet_level(),  # 플레이어의 탄환 레벨
    )
    draw_lives(screen, player.lives, HEART_RED)  # 플레이어 생명 표시

    if slow_motion_start_time is not None:  # 슬로우 모션이 활성화된 경우
        elapsed_time = ticks_manager.get_ticks() - slow_motion_start_time  # 슬로우 모션 경과 시간 계산
        if elapsed_time < slow_motion_duration:  # 슬로우 모션 지속 시간 내인 경우
            fps = 10  # FPS를 10으로 설정 (느린 효과)
        else:  # 슬로우 모션이 끝난 경우
            slow_motion_start_time = None  # 슬로우 모션 비활성화
            fps = MAX_FPS  # 기본 FPS로 복구
    else:
        if fps < MAX_FPS:  # FPS가 기본 값보다 낮은 경우
            fps = min(fps + 3, MAX_FPS)  # 천천히 기본 FPS로 복구

    if boss_warning:  # 보스 경고 상태일 때
        if boss_warning_start_time is None:  # 보스 경고 시작 시간이 없는 경우

            boss_warning_start_time = ticks_manager.get_ticks()  # 보스 경고 시작 시간 기록

        # "Boss is Coming!" 경고 메시지 표시
        warning_text = font.render("Boss is Coming!", True, (255, 0, 0))  # 경고 텍스트 생성
        warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # 화면 중앙에 위치 설정
        screen.blit(warning_text, warning_rect)  # 화면에 경고 텍스트 표시

        # 보스 경고 시간이 경과하면 보스 활성화
        if ticks_manager.get_ticks() - boss_warning_start_time > boss_spawn_delay:
            boss_active = True  # 보스를 활성화 상태로 전환
            boss_warning = False  # 보스 경고 상태 종료
            boss = Boss(  # 새로운 보스 생성
                x=SCREEN_WIDTH // 2 - 400 // 2,  # 화면 중앙에 보스 배치
                y=0,  # 화면 위쪽에서 시작
                stage=stage,  # 현재 스테이지 정보 전달
                image_path=boss_image_path  # 보스 이미지 경로
            )

    # 보스가 등장할 거리 조건 충족 시 경고 활성화
    if distance >= boss_spawn_distance and not boss_active and not boss_warning and not player.is_hyper_flight_active():
        boss_warning = True  # 보스 경고 활성화
        boss_warning_start_time = None  # 경고 시작 시간 초기화

    if boss_active and not player.is_hyper_flight_active():  # 보스가 활성화되고 하이퍼 플라이트 상태가 아닐 때
        boss.draw(screen)  # 화면에 보스 그리기
        if boss.y < 120:  # 보스가 지정된 y 위치까지 내려오도록 이동
            boss.y += 1  # y 좌표 증가
        else:
            boss.move(SCREEN_WIDTH)  # 보스가 좌우로 움직임

        # 플레이어의 탄환과 보스의 충돌 처리
        for bullet in player.bullets[:]:
            if bullet.rect.colliderect(boss.rect):  # 탄환이 보스와 충돌한 경우
                boss.take_damage(10)  # 보스의 체력을 10만큼 감소
                player.bullets.remove(bullet)  # 충돌한 탄환 제거

        # 플레이어와 보스의 충돌 처리
        if boss.rect.colliderect(player.rect):
            player.lives -= 3  # 플레이어 생명을 3 감소

            if player.lives > 0:  # 플레이어가 아직 생존 중이라면
                boss.y += boss.height  # 보스를 화면 아래로 밀어냄

        # 보스의 제한 시간이 초과되었는지 확인
        if boss.is_time_up():
            boss.y += boss.speed  # 보스를 아래로 이동
            if boss.y > SCREEN_HEIGHT:  # 보스가 화면 아래로 완전히 사라진 경우
                boss_active = False  # 보스 비활성화
                boss = None  # 보스 객체 제거
                print("Boss escaped!")  # 보스 도주 메시지 출력

        # 보스가 처치된 경우
        if boss.health <= 0:
            boss_active = False  # 보스 비활성화
            boss = None  # 보스 객체 제거
            stage_cleared = True  # 스테이지 클리어 상태로 전환
            score[0] += 100000  # 보스 처치 점수 추가

    # 스테이지 클리어 처리
    if stage_cleared:
        screen.fill(WHITE)  # 화면 초기화
        stage_text = font.render("{} STAGE CLEAR!".format(stage), True, (0, 255, 0))  # 스테이지 클리어 메시지 생성
        text_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # 화면 중앙에 메시지 위치 설정
        screen.blit(stage_text, text_rect)  # 화면에 메시지 표시
        pygame.display.flip()  # 화면 업데이트
        pygame.time.delay(3000)  # 3초간 대기
        stage += 1  # 다음 스테이지로 진행
        stage_cleared = False  # 스테이지 클리어 상태 초기화

    pygame.display.flip()  # 화면 업데이트
    clock.tick(fps)  # FPS에 따라 루프 속도 제어

pygame.quit()  # 게임 종료 및 Pygame 리소스 해제
