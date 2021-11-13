'''
A 杯子: m(L)
B 杯子: n(L)
目标: 在 m 杯子取 k(L) 水，已知: m > n > k.

求最小次数。(取水和倒水都要计次)

？？？ 未完成，例如：10 3 2
'''


def min_step(m, n, k):
    try:
        assert m>n>k
    except:
        return -1
    
    def step(m, n, k, r, mm):
        max_step = m//n
        t = False
        for i in range(1, max_step+1):
            if r==1:
                r += 1
            else:
                r += 2
            print(m, i*n)
            if k == m-i*n:
                t = True
                print(t)
                return r, t
        else:
            print(m, n, r)
            m = mm - (n - mm%n)
            r += 4
            if m>n and m%n!=0:
                print(m, n, r)
                step(m, n, k, r, mm)

        return r, t

    r, t = step(m, n, k, 1, m)
    print(r, t)
    if t:
        return r
    else:
        return -1


while True:
    try:
        strlist = input().strip().split(' ')
        intlist = [int(i) for i in strlist]
        m, n, k = intlist
        print(min_step(m, n, k))
    except:
        break
