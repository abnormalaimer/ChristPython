from mpmath import mp
from tqdm import tqdm

# 设置精度（这里设置为1亿位）
digits = 10 ** 4
mp.dps = digits  # 设置小数点后的精度

# Chudnovsky算法
def compute_pi_chudnovsky():
	C = 426880 * mp.sqrt(10005)
	M = 1
	L = 13591409
	X = 1
	K = 6
	S = L
	for i in range(1, mp.dps):
		M = (K ** 3 - 16 * K) * M // i ** 3
		L += 545140134
		X *= -262537412640768000
		S += mp.mpf(M * L) / X
		K += 12
		print(i)
	pi = C / S
	return pi


# 计算π
pi = compute_pi_chudnovsky()

# 将π转换为字符串
pi_str = str(pi)

# 移除前缀'3.'
pi_str = pi_str[2:]

# 写入文件
with open('./pi.txt', 'w') as file:
	for _ in tqdm(range(digits)):
		file.write(pi_str)
