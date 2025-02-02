class Fruit:
    def __init__(self, name, color, taste):
        """
        Fruit 클래스
        - name: 과일의 이름
        - color: 과일의 색
        - taste: 과일의 맛
        """
        self.name = name   # 과일의 이름
        self.color = color # 과일의 색
        self.taste = taste # 과일의 맛

    # 과일 정보를 출력하는 메서드
    def describe(self):
        print(f"이 과일은 {self.color}색 {self.name}이고, 맛은 {self.taste}입니다.")

    # 과일의 맛을 변경하는 메서드
    def change_taste(self, new_taste):
        self.taste = new_taste
        print(f"{self.name}의 맛이 {self.taste}(으)로 변경되었습니다.")

# 과일 객체 생성
fruit1 = Fruit("apple", "red", "sweet")

# describe 메서드 호출
fruit1.describe()  # 출력: 이 과일은 red색 apple이고, 맛은 sweet입니다.

# 과일의 맛을 변경하는 메서드 호출
fruit1.change_taste("sour")  # 출력: apple의 맛이 sour(으)로 변경되었습니다.

# 변경된 정보 확인
fruit1.describe()  # 출력: 이 과일은 red색 apple이고, 맛은 sour입니다.

