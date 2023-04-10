from datetime import datetime, timedelta
from geopy.distance import great_circle
import math

class Event:
    def __init__(self,event,earliest_arrival,latest_leaving):
        self.event=event
        self.earliest_arrival=earliest_arrival
        self.latest_leaving=latest_leaving
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, event):
        new_node = event
        new_node.next_node = self.head
        self.head = new_node



    # 这里有点错误，就是这里选择的是第一个可插入的地点，而不是最优的

    # 一次性插两个事件，为了方便确定取货在送货前面
    # 得到前一个结点，然后插入新结点，应该是前插法
    def insertNode(self,pick, deliver):
        current_node = self.head
        # 新事件的最晚结束时间不能早于调度中的最早开始时间
        while current_node.next is not None and pick.latest_leaving<= current_node.latest_leaving:
            current_node = current_node.next
        # 关键点：截止时间==最晚结束时间
        # 插入新事件x后，x之后的事件最早开始时间会变化，x之前事件的最晚离开时间会变化，但是关键点之前的最晚离开时间不会变化。
        while current_node is not None:
            slack_time = (current_node.latest_leaving - current_node.earliest_arrival).seconds
            distance = great_circle(((current_node.event.lat, current_node.event.lon), (pick.event.lat, pick.event.lon)).km)*60
            if distance > slack_time:
                # 不够时间，往下走
                current_node = current_node.next_node
            else:
                break

        if current_node.latest_leaving>=pick.earliest_arrival:
            pick.prev=current_node
            pick.next=current_node.next
            if current_node.next is not None:
                current_node.next.prev=pick
            current_node.next=pick
