'''
https://www.lintcode.com/problem/1428/
LintCode
1428 · 钥匙和房间
'''

def get_result(rooms):

    def get_room(n):
        result[n] = True
        for key in rooms[n]:
            if not result[key]:
                get_room(key)
    
    result = []
    for _ in rooms:
        result.append(False)
    
    get_room(0)

    for i in result:
        if not i:
            return False
    return True


get_result([[1], [2], [3], []])
get_result([[1], [2], [], []])

