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
pygame.display.set_caption("Ping Pong Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS 설정
fps_value = 60  # 초당 60프레임
clock = pygame.time.Clock()

# 테두리 및 여백 설정
border_thickness = 10
horizontal_padding = 60
vertical_padding = 40

# 플레이 구역 설정
play_area_x = border_thickness + horizontal_padding
play_area_y = border_thickness + vertical_padding
play_area_width = screen_width - 2 * (border_thickness + horizontal_padding)
play_area_height = screen_height - 2 * (border_thickness + vertical_padding)

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
        """공을 방향에 따라 이동시키는 메서드"""
        # 공의 위치 업데이트
        self.rect.centerx += self.speed * self.direction_x
        self.rect.centery += self.speed * self.direction_y

        # 왼쪽 경계에 부딪힌 경우
        if self.rect.left <= play_area_x:
            #기존의 반전값과 속도 증가 메서드를 삭제합니다.
            self.reset() # 다시 시작하는 초기화 함수

        # 오른쪽 경계에 부딪힌 경우
        if self.rect.right >= play_area_x + play_area_width:
            #기존의 반전값과 속도 증가 메서드를 삭제합니다.
            self.reset() # 다시 시작하는 초기화 함수

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
        # 방향은 초기화 하지 않습니다. (이유는 나중에 설명드리죠)
        # 공이 활성화 되지 않도록 하는 메서드
        self.enable = False


# 플레이어 클래스 정의
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)
        self.rect.centerx = x
        self.rect.centery = y

    def move_up(self):
        self.rect.centery -= 5

    def move_down(self):
        self.rect.centery += 5

# 플레이어 객체 생성
player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

# 공 객체 생성
ball = Ball(play_area_x + play_area_width // 2, play_area_y + play_area_height // 2)

# 게임 루프 시작
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # tab 키를 누르는 경우 공을 다시 움직이게 합니다. (공이 비활성화시)
            elif event.key == K_TAB and not ball.enable:
                ball.enable = True  # 공 활성화

    # 동시에 여러 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.rect.top > play_area_y:
        player1.move_up()
    if keys[pygame.K_s] and player1.rect.bottom < play_area_y + play_area_height:
        player1.move_down()
    if keys[pygame.K_UP] and player2.rect.top > play_area_y:
        player2.move_up()
    if keys[pygame.K_DOWN] and player2.rect.bottom < play_area_y + play_area_height:
        player2.move_down()


    # 공 이동 및 충돌 처리
    if ball.enable:
        ball.move(player1, player2)

    # 화면 그리기
    screen.fill(BLACK)

    # 테두리 그리기
    outer_rect_x = play_area_x - border_thickness
    outer_rect_y = play_area_y - border_thickness
    outer_rect_width = play_area_width + 2 * border_thickness
    outer_rect_height = play_area_height + 2 * border_thickness
    pygame.draw.rect(screen, WHITE, (outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height), border_thickness)

    # 중앙 점선 그리기
    mid_x = play_area_x + play_area_width // 2
    for y in range(play_area_y, play_area_y + play_area_height, 40):
        pygame.draw.line(screen, WHITE, (mid_x, y), (mid_x, y + 20), 5)

    # 플레이어 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    pygame.draw.rect(screen, WHITE, player2.rect)

    # 공 그리기
    pygame.draw.rect(screen, WHITE, ball.rect)

    # 화면 업데이트 및 FPS 유지
    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
