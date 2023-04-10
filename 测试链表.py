# 用双向链表
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, new_node):
        new_node = Node(new_node)
        new_node.next = self.head
        self.head = new_node
    def insert_node(self, new_node):
        """
        插入新结点并保证最短路径
        :param new_node: 新结点，字典类型，包含"position"，"start_time"和"end_time"三个键值对
        """
        # 如果链表为空，直接将新结点作为头结点
        if self.head is None:
            self.head = Node(new_node)
            return 0

        # 将链表按照结束时间升序排列
        curr = self.head
        while curr.next is not None and curr.data["end_time"] <= new_node["end_time"]:
            curr = curr.next

        if curr.data["end_time"] >= new_node["start_time"]:
            # 如果新结点开始时间晚于等于当前结点结束时间，则将新结点插入到当前结点之后
            new_node = Node(new_node)
            # new_node.prev = curr
            # new_node.next = curr.next
            # if curr.next is not None:
            #     curr.next.prev = new_node
            # curr.next = new_node
            new_node.next=curr
            new_node.prev=curr.prev
            curr.prev.next=new_node
            curr.prev=new_node
        #     这里失败，得看看是啥回事儿

        else:
            # 否则，将新结点作为新的头结点，并将原头结点作为新结点的后继结点
            # new_node = Node(new_node)
            # new_node.next = self.head
            # self.head.prev = new_node
            # self.head = new_node
            new_node = Node(new_node)
            curr.next = new_node
            new_node.prev = curr


linked_list = DoublyLinkedList()
linked_list.insert_at_beginning({"position": "A", "start_time": 0, "end_time": 5})
linked_list.insert_node({"position": "B", "start_time": 3, "end_time": 10})

linked_list.insert_node({"position": "D", "start_time": 11, "end_time": 20})
linked_list.insert_node({"position": "C", "start_time": 8, "end_time": 15})
linked_list.insert_node({"position": "E", "start_time": 13, "end_time": 18})
print(linked_list)