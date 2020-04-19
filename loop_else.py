j = 0
for i in [0, 1, 3, 2, 3, 6]:
    while j < 5:
        if i == j:
            j += 1
            print(i)
            break
        else:
            j += 1
    else:
        print('no: ' + str(i))
        break


for i in range(3):
    for j in range(3):
        for k in range(3):
            print(i, ', ', j, ', ', k)
            if i == j == k == 1:
                break
            else:    
                print(i, '----', j, '----', k)
        else:        # else1
            continue
        break        # break1
    else:            # else2
        continue
    break            # break2


for i in range(2):
    for j in range(5):
        print(i, ' ', j)
        if j > i:
            break
        else:
            pass
    else:
        break
