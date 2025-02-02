import pygame
import random

class Item:
    default_radius = 15  # 아이템 기본 크기
    BULLET_COLOR = (0, 0, 0)  # 검정색 총알 아이템 색상
    MAGNET_COLOR = (0, 255, 255)  # 하늘색 자석 아이템 색상

    def __init__(self, x, y, item_type='coin', radius=default_radius, color=(0, 255, 0), x_velocity=None, y_velocity=-6, gravity=0.3):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.type = item_type  # 아이템 종류 ('bullet', 'hyper_flight', 등)
        self.x_velocity = x_velocity if x_velocity is not None else random.randint(-3, 3)
        self.y_velocity = y_velocity
        self.gravity = gravity

    @property
    def rect(self):
        """아이템의 충돌 영역 반환"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        """포물선 이동"""
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.y_velocity += self.gravity  # 중력 효과 추가

        # 화면 경계 충돌 처리 (좌우 반사)
        if self.x - self.radius <= 0 or self.x + self.radius >= 540:  # 화면 크기 하드코딩 (수정 가능)
            self.x_velocity = -self.x_velocity

    def draw(self, surface):
        """아이템을 화면에 그리기"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    @classmethod
    def create_bullet_item(cls, x, y):
        """총알 아이템 생성"""
        return cls(x=x, y=y, item_type='bullet', color=cls.BULLET_COLOR)
    @classmethod
    def create_hyper_flight_item(cls, x, y):
        """Hiper Flight 아이템 생성"""
        return cls(x=x, y=y, item_type='hyper_flight', color=(255, 0, 255))  # 분홍색

    @classmethod
    def create_magnet_item(cls, x, y):
        """자석 아이템 생성"""
        return cls(x=x, y=y, item_type='magnet', color=cls.MAGNET_COLOR)