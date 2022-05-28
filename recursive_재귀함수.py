# 재귀 함수 호출 : 함수 내에 반복 조건을 만족하기 위해 앞으로 함수를 호출하지만, 반복조건을 만족하였을 시 앞으로 왔던 함수들을 다시 돌아오며 함수를 마무리해온다.
#                 즉 조건 만족까지 스스로 계속 호출한다.
# for i in range(1, 6):
#     print(i)
#     if i == 5:
#         print("번호 끝")

def count_1(): # 첫 번째 군인
    print(1)
    count_2()
    print("1 끝")

def count_2(): # 두 번째 군인
    print(2)
    count_3()
    print("2 끝")

def count_3(): # 세 번째 군인
    print(3)
    count_4()
    print("3 끝")

def count_4(): # 네 번째 군인
    print(4)
    count_5()
    print("4 끝")

def count_5(): # 다섯 번째 군인
    print(5)
    print("번호 끝")
    print("5 끝")

# count_1()

def count(num=1):
    print(num)
    if num == 5:
        print("번호 끝")
    else:
        count(num + 1)
    print(num, "끝")

count()