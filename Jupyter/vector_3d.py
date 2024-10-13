import matplotlib.pyplot as plt
import numpy as np

def draw_3DPoint(points, style=None):
	"""
	绘制三维点坐标的函数。
	
	参数:
	points -- 一个形状为(N, 3)的数组，其中N是点的数量，每一行代表一个点的(x, y, z)坐标。
	style -- 一个字典，包含用于scatter方法的样式参数，如颜色、标记和大小。
	"""
	# 创建一个新的图形
	fig = plt.figure()
	
	# 添加一个3D坐标轴
	ax = fig.add_subplot(111, projection='3d')
	
	# 分别提取x, y, z坐标
	x = points[:, 0]
	
	y = points[:, 1]
	z = points[:, 2]
	
	# 默认样式
	default_style = {'c': 'b', 'marker': 'o', 's': 50}
	
	# 更新样式，如果有提供
	if style is not None:
		default_style.update(style)
	
	# 使用scatter方法绘制点
	ax.scatter(x, y, z, **default_style)
	
	# 设置坐标轴标签
	ax.set_xlabel('X 轴')
	ax.set_ylabel('Y 轴')
	ax.set_zlabel('Z 轴')
	
	# 显示图形
	plt.show()

def draw_3DLine(ax, line, style=None):
	"""
   在三维空间中绘制线段，并在每个顶点处标记坐标。
    
    此函数接受一个三维坐标轴对象和一个包含顶点坐标的数组，然后在坐标轴上绘制线段。
    它还允许通过样式字典自定义线段和标记点的样式。
    
    参数:
    ax : matplotlib.axes._subplots.Axes3DSubplot
        用于绘制的三维坐标轴对象。
        
    line : numpy.ndarray
        一个形状为 (N, 3) 的数组，其中 N 是点的数量，每一行代表一个点的 (x, y, z) 坐标。
        
    style : dict, optional
        一个字典，包含用于 `plot` 方法的样式参数，如颜色、线型和线宽。
        默认值为 None，此时将使用内置的默认样式。
        
    默认样式:
        {'c': 'b', 'marker': 'o', 's': 50}
        其中 'c' 代表颜色（'b' 为蓝色），'marker' 代表标记样式（'o' 为圆圈），'s' 代表标记大小。
        
    示例:
        # 创建三维坐标轴
    	fig,ax = plt.subplots(subplot_kw={'projection': '3d'})
        # 定义线段的顶点
    	line_vertices = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
        # 调用函数绘制线段
    	draw_3DLine(ax, line_vertices, style={'c': 'r', 'linewidth': 2})
        # 显示图形
    	plt.show()
	"""
	x = line[:, 0]
	y = line[:, 1]
	z = line[:, 2]
	
	default_style = {'c': 'b', 'marker': 'o', 's': 50}
	
	# 更新样式，如果有提供
	if style is not None:
		default_style.update(style)
	# 绘制三维线条
	ax.plot(x, y, z, label='3D Line')
	
	# 在每个数据点处添加坐标标签
	for i in range(len(x)):
		ax.text(x[i], y[i], z[i], f'({x[i]}, {y[i]}, {z[i]})')

def draw_3Darrow(start, end, head_length=0.05, head_width=0.1):
	"""
  在3D空间中绘制一个箭头，表示从起点到终点的方向。
  
  参数:
  start : tuple
	  箭头的起点坐标，格式为 (x_start, y_start, z_start)。
  end : tuple
	  箭头的终点坐标，格式为 (x_end, y_end, z_end)。
  head_length : float, optional
	  箭头头部长度，相对于箭头总长度的比例。默认为 0.05。
  head_width : float, optional
	  箭头头部宽度，相对于箭头总宽度的比例。默认为 0.1。
	  
  返回:
  matplotlib.figure.Figure
	  返回一个包含绘制箭头的3D坐标轴的matplotlib图形对象。
	  
  示例:
   fig = draw_3Darrow((0, 0, 0), (1, 1, 1))
   plt.show()  # 显示箭头
  """
	
	fig = plt.figure()
	# 添加一个3D坐标轴
	ax = fig.add_subplot(111, projection='3d')
	# 计算箭头方向
	direction = np.array(end) - np.array(start)
	# 归一化方向向量
	direction = direction / np.linalg.norm(direction)
	# 计算箭头头部起点
	head_start = np.array(end) - (head_length * direction)
	# 计算箭头头部三角形的顶点
	left = head_start + np.array([direction[1], -direction[0], 0]) * head_width
	right = head_start + np.array([-direction[1], direction[0], 0]) * head_width
	
	# 绘制箭头主体
	ax.plot(*zip(start, end), color='k')
	# 绘制箭头头部
	ax.plot(*zip(end, left, right, end), color='k')