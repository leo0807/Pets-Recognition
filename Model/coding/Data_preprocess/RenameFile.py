import os
def renameFile(path):
    print('come into path:' + path)
    fileList = os.listdir(path)
    folderPath, folderName = os.path.split(path)
    i = 1000
    for file in fileList:
        filepath, filename = os.path.split(file)
        # print(filename.split('_')[1])
        oldfilename = path + os.sep + file
        newfilename = path + os.sep + folderName + '_' + str(i) + '.jpg'
        os.rename(oldfilename, newfilename)
        print(oldfilename + ' -> ' + newfilename)

        i += 1
    print("done")


# ----------------- rename files -------------------- #
# path = '/Users/zhouguozhi/PyhtonFile/Data for project'
# if os.path.exists(path):
#     print('path found')
# else:
#     print('path not found')
# for folders in os.listdir(path):
#     # print(folders)
#     folderPath = path + os.sep + folders
#     for folders in os.listdir(folderPath):
#         if '.DS' not in folders:
#             imagespath = folderPath + os.sep + folders
#             renameFile(imagespath)
# --------------------------------------------------- #

# remove files already existed
path = '../../../../Data for project/new/cat'
origin = '../../../../Data for project/cat'
for folder in os.listdir(path):
    # print(folder)
    if '.DS' not in folder:
        for file in os.listdir(path + os.sep + folder):
            filename, extend = os.path.splitext(file)
            # print(filename)
            folderName = '_'.join(filename.split('_')[:-1])
            # print(folderName)
            origin_file_name = origin + os.sep + folderName + os.sep + filename + extend
            if os.path.exists(origin_file_name):
                print(origin_file_name)
                os.remove(origin_file_name)


