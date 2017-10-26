import numpy as np
import scipy.integrate as integrate
from math import pi, sqrt
import matplotlib.pyplot as plt

def cauchy(x, k):
    return 1./pi/(1+(x-k)**2)

cV = np.vectorize(cauchy)
gr = np.linspace(-10,10,1000)
y1 = cV(gr, 1)
y2 = cV(gr, -1)
# print integrate.quad(lambda x: cauchy(x,1), -3-sqrt(7), -3+sqrt(7))[0]/2
# print (integrate.quad(lambda x: cauchy(x,-1), -1000,-3-sqrt(7))[0]+integrate.quad(lambda x: cauchy(x,-1),-3+sqrt(7),1000)[0])/2

plt.plot(gr, y1, label='k=\'a\'')
plt.plot(gr, y2, label='k=\'r\'')
plt.axvline(x=0, label='b_std', color='orange')
plt.axvline(x=-3+sqrt(7), label='b_verif', color='black')
plt.axvline(x=-3-sqrt(7), label='b_verif', color='black')
plt.legend(loc='best')
plt.show()