import json
from property import attribute, lianbiao4
from geopy.distance import great_circle
import itertools
from datetime import datetime, timedelta
import math
import time





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

# 任务获得可选工人,和最好的那个
# 这里不能更新链表呀
def getWorker(workers, Tasks_Place,ra):
    # 这里的worker应该要有调度表和容量，刚开始是null和0
    ava_worker = []
    for worker in workers:
        # 工人在任务的可选范围内
        if great_circle((Tasks_Place.task.lat, Tasks_Place.task.lon), (worker.lat, worker.lon)).km <ra:
            e_d1 = math.ceil(
                (great_circle((Tasks_Place.place.lat, Tasks_Place.place.lon), (Tasks_Place.task.lat, Tasks_Place.task.lon)).km) * 60)
            pick = lianbiao4.Event(Tasks_Place.place.lon, Tasks_Place.place.lat,
                                    datetime.strptime(Tasks_Place.task.start_time[11:-3], '%H:%M:%S'),
                                    datetime.strptime(Tasks_Place.task.expire_time[11:-3], '%H:%M:%S') - timedelta(
                                        seconds=e_d1))
            deliver = lianbiao4.Event(Tasks_Place.task.lon, Tasks_Place.task.lat,
                                       datetime.strptime(Tasks_Place.task.start_time[11:-3], '%H:%M:%S') + timedelta(
                                           seconds=e_d1),
                                       datetime.strptime(Tasks_Place.task.expire_time[11:-3], '%H:%M:%S'))

            # 这个工人为新工人
            if worker.capacity==0:
                head_worker = lianbiao4.Event(worker.lon, worker.lat, datetime.strptime(worker.time[11:-3], '%H:%M:%S'),
                                              datetime.strptime(worker.time[11:-3], '%H:%M:%S'))
                schedule = lianbiao4.LinkedList()
                schedule.insert_at_beginning(head_worker)
                schedule.insertNode(pick, deliver)
            #     这个工人已经有任务在身
            else:
                schedule=worker.shedule
                schedule.insertNode(pick, deliver)



            pass
        else:
             continue




    return ava_worker

# 贪心分配算法
def Greedy(workers,Tasks_Places,ra):
    finally_ass=[]
    for t_p in Tasks_Places:
        best_worker=None
        getWorker(workers,t_p,ra)
        for i in len(workers):

            pass


    pass

# 获得任务的单个策略
def getSingleStrategy(worker,tasks,Tasks_Places,ra):
    # 可选任务
    ava_tasks=getTask(worker, tasks,ra)
    single_str=[]
    for t_p in Tasks_Places:
        if t_p.task in ava_tasks:
            # 选完距离最小，接着判断工人是否能够达到
            start_time = datetime.strptime(t_p.task.start_time[11:-3], '%H:%M:%S')
            # 先忽视工人时间对任务的影响
            expire_time = datetime.strptime(t_p.task.expire_time[11:-3], '%H:%M:%S')
            # 任务持续时间（分钟）
            duration = (expire_time - start_time).seconds / 60
            # 看工人从现在位置到地点再到任务所需要的距离跟时间相比
            distance = great_circle((worker.lat, worker.lon), (t_p.place.lat, t_p.place.lon)).km + great_circle(
                (t_p.place.lat, t_p.place.lon), (t_p.task.lat, t_p.task.lon)).km
            if duration>distance:
                single_str.append(t_p)
    return single_str

