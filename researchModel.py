from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, Merge, Flatten
from keras.utils import np_utils
import numpy as np
import numpy.random as npr
from loadStudentInteractionData import parseByVideoAndStudent, aryInterestingEventTypes
from collections import defaultdict
import sys
from os import listdir

# helper functions
def listdir_nohidden(path):
	for f in listdir(path):
		if not f.startswith('.'):
			yield f

def oneHot(index, size):
	onehot = [0 for _ in range(size)]
	onehot[index] = 1
	return np.array(onehot).T # not sure if we need to transpose...

def mapping(lstOfItems):
	count = 0
	emptyDict = {}
	for item in lstOfItems:
		emptyDict[item] = count
		count += 1
	return emptyDict


#fileName = 'data/BerkeleyX_Stat_2.1x_1T2014-events.log'
allChosenStudents = set()
allDictData = {}
coursesInOrder = []
directory = 'data/events/'
#directory = 'data/temp/'
dictVideoToStudents = defaultdict(lambda: [])
for f in listdir_nohidden(directory):
	fileName = directory + f
	coursesInOrder.append(f[:-11]) # getting rid of "-events.log"
	dictData = parseByVideoAndStudent(fileName)
	#dictVideoToStudents = defaultdict(lambda: [])
	aryStudents = np.array(list(set([student for video, student in dictData.keys()])))
	print len(aryStudents)
	setChosenStudents = set(npr.choice(aryStudents, min(50, len(aryStudents) / 50), replace = False)) # choose 2% of students, but at least 50 students, from each class
	for video, student in dictData.keys():
  		if student in setChosenStudents:
    			dictVideoToStudents[video].append(student)
	allChosenStudents = allChosenStudents.union(setChosenStudents)
	allDictData.update({k:v for (k, v) in dictData.items() if k[1] in setChosenStudents})
	print "finished with", fileName


videoIDInputs = dictVideoToStudents.keys()
allActions = aryInterestingEventTypes
numActions = len(allActions)
videoToStudents = dictVideoToStudents
studentsToActions = {key: [event['event_type'] for event in allDictData[key] if key[-1] in allChosenStudents] for key in allDictData}
mappingOfVideosToInts = mapping(videoIDInputs)
mappingOfActionsToInts = mapping(allActions) # will get this as an input?

dictData = None # freeing a way-too-large object for garbage collection
allDictData = None

inputsToEmbeddingModel1 = []
inputsToEmbeddingModel2 = []
contextLabels = [] #for now its just one ahead
for video in videoIDInputs:
	for student in videoToStudents[video]:
		actionList = studentsToActions[(video, student)]
		for i in range(len(actionList) - 1):
				inputsToEmbeddingModel1.append(mappingOfVideosToInts[video])
				inputsToEmbeddingModel2.append(mappingOfActionsToInts[actionList[i]])
				contextLabels.append(oneHot(mappingOfActionsToInts[actionList[i+1]], numActions))
xTrainV = np.array(inputsToEmbeddingModel1).T
xTrainA = np.array(inputsToEmbeddingModel2).T
yTrain = np.array(contextLabels)

embedV = Embedding(len(videoIDInputs), 128, input_length=1)
embedA = Embedding(numActions, 3, input_length=1)
# above should have arguments: number of videos, size of output embedding, length of videoIDs
videoSeq = Sequential()
videoSeq.add(embedV)
videoSeq.add(Flatten())
actionSeq = Sequential()
actionSeq.add(embedA)
actionSeq.add(Flatten())
merged = Merge([videoSeq, actionSeq], mode='concat')
denseWindow = Dense(numActions) # for now only predict one action in advance
model = Sequential()
model.add(merged)
model.add(denseWindow)
model.add(Activation('softmax'))
print "made it to compiling"
model.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop', metrics=["accuracy"])
print xTrainV.shape, xTrainA.shape, yTrain.shape
model.fit([xTrainV, xTrainA], yTrain, nb_epoch = 5, batch_size = 16)

w = embedV.get_weights()[0]
videoVec = {}
for i in range(len(videoIDInputs)):
	videoVec[videoIDInputs[i]] = w[i]


