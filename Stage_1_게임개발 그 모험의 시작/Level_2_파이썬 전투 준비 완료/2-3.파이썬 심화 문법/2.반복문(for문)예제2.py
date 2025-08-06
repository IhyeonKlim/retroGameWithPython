# 리스트의 요소를 순회하는 for문

# 과일 리스트
fruits = ["apple", "banana", "cherry", "orange", "grape"]

for fruit in fruits:
    print(fruit)

# 출력:
# apple
# banana
# cherry
# orange
# grape

# break를 이용한 반복문 중단
for fruit in fruits:
    # "cherry"를 찾으면 반복을 중단하도록 조건 설정
    if fruit == "cherry":
        print(f"'{fruit}'를 찾았습니다. 반복을 종료합니다.")
        break
    print(f"'{fruit}'는 cherry가 아닙니다.")

# break로 중간에 반복문을 멈춘다면 orange와 grape는 출력되지 않아야 합니다.

# 출력
# 'apple'는 cherry가 아닙니다.
# 'banana'는 cherry가 아닙니다.
# 'cherry'를 찾았습니다. 반복을 종료합니다.

# continue를 이용한 반복문 중단
for fruit in fruits:
    # "banana"는 건너뛰고 나머지 과일 출력
    if fruit == "banana":
        print(f"'{fruit}'는 건너뛰고 다음 반복으로 이동합니다.")
        continue
    print(f"'{fruit}'를 출력합니다.")

#'apple'를 출력합니다.
#'banana'는 건너뛰고 다음 반복으로 이동합니다.
#'cherry'를 출력합니다.
#'orange'를 출력합니다.
#'grape'를 출력합니다.

print(f"len함수를 이용한 fruits 리스트의 크기는 {len(fruits)}입니다.")
#len함수를 이용한 fruits 리스트의 크기는 5입니다.

# len함수와 range함수 그리고 인덱스를 사용하여 리스트 순회
for i in range(len(fruits)):
    print(f"인덱스 {i}: {fruits[i]}")

# 출력:
# 인덱스 0: apple
# 인덱스 1: banana
# 인덱스 2: cherry
# 인덱스 3: orange
# 인덱스 4: grape
