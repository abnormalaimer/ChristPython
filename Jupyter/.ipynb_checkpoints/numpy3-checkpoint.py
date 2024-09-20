import matplotlib.pyplot as plt
import numpy as np
points=np.arange(-5,5,0.001)
xs,ys=np.meshgrid(points,points)
z=np.sqrt(xs**2+ys**2)
plt.imshow(z,cmap=plt.cm.gray);plt.colorbar()