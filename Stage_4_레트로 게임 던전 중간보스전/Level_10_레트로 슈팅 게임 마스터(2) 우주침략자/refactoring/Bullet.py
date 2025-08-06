import pygame
import Config
from pygame.locals import Rect

# 총알 클래스: 플레이어와 적이 사용하는 탄환 오브젝트
class Bullet:
    def __init__(self, color=Config.WHITE):
        self.rect = Rect(0, 0, 3, 7)      # 총알 크기 정의 (가로 3px, 세로 7px)
        self.enabled = False              # 활성화 여부 (화면에 발사되었는지)
        self.color = color                # 총알 색상 (기본: 흰색)

    # 총알 발사 메서드
    def fire(self, x, y):
        if self.enabled:
            return False                  # 이미 발사된 총알이면 무시
        self.rect.centerx = x             # X좌표 기준으로 중앙 정렬
        self.rect.y = y - self.rect.height  # Y좌표 기준 위쪽에 위치
        self.enabled = True               # 총알 활성화
        return True

    # 총알 그리기 (화면에 렌더링)
    def draw(self, surface):
        if self.enabled:
            pygame.draw.rect(surface, self.color, self.rect)  # 활성화된 총알만 그림

    # 위로 이동 (플레이어 총알)
    def move_up(self):
        if self.enabled:
            self.rect.centery -= 3        # 위로 3픽셀 이동
            if self.rect.centery < 0:
                self.enabled = False      # 화면을 벗어나면 비활성화

    # 아래로 이동 (적 총알)
    def move_down(self, screen_height):
        if self.enabled:
            self.rect.centery += 3        # 아래로 3픽셀 이동
            if self.rect.centery > screen_height:
                self.enabled = False      # 화면을 벗어나면 비활성화