def getCombineStrategy(worker,tasks,Tasks_Places,ra,ca):
    pipei=getSingleStrategy(worker,tasks,Tasks_Places,ra)
    workerStrategy = attribute.WorkerStr(worker, [], None)
    strategy=[]
    # 每轮要丢弃的东西
    remove_tasks=[]

    # 如果此时任务数量小于容量，则只要遍历到任务数量就行了
    # if len(pipei) <= worker.capacity:
    #     bianli = len(pipei) + 1
    # else:
    #     bianli = worker.capacity + 1
    if len(pipei) <= ca:
        bianli = len(pipei) + 1
    else:
        bianli = ca + 1

    for i in range(1, bianli):
        # 得到排列组合，从1开始，到capacity，
        # 看5选3是否有加入的策略，没有就不用看后面的了
        mini_strategy = []
        for j in itertools.combinations(pipei, i):  # 例如(1,2);(1,3)
            if i==1:
                # 看每个组合里的任务地点集，给他们调度排序
                # 先插入地点再插入任务
                head_worker = lianbiao4.Event(worker.lon, worker.lat, datetime.strptime(worker.time[11:-3], '%H:%M:%S'),
                                              datetime.strptime(worker.time[11:-3], '%H:%M:%S'))
                schedule = lianbiao4.LinkedList()
                schedule.insert_at_beginning(head_worker)
                flag = False
                s_tasks = []
                s_places = []
                for k in j:  # 例如1,2
                    # 遍历调度,如果有空闲时间，则可以插在前面；没有空闲时间，则只能插在后面
                    # 记录pick的插入位置，deliver只能插在pick的后面
                    # 简洁简单化一下：插入到第一个合适的位置
                    s_tasks.append(k.task)
                    s_places.append(k.place)
                    d1 = math.ceil((great_circle((k.place.lat, k.place.lon), (k.task.lat, k.task.lon)).km)*60)
                    # 取物的最早时间是任务的开始时间，最晚时间是任务最晚-距离
                    # 送货的最早时间的任务的开始时间+距离，最晚是任务的最晚时间
                    # 所以上面的最早晚于最晚，则不用看这个了
                    pick = lianbiao4.Event(k.place.lon, k.place.lat,
                                           datetime.strptime(k.task.start_time[11:-3], '%H:%M:%S'),
                                           datetime.strptime(k.task.expire_time[11:-3], '%H:%M:%S') - timedelta(seconds=d1))
                    deliver = lianbiao4.Event(k.task.lon, k.task.lat,
                                              datetime.strptime(k.task.start_time[11:-3], '%H:%M:%S') + timedelta(
                                                  seconds=d1),
                                              datetime.strptime(k.task.expire_time[11:-3], '%H:%M:%S'))
                    if pick.earliest_arrival>=pick.latest_leaving or deliver.earliest_arrival>=deliver.latest_leaving:
                        break
                    else:
                        flag = schedule.insertNode(pick, deliver)

                # 符合条件的加入
                if flag:
                    single=attribute.zuizhong(schedule, s_tasks, s_places)
                    workerStrategy.strs.append(single)
                    mini_strategy.append(single)
                #     不符合条件的就记录这个东西
                else:
                    remove_tasks.append(j)
            else:
                flag1=False
                for r in remove_tasks:
                    if r in j:
                        break
                    else:
                        continue
                if flag1:
                #     要插入的元素只有j[-1],其他的在上一轮的获取
                    e_d1 = math.ceil((great_circle((j[-1].place.lat, j[-1].place.lon), (j[-1].task.lat, j[-1].task.lon)).km) * 60)
                    pick1 = lianbiao4.Event(j[-1].place.lon, j[-1].place.lat,
                                            datetime.strptime(j[-1].task.start_time[11:-3], '%H:%M:%S'),
                                            datetime.strptime(j[-1].task.expire_time[11:-3], '%H:%M:%S') - timedelta(seconds=e_d1))
                    deliver1 = lianbiao4.Event(j[-1].task.lon, j[-1].task.lat,
                                               datetime.strptime(j[-1].task.start_time[11:-3], '%H:%M:%S') + timedelta(
                                                  seconds=e_d1),
                                               datetime.strptime(j[-1].task.expire_time[11:-3], '%H:%M:%S'))
                    if pick1.earliest_arrival >= pick1.latest_leaving or deliver1.earliest_arrival >= deliver1.latest_leaving:
                        break
                    else:
                    #     这里要倒序遍历workerStrategy,然后找到包含j[0:-1]的那个策略
                        alltasks=[]
                        flag3=False
                        c_t=[]
                        c_p=[]
                        c_s= lianbiao4.LinkedList()
                        for b in j[0:-1]:
                            alltasks.append(b.task)
                        for v in workerStrategy.strs[::-1]:
                            if len(alltasks)==len(list(set(alltasks).intersection(set(v.tasks)))):
                                c_t=v.tasks.copy()
                                c_p=v.places.copy()
                                c_s=v.schedule.copy()
                                c_t.append(j[-1].task)
                                c_p.append(j[-1].place)
                                flag3=c_s.insertNode(pick1, deliver1)
                        if flag3:
                            single1 = attribute.zuizhong(c_s, c_t, c_p)
                            workerStrategy.strs.append(single1)
                            mini_strategy.append(single1)
                            workerStrategy.strs.append()
                # 判断元素是否在remove_tasks里面
                if j[0:-1] in remove_tasks:
                    continue
                else:
                    pass

        if len(mini_strategy) == 0:
            break
        else:

            strategy += mini_strategy
    # 策略翻转，多的任务和工人集在前面
    strategy.reverse()

    return workerStrategy





