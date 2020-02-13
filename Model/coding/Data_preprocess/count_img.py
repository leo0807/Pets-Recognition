import os
import helper

originPath = '../../../../Data for project/cat/'
foldersPath = '../../../../Data for project/new/cat/'
print(os.path.exists(foldersPath))



cat_after, count = helper.walkPath(foldersPath)
cat_before, count_0 = helper.walkPath(originPath)
print(count)
print(count/count_0)


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