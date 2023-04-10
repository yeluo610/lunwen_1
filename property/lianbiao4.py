from datetime import datetime, timedelta
from geopy.distance import great_circle
import math


# 定义事件,把事件插入调度中，查看合适的位置
class Event:
    # 位置，最早到达，最晚离开，任务负载
    # def __init__(self, lon=0, lat=0, earliest_arrival=0,
    #              latest_leaving=0):

    def __init__(self, lon=0, lat=0, earliest_arrival=datetime.strptime('00:00:00', '%H:%M:%S'), latest_leaving=datetime.strptime('00:00:00', '%H:%M:%S')):
        self.lon = lon
        self.lat = lat
        self.earliest_arrival = earliest_arrival
        self.latest_leaving = latest_leaving
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None

    # insert node at the beginning of the list
    def insert_at_beginning(self, event):
        new_node = event
        new_node.next_node = self.head
        self.head = new_node

    # insert node at the end of the list
    def insert_at_end(self, event):
        new_node = event
        if self.head is None:
            self.head = new_node
            return
        else:
            last_node = self.head
            while last_node.next_node is not None:
                last_node = last_node.next_node
            last_node.next_node = new_node
    def isVaild(self):
        current_node=self.head
        while current_node:
            if current_node.earliest_arrival>current_node.latest_leaving:
                return False
        return True
    # 这里有点错误，就是这里选择的是第一个可插入的地点，而不是最优的

    # 一次性插两个事件，为了方便确定取货在送货前面
    # 得到前一个结点，然后插入新结点，应该是前插法
    def insertNode(self, event, de_event):

        # 虚拟前结点
        p = Event()
        current_node = self.head
        p.next_node = current_node
        # 这个为取货的index，结点从0开始，比如结点1有空闲，事件可以在1前插入，则current_index=0，
        # 事件成为新的结点1，然后送货需要在节点1以后插入
        current_index = 0
        # 取送货的距离
        # distance1=great_circle((event.lat,event.lon),(de_event.lat,de_event.lon)).km
        # 结点的时间差 ;插入取货,需要考虑在最后一个结点后插的情况
        while current_node is not None:
            slack_time = (current_node.latest_leaving - current_node.earliest_arrival).seconds / 60
            # 该点是否有足够的空闲时间插入，如果有，则可以在该结点前插入事件
            distance = great_circle((current_node.lat, current_node.lon), (event.lat, event.lon)).km
            if distance > slack_time:
                # 不够时间，往下走
                current_node = current_node.next_node
                p = p.next_node
                current_index += 1
            else:
                break
        # 插入操作
        p.next_node = event
        event.next_node = current_node
        # 这个是前结点与事件的距离
        distance5 = math.ceil((great_circle((p.lat, p.lon), (event.lat, event.lon)).km)*60)
        # print("事件最早",event.earliest_arrival)
        # print("结点最早",p.earliest_arrival)
        if current_index==1:
            event.earliest_arrival=max((p.earliest_arrival + timedelta(seconds=distance5)),event.earliest_arrival)
        else:
            event.earliest_arrival = p.earliest_arrival + timedelta(seconds=distance5)
        # print("最后的事件最早",event.earliest_arrival)
        p = p.next_node
        # 这个是最终取货的下标，从0开始,这个可作前标
        quhuo_index = current_index

        # 更新最晚时间（这个只要更新事件的就行），判断是否为末尾插入
        if current_node is not None:
            distance2 = math.ceil((great_circle((event.lat, event.lon), (current_node.lat, current_node.lon)).km)*60)
            event.latest_leaving = min(de_event.latest_leaving,
                                       current_node.latest_leaving - timedelta(seconds=distance2))

        #  然后更新最早时间（这个是事件后面的结点都要更新）
        while current_node is not None:
            distance6 = math.ceil((great_circle((p.lat, p.lon), (current_node.lat, current_node.lon)).km)*60)
            current_node.earliest_arrival = p.earliest_arrival + timedelta(seconds=distance6)
            p = p.next_node
            current_node = current_node.next_node


        # 插入配送结点
        # 工人信息
        task_node = self.head
        # 虚拟前结点
        q = Event()
        q.next_node = task_node
        index = 0
        # 这里的q指向取物结点，task_node指向下一个结点

        # 这里卡bug了，取货index找不到？好奇怪啊，一直在task_node判断，然后if下不去
        while task_node is not None:
            # 找到取货后面
            if index <= quhuo_index:
                q = q.next_node
                task_node = task_node.next_node
                index += 1
            else:
                break
        while task_node is not None:
            slack_time1 = (task_node.latest_leaving - task_node.earliest_arrival).seconds / 60
            t_distance1 = great_circle((task_node.lat, task_node.lon), (de_event.lat, de_event.lon)).km
            if slack_time1 < t_distance1:
                task_node = task_node.next_node
                q = q.next_node
            else:
                break
            # else:
            #     # 这里有错误，记一下
            #     q = q.next_node
            #     task_node = task_node.next_node
            #     slack_time1 = (task_node.latest_leaving - task_node.earliest_arrival).seconds / 60
            #     t_distance1 = great_circle((task_node.lat, task_node.lon), (de_event.lat, de_event.lon)).km
            #     if slack_time1 < t_distance1:
            #         task_node = task_node.next_node
            #         q = q.next_node
            #         index += 1
            #     else:
            #         break
        # 插入操作
        q.next_node = de_event
        de_event.next_node = task_node
        # 更新事件的最早事件
        t_distance2 = math.ceil((great_circle((q.lat, q.lon), (de_event.lat, de_event.lon)).km)*60)
        de_event.earliest_arrival = q.earliest_arrival + timedelta(seconds=t_distance2)
        q = q.next_node
        # 更新事件最晚时间,判断是否是最后面插入
        if task_node is not None:
            t_distance3 = math.ceil((great_circle((task_node.lat, task_node.lon), (de_event.lat, de_event.lon)).km)*60)
            de_event.latest_leaving = min(de_event.latest_leaving,
                                          task_node.latest_leaving - timedelta(seconds=t_distance3))
        # 更新节点的最早时间
        while task_node is not None:
            t_distance4 = math.ceil((great_circle((q.lat, q.lon), (task_node.lat, task_node.lon)).km)*60)
            task_node.earliest_arrival = q.earliest_arrival + timedelta(seconds=t_distance4)
            q = q.next_node
            task_node = task_node.next_node
        # 这边跑不下去
        # 判断是调度否有效，时间差
        # 这里有错误，因为工人的开始时间是个变量，如果工人的开始时间大于
        x_valid = self.head
        # 这里最好判断是否为头元素
        isHead=0
        while x_valid is not None:
            if isHead==0:
                x_valid = x_valid.next_node
            else:
                if x_valid.earliest_arrival >= x_valid.latest_leaving:
                    return False
                else:
                    x_valid = x_valid.next_node
            isHead+=1
        return True

