# moocdiff

This github has a collection of all or our scripts, along with some intermediate results.

Specifically, we have:

edX_video_parsing.py reads the xml directory which contains information about course structure, so as to find the videos (and their ordering) for a course

getUsableCourses.py is the method by which we extract data from the edX student interaction logs

researchModel.py contains the first part of our model, the skipgram embedding layer, outputs videoVec128.txt

modelPart2.py contains the rNN and runs it on the results of part 1

