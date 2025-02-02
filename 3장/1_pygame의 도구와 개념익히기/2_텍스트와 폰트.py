import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color and Font Example")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 화면 배경을 흰색으로 설정
screen.fill(WHITE)

# 텍스트와 폰트 설정
font = pygame.font.SysFont('Arial', 40)  # Arial 폰트, 크기 40
text_surface = font.render("Hello, Pygame!", True, BLUE)  # 텍스트 색상을 파란색으로
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 텍스트를 화면 중앙에 배치

# 게임 루프 (텍스트를 잠시 띄우고 종료)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 텍스트를 화면에 그리기
    screen.fill(WHITE)  # 배경을 흰색으로 유지
    screen.blit(text_surface, text_rect)  # 텍스트를 화면에 그리기
    pygame.display.flip()  # 화면 업데이트

# Pygame 종료
pygame.quit()