def game(wokers, tasks,Tasks_Places,ra,ca):
    # 得到初始的分配
    init_Assignment = []
    for worker in wokers:
        workerStrategy = getCombineStrategy(worker, tasks,Tasks_Places,ra,ca)
        if len(workerStrategy.strs)>0:
            workerStrategy.finnalStr=workerStrategy.strs[0]
            init_Assignment.append(workerStrategy)

    if len(init_Assignment) > 0:

        # 遍历工人
        g_iter = 0
        Ap2 = []
        # 至少要轮一次
        # 遍历完了就要删任务和工人和地点了
        while (Ap2 != init_Assignment or g_iter <= len(wokers)):
            Ap2 = init_Assignment
            for i in init_Assignment:
                g_iter+=1
                if len(i.strs)>0:
                    worker_index=0
                    for st in i.strs:
                        flag=0
                        isalllNone = 0
                        for j in range(len(init_Assignment)):
                            if init_Assignment[j].worker.user_id==i.worker.user_id:
                                worker_index = j
                            else:
                                if init_Assignment[j].finnalStr is not None:
                                    chonghe_task = list(set(st.tasks).intersection(
                                        set(init_Assignment[j].finnalStr.tasks)))
                                    chonghe_place = list(
                                        set(st.places).intersection(set(init_Assignment[j].finnalStr.places)))
                                    if len(chonghe_task) > 0 or len(chonghe_place) > 0:
                                        flag = 0
                                    else:
                                        flag = 1
                                        continue
                                else:
                                    isalllNone += 1
                                    continue

                        if flag == 1 or isalllNone == len(init_Assignment) - 1:
                            init_Assignment[worker_index].finnalStr = st
                            break
                        elif flag == 0:
                            init_Assignment[worker_index].finnalStr= None
                            continue
                else:
                     continue

        print("遍历次数", g_iter)
    else:
        print("所有工人的策略集为空")
    return init_Assignment


# 遍历完了就要删任务和工人和地点了,获得的剩下的工人地点和任务
def getLeft(Assignment, workers, tasks, places):
    finish_workers = []
    finish_tasks = []
    finish_places = []
    if len(Assignment) > 0:
        for i in Assignment:
            if i.finnalStr is not None:
                finish_tasks += i.finnalStr.tasks
                finish_places += i.finnalStr.places
                finish_workers.append(i.worker)
                # if len(i["strategy"].tasks) == i["worker"].capacity:
                #     finish_workers.append(i["worker"])

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


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)
    # 总数量
    sum_worker, sum_task, sum_place = getSum()

    sum_task1 = [100,300,500,800]

    def Effect_Task(num_place):
        # 初始访问值
        Fangwen_worker, Fangwen_task, Fangwen_place = 0, 0, 0
        # 要处理的数据
        deal_tasks = []
        deal_places = []
        deal_workers = []
        iter1 = 0
        isEmpty=0
        while len(deal_workers) > 0 and len(deal_tasks) > 0 and len(deal_places) > 0 or iter1 == 0:
            # 一次性获取小块数据
            Fangwen_worker, batch_workers = getData(Fangwen_worker, sum_worker, "workers")
            Fangwen_task, batch_tasks = getData(Fangwen_task, sum_task, "tasks")
            Fangwen_place, batch_places = getData(Fangwen_place, num_place, "places")
            deal_tasks += batch_tasks
            deal_workers += batch_workers
            deal_places += batch_places
            Tasks_Places=getTaskPlace(deal_tasks,deal_places,8)
            # 如果超过四次没有有效的任务分配，maybe表示剩下的工人，任务，地点无法完成分配
            ass = game(deal_workers, deal_tasks, Tasks_Places,8,4)
            if len(ass)==0:
                isEmpty+=1
            else:
                isEmpty=0
            if isEmpty>10:
                print("结束了")
                break
            print(ass)
            cdu = 0
            for i in ass:
                if i.finnalStr is not None:
                    cdu += 1
            print("得到的ass不为空的个数",cdu,"while的遍历次数",iter1)
            # left_workers, left_tasks, left_places = getLeft(ass, deal_workers, deal_tasks, deal_places)
            deal_workers, deal_tasks, deal_places = getLeft(ass, deal_workers, deal_tasks, deal_places)
            iter1 += 1





    times=[]
    for t in sum_task1:
        start_time = time.time()
        Effect_Task(t)

        end_time=time.time()
        elapsed_time=int(end_time-start_time)
        times.append(elapsed_time)

    # plt.ylim([0,150])
    plt.plot(sum_task1,times,'-o')
    plt.xlabel("地点数量",fontproperties=font)
    plt.ylabel("响应时间",fontproperties=font)
    plt.title("地点数量对响应时间的影响",fontproperties=font)
    for i in range(len(sum_task1)):
        plt.text(sum_task1[i], times[i], f'{times[i]:.2f}')

    plt.savefig("Effect_place.png")
    plt.show()

    # print(getStrategy2(batch_workers[0], batch_tasks, batch_places))
