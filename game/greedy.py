import json
from property import attribute, lianbiao4,lianbiao5
from geopy.distance import great_circle
import itertools
from datetime import datetime, timedelta
import math
import time


time_format = "%m/%d/%Y %I:%M:%S %p"

# 获取工人，任务和地点的总数量
def getSum():
    task_file = json.load(open('../data/Tasks2.json', 'r'))
    task = len(task_file)

    worker_file = json.load(open('../data/Workers2.json', 'r'))
    worker = len(worker_file)

    place_file = json.load(open('../data/Places2.json', 'r'))
    place = len(place_file)

    return worker, task, place


# input：根据传入的Fangwen即已经访问的数量，和总数量以及类型（工人，任务，地点），差不多每次20个
# output：返回已经访问的数量；和此次获取东西（工人，任务，地点）

# 获取数据,工人,任务,地点
def getData(Fangwen, sum, type):
    # 每次进行任务分配的工人数
    C_fw = 4
    # 终止条件,如果最后一次超出范围的话，则重新定义每次访问的数量
    Fangwen += C_fw
    if Fangwen > sum:
        Fangwen -= C_fw
        C_fw = sum - Fangwen
        Fangwen = sum
    if type == "tasks":
        # 获取符合条件的任务
        tasks = []
        task_file = json.load(open('../data/Tasks2.json', 'r'))

        for i in range(len(task_file)):
            if i < Fangwen - C_fw:
                pass
            elif Fangwen - C_fw <= i < Fangwen:
                tasks.append(
                    attribute.Task(task_file[i]["task_id"], task_file[i]["Longitude"], task_file[i]["Latitude"],
                                   task_file[i]["start_time"],
                                   task_file[i]["expire_time"], task_file[i]["good"], task_file[i]["radius"],
                                   task_file[i]["rank"],
                                   task_file[i]["fare"]))
            else:
                break

        return Fangwen, tasks
    elif type == "workers":
        # 获取符合条件的任务
        workers = []
        worker_file = json.load(open('../data/Workers2.json', 'r'))
        for i in range(len(worker_file)):
            if i < Fangwen - C_fw:
                pass
            elif Fangwen - C_fw <= i < Fangwen:
                workers.append(
                    attribute.Worker(worker_file[i]["user_id"], worker_file[i]["Longitude"], worker_file[i]["Latitude"],
                                     worker_file[i]["time"], worker_file[i]["capacity"], worker_file[i]["radius"],
                                     worker_file[i]["rank"]))
            else:
                break

        return Fangwen, workers

    elif type == "places":
        # 获取符合条件的任务
        places = []
        place_file = json.load(open('../data/Places2.json', 'r'))
        for i in range(len(place_file)):
            if i < Fangwen - C_fw:
                pass
            elif Fangwen - C_fw <= i < Fangwen:
                places.append(
                    attribute.Place(place_file[i]["place_id"], place_file[i]["Longitude"], place_file[i]["Latitude"],
                                    place_file[i]["goods"], place_file[i]["rank"]))
            else:
                break

        return Fangwen, places

    else:
        print("你输入错类型了")

# 任务和地点的一对一匹配
def getTaskPlace(tasks, places1,ra):
    # 按照报酬排序
    tasks.sort(key=lambda x: x.fare)
    places = places1.copy()
    pipei = []
    for task in tasks:
        min_distance = float('inf')
        i = 0
        ava_place = None
        # 如果任务比地点多怎么办？
        if len(places) > 0:
            for j in range(len(places)):
                distance = great_circle((task.lat, task.lon), (places[j].lat, places[j].lon)).km
                # 距离最小，在任务可选范围内，有交叉的物品
                if (distance < min_distance and len(
                        list(set(task.good).intersection(set(places[j].goods)))) > 0 and distance < ra):
                    min_distance = distance
                    i = j
                    ava_place = places[j]

            # 这里还需要判断ava_place是否为none，
            if ava_place is not None:
                e_d1 = math.ceil(
                    (great_circle((ava_place.lat, ava_place.lon), (task.lat, task.lon)).km) * 60)
                pick1 = lianbiao4.Event(ava_place.place.lon, ava_place.place.lat,
                                        datetime.strptime(task.start_time[11:-3], '%H:%M:%S'),
                                        datetime.strptime(task.expire_time[11:-3], '%H:%M:%S') - timedelta(
                                            seconds=e_d1))
                deliver1 = lianbiao4.Event(task.lon, task.lat,
                                           datetime.strptime(task.start_time[11:-3], '%H:%M:%S') + timedelta(
                                               seconds=e_d1),
                                           datetime.strptime(task.expire_time[11:-3], '%H:%M:%S'))
                if pick1.earliest_arrival >= pick1.latest_leaving or deliver1.earliest_arrival >= deliver1.latest_leaving:
                    pipei.append(attribute.Task_Place(task, None))
                else:
                    pipei.append(attribute.Task_Place(task,ava_place))
                    del places[i]
            else:
                pipei.append(attribute.Task_Place(task, None))
        else:
            pipei.append(attribute.Task_Place(task, None))
    pipei2 = []
    for p1 in pipei:
        if p1.place is not None:
            pipei2.append(p1)
    return pipei2

