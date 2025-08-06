#숫자와 숫자를 더하기
print(10+20) # 출력 30

#문자와 문자를 더하기
print('10'+'20') # 출력 1020

#문자와 숫자를 더하기
#print('10'+20) 주석을 풀면 에러가 발생합니다.

# 1. 문자열을 정수로 변환 (str to int)
string_number = "123"
integer_number = int(string_number)

print(f"변환 전: {string_number}, 타입: {type(string_number)}")
print(f"변환 후: {integer_number}, 타입: {type(integer_number)}")
print("-" * 30)
#출력
#변환 전: 123, 타입: <class 'str'>
#변환 후: 123, 타입: <class 'int'>
#------------------------------

# 2. 정수를 문자열로 변환 (int to str)
my_age = 30
string_age = str(my_age)

print(f"변환 전: {my_age}, 타입: {type(my_age)}")
print(f"변환 후: {string_age}, 타입: {type(string_age)}")
print("-" * 30)
#출력
#변환 전: 30, 타입: <class 'int'>
#변환 후: 30, 타입: <class 'str'>
#------------------------------

# 3. 실수를 정수로 변환 (float to int) - 소수점 이하 버림
pi_value = 3.14159
integer_pi = int(pi_value)

print(f"변환 전: {pi_value}, 타입: {type(pi_value)}")
print(f"변환 후: {integer_pi}, 타입: {type(integer_pi)}")
print("-" * 30)

#출력
#변환 전: 3.14159, 타입: <class 'float'>
#변환 후: 3, 타입: <class 'int'>
#------------------------------

# 4. 정수를 실수로 변환 (int to float)
my_score = 95
float_score = float(my_score)

print(f"변환 전: {my_score}, 타입: {type(my_score)}")
print(f"변환 후: {float_score}, 타입: {type(float_score)}")
print("-" * 30)
#출력
#변환 전: 95, 타입: <class 'int'>
#변환 후: 95.0, 타입: <class 'float'>
#------------------------------

# 5. 문자열을 실수로 변환 (str to float)
price_str = "19.99"
float_price = float(price_str)

print(f"변환 전: {price_str}, 타입: {type(price_str)}")
print(f"변환 후: {float_price}, 타입: {type(float_price)}")
print("-" * 30)
#출력
#변환 전: 19.99, 타입: <class 'str'>
#변환 후: 19.99, 타입: <class 'float'>
#------------------------------

# 6. 형변환 시 발생할 수 있는 오류 (ValueError)
# 잘못된 문자열을 숫자로 변환하려고 할 때
invalid_string = "Hello"
print(f"변환 시도: {invalid_string}")
'''
try:
    # 이 줄에서 ValueError가 발생합니다.
    invalid_number = int(invalid_string)
    print(f"변환 후: {invalid_number}")
except ValueError:
    print("오류: 'Hello'는 정수로 변환할 수 없습니다!")
'''