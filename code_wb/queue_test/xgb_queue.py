from multiprocessing import Process, Queue


max = 3
q = Queue(maxsize=max)
print(q.empty())  # 队列是否为空
print(q.full())  # 队列书否已满
peple = ["a", 'b', 'c', 'd', 'e', 'f', 'g']
for i in peple:
    if q.full():
        print("队列已满")
        data = q.get()  # 取走一个数据。先进先出原则，总是取最早进入队列的数据
        print("取走了一个 %s, 还有%d 个" % (data, q.qsize()))
    else:
        q.put(i)  # 如果队列满了，会阻塞，一直停在这，直到有数据被取走，再继续往队列尾端加数据
        # q.put_nowait(i)  # 如果队列满了，不会阻塞，会报错
        print("加入一个")
        print("当前队列数量：", q.qsize())


"""多进程使用消息队列"""
from multiprocessing import Process, Queue
import time
import os
 
 
def read_file(file_name):
    """从文件内读取数据"""
    with open(file_name, "r") as f:
        num = int(f.read())
    return num


def write_file(file_name, data):
    """将数据写入文件"""
    with open(file_name, "w") as f:
        f.write(str(data))


def inputQ(queue):
    """加入队列"""
    queue.put(str(os.getpid()) + " -- " + str(time.time()))  # 当队列已满时，会阻塞，等待
    print("已生产 %d  ，添加到队列" % os.getpid())
 
 
def outputQ(queue):
    """从队列内取数据"""
    data = queue.get()  # 当队列内无数据时，会阻塞等待
    if data is None:
        return
    else:
        print(str(os.getpid()) + "已消费")
        return 0
 
 
def add_queue(q):
    for i in range(10):
       inputQ(q)
    q.put(None)  # 也可以在主进程内，在生产者结束（join()）后发
 
 
def delete_queue(q):
    # 抽奖用户数比奖品数量多, 这种情况如果使用get()会阻塞
    while True:
        num = outputQ(q)
        if num is None:
            break
 
 
if __name__ == '__main__':
    file_name = "../datasets/save_temp.csv"
    record_in = []
    record_out = []
    # q = Queue(2)  # 设置队列长度
    q = Queue()  # 默认队列无限长
    p1 = Process(target=add_queue, args=(q,))
    p2 = Process(target=delete_queue, args=(q,))
    p1.start()
    p2.start()
    p1.join()

