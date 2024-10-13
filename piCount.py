import matplotlib.pyplot as plt
import numpy as np

def vector(*args):
    # 默认起始点为零向量
    start = np.array((0, 0))
    
    # 检查最后一个参数是否为字符串
    if len(args) > 0 and isinstance(args[-1], str):
        # 如果字符串是'1'，则使用默认起始点
        if args[-1] == '1':
            vectors = args[:-1]
        else:
            # 否则不使用起始点
            vectors = args
            start = None
    else:
        vectors = args
    
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    
    # 如果提供了起始点，初始化总和向量为起始点
    if start is not None:
        sum_vector = np.array(start)
    else:
        # 如果没有提供起始点，则直接从第一个向量开始
        sum_vector = np.array(vectors[0])
        vectors = vectors[1:]
    
    # 累加所有向量
    for vec in vectors:
        sum_vector = np.add(sum_vector, vec)
    
    # 绘制从起始点到总和向量的箭头
    if start is not None:
        plt.annotate('', xy=tuple(sum_vector), xytext=tuple(start),
                     arrowprops={'facecolor': 'red', 'arrowstyle': "->"})
    else:
        # 如果没有提供起始点，只绘制向量本身
        plt.annotate('', xy=tuple(sum_vector), xytext=(0, 0),
                     arrowprops={'facecolor': 'red', 'arrowstyle': "->"})

# 使用示例
k = np.array([1, 3])
g = np.array([3, 4])

# 不提供起始点，将直接从第一个向量开始
vector(k, g)

# 提供起始点
vector(k, g, '1')

# 显示图形
plt.show()