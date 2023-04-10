import json
import random
# csv转成json格式，由i来控制从哪儿转变
def csvTojson():
    # 列名
    column=['Trip ID', 'Taxi ID', 'Trip Start Timestamp', 'Trip End Timestamp', 'Trip Seconds', 'Trip Miles', 'Pickup Census Tract', 'Dropoff Census Tract', 'Pickup Community Area', 'Dropoff Community Area', 'Fare', 'Tips', 'Tolls', 'Extras', 'Trip Total', 'Payment Type', 'Company', 'Pickup Centroid Latitude', 'Pickup Centroid Longitude', 'Pickup Centroid Location', 'Dropoff Centroid Latitude', 'Dropoff Centroid Longitude', 'Dropoff Centroid  Location']
    fo=open("Taxi_Trips.csv","r",encoding="ISO-8859-1")  #打开csv文件
    ls=[]
    i=0
    for line in fo:
        i=i+1
        if(i<1000):
            line=line.replace("\n","")  #将换行换成空
            ls.append(line.split(','))  #以，为分隔符
        else:
            break
    fo.close()  #关闭文件流
    fw=open("task2.json","w",encoding="utf-8")  #打开json文件
    for i in range(1,len(ls)):  #遍历文件的每一行内容，除了列名
        ls[i]=dict(zip(ls[0],ls[i]))  #ls[0]为列名，所以为key,ls[i]为value,
        #zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
    json.dump(ls[1:],fw,sort_keys=True,indent=0)
    #将Python数据类型转换成json格式，编码过程
    # 默认是顺序存放，sort_keys是对字典元素按照key进行排序
    #indet参数用语增加数据缩进，使文件更具有可读性
    fw.close()


# 将数据拆分为两个表,这个是Tasks和Places
def divideJson():
    json_file=json.load(open("task2.json",'r'))
    i=0
    # 创建物品和等级
    all_skills = ['A', 'B', 'C', 'D', 'E','F']
    tasks=[]
    places=[]
    for line in json_file:
        n = random.randint(3, 6)
        goods = random.sample(all_skills, n)

        # task={"task_id":i,"Longitude":line["Dropoff Centroid Longitude "],"Latitude":line["Dropoff Centroid Latitude "],"start_time":line["Trip Start Timestamp "],
        #       "expire_time":line["Trip End Timestamp "],"good":random.sample(all_skills, 1),"radius":10,"rank":random.randint(1, 5),"fare":line["Fare "]}
        # place={"place_id":i,"Longitude":line["Pickup Centroid Longitude "],"Latitude":line["Pickup Centroid Latitude "],"goods":goods,"rank":random.randint(1, 5)}

        task = {"task_id": i, "Longitude": line["Dropoff Centroid Longitude"],
                "Latitude": line["Dropoff Centroid Latitude"], "start_time": line["Trip Start Timestamp"],
                "expire_time": line["Trip End Timestamp"], "good": random.sample(all_skills, 1), "radius": 10,
                "rank": random.randint(1, 5), "fare": line["Fare"]}
        place = {"place_id": i, "Longitude": line["Pickup Centroid Longitude"],
                 "Latitude": line["Pickup Centroid Latitude"], "goods": goods, "rank": random.randint(1, 5)}


        i=i+1
        with open('Places.json', 'a', encoding='utf8') as fp:
            # fp.write(json.dumps(place,indent=4,ensure_ascii=False))
            fp.write(json.dumps(place) + "\n")
        # with open('Tasks.json', 'a', encoding='utf8') as fp:
        #     fp.write(json.dumps(task) + "\n")


        # print(line["Dropoff Centroid Latitude "])

# divideJson()

# 将数据拆分为两个表,这个是Tasks2和Places2
# 删除了那些没有经纬度的数据
def divideJson2():
    json_file=json.load(open("task2.json",'r'))
    i=0
    # 创建物品和等级
    all_skills = ['A', 'B', 'C', 'D', 'E','F']
    tasks=[]
    places=[]
    for line in json_file:
        if(line["Dropoff Centroid Longitude"]=="" or line["Pickup Centroid Longitude"]==""):
            continue
        else:
            n = random.randint(3, 6)
            goods = random.sample(all_skills, n)
            task = {"task_id": i, "Longitude": line["Dropoff Centroid Longitude"],
                    "Latitude": line["Dropoff Centroid Latitude"], "start_time": line["Trip Start Timestamp"],
                    "expire_time": line["Trip End Timestamp"], "good": random.sample(all_skills, 1), "radius": 10,
                    "rank": random.randint(1, 5), "fare": line["Fare"]}
            tasks.append(task)
            place = {"place_id": i, "Longitude": line["Pickup Centroid Longitude"],
                     "Latitude": line["Pickup Centroid Latitude"], "goods": goods, "rank": random.randint(1, 5)}
            places.append(place)


            i=i+1
    with open('Places2.json', 'w', encoding='utf8') as fp:
        fp.write(json.dumps(places,indent=4,ensure_ascii=False))
        # fp.write(json.dumps(places) + "\n")
    with open('Tasks2.json', 'w', encoding='utf8') as fp:
        fp.write(json.dumps(tasks,indent=4,ensure_ascii=False))


# 根据task的地点，开始时间来获得工人数据
def prodeceWorker():
    json_file=json.load(open("Tasks2.json",'r'))
    i=0
    workers=[]
    for line in json_file:
        worker={"user_id":i,"Longitude":line["Longitude"],"Latitude":line["Latitude"],"time":line["start_time"],"capacity":4,"radius":5,'rank':random.randint(1, 5)}
        workers.append(worker)
        i=i+1
    with open('Workers2.json', 'w', encoding='utf8') as fp:
        fp.write(json.dumps(workers,indent=4,ensure_ascii=False))


if __name__ == '__main__':
    # 转格式
    # csvTojson()
    # # 拆分这个是Tasks和Places
    # divideJson()
    # 拆分这个是Tasks2和Places2
    # divideJson2()
    prodeceWorker()