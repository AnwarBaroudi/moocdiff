from collections import defaultdict
import os
import re

# manual processing here 
setSameCourses = set()
setSameCourses.add(("BerkeleyX", ("CS169.1x", "CS_CS169.1x", "CS.CS169.1x")))
setSameCourses.add(("BerkeleyX", ("CS169.2x", "CS_CS169.2x", "CS.CS169.2x", "CS.169.2x")))
setSameCourses.add(("EPFLx", ("EE102Bx", "EE102B.1x")))

dictCourseRenaming = dict()
for strSchool, listOfClasses in setSameCourses:
    for strClass in listOfClasses:
        dictCourseRenaming[strSchool + '-' + strClass] = strSchool + '-' + listOfClasses[0]

def sortClasses(aryTupleClassAndTime):
    for i in range(0, len(aryTupleClassAndTime)):
        for j in range(i + 1, len(aryTupleClassAndTime)):
            if compareClasses(aryTupleClassAndTime[i][1], aryTupleClassAndTime[j][1]) > 0:
                aryTupleClassAndTime[i], aryTupleClassAndTime[j] = aryTupleClassAndTime[j], aryTupleClassAndTime[i]
    return aryTupleClassAndTime

def compareClasses(time1, time2):
    time1 = standardizeTime(time1)
    time2 = standardizeTime(time2)
    if time1[0] != time2[0]:
        return time1[0] - time2[0]
    if int == type(time1[1]) and int == type(time2[1]):
        return time1[1] - time2[1]
    raise Exception("QQ: %s, %s" % (time1, time2))

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
# return tuple of year, time of year
def standardizeTime(time):
    if len(time) == 7:
        time = time.replace('_', '')
    if len(time) == 6:
        parts = map(int, re.split('\\D', time))
        return max(parts), min(parts)
    year = int(time[:4])
    yearPart = time[5:]
    if yearPart in months:
        yearPart = months.index(yearPart) + 1
    if yearPart in seasons:
        yearPart = seasons.index(yearPart) * 3 + 1
    return year, yearPart

#dictJson = defaultdict(lambda: {})
#for fileName in os.listdir('json'):
#    lineParts = fileName[:-37].split('-')
#    strCourseName = '-'.join(lineParts[:-1])
#    dictJson[strCourseName][lineParts[-1]] = fileName

dictXml = defaultdict(lambda: set())
for strFolderName in os.listdir('xml'):
    lineParts = strFolderName.split('-')
    strCourseName = '-'.join(lineParts[:-1])
    if strCourseName in dictCourseRenaming:
        strCourseName = dictCourseRenaming[strCourseName]
    dictXml[strCourseName].add((strFolderName, lineParts[-1]))
dictXml = dict(dictXml)

for strCourseName in dictXml:
    dictXml[strCourseName] = [strFolderName for strFolderName, strSemester in sortClasses(list(dictXml[strCourseName]))]

dictNumOccurrencesToListCourseNames = defaultdict(lambda: [])
for course in dictXml:
    dictNumOccurrencesToListCourseNames[len(dictXml[course])].append(course)
