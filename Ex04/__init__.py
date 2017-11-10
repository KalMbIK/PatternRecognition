import numpy as np
import re

# FILE PARSER
# 1 block - is a set of lines in file correspond to a one entity
# we split the file into the blocks and handle them in a loop using regexp
# IMPORTANT: k = 10 in the problem set corresponds to a 0 element of an array pics
# the other values of k corresponds to a k element of an array
def parseFile(f):
    K = int(f.readline())
    D = int(f.readline())
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
    return pics, K, D

# FILE IS PARSED: ALL DATA IN THE ARRAY @pics

# PARAMETER ESTIMATION
# we use given formulas to estimate the parameters of the distribution
def estimateParameters(D, K, pics):
    means = [np.zeros(D) for i in range(K)]
    covariance = np.zeros(D)
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
    for klass, mean in zip(pics, means):
        for vector in klass:
            covariance += (vector-mean)**2
    covariance /= N
    return means, covariance, priors, Nk, N

# PARAMETERS ARE ESTIMATED: MEANS, COVARIANCE MATRIX, PRIORS AND TOTAL AMOUNT OF DATA

# PARAMETER FILE GENERATION
# some useful functions to produce the output file.
# But they are not completed (the case of full covariance matrix is not handled)
def writeLine(file, element):
    file.write(str(element)+'\n')

def writeClass(file, type, i, means, covariance, priors):
    if i==0:
        writeLine(file, 10)
    else:
        writeLine(file, i)
    writeLine(file, priors[i])
    writeLine(file, arrayToString(means[i]))
    if type == 'd':
        writeLine(file, arrayToString(covariance))

def arrayToString(array):
    s = ''
    for element in array:
        s += str(element) + ' '
    return s

def genOutput(file, type, K, D, means, covariance, priors):
    writeLine(file, type)
    writeLine(file, K)
    writeLine(file, D)

    for i in range(1,K):
        writeClass(file,type,i,means,covariance,priors)

    writeClass(file,type,0,means,covariance,priors)

# FILE IS GENERATED

# CLASSIFIER ITSELF
# this is our classificatior (see 45 page of the lecture notes)
def classificatorCore(x, means, covariances, priors):
    sigmaMatrix = np.diag(covariances)
    sigmaMinus1 = np.linalg.inv(sigmaMatrix)
    def f(k):
        return -1/2.*np.dot(np.dot(np.transpose(x-means[k]), sigmaMinus1),(x-means[k]))+np.log(priors[k])
    values = np.array([f(k) for k in range(len(means))])
    return values.argmax()

# here is nothing to comment :)
def generateConfMatrix(pics, classify):
    confMatrix = np.zeros((K, K))
    for klass, k in zip(pics, range(K)):
        for vector in klass:
            kbar = classify(vector)
            confMatrix[k][kbar] += 1
    return confMatrix
#

# READ INPUT FILES, PARSE THEM AND FINALLY GENERATE A PARAMETER FILE
out = file('dolgoprudny.out', mode='w')
f = file('usps.train','r')
f1 = file('usps.test','r')
pics, K, D = parseFile(f)
pics1, K, D = parseFile(f1)
means, covariance, priors, Nk, N = estimateParameters(D, K, pics)
# here we define our decision rule using the obtained parameters and core-function
classify = lambda x: classificatorCore(x, means, covariance, priors)
# here we generate the parameter file
genOutput(out,'d',K,D,means,covariance,priors)
out.close()
f.close()
f1.close()

# FILES ARE PARSED IN @pics and @pics1

# CLASSIFICATION
# useful function to obtain the required ratio from the confusion matrix and print the data
def getResult(cm):
    wrRes = 0
    allEvs = 0
    for i in range(len(cm)):
        for j in range(len(cm)):
            if i!=j:
                wrRes+=cm[i][j]
            allEvs+=cm[i][j]
    print 'Empirical Error Rate='+str(wrRes/allEvs)
    # print 'allEvs='+str(allEvs)
    print cm

# printing the result
cm = generateConfMatrix(pics1,classify)
getResult(cm)