# 转换格式
def changeWorker(workers):
    workerstr=[]
    for worker in workers:
        shedule=lianbiao4.LinkedList()
        head_worker = lianbiao5.Event(worker, datetime.strptime(worker.time, time_format),
                                      datetime.strptime(worker.time, time_format))
        shedule.insert_at_beginning(head_worker)
        mid_shedule=shedule
        workerstr.append(attribute.WorkerStr(worker,shedule,mid_shedule,profit=0,up_profit=0,most_profit=0))
    return workerstr
#获取备选工人
# 返回什么呀？
def getWorker(workers, Tasks_Place,ra):
    # 这里的worker应该要有调度表和容量，刚开始是null和0
    workerstr=changeWorker(workers)
    ava_workers = []
    for worker in workerstr:
        # 工人在任务的可选范围内
        if great_circle((Tasks_Place.task.lat, Tasks_Place.task.lon), (worker.worker.lat, worker.worker.lon)).km <ra:
            distance =great_circle((Tasks_Place.place.lat, Tasks_Place.place.lon), (Tasks_Place.task.lat, Tasks_Place.task.lon)).km
            upper_Profit = Tasks_Place.task.fare -distance
            if upper_Profit>0:
                worker.most_profit=upper_Profit
                ava_workers.append(worker)
            else:
                continue
        else:
             continue

    return ava_workers

# 确定最终的工人是谁
def getFinallyWorker(wokers,Task_Place,ra,ca):
    ava_workers=getWorker(wokers,Task_Place,ra)
    best_worker={"up_profit":0,"best":None}
    # 感觉还是用index比较容易更新和删除
    index =int('inf')

    for i in range(len(ava_workers)):
        # 这里不需要考虑工人容量，满了的都是删除掉了的
        if ava_workers[i].most_profit>best_worker['best']:
            e_d1 = math.ceil(
                (great_circle((Task_Place.place.lat, Task_Place.place.lon),
                              (Task_Place.task.lat, Task_Place.task.lon)).km) * 60)
            pick = lianbiao5.Event(Task_Place.place,
                                   datetime.strptime(Task_Place.task.start_time, time_format),
                                   datetime.strptime(Task_Place.task.expire_time, time_format) - timedelta(
                                       seconds=e_d1))
            deliver = lianbiao5.Event(Task_Place.task,
                                      datetime.strptime(Task_Place.task.start_time,time_format) + timedelta(
                                          seconds=e_d1),
                                      datetime.strptime(Task_Place.task.expire_time, timedelta))
            shedule=ava_workers[i].mid_shedule
            # 感觉还是要返回增长的利润,如果增长利润大于初始值
            zz_profit=shedule.insertNode(pick, deliver)
            if zz_profit>best_worker["up_profit"]:
                best_worker["best"]=ava_workers[i]
                index=i
            else:
                continue

        else:
            continue
    # 更新工人数据,容量，最终调度，报酬
    if index!=int('inf'):
        ava_workers[index].shedule=best_worker['best'].mid_shedule
        ava_workers[index].capacity+=1
        ava_workers[index].profit+=best_worker["up_profit"]
        return ava_workers[index]
    else:
        return None




# 贪心分配算法
def Greedy(workers,Tasks_Places,ra,ca):
    finally_ass=[]
    for t_p in Tasks_Places:
        best_worker=getFinallyWorker(workers,t_p,ra,ca)
        if best_worker!=None:
            finally_ass.append(attribute.GreedyResult(workers,t_p))
        else:
            continue

    return finally_ass

# 删除工人，任务，地点
# 遍历完了就要删任务和工人和地点了,获得的剩下的工人地点和任务
def getLeft(Assignment, workers, tasks, places):
    finish_workers = []
    finish_tasks = []
    finish_places = []
    if len(Assignment) > 0:
        for i in Assignment:
            finish_tasks+=i.task_palce.task
            finish_places+=i.task_palce.place
            finish_workers+=i.workerstr.woker


    w_jioa = list(set(workers).intersection(set(finish_workers)))
    for i in w_jioa:
        if i in workers:
            workers.remove(i)

    t_jioa = list(set(tasks).intersection(set(finish_tasks)))
    for i in t_jioa:
        if i in tasks:
            tasks.remove(i)
    p_jioa = list(set(places).intersection(set(finish_places)))
    for i in p_jioa:
        if i in places:
            places.remove(i)
    return workers, tasks, places



# 获取任务的可选工人（这里需要计算好工人的容量和调度）
if __name__ == '__main__':
    sum_worker, sum_task, sum_place = getSum()
    Fangwen_worker, Fangwen_task, Fangwen_place = 0, 0, 0
    # 要处理的数据
    deal_tasks = []
    deal_places = []
    deal_workers = []
    Fangwen_worker, batch_workers = getData(Fangwen_worker, sum_worker, "workers")
    Fangwen_task, batch_tasks = getData(Fangwen_task, sum_task, "tasks")
    Fangwen_place, batch_places = getData(Fangwen_place, sum_place, "places")
    deal_tasks += batch_tasks
    deal_workers += batch_workers
    deal_places += batch_places
