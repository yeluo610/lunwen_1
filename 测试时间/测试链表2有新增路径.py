import math

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_node(self, new_node):
        """
        插入新结点并保证最短路径
        :param new_node: 新结点，字典类型，包含"position"，"start_time"和"end_time"三个键值对，以及"x"和"y"两个键值对表示坐标
        :return: 新增路径的长度
        """
        # 如果链表为空，直接将新结点作为头结点
        if self.head is None:
            self.head = Node(new_node)
            return 0

        # 将链表按照结束时间升序排列
        curr = self.head
        while curr.next is not None and curr.data["end_time"] <= new_node["end_time"]:
            curr = curr.next

        if curr.data["end_time"] <= new_node["start_time"]:
            # 如果新结点开始时间晚于等于当前结点结束时间，则将新结点插入到当前结点之后
            new_node = Node(new_node)
            new_node.prev = curr
            new_node.next = curr.next
            if curr.next is not None:
                curr.next.prev = new_node
            curr.next = new_node
        else:
            # 否则，将新结点作为新的头结点，并将原头结点作为新结点的后继结点
            new_node = Node(new_node)
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        # 计算新增路径的长度
        length = 0
        if curr is not None and curr.prev is not None:
            length += math.sqrt((curr.data["x"] - curr.prev.data["x"])**2 + (curr.data["y"] - curr.prev.data["y"])**2)
        if curr.next is not None:
            length += math.sqrt((curr.next.data["x"] - new_node["x"])**2 + (curr.next.data["y"] - new_node["y"])**2)
        if curr is not None:
            length += math.sqrt((curr.data["x"] - new_node["x"])**2 + (curr.data["y"] - new_node["y"])**2)
        return length
linked_list = DoublyLinkedList()
linked_list.insert_node({"position": "A", "start_time": 0, "end_time": 5, "x": 0, "y": 0})
linked_list.insert_node({"position": "B", "start_time": 3, "end_time": 10, "x": 2, "y": 2})
linked_list.insert_node({"position": "C", "start_time": 8, "end_time": 15, "x": 4, "y": 4})
print(linked_list)
