#!/usr/bin/python
# -*- coding: UTF-8 -*-
import turtle


def plus(numList):
    if len(numList) == 1:
        return numList[0]
    else:
        return numList[0] + plus(numList[1:])


# def tree(branch_len):
# 	if branch_len > 5:
# 		t.forward(branch_len)
# 		t.right(20)
# 		tree(branch_len - 15)
# 		t.left(40)
# 		tree(branch_len - 15)
# 		t.right(20)
# 		t.backward(branch_len)

def dp(coinValuelist, change, mincoins):
    for cents in range(1, change + 1):
        coinCount = cents
        for j in [c for c in coinValuelist if c <= cents]:
            if mincoins[cents - j] + 1 < coinCount:
                coinCount = mincoins[cents - j] + 1
        mincoins[cents] = coinCount
    return mincoins[change]


if __name__ == '__main__':
    print(dp([1, 5, 10, 21, 25], 6, [0] * 160))

# t = turtle.Turtle()
# t.left(90)
# t.backward(60)
# tree(75)
# 	# for i in range(360):
# 	# 	t.forward(10)
# 	# 	t.right(8)
# turtle.done()
