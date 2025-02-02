import pygame
import random
from coin import Coin
from item import Item

class Monster:
    # 클래스 속성: 기본값 설정
    default_width = 80  # 몬스터 기본 가로 크기
    default_height = 80  # 몬스터 기본 세로 크기

    def __init__(self, x, y, width=default_width, height=default_height, speed=3, color=(128, 128, 128), health=10, special=False, stage=1, image_path=None):
        """
        몬스터 객체 초기화
        :param x: 몬스터의 x 좌표
        :param y: 몬스터의 y 좌표
        :param width: 몬스터의 너비
        :param height: 몬스터의 높이
        :param speed: 몬스터 이동 속도
        :param color: 몬스터 색상
        :param health: 몬스터 체력
        :param special: 특별 몬스터 여부
        :param stage: 현재 스테이지
        :param image_path: 몬스터 이미지 경로
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed + stage * 0.1  # 스테이지에 따라 속도 증가
        self.color = color
        self.health = health + stage * 0.1  # 스테이지에 따라 체력 증가
        self.max_health = health  # 최대 체력 저장
        self.special = special  # 특별 몬스터 여부

        # 이미지 로드 및 크기 조정
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))  # 크기 조정
            except pygame.error as e:
                self.image = None  # 이미지 로드 실패 시 None 설정
        else:
            self.image = None

    @property
    def rect(self):
        """몬스터의 충돌 영역 반환"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """몬스터를 아래로 이동"""
        self.y += self.speed

    def draw(self, surface):
        """몬스터를 화면에 그리기"""
        if self.image:  # 이미지가 있는 경우
            surface.blit(self.image, (self.x, self.y))
        else:  # 이미지가 없는 경우 기본 색상으로 사각형 그리기
            pygame.draw.rect(surface, self.color, self.rect)

        # 체력 막대 그리기
        health_ratio = max(0, self.health / self.max_health)  # 체력 비율 계산
        health_bar_width = self.width * health_ratio  # 체력 비율에 따른 너비
        health_bar_height = 5  # 체력 바의 높이
        health_bar_color = (255, 0, 0)  # 빨간색 체력 바

        # 체력바 그리기
        pygame.draw.rect(surface, health_bar_color,
                         (self.x, self.y - health_bar_height - 2, health_bar_width, health_bar_height))

    def take_damage(self, damage):
        """몬스터가 데미지를 받음"""
        self.health -= damage

    @classmethod
    def create_row(cls, screen_width, y, count, margin=20, distance=0, stage=1, image_path=None, special_image_path=None):
        """
        화면의 중심을 기준으로 몬스터를 한 줄로 균등 배치.
        - screen_width: 화면 가로 길이
        - y: 몬스터의 초기 y 좌표
        - count: 몬스터 수
        - margin: 화면 가장자리와 몬스터 간의 최소 거리
        - distance: 누적 이동 거리
        - stage: 현재 스테이지
        - image_path: 일반 몬스터 이미지 경로
        - special_image_path: 특별 몬스터 이미지 경로
        """
        available_width = screen_width - 2 * margin  # 배치 가능한 너비 계산
        gap = (available_width - count * cls.default_width) // (count - 1)  # 몬스터 간 간격 계산
        monsters = []  # 몬스터 리스트 초기화
        start_x = margin  # 첫 번째 몬스터 시작 위치

        special_index = random.randint(0, count - 1)  # 특별 몬스터의 위치 선택

        for i in range(count):
            x = start_x + i * (cls.default_width + gap)  # 각 몬스터의 x 좌표 계산

            # 거리 기반 몬스터 속성 설정
            if distance < 500:
                color = (128, 128, 128)  # 회색
                health = 30
            elif distance < 3000:
                color = (255, 255, 0)  # 노란색
                health = 50
            elif distance < 5000:
                color = (0, 0, 255)  # 파란색
                health = 70
            else:
                color = (255, 0, 0)  # 빨간색
                health = 100

            # 특별 몬스터 설정
            if i == special_index:
                special = True
                image_to_use = special_image_path  # 특별 몬스터 이미지 사용
            else:
                special = False
                image_to_use = image_path  # 일반 몬스터 이미지 사용

            # 몬스터 생성
            monster = cls(x=x, y=y, color=color, health=health, special=special, stage=stage, image_path=image_to_use)
            monsters.append(monster)

        return monsters

    @staticmethod
    def handle_collision(monsters, bullets, score, coin_list, item_list):
        """
        몬스터와 탄환 간 충돌 처리.
        - monsters: 몬스터 리스트
        - bullets: 탄환 리스트
        - score: 현재 점수 (참조형 변수)
        - coin_list: 생성된 코인 리스트
        - item_list: 생성된 아이템 리스트
        """
        for bullet in bullets[:]:  # 탄환 리스트 순회
            for monster in monsters[:]:  # 몬스터 리스트 순회
                if bullet.rect.colliderect(monster.rect):  # 탄환과 몬스터가 충돌했을 경우
                    monster.take_damage(bullet.damage)  # 몬스터 체력 감소

                    if monster.health <= 0:  # 몬스터 체력이 0 이하인 경우
                        # 특별 몬스터 처치 시
                        if monster.special:
                            monsters.clear()  # 해당 줄의 모든 몬스터 제거
                            score[0] += 500  # 특별 몬스터 점수 추가
                        else:
                            score[0] += 100  # 일반 몬스터 점수 추가
                            monsters.remove(monster)  # 몬스터 제거

                        # 코인 생성 (50% 확률)
                        if random.randint(1, 100) <= 50:
                            coin_list.append(Coin.create_random_coin(monster.x + monster.width // 2, monster.y))

                        # 아이템 생성
                        if random.randint(1, 100) <= 1:  # 하이퍼 플라이트
                            item_list.append(Item.create_hyper_flight_item(monster.x + monster.width // 2, monster.y))
                        if random.randint(1, 100) <= 10:  # 더블샷
                            item_list.append(Item.create_bullet_item(monster.x + monster.width // 2, monster.y))
                        if random.randint(1, 100) <= 10:  # 자석
                            item_list.append(Item.create_magnet_item(monster.x + monster.width // 2, monster.y))

                    bullets.remove(bullet)  # 충돌한 탄환 제거
                    break  # 다음 탄환 처리
        if not monsters:  # 몬스터가 모두 제거된 경우
            score[0] += 1000  # 추가 점수 보상

    @staticmethod
    def handle_hyper_flight_collision(monsters, mid_screen_height, score, coin_list, item_list, item_spawn_chance):
        """
        하이퍼 플라이트 상태에서 화면 중간 높이 이하의 몬스터를 충돌 처리.
        - mid_screen_height: 화면 중간 높이
        - item_spawn_chance: 아이템 생성 확률 (기본값 30%)
        """
        for monster in monsters[:]:  # 몬스터 리스트 순회
            if monster.rect.y >= mid_screen_height:  # 화면 중간 높이 이하의 몬스터만 처리
                score[0] += 100  # 점수 100점 추가

                # 아이템 생성
                if random.randint(1, 100) <= item_spawn_chance:
                    item_list.append(Item.create_bullet_item(monster.rect.centerx, monster.rect.centery))
                    coin_list.append(Coin(x=monster.rect.centerx, y=monster.rect.centery))

                # 하이퍼 플라이트 보너스
                if random.randint(1, 100) <= 5:
                    item_list.append(Item.create_hyper_flight_item(monster.x + monster.width // 2, monster.y))

                monsters.remove(monster)  # 몬스터 제거
        if not monsters:  # 몬스터가 모두 제거된 경우
            score[0] += 1000  # 추가 점수 보상
