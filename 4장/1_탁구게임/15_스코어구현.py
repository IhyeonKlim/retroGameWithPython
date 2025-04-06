import sys
import pygame
from pygame import QUIT, KEYDOWN, K_TAB, Rect

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("ping pong game")

# 색상 정의
BLACK = (0, 0, 0)  # 배경색 (검정)
WHITE = (255, 255, 255)  # 테두리 및 점선 (하얀색)
RED = (255, 0, 0)  # 빨간색 (꼭지점 및 라켓 표시용)

# FPS 설정
fps_value = 60
clock = pygame.time.Clock()

# 테두리 및 여백 설정
border_thickness = 10  # 테두리 두께
horizontal_padding = 60  # 좌우 패딩
vertical_padding = 40  # 위아래 패딩

# 플레이 구역 설정
play_area_x = border_thickness + horizontal_padding  # 구역의 X 좌표 시작점
play_area_y = border_thickness + vertical_padding  # 구역의 Y 좌표 시작점
play_area_width = screen_width - 2 * (border_thickness + horizontal_padding)  # 구역의 너비
play_area_height = screen_height - 2 * (border_thickness + vertical_padding)  # 구역의 높이

# 점선 설정
dashed_line_width = 10  # 점선의 두께
dash_height = 20  # 점선의 한 개 길이
gap_between_dashes = 20  # 점선 사이의 간격

# 꼭지점 좌표 계산
top_left = (play_area_x, play_area_y)
top_right = (play_area_x + play_area_width, play_area_y)
bottom_left = (play_area_x, play_area_y + play_area_height)
bottom_right = (play_area_x + play_area_width, play_area_y + play_area_height)

#keyboard를 계속 입력받도록 하는 코드
pygame.key.set_repeat(5, 5)

def draw_center_dashed_line(surface, color, start_x, start_y, height, dash_height, gap_height, line_width):
    """ 중앙에 수직 점선을 쉽게 그리는 함수 """
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y), (start_x, y + dash_height), line_width)

# 폰트 설정 (스코어 표시용)
font = pygame.font.Font(None, 50)  # 크기 50의 기본 폰트 사용

# 스코어 변수 초기화
player1_score = 0
player2_score = 0


# 공 클래스 정의
class Ball:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 20, 20)  # 공의 크기 설정 (가로 20, 세로 20)
        self.rect.centerx = x  # 공의 X축 중심 좌표
        self.rect.centery = y  # 공의 Y축 중심 좌표

        # 속도 및 방향 설정
        self.speed = 4  # 초기 속도 설정 (픽셀 단위)
        self.direction_x = 1  # X축 방향 (1: 오른쪽, -1: 왼쪽)
        self.direction_y = 1  # Y축 방향 (1: 아래쪽, -1: 위쪽)
        self.acceleration = 1.1  # 가속도 설정 (충돌 시 10% 속도 증가)
        self.max_speed = 8  # 최대 속도 제한
        self.enable = True # 공이 활성화 되어있는 상태

    # player1과 player2의 객체를 파라미터로 받습니다. (공이 움직일 때 체크하기 위해서)
    def move(self, player1, player2):
        global player1_score, player2_score
        # 공의 위치 업데이트
        self.rect.centerx += self.speed * self.direction_x
        self.rect.centery += self.speed * self.direction_y

        # 왼쪽 경계를 벗어난 경우 player2 스코어 증가
        if self.rect.left <= play_area_x:
            player2_score = player2_score + 1
            self.reset()

        # 오른쪽 경계를 벗어난 경우 player1 스코어 증가
        if self.rect.right >= play_area_x + play_area_width:
            player1_score = player1_score + 1
            self.reset()

        # 위쪽 경계에 부딪힌 경우
        if self.rect.top <= play_area_y:
            self.direction_y *= -1  # Y축 방향 반전
            self.increase_speed()  # 속도 증가

        # 아래쪽 경계에 부딪힌 경우
        if self.rect.bottom >= play_area_y + play_area_height:
            self.direction_y *= -1  # Y축 방향 반전
            self.increase_speed()  # 속도 증가

        # 플레이어와의 충돌 처리 colliderect 함수를 사용하여 간단하게 구현합니다.
        if self.rect.colliderect(player1.rect) or self.rect.colliderect(player2.rect):
            self.direction_x *= -1  # X축 방향 반전
            self.increase_speed()  # 속도 증가

    def increase_speed(self):
        """속도를 증가시키되 최대 속도를 초과하지 않도록 제한"""
        new_speed = self.speed * self.acceleration  # 속도 증가
        self.speed = min(new_speed, self.max_speed)  # 최대 속도를 9로 제한

    #공을 초기화 시키는 메서드
    def reset(self):
        # 화면의 중앙에 오도록 x,y 좌표값을 초기화 시킵니다.
        self.rect.centerx = play_area_x + play_area_width // 2
        self.rect.centery = play_area_y + play_area_height // 2
        # 속도 역시 초기화 시켜줍니다.
        self.speed = 4
        # 공이 활성화 되지 않도록 하는 변수
        self.enable = False


