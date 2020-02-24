import os
import helper

originPath = '../../../../Data for project/dog/'
classes = ['dog_angry', 'dog_happy', 'dog_fearful', 'dog_sadness', 'dog_neutral']
foldersPath = '../../../../Data for project/new/dog/'
print(os.path.exists(foldersPath))

after, count = helper.walkPath(foldersPath)
before, count_b = helper.walkPath(originPath)
total = 0


