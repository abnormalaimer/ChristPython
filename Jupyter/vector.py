import matplotlib.pyplot as plt
import numpy as np

def to_cartesian(polar_vector):
	"""
  将极坐标转换为笛卡尔坐标。
  参数:
  polar_vector : tuple
	  一个表示极坐标的元组，格式为 (length, angle)，其中 length 是极径，angle 是极角（以弧度为单位）。
  返回:
  tuple
	  返回一个元组，表示笛卡尔坐标 (x, y)。
  示例:
   to_cartesian((1, np.pi/4))
  (0.7071067811865475, 0.7071067811865475)
  """
	length, angle = polar_vector[0], polar_vector[1]
	return length * np.cos(angle), length * np.sin(angle)

def to_polarCoordinates(cartesian_coords):
	"""
  将笛卡尔坐标转换为极坐标。
  
  参数:
  cartesian_coords : list of tuples
	  包含笛卡尔坐标点的列表，每个坐标点是一个元组 (x, y)。
	  
  返回:
  list of tuples
	  返回一个列表，包含转换后的极坐标点，每个点是一个元组 (r, theta)，其中 r 是极径，theta 是极角（以弧度为单位）。
	  
  示例:
   to_polarCoordinates([(1, 1)])
  [(1.4142135623730951, 0.7853981633974483)]
  """
	
	polar_coords = []
	for v in cartesian_coords:
		r = np.sqrt(v[0] ** 2 + v[1] ** 2)  # 半径
		theta = np.arctan2(v[1], v[0])  # 角度，使用atan2确保角度在正确的象限
		polar_coords.append((r, theta))
	return polar_coords

def rotate(angle, vectors):
	"""
  旋转向量坐标。
  
  参数:
  angle : float
	  旋转角度（以弧度为单位）。
  vectors : list of tuples
	  包含笛卡尔坐标点的列表，每个坐标点是一个元组 (x, y)。
	  
  返回:
  list of tuples
	  返回一个列表，包含旋转后的笛卡尔坐标点。
	  
  示例:
   rotate(np.pi/2, [(1, 0)])
  [(6.123233995736766e-17, 1.0)]
  """
	
	vectors_polar = to_polarCoordinates(vectors)
	vectors_rotated_polar = [(l, angle + rota_angle) for l, rota_angle in vectors_polar]
	vectors_rotaed = [to_cartesian(p) for p in vectors_rotated_polar]
	return vectors_rotaed

def draw_vector(*args, arrow_style=None):
	"""
	绘制向量累加结果的函数。
    
    该函数接受一个或多个向量作为参数，并从起始向量开始绘制这些向量的累加结果。
    起始向量是第一个参数，其余参数是需要累加的向量。绘制时，使用箭头来表示向量，
    且箭头的样式可以通过 `arrow_style` 参数进行自定义。
    
    参数:
    - *args: 一个或多个向量，其中第一个向量是起始向量，其余向量将累加到起始向量上。
             每个向量都应该是一个可迭代的数值对象，如列表或元组。
    - arrow_style (dict, 可选): 箭头的样式字典。默认值为 None，此时将使用内置的样式。
    
    箭头样式字典可以包含以下键（默认值在括号中）:
    - 'facecolor' (red): 箭头颜色。
    - 'edgecolor' (black): 箭头边缘颜色。
    - 'arrowstyle' (->): 箭头样式，例如 '->' 表示带箭头的线。
    - 'linewidth' (1.5): 箭头线宽。
    - 'linestyle' (-): 箭头线型，例如 '-' 表示实线。
    - 'mutation_scale' (20): 箭头大小。
    - 'connectionstyle' ("arc3,rad=0.2"): 连接样式，用于控制箭头和起始点之间的连接方式。
    
    示例:
  	draw_vector([0, 0], [1, 2], [3, 1])  # 从原点绘制两个向量的累加结果
    plt.show()
	"""
	plt.axhline(0, color='black', linewidth=0.5)
	plt.axvline(0, color='black', linewidth=0.5)
	if arrow_style is None:
		arrow_style = dict(
			facecolor='red',  # 箭头颜色
			edgecolor='black',  # 箭头边缘颜色
			arrowstyle='->',  # 箭头样式
			linewidth=1.5,  # 箭头线宽
			linestyle='-',  # 箭头线型
			mutation_scale=20,  # 箭头大小
			connectionstyle="arc3,rad=0.0"  # 连接样式
		)
	start = np.array(args[0])
	
	# 剩余的参数是需要累加的向量
	vectors = args[1:]
	
	sum_vector = np.array(start, dtype=float)
	# 累加所有向量
	for vec in vectors:
		sum_vector += np.array(vec)
	
	# 使用 plt.annotate 来绘制向量
	plt.annotate('', xy=tuple(sum_vector), xytext=tuple(start), arrowprops=arrow_style)

def draw_cartesian(cartesian_coords, style='b-o'):
	"""
   绘制二维笛卡尔坐标系中的点序列，并自动连接首尾以形成一个闭合图形。
   
   该函数接收一个包含二维坐标点的列表，并在指定的y水平线上绘制这些点，
   然后使用线条将它们连接起来。默认情况下，所有点都将在y=0的水平线上绘制。
   
   参数:
   cartesian_coords : list of tuples
	   包含二维坐标点的列表，每个坐标点是一个元组 (x, y)。
   style: 绘图样式，格式为'[颜色][线型][标记]'，例如 'ro-' 表示红色实线圆形标记。
			颜色：‘b’（蓝色）、‘g’（绿色）、‘r’（红色）、‘c’（青色）、‘m’（洋红）、‘y’（黄色）、‘k’（黑色）、‘w’（白色）等。
			线型：‘-’（实线）、‘–’（虚线）、‘-. ‘（点划线）、’:’（点线）等。
			标记：‘o’（圆形）、‘s’（正方形）、‘^’（三角形）、‘v’（倒三角形）、‘*’（星形）等。
   示例:
   # 绘制一个正方形的四个顶点，并连接成一个闭合图形
   draw_cartesian([(1, 0), (2, 0), (2, 1), (1, 1)])
   
   # 绘制一个三角形，并将所有点放在y=1的水平线上
   draw_cartesian([(1, 1), (3, 1), (2, 2)], y=1)
   
   特点:
   - 在绘制之前，会先绘制坐标轴的水平和垂直辅助线。
   - 点与点之间使用线条连接，并自动连接最后一个点到第一个点以形成闭合图形。
   - 默认情况下，所有点都绘制在x轴上（y=0），但可以通过y参数修改。
   """
	
	cartesian_coords.append(cartesian_coords[0])
	plt.axhline(0, color='black', linewidth=0.5)
	plt.axvline(0, color='black', linewidth=0.5)
	plt.plot([coord[0] for coord in cartesian_coords],
			 [coord[1] for coord in cartesian_coords], style)