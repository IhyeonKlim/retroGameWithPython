x = "global"  # 전역 변수

def outer_function():
    x = "enclosing"  # 외부 함수의 변수

    def inner_function():
        x = "local"  # 내부 함수의 변수
        print(f"Inner: {x}")

    inner_function()
    print(f"Outer: {x}")

outer_function()
print(f"Global: {x}")

# 출력
#Inner: local
#Outer: enclosing
#Global: global


x = "global"

def modify_global():
    global x # global 키워드로 전역 변수 접근
    x = "modified" #전역변수의 값을 변경.
    print(f"Inside function: {x}")

modify_global() # 함수 실행 이후 x의 값이 바뀌었는지 확인
print(f"Outside function: {x}")

#출력
#Inside function: modified
#Outside function: modified