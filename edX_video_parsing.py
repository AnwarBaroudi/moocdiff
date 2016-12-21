import json
from os import listdir
import xml.etree.ElementTree as ET
import compareLists
import getUsableCourses
# from this import we get:
# dictNumOccurencesToListCorseNames
# dictXml

# this code is intended to be run from our root directory, moocdiff. 

def listdir_nohidden(path):
    for fil in listdir(path):
        if not fil.startswith('.'):
            yield fil

def videosForCourse(coursename):
    coursefile = "xml/" + coursename + "/course"
    courseDir = listdir_nohidden(coursefile)
    coursefile = coursefile + "/" + next(courseDir)
    xmlParsing = ET.parse(coursefile).getroot()
    chapterList = []
    for child in xmlParsing:
        if child.tag == 'chapter':
            chapterList.append(child.attrib['url_name'])
    sequentialList = []
    for chapter in chapterList:
        xmlParsing = ET.parse("xml/" + coursename + "/chapter/" + chapter + ".xml").getroot()
        if 'visible_to_staff_only' in xmlParsing.attrib and xmlParsing.attrib['visible_to_staff_only'] == 'true':
           # print 'found only_staff tag in ', coursename, 'in chapter ', chapter   
	    continue	   
        for child in xmlParsing:
            if child.tag == 'sequential':
                sequentialList.append(child.attrib['url_name'])
    verticalList = []
    for sequential in sequentialList:
        xmlParsing = ET.parse("xml/" + coursename + "/sequential/" + sequential + ".xml").getroot()   
        if 'visible_to_staff_only' in xmlParsing.attrib and xmlParsing.attrib['visible_to_staff_only'] == 'true':
           # print 'found only_staff tag in ', coursename, 'in sequential ', sequential   
	    continue
        for child in xmlParsing:
            if child.tag == 'vertical':
                verticalList.append(child.attrib['url_name'])
    orderedVideoList = []
    for vertical in verticalList:
        xmlParsing = ET.parse("xml/" + coursename + "/vertical/" + vertical + ".xml").getroot()    
        if 'visible_to_staff_only' in xmlParsing.attrib and xmlParsing.attrib['visible_to_staff_only'] ==' true':
           # print 'found only_staff tag in ', coursename, 'in vertical ', vertical   
	    continue
	for child in xmlParsing:
            if child.tag == 'video':
                orderedVideoList.append(child.attrib['url_name'])
    return orderedVideoList

directory = "xml"

coursePairsToVideos = {}
for course in getUsableCourses.dictNumOccurrencesToListCourseNames[2]:
    coursePairsToVideos[course] = [videosForCourse(x) for x in getUsableCourses.dictXml[course]]
for course in getUsableCourses.dictNumOccurrencesToListCourseNames[3]:
    coursePairsToVideos[course] = [videosForCourse(x) for x in getUsableCourses.dictXml[course][:2]]
for course in getUsableCourses.dictNumOccurrencesToListCourseNames[4]:
    coursePairsToVideos[course] = [videosForCourse(x) for x in getUsableCourses.dictXml[course][:2]]
#for course in coursePairsToVideos:
#    x = compareLists.compareLists(coursePairsToVideos[course])
#    print course, ':', len(coursePairsToVideos[course][0]), ' ', len(x)
#    print x
#    print 'notes:'
#    print ''
 
