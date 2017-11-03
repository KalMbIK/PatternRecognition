import numpy as np
import matplotlib.pyplot as plt
from math import log
from scipy import optimize

m0 = np.array([2., 0.])
m1 = np.array([1., 2.])
m2 = np.array([0., 1.])
std2 = np.array([2., 1.])
p = np.array([1./3, 1./3, 1./3])
m = np.array([m0, m1, m2])

k = 0
c = 1
for k,c in ((0,1), (0,2), (1,2)):
    mkc = (m[k][:]-m[c][:])/std2[:]
    e = np.array([1.,1.])
    Dkc = (m[k][:]**2-m[c][:]**2)/std2[:]/2
    # print Dkc
    dkc = np.dot(Dkc, e) - log(p[k]/p[c])
    # print dkc
    def f(x):
        return np.dot(mkc,x)-dkc

    x0 = optimize.root(f,np.array([0,0]),method='linearmixing').get('x')
    def line(x):
        return (dkc-x*mkc[0])/mkc[1]

    lineV = np.vectorize(line)
    x = np.linspace(0, 5, 100, True)
    y = lineV(x)
    print f(np.array([x[5],y[5]]))
    plt.plot(x,y,label='bc: '+str(k+1)+' and '+str(c+1))
plt.legend(loc='best')
plt.show()