# 플레이어 클래스 정의
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)  # 라켓의 크기와 위치
        self.rect.centerx = x
        self.rect.centery = y
        self.top = self.rect.top  # 초기 top 값 설정
        self.bottom = self.rect.bottom  # 초기 bottom 값 설정

    def update_position(self):
        """현재 rect의 top과 bottom 값을 업데이트"""
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def move_up(self):
        self.rect.centery -= 5
        self.update_position()

    def move_down(self):
        self.rect.centery += 5
        self.update_position()

# 플레이어 1 (왼쪽)
# 라켓의 Y 위치를 play_area의 중앙에 맞춤
player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)

# 플레이어 2 (오른쪽)
# 라켓의 X 위치를 play_area의 가로길이 만큼 이동
# 라켓의 Y 위치를 play_area의 중앙에 맞춤
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

# 공 객체 생성
ball = Ball(play_area_x + play_area_width // 2, play_area_y + play_area_height // 2)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_TAB and not ball.enable:
                ball.enable = True  # 공 활성화

    # 동시에 여러 키 입력 처리
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player1.top > play_area_y:
        player1.move_up()
    if keys[pygame.K_s] and player1.bottom < play_area_y + play_area_height:
        player1.move_down()
    if keys[pygame.K_UP] and player2.top > play_area_y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.bottom < play_area_y + play_area_height:
        player2.move_down()

    screen.fill(BLACK)

    # 플레이 구역 바깥에 테두리 그리기 (테두리가 안쪽으로 침범되지 않도록)
    outer_rect_x = play_area_x - border_thickness
    outer_rect_y = play_area_y - border_thickness
    outer_rect_width = play_area_width + 2 * border_thickness
    outer_rect_height = play_area_height + 2 * border_thickness
    pygame.draw.rect(screen, WHITE, (outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height), border_thickness)

    # 중앙에 점선을 그림
    mid_x = play_area_x + play_area_width // 2  # 중앙선 X 좌표 계산
    draw_center_dashed_line(screen, WHITE, mid_x, play_area_y, play_area_height, dash_height, gap_between_dashes, dashed_line_width)

    # 플레이어1 라켓 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    # 플레이어2 라켓 그리기
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 이동 및 충돌 처리
    if ball.enable:
        ball.move(player1, player2)

    # 화면 그리기
    # 공 그리기
    pygame.draw.rect(screen, WHITE, ball.rect)

    # 스코어 표시 (00 형식)
    player1_score_text = font.render(f"{player1_score:02}", True, WHITE)
    player2_score_text = font.render(f"{player2_score:02}", True, WHITE)\

    # 플레이어 1 스코어 위치 (왼쪽 1/4 지점, 테두리 위)
    player1_score_pos = (
        screen_width // 4 - player1_score_text.get_width() // 2,  # X 좌표 중앙 정렬
        10  # 화면 위쪽에 10px 간격
    )

    # 플레이어 2 스코어 위치 (오른쪽 3/4 지점, 테두리 위)
    player2_score_pos = (
        3 * (screen_width // 4) - player2_score_text.get_width() // 2,  # X 좌표 중앙 정렬
        10  # 화면 위쪽에 10px 간격
    )
    # 스코어 텍스트를 화면에 그리기
    screen.blit(player1_score_text, player1_score_pos)
    screen.blit(player2_score_text, player2_score_pos)

    # 화면 업데이트 및 FPS 유지
    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
