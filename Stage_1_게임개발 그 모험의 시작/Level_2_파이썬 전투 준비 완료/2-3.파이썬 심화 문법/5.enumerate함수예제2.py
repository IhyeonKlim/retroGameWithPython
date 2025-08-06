# 리스트 요소 변경
numbers = [10, 20, 30, 40]

for index, num in enumerate(numbers):
    numbers[index] = num * 2  # 기존 값의 2배로 변경

print(numbers)
# 출력
#[20, 40, 60, 80]

# 학생 이름 리스트
names = ["유재석", "손흥민", "카리나"]
# 학생 영어 점수 리스트
english_scores = [85, 92, 78]

# zip() 함수를 사용하여 이름과 점수를 짝짓습니다.
# zip_data는 (이름, 점수) 형태의 튜플들을 생성합니다.
zipped_data = zip(names, english_scores)

print("--- zip() 함수를 사용한 데이터 짝짓기 ---")
# zip 객체를 순회하며 각 튜플을 출력합니다.
for name, score in zipped_data:
    print(f"이름: {name}, 영어 점수: {score}")

# 출력
# 이름: 유재석, 영어 점수: 85
# 이름: 손흥민, 영어 점수: 92
# 이름: 카리나, 영어 점수: 78

# 특정 요소 찾기
words = ["apple", "banana", "cherry", "banana"]

for index, word in enumerate(words):
    if word == "banana":
        print(f"바나나는 {index}번째 위치에 있습니다.")
# 출력
# 바나나는 1번째 위치에 있습니다.
# 바나나는 3번째 위치에 있습니다.

#딕셔너리 타입을 for문을 통해 확인 할 때 (enumerate 미사용)
my_dict = {'a': 10, 'b': 20, 'c': 30}
for key, value in my_dict.items():
    print(key, value)
#출력
#a 10
#b 20
#c 30

#딕셔너리 타입을 for문을 통해 확인 할 때 (enumerate 사용)
for index, (key, value) in enumerate(my_dict.items()):
    print(index, key, value)
#출력
#0 a 10
#1 b 20
#2 c 30


# range와 len 함수를 이용한 for문 사용
numbers = [100, 200, 300]

for i in range(len(numbers)):
    print(i, numbers[i])
#출력
#0 100
#1 200
#2 300

# enumertate 사용
for index, num in enumerate(numbers):
    print(index, num)
#출력
#0 100
#1 200
#2 300