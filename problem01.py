# 使用循环每次 + 1，直到找到符合标准的结果，当遇到 ‘99999999999’ 这类输入的时候效率很低。
# 观察到每次A, B 差值都是 9 的倍数，改为每次 + 9
def getB(A):
    A = int(A)
    if A == 0:
        print('Input cannot be 0')
    else:
        sumA = sum(list(map(int, list(str(A)))))
        B = A + 9
        while sum(list(map(int, list(str(B))))) != sumA:
            B += 9
        else:
            print(B)


A = input()
getB(A)



# 利用规则进行处理
def getB(A):
    A = int(A)
    if A == 0:
        print('Input cannot be 0')
    else:
        lenA = len(str(A))
        for i in range(lenA):
            
            if str(A)[-1] == '0' and :
                B = int(A) + 90
            else:
                B = int(A) + 9


A = input()
getB(A)


