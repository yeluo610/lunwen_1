# 网格存储工人,输入批工人
class GeoSearch:
    def __init__(self,workers):
        self.worker=workers
        # 读取空间数据到内存中,并获取整个空间数据的外接矩形范围
        objArray = []
        dXMax = -999.0  # 初始化一个无穷小的范围
        dXMin = 999.0
        dYMax = -999.0
        dYMin = 999.0

        for worker in workers:
            mydXMax = mydXMin = float(worker.lon)
            mydYMax = mydYMin = float(worker.lat)
            objArray.append(worker)
            if dXMax < mydXMax:
                dXMax = mydXMax
            if dXMin > mydXMin:
                dXMin = mydXMin
            if dYMax < mydYMax:
                dYMax = mydYMax
            if dYMin > mydYMin:
                dYMin = mydYMin
        #         确定范围
        print("网格范围", dXMax, dXMin, dYMax, dYMin)
        # 将整个空间范围划分等份的网格
        self.m_nGridCount = 32
        self.m_dOriginX = dXMin
        self.m_dOriginY = dYMin
        # 每个小网格的大小范围,保留4位小数
        self.dSizeX = round(float((dXMax - dXMin) / self.m_nGridCount), 4)
        self.dSizeY = round(float((dYMax - dYMin) / self.m_nGridCount), 4)
        self.m_vIndexCells = []
        for i in range(0, self.m_nGridCount * self.m_nGridCount):
            self.m_vIndexCells.append([])
        # self.m_vIndexCells = [list()] * (self.m_nGridCount * self.m_nGridCount)
        print("小网格信息", self.m_nGridCount, self.m_dOriginX, self.m_dOriginY,
              self.dSizeX, self.dSizeY, len(self.m_vIndexCells), len(objArray))

        # 将每个对象注册到空间索引中
        for obj in objArray:
            # 确定地点的编号么？
            nXCol = int((obj.x - self.m_dOriginX) / self.dSizeX)
            nYCol = int((obj.y - self.m_dOriginY) / self.dSizeY)
            if nXCol < 0:
                nXCol = 0
            if nXCol >= self.m_nGridCount:
                nXCol = self.m_nGridCount - 1
            if nYCol < 0:
                nYCol = 0
            if nYCol <= self.m_nGridCount:
                nYCol = self.m_nGridCount - 1

            iIndex = nXCol * self.m_nGridCount + nYCol
            self.m_vIndexCells[iIndex].append(obj)

        # 这里可能需要修改一下，应该是dXMin，dYMin为任务的位置，然后加上一个radius，则为可选的范围，找到备选工人

    def Search(self, dXMax, dXMin, dYMax, dYMin):
        # 计算输入外接矩形所在网格的范围
        # 这里就很有问题了,如果距离很小,还没有一度,怎么设置范围,都集中在一个方块里了
        nXMin = int((dXMin - self.m_dOriginX) / self.dSizeX)
        nXMax = int((dXMax - self.m_dOriginX) / self.dSizeX + 0.5)  # 四舍五入
        nYMin = int((dYMin - self.m_dOriginY) / self.dSizeY)
        nYMax = int((dYMax - self.m_dOriginY) / self.dSizeY + 0.5)
        print(nXMin, nXMax, nYMin, nYMax)

        # 遍历这些网格得到所有符合条件的设备
        for n in range(nYMin, nYMax):
            for m in range(nXMin, nXMax):
                iIndex = n * self.m_nGridCount + m
                # 找到小格子，然后找符合的工人信息
                for obj in self.m_vIndexCells[iIndex]:
                    if obj.log <= dXMax and obj.log>= dXMin and obj.lat <= dYMax and obj.lat >= dYMin:
                        print("待选名字", obj.id)

if __name__ == '__main__':
    geoSearch = GeoSearch()
    geoSearch.Search( -72.049023019,-119.99051283,40.94398,26.146156)