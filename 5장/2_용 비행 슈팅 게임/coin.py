import pygame
import random

class Coin:
    default_radius = 10
    def __init__(self, x, y, radius=default_radius, color=(255, 223, 0), value=10, coin_type="gold",
                 x_velocity=None, y_velocity=-6, gravity=0.3):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.value = value  # 코인의 가치
        self.type = coin_type  # 코인의 유형
        self.x_velocity = x_velocity if x_velocity is not None else random.randint(-2, 2)
        self.y_velocity = y_velocity
        self.gravity = gravity

    @property
    def rect(self):
        """코인의 충돌 영역 반환"""
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
        """코인을 화면에 그리기"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    @classmethod
    def create_gold_coin(cls, x, y):
        """골드 코인 생성"""
        return cls(x=x, y=y, color=(255, 223, 0), value=10, coin_type="gold")

    @classmethod
    def create_ruby_coin(cls, x, y):
        """루비 코인 생성"""
        return cls(x=x, y=y, color=(255, 0, 0), value=50, coin_type="ruby")

    @classmethod
    def create_sapphire_coin(cls, x, y):
        """사파이어 코인 생성"""
        return cls(x=x, y=y, color=(0, 0, 255), value=100, coin_type="sapphire")

    @classmethod
    def create_emerald_coin(cls, x, y):
        """사파이어 코인 생성"""
        return cls(x=x, y=y, color=(0, 0, 255), value=100, coin_type="sapphire")

    @classmethod
    def create_pearl_coin(cls, x, y):
        """사파이어 코인 생성"""
        return cls(x=x, y=y, color=(0, 0, 255), value=100, coin_type="sapphire")

    @classmethod
    def create_random_coin(cls, x, y):
        """랜덤한 코인 생성"""
        if random.randint(1, 100) <= 10:
            return cls.create_ruby_coin(x, y)
        elif random.randint(1, 100) <= 5:
            return cls.create_sapphire_coin(x, y)
        elif random.randint(1, 100) <= 5:
            return cls.create_emerald_coin(x, y)
        else:
            return cls.create_gold_coin(x, y)