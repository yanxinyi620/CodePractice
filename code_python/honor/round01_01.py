'''
x = 10 * log(S/N) - 10 * log(S/(N+k*N))
  = 10 * log((S/N) / (S/(N+k*N)))
  = 10 * log(1+k)

k = 10**(0.1*x) - 1
'''

import math


while True:
    try:
        s = input()
        x = float(s)

        k = 10**(0.1*x) - 1
        r = int(10*math.log10(k))
        print(str(r))
    except:
        break
