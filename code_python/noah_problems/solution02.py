'''
@Author: yanxinyi620@163.com
@Date: 2020-04-18
@Title：get_noah_sum
@Usage：输入目录，返回数字
@Description：获取目录下所有文件中 noah-整数 模式的数字累加值
'''

import os 
import re

def get_noah_sum(mypath):

    mypath = os.walk(mypath)
    
    # step1: 遍历路径，获取所有 .txt 结尾文件
    filelist = []
    for path, dir_list, file_list in mypath:  
        for file_name in file_list:
            if file_name[-4:] == '.txt':
                print(os.path.join(path, file_name))
                filelist.append(os.path.join(path, file_name))
            else:
                print('no txt filename', os.path.join(path, file_name))

    # step2: 遍历所有 txt 文件，对每行进行分词，获取相关模式的 word ，对数字进行累加
    noahsum = 0
    for txtfile in filelist:
        for line in open(txtfile):
            # print(line)
            wordlist = line.strip().split(' ')
            noahnum = [re.findall(r'\d+', i)[0] for i in wordlist if re.match(r'noah-\d+[,.?!]?$', i)]
            if noahnum:
                noahsum = noahsum + sum(map(int, noahnum))
    return noahsum
    

mypath = "C:/Users/yanxinyi/Documents/GitHub/My_test_yanxinyi/txtfile"
noahsum = get_noah_sum(mypath)
print('The sum fo numbers in mypath' + ' is ' + str(noahsum))

