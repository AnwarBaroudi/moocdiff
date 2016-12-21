from collections import defaultdict

import json
import operator
import sys

aryInterestingEventTypes = [
                            'load_video', 'pause_video', 'play_video', 'seek_video', 'speed_change_video', 'stop_video',
#                            'problem_check', 'problem_check_fail', 'problem_show', 'problem_show', 'reset_problem', 'save_problem_success', 'showanswer',
#                            'seq_goto', 'seq_next', 'seq_prev', 'page_close'
                           ]
fnFilterInteresting = lambda event: event['event_type'] in aryInterestingEventTypes
x = []

def parseByStudent(fileName):
  dictStudentToListEvents = defaultdict(lambda: [])
  for line in open(fileName, 'rb'):
#    x.append(line)
    try:
      parsedLine = json.loads(line)
      if parsedLine['event_type'] not in aryInterestingEventTypes:
        continue
      if 'event' in parsedLine and type(parsedLine['event']) != dict:
        if len(parsedLine['event']) > 0:
          parsedLine['event'] = json.loads(parsedLine['event'])
        else:
          continue
      dictStudentToListEvents[parsedLine['username']].append(parsedLine)
    except:
      pass
  for student in dictStudentToListEvents:
    dictStudentToListEvents[student] = sorted(dictStudentToListEvents[student], key = operator.itemgetter('time'))
  return dictStudentToListEvents

def parseByVideoAndStudent(fileName):
  dictVideoToStudentToListEvents = defaultdict(lambda: [])
  for studentId, listEvents in parseByStudent(fileName).items():
    for event in listEvents:
      dictVideoToStudentToListEvents[event['event']['id'], studentId].append(event)
  return dictVideoToStudentToListEvents

# sampleDict = parseByStudent('data/sampleEvents.log')
# sampleDict2 = parseByVideoAndStudent('data/sampleEvents.log')

fileName = 'data/events/HKUx_HKU01x_3T2014-events.log'
dictData = parseByVideoAndStudent(fileName)

# Information functions:
def getAllEventTypesAndFrequencies(fileName):
  freqEventTypes = defaultdict(lambda: 0)
  for line in open(fileName, 'rb'):
    parsedLine = json.loads(line)
    freqEventTypes[parsedLine['event_type']] += 1
  return freqEventTypes
