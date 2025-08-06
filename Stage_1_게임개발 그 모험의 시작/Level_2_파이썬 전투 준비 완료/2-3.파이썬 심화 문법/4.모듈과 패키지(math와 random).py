# 파이썬 표준 라이브러리에서 math 모듈 불러오기
import math
import random

# math 모듈을 통한 자주 쓰는 함수들

# 1. sqrt() - 제곱근을 구하는 함수
print(math.sqrt(16))  # 출력: 4.0

# 2. pow() - 거듭제곱을 계산하는 함수
print(math.pow(2, 3))  # 출력: 8.0

# 3. ceil() - 주어진 수보다 크거나 같은 가장 작은 정수를 반환 (올림)
print(math.ceil(4.2))  # 출력: 5

# 4. floor() - 주어진 수보다 작거나 같은 가장 큰 정수를 반환 (내림)
print(math.floor(4.9))  # 출력: 4

# 5. fabs() - 절대값을 반환
print(math.fabs(-7.25))  # 출력: 7.25

# 6. factorial() - 정수의 팩토리얼을 계산
print(math.factorial(5))  # 출력: 120

# 7. degrees() - 라디안 값을 각도로 변환
print(math.degrees(math.pi))  # 출력: 180.0

# 8. radians() - 각도를 라디안 값으로 변환
print(math.radians(180))  # 출력: 3.141592653589793

# random 모듈을 통한 자주 쓰는 함수들

# 1. random() - 0과 1 사이의 임의의 부동소수점 숫자 생성
print(random.random())  # 출력: 0과 1 사이의 임의의 값 (예: 0.7824)

# 2. randint() - 주어진 범위 내에서 임의의 정수 생성
print(random.randint(1, 10))  # 출력: 1부터 10 사이의 임의의 정수 (예: 7)

# 3. choice() - 리스트나 튜플에서 임의의 값을 선택
fruits = ["apple", "banana", "cherry"]
print(random.choice(fruits))  # 출력: 리스트에서 임의의 값 선택 (예: banana)

# 4. shuffle() - 리스트의 요소를 무작위로 섞음
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(numbers)  # 출력: 리스트가 무작위로 섞인 결과 (예: [3, 1, 5, 2, 4])