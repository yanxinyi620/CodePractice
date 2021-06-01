'''
@Author: yanxinyi620@163.com
@Date: 2020-04-18
@Title：pattern_miningAB
@Usage：输入两个列表，返回序列判断结果
@Description：判断 A 是 B 的子序列（A中的每个字符串是B中的子字符串，且顺序一致）
'''

def pattern_miningAB(smallA, bigB):
    
    # smallA: 子字符串序列 (list)
    # bigB: 总字符串序列 (list)
    
    max_len = len(bigB) - len(smallA) + 1
    n = 0

    # 遍历 samllA 中的元素，每次找到匹配项后，对下一个 samllA 进行判断前，将 bigB 的对应位置进行更新。
    for i in range(len(smallA)):
        while n < max_len:
            if smallA[i] in bigB[n]:
                max_len += (n + 1)
                n += 1
                break
            else:
                n += 1
        else:
            # 当 samllA 中任意一个元素无法在 bigB 中找到，则结束循环
            print('samllA 不是 bigB 的子序列(序列模式判断)')
            break
    else:
        print('samllA 是 bigB 的子序列(序列模式判断)')


# examples
bigB = ['ab1c', 'bd2d', 'hello', 'world']

smallA_1 = ['ab']
pattern_miningAB(smallA_1, bigB)

smallA_2 = ['bd2d', 'or']
pattern_miningAB(smallA_2, bigB)

smallA_4 = ['or', 'bd']
pattern_miningAB(smallA_4, bigB)

smallA_5 = ['dd']
pattern_miningAB(smallA_5, bigB)

