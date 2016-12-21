from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, Merge, Flatten
from keras.utils import np_utils
from keras.layers.recurrent import LSTM
from numpy import array, float32
import numpy as np

#################
### Load data ###
#################

from getUsableCourses import dictXml
from edX_video_parsing import coursePairsToVideos

strVideoVectorsFile = 'videoVec.txt'
with open(strVideoVectorsFile) as fIn:
  dictVideoToVector = eval(''.join(fIn))
  dictVideoToVector = {video.split('-')[-1]: vector for video, vector in dictVideoToVector.items()}

strVideoChangesFile = 'labeledData.txt'
with open(strVideoChangesFile) as fIn:
  dictCourseToChanges = {}
  strCurrCourse = None
  for line in fIn:
    if strCurrCourse is not None:
      dictCourseToChanges[strCurrCourse] = eval(line)
      strCurrCourse = None
    if '-' in line:
      strCurrCourse = line.strip()

numHiddenLayers = 20

###################
### Build model ###
###################

def getXandY(strCourse):
  strIter1 = dictXml[strCourse][0]
  listVideos = coursePairsToVideos[strCourse][0]
  listIndices = [index for index, video in enumerate(listVideos) if video in dictVideoToVector]
  listVideos = [listVideos[index] for index in listIndices]
  listChanges = dictCourseToChanges[strCourse]
  listChanges = [listChanges[index] for index in listIndices]
#  print len(listVideos), len(listChanges)
  return ([dictVideoToVector[video] for video in listVideos], np_utils.to_categorical(listChanges, 5).tolist())

def trainModel(aryCourses, modelBuilder = LSTM):
  model = Sequential()
#  model.add(LSTM(numHiddenLayers, input_shape = (None, 28)))
  model.add(Dense(output_dim = 100, input_dim = 28))
  model.add(Dense(5))
  model.add(Activation('softmax'))
  model.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop')
  X = []
  Y = []
  for strCourse in aryCourses:
    courseX, courseY = getXandY(strCourse)
#    courseY = courseY.reshape((courseY.shape[1], 5))
#    print courseY
    X += courseX
    Y += courseY
#  print type(X), len(X), type(X[0]), len(X[0]), type(X[0][0])
#  print type(Y), len(Y)
  X = np.array(X)
#  X =  X.reshape(X.shape[1], X.shape[2], 1)
  Y = np.array(Y)
#  Y = Y.reshape(Y.shape[1], Y.shape[2], 1)
  print X.shape
  print Y.shape
  model.fit(X, Y, nb_epoch = 50, batch_size = 16)
  return model

def leaveOneOutTesting(aryCourses):
  totalLoss = 0.0
  for i in range(len(aryCourses)):
    model = trainModel(aryCourses[:i] + aryCourses[(i + 1):])
    courseX, courseY = getXandY(aryCourses[i])
    totalLoss += model.evaluate(np.array(courseX), np.array(courseY), batch_size = 1)
  return totalLoss / len(aryCourses)

allCourses = ['BerkeleyX-ColWri2.3x', 'BerkeleyX-GG101x', 'BUx-ARPO222x', 'BUx-PY1x', 'DelftX-AE1110x',
              'DelftX-EX101x', 'DelftX-TOPOCMx', 'EPFLx-EE102Bx', 'GeorgetownX-MEDX202_01', 'HKUx-HKU01x',
              'IITBombayX-EE210.2X', 'TsinghuaX-70120073x']

testCourses = ['BerkeleyX-ColWri2.3x', 'DelftX-TOPOCMx']
trainCourses = [course for course in allCourses if course not in testCourses]

m = leaveOneOutTesting(trainCourses)
print m