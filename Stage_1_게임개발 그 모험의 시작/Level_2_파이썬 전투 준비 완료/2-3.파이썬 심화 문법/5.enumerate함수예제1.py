# 기존 방식(인덱스를 직접 관리)
fruits = ["사과", "바나나", "체리"]

index = 0
for fruit in fruits:
    print(index, fruit)
    index += 1
# 출력
#0 사과
#1 바나나
#2 체리

# enumerate()를 사용한 방식
for index, fruit in enumerate(fruits):
    print(index, fruit)
# 출력
#0 사과
#1 바나나
#2 체리

# start 지점의 인덱스를 변경 9부터 시작하도록 임의 설정
for index, fruit in enumerate(fruits, start=9):
    print(index, fruit)
# 출력
#9 사과
#10 바나나
#11 체리

# list로 변환. 요소는 튜플.
fruit_list= list(enumerate(fruits))
print(fruit_list)
# 출력
# [(0, '사과'), (1, '바나나'), (2, '체리')]


# dict로 변환. 인덱스는 key로 변환
fruit_dict = dict(enumerate(fruits, start=1))
print(fruit_dict)
# 출력
#{1: '사과', 2: '바나나', 3: '체리'}