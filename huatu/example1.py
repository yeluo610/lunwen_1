# import matplotlib.pyplot as plt; plt.rcdefaults()
# import numpy as np
# import matplotlib.pyplot as plt
#
# objects = ('XFTRL', 'DNN', 'Wide&Deep', 'AutoInt', 'DIN')
# y_pos = np.arange(len(objects))
#
# performance = [0.684,0.70,0.695,0.704,0.712]
#
#
# plt.ylim([0.68, 0.715])
# plt.bar(y_pos, performance, align='center', alpha=0.5, color=['black', 'red', 'green', 'blue', 'cyan'])
# plt.xticks(y_pos, objects, rotation=15)
# plt.ylabel('AUC')
#
# plt.savefig('previous.eps')
# plt.show()




# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
#
# font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)
#
# x = [0, 1, 2, 3, 4]
# y = [10, 24, 36, 40, 28]
#
# plt.bar(x, y, width=0.5, color='steelblue', edgecolor='black', linewidth=2, tick_label=['A', 'B', 'C', 'D', 'E'])
#
# plt.title('柱状图示例',fontproperties=font)
# plt.xlabel('X 轴标签',fontproperties=font)
# plt.ylabel('Y 轴标签',fontproperties=font)
#
# plt.show()


# import matplotlib.pyplot as plt; plt.rcdefaults()
# import numpy as np
# import matplotlib.pyplot as plt
#
# fig = plt.figure()
#
# objects = ('XFTRL', 'DNN', 'Wide&Deep', 'AutoInt', 'DIN')
# y_pos = np.arange(len(objects))
#
# performance = [0.684,0.70,0.695,0.704,0.712]
#
#
# plt.ylim([0.68, 0.715])
#
# ax = fig.add_subplot(111)
# bars = ax.bar(y_pos, performance, align='center', alpha=0.5,  color='white')
# patterns = ('-', '+', 'x', '\\', 'O')
# for bar, pattern in zip(bars, patterns):
#     bar.set_hatch(pattern)
#
# plt.xticks(y_pos, objects, rotation=15,fontsize=18)
# plt.ylabel('AUC',fontsize=18)
#
#
# plt.savefig('previous2.eps')
# plt.show()



import time
import matplotlib.pyplot as plt
from matplotlib.font_manager import  FontProperties
font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)

def my_func(param):
    # 在这里编写需要进行测试的函数
    time.sleep(param)  # 模拟函数执行时间

params = [1, 2, 3, 4, 5]  # 不同的参数列表

times = []  # 用于存储运行时间

for p in params:
    start_time = time.time()  # 记录开始时间
    my_func(p)  # 调用需要测试的函数
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    times.append(elapsed_time)  # 将运行时间添加到列表中

plt.plot(params, times, '-o')  # 画出折线图
plt.xlabel('参数',fontproperties=font)
plt.ylabel('运行时间（秒）',fontproperties=font)
plt.title('参数对应的运行时间',fontproperties=font)
for i in range(len(params)):
    plt.text(params[i],times[i],f'{times[i]:.2f}')
plt.savefig("1.png")
plt.show()
