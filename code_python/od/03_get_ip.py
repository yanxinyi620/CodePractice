# 根据数字串，生成所有可能的 ip 地址

def _check_ip(ip_str):

    ip = [int(i) for i in ip_str]

    if ip[0] < 10 or ip[0] > 255 or ip_str[0][0]=='0':
        return False
    if ip[1] < 10 or ip[1] > 255 or ip_str[1][0]=='0':
        return False
    if ip[2] < 10 or ip[2] > 255 or ip_str[2][0]=='0':
        return False
    if ip[3] < 1 or ip[2] > 255 or ip_str[3][0]=='0':
        return False
    
    return True


def get_all_ip(s):

    ip1_len = [2, 3]
    ip2_len = [2, 3]
    ip3_len = [2, 3]
    ip4_len = [1, 2, 3]

    all_ip_len = []
    for l1 in ip1_len:
        for l2 in ip2_len:
            for l3 in ip3_len:
                for l4 in ip4_len:
                    all_ip_len.append([l1+l2+l3+l4, l1, l2, l3, l4])

    s_len = len(s)
    if s_len < 7:
        return
    elif s_len > 12:
        return
    else:
        select_ip_len = [x[1:] for x in all_ip_len if x[0]==s_len]

    select_ip = []
    for i in select_ip_len:
        ip1 = s[0: i[0]]
        ip2 = s[i[0]: i[0]+i[1]]
        ip3 = s[i[0]+i[1]: i[0]+i[1]+i[2]]
        ip4 = s[i[0]+i[1]+i[2]: ]
        select_ip.append([ip1, ip2, ip3, ip4])

    ip_list = []
    for ip_str in select_ip:
        if _check_ip(ip_str):
            ip_list.append('.'.join(ip_str))

    return(ip_list)


ip_list = get_all_ip('102551016')
print(ip_list)

