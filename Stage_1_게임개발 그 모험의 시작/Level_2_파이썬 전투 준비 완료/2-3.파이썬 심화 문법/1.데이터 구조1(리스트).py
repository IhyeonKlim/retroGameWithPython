# 과일 리스트 선언 및 사용
fruits = ["apple", "banana", "cherry"]
print(fruits[0])  # 출력: apple (첫 번째 요소, 인덱스 0)
print(fruits[1])  # 출력: banana (두 번째 요소, 인덱스 1)
print(fruits[2])  # 출력: cherry (세 번째 요소, 인덱스 2)
print(fruits[-1])  # 출력: cherry (마지막(세번째) 요소, 인덱스 -1)

# 리스트에 값 추가
add_data = "orange"
fruits.append(add_data)
print(f"fruits에 {add_data} 추가")
print(fruits)  # 출력: ['apple', 'banana', 'cherry', 'orange']

# 리스트의 각 요소를 '인덱스'를 사용해 접근
print(fruits[0])  # 출력: apple (첫 번째 요소, 인덱스 0)
print(fruits[1])  # 출력: banana (두 번째 요소, 인덱스 1)
print(fruits[2])  # 출력: cherry (세 번째 요소, 인덱스 2)
print(fruits[3])  # 출력: orange (네 번째 요소, 인덱스 3)
print(fruits[-1])  # 출력: orange (마지막 요소, 인덱스 -1)
print(fruits[-2])  # 출력: cherry (끝에서 두번째 요소, 인덱스 -2)

# 리스트에 값 삭제
remove_data = "apple"
fruits.remove(remove_data)
print(f"fruits에 {remove_data} 삭제")
# 리스트의 각 요소를 '인덱스'를 사용해 접근
print(fruits[0])  # 출력: banana (첫 번째 요소, 인덱스 0)
print(fruits[1])  # 출력: cherry(두 번째 요소, 인덱스 1)
print(fruits[2])  # 출력: orange (세 번째 요소, 인덱스 2)

# 인덱스를 이용한 과일 리스트의 마지막 데이터 삭제
print(f"fruits에 {fruits[-1]} 삭제") # 출력 : fruits에 orange 삭제
fruits.remove(fruits[-1])
print(f"fruits의 마지막 과일은 {fruits[-1]}입니다") # 출력 : fruits의 마지막 과일은 cherry입니다


# 인덱스를 이용한 과일 리스트의 마지막 데이터 변경
before_fruit = fruits[0]
print(f"fruits에 {fruits[0]} 변경") # 출력 : fruits에 banana 변경
fruits[0] = "monkey ate"
print(f"fruits의 {before_fruit}는 {fruits[0]}입니다") # 출력 : fruits의 banana는 monkey ate입니다

#인덱스 번호가 없는 경우는 에러가 생깁니다.
#fruits[999] = "none" #주석을 지우고 동작시 에러 발생 IndexError: list assignment index out of range
