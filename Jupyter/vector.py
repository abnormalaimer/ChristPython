import matplotlib.pyplot as plt
import numpy as np


# 把极向量坐标转为笛卡尔坐标
def to_cartesian(polar_vector):
	length, angle = polar_vector[0], polar_vector[1]
	return length * np.cos(angle), length * np.sin(angle)


# 将笛卡尔坐标转换为极坐标
def to_polarCoordinates(cartesian_coords):
	polar_coords = []
	for v in cartesian_coords:
		r = np.sqrt(v[0] ** 2 + v[1] ** 2)  # 半径
		theta = np.arctan2(v[1], v[0])  # 角度，使用atan2确保角度在正确的象限
		polar_coords.append((r, theta))
	return polar_coords


# 旋转向量坐标
def rotate(angle, vectors):
	vectors_polar = to_polarCoordinates(vectors)
	vectors_rotated_polar = [(l, angle + rota_angle) for l, rota_angle in vectors_polar]
	vectors_rotaed = [to_cartesian(p) for p in vectors_rotated_polar]
	return vectors_rotaed


# 绘画出笛卡尔坐标系中的向量
def draw_vector(*args):
	plt.axhline(0, color='black', linewidth=0.5)
	plt.axvline(0, color='black', linewidth=0.5)
	# 检查是否提供了'1'作为参数,1判断是否将(0,0)作为起始坐标
	if len(args) > 0 and isinstance(args[-1], str) and args[-1] == '1':
		vectors = args[:-1]
		start = np.array((0, 0))
	else:
		vectors = args
		start = vectors[0]
		vectors = vectors[1:]
	sum_vector = np.array(start)
	# 累加所有向量
	for vec in vectors:
		sum_vector = np.add(sum_vector, vec)
	
	# 使用 plt.annotate 来绘制向量
	plt.annotate('', xy=tuple(sum_vector), xytext=start, arrowprops=dict(facecolor='red', arrowstyle="->"))


# 绘画出在笛卡尔坐标系中的图形
def draw_cartesian(cartesian_coords, y=0):
	# 此处增加首坐标，首尾相连。
	cartesian_coords.append(cartesian_coords[0])
	plt.axhline(0, color='black', linewidth=0.5)
	plt.axvline(0, color='black', linewidth=0.5)
	plt.plot([coord[0] for coord in cartesian_coords],
			 [coord[1] for coord in cartesian_coords], 'o-', y)