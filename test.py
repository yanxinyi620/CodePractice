
def pattern_miningAB(smallA, bigB):
    
    # smallA: 子字符串序列 (list)
    # bigB: 总字符串序列 (list)
    
    max_compare_len = len(bigB) - len(smallA) + 1
    compare_start = 0

    for i in range(compare_start, max_compare_len):
        for j in bigB:
            if i in j:
        





# examples
bigB = ['ab1c', 'bd2d', 'hello', 'world']

smallA_1 = ['ab']
pattern_miningAB(smallA_1, bigB)

smallA_2 = ['d2d', 'lo']
pattern_miningAB(smallA_2, bigB)

smallA_3 = ['2d', 'or']
pattern_miningAB(smallA_3, bigB)

smallA_4 = ['or', 'bd']
pattern_miningAB(smallA_4, bigB)

smallA_5 = ['dd']
pattern_miningAB(smallA_5, bigB)


