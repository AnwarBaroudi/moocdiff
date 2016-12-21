import numpy as np
import operator

# Just DR; run before following two functions
from sklearn.decomposition import PCA
def dimensionalityReductionViaPCA(matrixWordVectors):
  pca = PCA(n_components = 2)
  return pca.fit_transform(matrixWordVectors)

# Potential way of finding interesting result of K means; need to cross-validate to choose number of clusters
from sklearn.cluster import KMeans
def clusteringViaKMeans(matrixPoints, numClusters):
  kmeans = KMeans(n_clusters = numClusters)
  return kmeans.fit_predict(matrixPoints)

# Probable method of analysis: returns the indices of the closest word vectors (sorted from closest to farthest)
def getClosestWords(matrixPoints, index):
  aryDistances = [(i, cosineDist(matrixPoints[i], matrixPoints[index])) for i in range(len(matrixPoints))]
  sort = sorted(aryDistances, key = operator.itemgetter(1), reverse = True)
  return map(operator.itemgetter(0), sort[1:])
def magnitude(point):
  return sum([v ** 2 for v in point]) ** 0.5
def cosineDist(pointX, pointY):
  return (pointX[0] * pointY[0] + pointX[1] * pointY[1]) / (magnitude(pointX) * magnitude(pointY))

# Plotting function; you can ignore most of the non-required parameters
import matplotlib.pyplot as plt
def plotScatterPlot(aryTupleXYPairs, strTitle, strXAxisLabel, strYAxisLabel, **kwargs):
  fig, ax = getSubplots()
  aryXValues, aryYValues = zip(*aryTupleXYPairs)
  plt.scatter(aryXValues, aryYValues)
  genericPlottingFunction(strTitle, strXAxisLabel, strYAxisLabel, **kwargs)
def genericPlottingFunction(strTitle, strXAxisLabel, strYAxisLabel,
                            tupleXAxisLimits = None, tupleYAxisLimits = None, aryXLabels = None,
                            floatBottomSpace = None):
  global savedSubplots
  fig, ax = savedSubplots
  plt.suptitle(strTitle)
  ax.set_xlabel(strXAxisLabel)
  ax.set_ylabel(strYAxisLabel)
  if tupleXAxisLimits is not None:
    plt.xlim(tupleXAxisLimits)
  if tupleYAxisLimits is not None:
    plt.ylim(tupleYAxisLimits)
  if aryXLabels is not None:
    if type(aryXLabels[0]) is tuple:
      plt.xticks(*zip(*aryXLabels))
    else: # assuming numeric
      plt.xticks(aryXLabels, aryXLabels)
  if floatBottomSpace is not None:
    fig.subplots_adjust(bottom = floatBottomSpace)
  plt.show()
  plt.close()
savedSubplots = None
def getSubplots():
  global savedSubplots
  if savedSubplots is None:
    savedSubplots = plt.subplots()
  return savedSubplots

########################
#        script        #
########################
f = open("word2vec.txt", "r")
temp = f.readline()
d = eval(temp)
lstofwords = []
lstofvectors = []
for k in d:
  lstofwords.append(k)
  lstofvectors.append(d[k])
dr = dimensionalityReductionViaPCA(lstofvectors)

def useFinder(word, numWords):
  if word in d:
    i = lstofwords.index(word)
    listofbestwords = getClosestWords(dr, i)
    j = 0
    for index in listofbestwords:
      if j == numWords:
        break
      print(lstofwords[index])
      j += 1

def analogyFinder(word1, word2, word3):
  print(word1 + " is to " + word2 + " as " + word3 + " is to:")
  i1, i2, i3 = lstofwords.index(word1), lstofwords.index(word2), lstofwords.index(word3)
  newVector = dr[i1] + dr[i2] - dr[i3]
  tempDR = np.vstack([dr, newVector])
  m = getClosestWords(tempDR, -1)
  print(lstofwords[next(m)])

def getCluster(totalClusters, c):
  k = clusteringViaKMeans(dr, totalClusters)
  indexList = []
  for i in range(len(k)):
    if k[i] == c:
      indexList.append(i)
  words = [lstofwords[j] for j in indexList]
  return words

