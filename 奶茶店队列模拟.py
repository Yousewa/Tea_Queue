 from pythonds.basic.queue import Queue
import random


class TeaMaker:
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
        self.teas = random.randrange(1, 6)  # 随机生成1~5杯奶茶的数量

    def getStamp(self):
        return self.timestamp

    def getTeas(self):
        return self.teas

    def waitTime(self, currenttime):  # 给定一个走到第几秒来计算等待时间
        return currenttime - self.timestamp


def newTeaTask():
    num = random.random()
    if num < 1 / 500:  # 高峰时段
        return 'ing', 'high'
    elif num < 1 / 180:  # 正常情况
        return 'ing', 'normal'
    else:
        return 'break', 'break'


def simulation(numSeconds, teasPerMinute):
    # 这里定义一个抽象的奶茶店设置对象
    labTeaMaker = TeaMaker(teasPerMinute)
    # 定义一个奶茶店队列
    teaQueue = Queue()
    # 定义一个列表保存每次多个任务执行时的等待时间
    waitingtimes = []
    # 从第1秒开始线性的走时间

    for currentSecond in range(numSeconds):

        teaMaking, highTime = newTeaTask()
        if teaMaking == 'ing':
            task = Task(currentSecond)
            teaQueue.enqueue(task)
            if highTime == 'high' and labTeaMaker.teaRate < 2 * teaQuality:  # 高峰时段，提高制作速度
                labTeaMaker.teaRate *= 2
                print("高峰时段，加派人手，制作速度提至每分钟%d杯" % labTeaMaker.teaRate)
            elif teaMaking == 'break' and highTime == 'break':  # 既不是高峰时段也不是正常时段
                print("现在没有顾客。")
        if (not labTeaMaker.busy()) and (not teaQueue.isEmpty()):
            nexttask = teaQueue.dequeue()
            waitingtimes.append(nexttask.waitTime(currentSecond))
            labTeaMaker.startNext(nexttask)
        labTeaMaker.tick()

    if len(waitingtimes) > 0:
        averageWait = sum(waitingtimes) / len(waitingtimes)
    else:
        averageWait = 0

    print("平均等待时间为%-6.2f 秒 %1d 杯奶茶在排队." % (averageWait, teaQueue.size()))


teaQuality = 0.5  # 初始制作速度，每分钟做0.5杯奶茶
simuTimes = 10 # 模拟的次数
for i in range(1, simuTimes + 1):
    print("模拟第%d次,初始制作速度为每分钟做%.1f杯" % (i, teaQuality))
    simulation(3600, teaQuality)
