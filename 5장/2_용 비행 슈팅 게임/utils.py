import pygame

# 폰트 초기화
pygame.font.init()
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

def draw_score_and_items(surface, score, coins, distance, color,
                         bullet_effect_time_left=None, hyper_flight_time_left=None, hyper_flight_message=None, magnet_time_left=None, bullet_level=1):
    """
    점수와 코인, 아이템, 거리, 남은 효과 시간 표시.
    - bullet_effect_time_left: 남은 총알 효과 시간 (초 단위)
    - hyper_flight_time_left: 남은 하이퍼 플라이트 시간 (초 단위)
    - hyper_flight_message: 하이퍼 플라이트 메시지
    """
    score_text = font.render(f"Score: {score}", True, color)
    coin_text = font.render(f"Coins: {coins}", True, color)
    distance_text = font.render(f"{distance}", True, color)
    m_text = font.render("m", True, color)
    bullet_level_text = font.render(f"Bullet Lv: {bullet_level}", True, color)

    surface.blit(score_text, (10, 10))
    surface.blit(coin_text, (10, 50))
    surface.blit(distance_text, (surface.get_width() - 130, 10))
    surface.blit(m_text, (surface.get_width() - 60, 10))
    surface.blit(bullet_level_text, (10, 600))

    # 총알 효과 시간 남은 경우 표시
    if bullet_effect_time_left is not None:
        effect_text = font.render(f"Bullet Time: {bullet_effect_time_left}s", True, color)
        surface.blit(effect_text, (10, 130))

    # 하이퍼 플라이트 시간 남은 경우 표시
    if hyper_flight_time_left is not None:
        hyper_text = font.render(f"Hyper Flight: {hyper_flight_time_left}s", True, color)
        surface.blit(hyper_text, (10, 170))

    # 하이퍼 플라이트 메시지 표시
    if hyper_flight_message:
        message_text = font.render(hyper_flight_message, True, (255, 0, 255))  # 분홍색 텍스트
        surface.blit(message_text, (surface.get_width() // 2 - message_text.get_width() // 2, 200))

    # 자석 효과 시간 남은 경우 표시
    if magnet_time_left is not None:
        magnet_text = font.render(f"Magnet Time: {magnet_time_left}s", True, (0, 0, 255))
        surface.blit(magnet_text, (10, 150))


# 게임 오버 텍스트 그리기
def draw_game_over(surface,BACKGROUND_COLOR, COLOR):
    surface.fill(BACKGROUND_COLOR)
    text = game_over_font.render("GAME OVER", True, COLOR)
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(text, text_rect)

    restart_text = font.render("Press R to Restart!", True, COLOR)
    restart_rect = restart_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 50))
    surface.blit(restart_text, restart_rect)

# 플레이어 하트(lives) 그리기
def draw_lives(surface, lives, HEART_RED):
    heart_width = 30  # 각 하트의 너비
    total_width = lives * heart_width  # 하트 전체의 너비
    start_x = (surface.get_width() - total_width) // 2  # 하트 시작 x 좌표 계산

    for i in range(lives):
        heart_x = start_x + i * heart_width  # 각 하트의 x 좌표
        heart_y = surface.get_height() - 50  # 하트의 y 좌표
        pygame.draw.polygon(surface, HEART_RED, [
            (heart_x, heart_y),
            (heart_x + 10, heart_y + 10),
            (heart_x + 20, heart_y),
            (heart_x + 10, heart_y - 20)
        ])


# 인트로 화면 그리기
def draw_intro(surface, BACKGROUND_COLOR, TEXT_COLOR):
    surface.fill(BACKGROUND_COLOR)
    intro_text = game_over_font.render("Press ENTER to Start!", True, TEXT_COLOR)
    intro_rect = intro_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(intro_text, intro_rect)
