import json
from property import attribute, lianbiao4
from geopy.distance import great_circle
import itertools
from datetime import datetime, timedelta
import math
import time
# 才一秒，艹！！！
# 是否可以在这里也用博弈，任务选地点

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

# ra是半径，ca的工人容量
# 工人获得可选任务
def getTask(worker, tasks,ra):
    ava_tasks = []
    for task in tasks:
        distance = great_circle((task.lat, task.lon), (worker.lat, worker.lon)).km
        # if (distance < worker.radius):
        if (distance < ra):
            ava_tasks.append(task)
    return ava_tasks

# 任务和地点的一对一匹配
def getTaskPlace(tasks, places1,ra):
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


# 任务和地点的一对一匹配
def getTaskPlace1(tasks, places1,ra):
    places = places1.copy()
    # 总的结果
    pipei = []
    for task in tasks:
        task.p_str=[]
        if len(places) > 0:
            for j in range(len(places)):
                distance = great_circle((task.lat, task.lon), (places[j].lat, places[j].lon)).km
                if len(list(set(task.good).intersection(set(places[j].goods)))) > 0 and distance < ra:
                    task.p_str.append({"ava_place":places[j],"dis":distance})
    for task in tasks:
        str1=""
        if len(task.p_str)!=0:
            task.p_str.sort(key=lambda x:x["dis"])
            str1=task.p_str[0]
        attribute.PlaceStr(task,task.p_str,str1)
    # 博弈：

    return tasks


    # for task in tasks:
    #     min_distance = float('inf')
    #     i = 0
    #     ava_place = None
    #     # 如果任务比地点多怎么办？
    #     if len(places) > 0:
    #         for j in range(len(places)):
    #             distance = great_circle((task.lat, task.lon), (places[j].lat, places[j].lon)).km
    #             # 距离最小，在任务可选范围内，有交叉的物品
    #             if (distance < min_distance and len(
    #                     list(set(task.good).intersection(set(places[j].goods)))) > 0 and distance < ra):
    #
    #                 min_distance = distance
    #                 i = j
    #                 ava_place = places[j]
    #         # 这里还需要判断ava_place是否为none，
    #         if ava_place is not None:
    #             pipei.append(attribute.Task_Place(task,ava_place))
    #             del places[i]
    #         else:
    #             pipei.append(attribute.Task_Place(task, None))
    #     else:
    #         pipei.append(attribute.Task_Place(task, None))
    # pipei2 = []
    # for p1 in pipei:
    #     if p1.place is not None:
    #         pipei2.append(p1)
    # return pipei2

if __name__ == '__main__':
    start_time = time.time()
    sum_worker, sum_task, sum_place = getSum()
    Fangwen_worker, Fangwen_task, Fangwen_place = 0, 0, 0
    # 要处理的数据
    deal_tasks = []
    deal_places = []
    deal_workers = []

    while  len(deal_tasks) < sum_task and len(deal_places) < sum_place:
        # 一次性获取小块数据
        # Fangwen_worker, batch_workers = getData(Fangwen_worker, sum_worker, "workers")
        Fangwen_task, batch_tasks = getData(Fangwen_task, sum_task, "tasks")
        Fangwen_place, batch_places = getData(Fangwen_place, sum_place, "places")
        deal_tasks += batch_tasks
        # deal_workers += batch_workers
        deal_places += batch_places
        Tasks_Places = getTaskPlace1(batch_tasks, batch_places, 8)
        print(Tasks_Places)
    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    print(elapsed_time)