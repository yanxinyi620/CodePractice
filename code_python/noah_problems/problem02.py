class Simu_queue(object):
    def __init__(self):
        self.stackA = []
        self.stackB = []

    @property
    def stackA(self):
        return self._stackA

    @stackA.setter
    def stackA(self, listA):
        if len(listA) > 10:
            raise ValueError('queue must less than 10!')
        self._stackA = listA

    @property
    def stackB(self):
        return self._stackB

    @stackB.setter
    def stackB(self, listB):
        if len(listB) > 10:
            raise ValueError('queue must less than 10!')
        self._stackB = listB

    def push(self, node):
        while self.stackB != []:
            self.stackA.append(self.stackB.pop())
            if len(self.stackA) > 10:
                print('queue must less than 10!')
        return self.stackA.append(node)
        
    def pop(self):
        while self.stackA != []:
            self.stackB.append(self.stackA.pop())
        return self.stackB.pop()
    
    def isempty(self):
        if self.stackA == [] and self.stackB == []:
            return 'Queue is empty'
        else:
            return 'Queue is not empty'


if __name__ == "__main__":

    # test1
    queue1 = Simu_queue()
    queue1.push(2)
    queue1.pop()
    queue1.isempty()

    # test2
    queue2 = Simu_queue()
    queue2.stackA = list(range(10))
    queue2.push(2)
    queue2.pop()
    queue2.isempty()
