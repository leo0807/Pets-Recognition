import os

originPath = '../../../../Data for project/dog/'
foldersPath = '../../../../Data for project/new/dog/'
print(os.path.exists(foldersPath))
def walkPath(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            paths.append(filepath)
    return paths, len(paths)


cat_after, count = walkPath(foldersPath)
cat_before, count_0 = walkPath(originPath)
print(count)
print(count/count_0)



# for folders in os.listdir(folderPath):
#     folder = folderPath + os.sep + folders
#     for image in os.listdir(folder):
#         print(image)
#         ipath = folder + os.sep + image
#         label = find_label(ipath)
#         pixel = None
#         if classify == 'dog':
#             pixels = dog_preprocess(ipath, savePath)
#         else:
#             pixels = cat_preprocess(ipath, savePath)
#         if label != -1 and pixels is not None:
#             pixel = pixels
#             images.append([label, pixel])


def pad_image(image, target_size):
    print("image_path",image[0])
    img = Image.open(image[0])
    iw, ih = img.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    print(img.size, target_size)
    rw = float(w) / float(iw)
    rh = float(h) / float(ih)
    scale = min(rw, rh)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)
    img = img.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()
    new_image = Image.new('RGB', (w,h), (128, 128, 128))  # 生成灰色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(img, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式