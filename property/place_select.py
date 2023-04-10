# !/bin/python3
# quadtree.py
"""Quadtree Implementation in Python."""

import random
import json
import time
from property import attribute
from geopy.distance import great_circle



RECTANGLES = []
POINTS = []


# 获取范围，最大最小经纬度

class Point:
    """Properties of a point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # To make our object work with print function
    def __repr__(self):
        return f'{{"x": {self.x}, "y": {self.y}}}'


class Rectangle:
    """Creating a Rectangle."""

    def __init__(self, dXMin,dYMin,dXMax, dYMax ):
        """Properties of the Rectangle."""
        self.dXMin=dXMin
        self.dXMax=dXMax
        self.dYMin=dYMin
        self.dYMax=dYMax

        self.points = []  # list to store the contained points


    # 点在这个范围内,那这里就需要距离了
    def contains(self, point):
        check_x = self.dXMin < point.x <= self.dXMax,
        check_y = self.dYMin < point.y <= self.dYMax
        return check_x and check_y

    def insert(self, point):
        if not self.contains(point):
            return False

        self.points.append(point)
        return True

# 四叉树
class Quadtree:
    """Creating a quadtree."""

    def __init__(self, boundary, capacity):
        """Properties for a quadtree."""
        self.boundary = boundary  # object of class Rectangle
        self.capacity = capacity  # 4
        self.divided = False  # to check if the tree is divided or not
        self.northeast = None
        self.southeast = None
        self.northwest = None
        self.southwest = None

    def subdivide(self):
        """Dividing the quadtree into four sections."""
        x, y, x1, y1=self.boundary.dXMin,self.boundary.dYMin,self.boundary.dXMax,self.boundary.dYMax
        # distance_x=great_circle((x,y),(x1,y1))
        # distance_y=great_circle((x,y),(x1,y1))

        north_east = Rectangle((x+x1)/2, y, x1, (y+y1)/2)
        self.northeast = Quadtree(north_east, self.capacity)

        south_east = Rectangle((x+x1)/2, (y+y1)/2, x1, y1)
        self.southeast = Quadtree(south_east, self.capacity)

        south_west = Rectangle(x, (y+y1)/2, (x+x1)/2, y1)
        self.southwest = Quadtree(south_west, self.capacity)

        north_west = Rectangle(x, y, (x+x1)/2, (y+y1)/2)
        self.northwest = Quadtree(north_west, self.capacity)
        self.divided = True

        for i in self.boundary.points:
            self.northeast.insert(i)
            self.southeast.insert(i)
            self.northwest.insert(i)
            self.southwest.insert(i)

    def insert(self, point):
        # If this major rectangle does not contain the point no need to check subdivided rectangle
        if not self.boundary.contains(point):
            return

        if len(self.boundary.points) < self.capacity:
            self.boundary.insert(point)  # add the point to the list if the length is less than capacity
        else:
            if not self.divided:
                self.subdivide()

            self.northeast.insert(point)
            self.southeast.insert(point)
            self.southwest.insert(point)
            self.northwest.insert(point)

    def printsub(self):
        global RECTANGLES, POINTS
        if self.divided is False and len(self.boundary.points):
            print((self.boundary.dXMin,self.boundary.dYMin,self.boundary.dYMin,self.boundary.dYMax))
            list=[]
            for u in self.boundary.points:
                list.append({"x":u.x,"y":u.y})
            print(list)
            # print(self.boundary.points[0].x)
            RECTANGLES.append(self.boundary)
            POINTS.append(self.boundary.points)
        else:
            if self.northeast is not None:
                self.northeast.printsub()
            if self.southeast is not None:
                self.southeast.printsub()
            if self.northwest is not None:
                self.northwest.printsub()
            if self.southwest is not None:
                self.southwest.printsub()
# 算距离
import math
def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(math.radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    distance = 2 * math.asin(math.sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    # 单位是km
    distance = round(distance / 1000, 4)
    return distance


# 得到了四叉树后，需要进行遍历，遍历每个小矩形的任务，得到他们的候选地点
# 反正都是存储为对象的
def getPOI(task,places):
    TTP=[]
    for place in places:
        distance = geodistance(place.longitude, place.latitude, task.longitude, task.latitude)
        if distance < 1000 and len(list(set(task.goods).intersection(set(place.category)))) > 0:
            TTP.append(place)
    return TTP

#真正的遍历中
def select(points,places):
    # 一共4个组，一个组里最多只有4个任务
    # 这里少了判断任务是否是地点集最少的那个


    # 第一个组：POINTS[0]
    # 组中其他任务的地点集与第一个任务地点的距离
    minD={}
    # P放的是所有任务对应的一个地点{任务：地点}
    P={}
    maxoptP=float('inf')
    optP={}
    for i in  range(1,len(POINTS[0])):
    #     选第一个为Tm，这里应该建立一个对象，存储距离和地点信息
    #     minD[POINTS[0][i].place_id]=float('inf')
        minD[POINTS[0][i].task_id] = attribute.DisandPlace(float('inf'),places)

    for place in getPOI(POINTS[0][0],places):
        # P.append(place)
        P[POINTS[0][0].task_id]=place
        for i in range(1, len(POINTS[0])):
            for place2 in getPOI(POINTS[0][i],places):
                dis=geodistance(place.x,place.y,place2.x,place2.y)
                if(dis<minD[POINTS[0][i].task_id].distance):
                    minD[POINTS[0][i].task_id].distance=dis
        #  遍历minD中的places，把它加入到P中
        for k,v in minD.items():
            P[k]=v.place
        # 这里可能得修改一下，字典里面没有distance
        maxP=max(minD.values().distance)

        if len(optP)==0 or maxP < maxoptP:
            maxoptP=maxP
            optP=P
    # 得到的是{任务：地点}的集合
    return optP






    TTP=getPOI()




if __name__ == '__main__':
    root = Rectangle(-119,26,-72,40)
    qt = Quadtree(root, 4)
    random.seed(time.time())

    file = open("../game/Places2.json", 'r', encoding='utf-8')

    for line1 in file.readlines():
        line1 = json.loads(line1)
        p=attribute.Place(line1['place_id'],line1['longitude'],line1['latitude'],line1['category'],line1['rank'])
        qt.insert(p)

    qt.printsub()
    # 被分为4个矩形了，但是上面的(x + w / 2, y, x1, y+h/2)有点错误，需要改正
    # RECTANGLES是边界加点，POINTS是总点

    # for i in range(len(RECTANGLES)):
    #     for points in RECTANGLES[i].points:
    #         print(len(points))
    # for point in POINTS:
    #     for i in range(len(point)):
    #         print(point[i].x)
    print(POINTS[0][0])

# 这里应该是将任务四叉树化，而不是places