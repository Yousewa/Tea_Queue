from pythonds.basic.queue import Queue
import random as r

class T_M:
    def __init__(self, tpm):
        self.teaRate = tpm  # 做奶茶的速度
        self.currentTask = None  # 当前任务
        self.timeRemaining = 0  # 任务倒计时

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self, newtask):
        self.currentTask = newtask
        # 新起一个奶茶任务，计算并设置等待时间，原速度为分，最后乘以60转化为秒
        self.timeRemaining = newtask.getTeas() / self.teaRate * 60

class Task:
    def __init__(self, time):
        self.timestamp = time  # 在3600秒内的第几秒生成任务
        self.teas = r.randrange(1, 6)  # 随机生成1~5杯奶茶的数量

    def getStamp(self):
        return self.timestamp

    def getTeas(self):
        return self.teas

    def waitTime(self, currenttime):  # 给定一个走到第几秒来计算等待时间
        return currenttime - self.timestamp

def newTeaTask():
    num = r.random()
    if num < 1 / 500:  # 高峰时段
        return 'dy', 'high'
    elif num < 1 / 180:  # 正常情况
        return 'dy', 'normal'
    else:
        return 'break', 'break'

def simulation(numSeconds, teasPerMinute):
    # 这里定义一个抽象的奶茶店设置对象
    labT_M = T_M(teasPerMinute)
    # 定义一个奶茶店队列
    teaQueue = Queue()
    # 定义一个列表保存每次多个任务执行时的等待时间
    waitingtimes = []
    # 从第1秒开始线性的走时间

    for currentSecond in range(numSeconds):

        teaMaking, highTime = newTeaTask()
        if teaMaking == 'dy':
            
            if highTime == 'high':  # 高峰时段，提高制作速度
                task = Task(currentSecond)
                teaQueue.enqueue(task)
                labT_M.teaRate = 1.0
                if c == 'T':
                    print("有顾客在%d秒提交奶茶申请，且为高峰时段" % currentSecond)
                    print("高峰时段，加派人手，制作速度变为每分钟%d杯" % labT_M.teaRate)
            elif highTime == 'normal':
                task = Task(currentSecond)
                teaQueue.enqueue(task)
                if c == 'T':
                    print("有顾客在%d秒提交奶茶申请，且为正常时段" % currentSecond)
                    print('正常时段，减少人手，制作速度变为每分钟%.1f杯'% teaQuality)
        if (not labT_M.busy()) and (not teaQueue.isEmpty()):
            nexttask = teaQueue.dequeue()
            waitingtimes.append(nexttask.waitTime(currentSecond))
            labT_M.startNext(nexttask)
        labT_M.tick()

    if len(waitingtimes) > 0:
        averageWait = sum(waitingtimes) / len(waitingtimes)
    else:
        averageWait = 0

    print("平均等待时间为%-6.2f 秒 %1d 杯奶茶在排队." % (averageWait, teaQueue.size()))

c = input('是否查看每秒的具体情况(输入T查看):')
teaQuality = 0.5  # 初始制作速度，每分钟做0.5杯奶茶
simuTimes = 10 # 模拟的次数
for i in range(1, simuTimes + 1):
    print("模拟第%d次,初始制作速度为每分钟做%.1f杯" % (i, teaQuality))
    simulation(3600, teaQuality)
