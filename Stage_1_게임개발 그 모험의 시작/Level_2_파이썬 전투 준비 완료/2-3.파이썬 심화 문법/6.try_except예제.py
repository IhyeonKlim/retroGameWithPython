#try 구문없이 마구 입력 하면 프로그램이 에러로 종료됩니다.
#choice = int(input("숫자를 입력하세요 : "))

while True :
    try :
        choice = int(input("숫자를 입력하세요 : "))
        if choice >= 0:
            print("감사합니다.")
            break
    except:
        print("제발 숫자만 입력해주세요.")
