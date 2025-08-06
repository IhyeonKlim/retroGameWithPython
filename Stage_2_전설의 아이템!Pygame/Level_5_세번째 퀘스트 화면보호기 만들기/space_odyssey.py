import pygame
import random
import math

class Star:
    def __init__(self, screen, index):
        self.size = 1
        self.color = (255, 255, 255)

        self.center = {
            'x': screen.get_width() / 2,
            'y': screen.get_height() / 2
        }
        self.radius = 0
        self.theta = 0

        self.screen = screen

        self.init(index)

    def get_limit_distance(self):
        return int(math.sqrt(math.pow(self.center['x'], 2) + 
                             math.pow(self.center['y'], 2)))

    def init(self, index):
        self.radius = float(random.randint(0, self.get_limit_distance()))
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        self.degree = (360 / 50) * index
        self.theta = float(self.degree) * math.pi / 180

    def draw(self, color):
        x = self.center['x'] + self.radius * math.cos(self.theta)
        y = self.center['y'] + self.radius * math.sin(self.theta)

        pygame.draw.circle(self.screen, color, [x, y], self.size)
        pygame.display.update()

    def move(self):
        self.draw((0, 0, 0))

        self.radius += 1 + (float(self.radius) / 10)
        self.size = 1 + (self.radius / 100)

        self.draw(self.color)

        if self.radius > self.get_limit_distance():
            self.radius = float(random.randint(0, self.get_limit_distance()))

screen_size = {
    'width': 1024,
    'height': 768
}

pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("Space Odyssey")

stars = []
for i in range(0, 50):
    star = Star(screen, i)
    stars.append(star)

count = 0
delay = 1000
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    count += 1
    if count > delay:
        count = 0
        for star in stars:
            star.move()