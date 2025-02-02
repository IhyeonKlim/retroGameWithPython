import pygame

class Bullet:
    def __init__(self, x, y, width=5, height=10, speed=10, color=(255, 0, 0), damage=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.damage = damage  # 탄환의 데미지 추가

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """탄환 이동"""
        self.y -= self.speed

    def draw(self, surface):
        """탄환을 화면에 그리기"""
        pygame.draw.rect(surface, self.color, self.rect)
