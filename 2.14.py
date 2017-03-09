from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')


X = np.arange(-2, 2, 0.01)
Y = np.arange(-2, 2, 0.01)
X, Y = np.meshgrid(X, Y)


Z = ((1 + ((X + Y + 1 )**2) * (19 - ( 14 * X )+ (3 * X)**2) - (14*Y) + (6*X*Y) + (3 * Y)**2)) *(30 + ((2 * X) - (3 * Y)**2 )* (18 - (32*X) + ((12 * X)**2) + (48*Y) - (36*X*Y) + (27 * Y**2)))


surf = ax.plot_surface(X, Y, Z, cmap=cm.gist_stern,
                       linewidth=0, antialiased=False)


ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()