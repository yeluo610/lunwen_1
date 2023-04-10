# class Worker:
#     # ID：工人id、名字：工人名字、x:经度、y：纬度、能力：3，等级：rank，半径：统一0.2km、
#     # 少了时间
#     def __init__(self, user_id,name, capacity,rank,y,x, radius):
#         self.user_id = user_id
#         self.name = name
#         self.x = x
#         self.y = y
#         self.rank=rank
#         self.capacity=capacity
#         self.radius=radius

# 工人
class Worker:
    def __init__(self, user_id, lon, lat, time, capacity, radius, rank):
        self.user_id = user_id
        self.lon = lon
        self.lat = lat
        self.time = time
        self.capacity = capacity
        self.radius = radius
        self.rank = rank


# 场地
class Place:
    def __init__(self, palce_id, lon, lat, goods, rank):
        self.palce_id = palce_id
        self.lon = lon
        self.lat = lat
        self.goods = goods
        self.rank = rank


# 任务
class Task:
    def __init__(self, task_id, lon, lat, start_time, expire_time, good, radius, rank, fare):
        self.task_id = task_id
        self.lon = lon
        self.lat = lat
        self.start_time = start_time
        self.expire_time = expire_time
        self.good = good
        self.radius = radius
        self.rank = rank
        self.fare = fare



# class Strategy:
#     def __init__(self,worker,strategy):
#         self.worker=worker
#         self.strategy=strategy

class Task_Place:
    def __init__(self, task, place):
        self.task = task
        self.place = place


# 定义事件,把事件插入调度中，查看合适的位置
class Event:
    # 位置，最早到达，最晚离开，任务负载
    def __init__(self, lon, lat, earliest_arrival, latest_leaving, task_load):
        self.lon = lon
        self.lat = lat
        self.earliest_arrival = earliest_arrival
        self.latest_leaving = latest_leaving
        self.task_load = task_load


# 定义调度,调度中的事件，和事件中的下一个联系，有点像链表
class Schedule:
    def __init__(self, event):
        self.event = event
        self.next = None


# 存储任务和距离信息minD
class DisandPlace:
    def __init__(self, distance, place):
        self.distance = distance
        self.place = place


class zuizhong:
    def __init__(self, schedule, tasks, places):
        self.schedule = schedule
        self.tasks = tasks
        self.places = places


# 记录每个工人的备选策略和当时的可选策略
class WorkerStr:
    def __init__(self, worker, strs, finnalStr):
        self.worker = worker
        self.strs = strs
        self.finnalStr = finnalStr



# 工人的基本信息，当前调度，参与争夺后的调度，容量，利润，增长利润,将改任务分配给工人可获得的最大利润
class WorkerStr:
    def __init__(self, worker,shedule=None,mid_shedule=None,capacity=0,profit=0,up_profit=0,most_profit=0):
        self.worker = worker
        self.capacity=capacity
        self.shedule=shedule
        self.mid_shedule=mid_shedule
        self.profit=profit
        self.up_profit=up_profit
        self.most_profit=most_profit

class GreedyResult:
    def __init__(self,workerstr,task_palce):
        self.workerstr=workerstr
        self.task_palce=task_palce