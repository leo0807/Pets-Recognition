import os
import sys
import _thread
from icrawler.builtin import FlickrImageCrawler
from icrawler.builtin import GoogleImageCrawler

image_path = '..\\Dataset\\'

Flicker_API = "826864874f2a0f2f3d68af19c49c6142"

EmotionList = open('EmotionList.txt', 'rt')


def search_image(pet, target, savePath):
    emotion = target.strip('\n')
    imageDir = savePath + os.sep + emotion
    print(imageDir)
    searchName = emotion + ' ' + pet
    print(searchName)
    flickr_crawler = FlickrImageCrawler(Flicker_API, storage={'root_dir': imageDir})
    flickr_crawler.crawl(max_num=1000, tags=searchName, text=searchName)
    google_crawler = GoogleImageCrawler(storage={'root_dir': imageDir})
    google_crawler.crawl(keyword=searchName, max_num=1000)


saveCatPath = image_path + 'cat' + os.sep
saveDogPath = image_path + 'dog' + os.sep

# print(saveCatPath)

# download images from website
# for nameList in EmotionList:
#     search_image('cat', nameList, saveCatPath)
#     search_image('dog', nameList, saveDogPath)
# print("Collection is done")

