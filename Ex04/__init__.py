import numpy as np
import re

# FILE PARSER
def parseFile(f,K):
    pics = [[] for i in range(K)]
    i = 0
    blocks = []
    t = []
    for line in f:
        t.append(line)
        i += 1
        if i % 17 == 0:
            blocks.append(t)
            t = []

    for block in blocks:
        k = int(block[0])%K
        x = []
        for line in block[1:]:
            tt = re.findall('[0-9]{1,4}', line)
            try:
                x+=([float(t) for t in tt])
            except ValueError:
                print line
                break
        if len(x)!=256:
            for line in block[1:]:
                print line
            print x
            print len(x)
            break
        pics[k].append(np.array(x))
    return pics

# FILE IS PARSED: ALL DATA IN THE ARRAY @pics

# PARAMETER ESTIMATION

def estimateParameters(D,K, pics):
    means = [np.zeros(D) for i in range(K)]
    covariances = np.zeros(D)
    priors = np.zeros(K)
    Nk = np.zeros(K, dtype=np.int32)
    N = 0.
    for klass, mean, i in zip(pics, means, range(K)):
        Nk[i] = len(klass)
        N += Nk[i]
        for vector in klass:
                mean += vector
        mean /= Nk[i]
    for i in range(K):
        priors[i] = Nk[i]/N
    return means, covariances, priors, Nk, N

# PARAMETERS ARE ESTIMATED: MEANS, PRIORS AND TOTAL AMOUNT OF DATA

# TODO POOLED COVARIANCE MATRIX????? Index subK makes the matrices to be dependent of k!!


f = file('usps.train')
K = int(f.readline())
D = int(f.readline())
pics = parseFile(f,K)
print np.size(pics)
f.close()
means, covariances, priors, Nk, N = estimateParameters(D,K, pics)

p = 0.

for i in range(K):
    p+=priors[i]
    print priors[i]

print p

