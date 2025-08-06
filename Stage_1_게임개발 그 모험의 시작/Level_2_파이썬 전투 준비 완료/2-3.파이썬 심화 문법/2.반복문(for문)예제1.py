#while문과 비교하여 for문 익히기
# 숫자를 세기 위한 변수를 0으로 설정합니다.
current_number = 0

# 숫자를 5개 셉니다.
while current_number < 5:
    # 현재 숫자를 출력합니다.
    print(current_number)

    # 다음 숫자를 위해 current_number를 1 증가시킵니다.
    current_number += 1
print("while문으로 다섯개의 숫자 세기가 완료되었습니다!")

# 출력:
# 0
# 1
# 2
# 3
# 4
# while문의 숫자 세기가 완료되었습니다!

# range() 함수를 사용하여 5개의 숫자를 세는 for문
for current_number in range(5):
    print(current_number)
print("for문으로 다섯개의 숫자 세기가 완료되었습니다!")
# 출력:
# 0
# 1
# 2
# 3
# 4
# for문으로 다섯개의 숫자 세기가 완료되었습니다!


# 다섯개의 숫자를 세기 위한 리스트
numbers_to_count = [0, 1, 2, 3, 4]

# 리스트의 현재 위치(인덱스)를 추적할 변수를 0으로 설정합니다.
index = 0

# index가 리스트의 마지막 유효 인덱스(4)보다 작거나 같을 때까지 반복합니다.
while index <= 4:  # numbers_to_count 리스트의 마지막 인덱스는 4입니다.
    # 현재 인덱스에 해당하는 숫자를 리스트에서 가져와 출력합니다.
    current_number = numbers_to_count[index]
    print(current_number)

    # 다음 숫자로 이동하기 위해 인덱스를 1 증가시킵니다.
    index += 1

print("while문으로 리스트에 담긴 다섯개의 숫자 세기가 완료되었습니다!")

# 출력:
# 0
# 1
# 2
# 3
# 4
# while문으로 리스트의 숫자 세기가 완료되었습니다!


# 다섯개의 숫자를 세기 위한 리스트
numbers_to_count = [0, 1, 2, 3, 4]
for current_number in numbers_to_count: # 묶음의 각 요소를 순회
    print(current_number)
print("for문으로 리스트에 담긴 다섯개의 숫자 세기가 완료되었습니다!")

# 출력:
# 0
# 1
# 2
# 3
# 4
# for문으로 리스트에 담긴 다섯개의 숫자 세기가 완료되었습니다!
