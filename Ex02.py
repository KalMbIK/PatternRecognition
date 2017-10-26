import numpy as np
from math import pi, sqrt
import matplotlib.pyplot as plt

def cauchy(x, k):
    return 1./pi/(1+(x-k)**2)

cV = np.vectorize(cauchy)
gr = np.linspace(-10,10,100)
y1 = cV(gr, 1)
y2 = cV(gr, -1)

plt.plot(gr, y1, label='k=\'a\'')
plt.plot(gr, y2, label='k=\'r\'')
plt.axvline(x=0, label='b_std', color='black')
plt.axvline(x=-3+sqrt(7), label='b_verif', color='black')
plt.legend(loc='best')
plt.show()