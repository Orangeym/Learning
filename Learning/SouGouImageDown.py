import os,re
import requests
from urllib.parse import urlencode

header ={
    'Accept':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
COUNT = 0

# 通过输入尺寸大小和壁纸种类返回壁纸资源的url
def get_wallPaperTypeAndDpi():
    dpi = ((1920, 1080), (1366, 768), (1280, 720))  # 图片分辨率
    url = 'http://pic.sogou.com/pics/recommend?category=%B1%DA%D6%BD&from=home'
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            allTop = re.findall('var jsonTag = (\[.*?\]);',response.text, re.S)
            wallPaperList = allTop[0][2:-2]
            wallPaperList = wallPaperList.split('","')  # 获取列表

            for num,item in zip(range(1,30),wallPaperList):
                print(num,item)
            type_num = input('请输入壁纸类型（输入对应的数字即可）:')
            for num,(x,y) in zip(range(1,4),dpi):
                print(num, x, '*', y)
            dpi_unm = input('输入壁纸分辨率（输入对应数字即可）:')
            print('|-------------------|')
            print(' 正在下载请稍后......')
            print(wallPaperList[int(type_num)-1], dpi[int(dpi_unm)-1])
            return wallPaperList[int(type_num)-1], dpi[int(dpi_unm)-1]
        else:
            print('response.status_code = ', response.status_code)
    except:
        print('请求失败或输入错误！')

# 获取其中一类图片的资源列表
def get_url(dpi=(1920, 1080),start=0,picType='全部'):
    params = {
        'category': '壁纸',
        'tag': picType,
        'start': start,
        'len': '15',
        'width': dpi[0],
        'height': dpi[1],
    }
    print(params)
    return 'http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?'+ urlencode(params)

# 获取图片的下载url
def get_imageUrl(url):
    response = requests.get(url, header=header)
    if response.status_code == 200:
        all_items = response.json().get('all_items')
        if all_items != None:
            for item in  all_items:
                pic_url = item.get('pic_url')
                id = item.get('id')
                yield{
                    'url': 'http://imgstore04.cdn.sogou.com/v2/thumb/dl/'+str(
                        id)+'.jpg?appid=10150005&referer=sogou.com&url=' + pic_url,
                    'title': str(id) + '.jpg'
                }
# 保存图片
def saveimage(image_info):
    global COUNT
    savePath = 'E:\\picture\\'
    if not os.path.isdir(savePath):
        print('图片存储目录不存在正在创建图片存储目录')
        os.makedirs(savePath)
        print('目录创建成功')
    else:
        print('目录已存在正在保存')
    try:
        print(image_info.get('url'))

        response = requests.get(image_info.get('url'), header=header)
        savePath = savePath + image_info.get('title')
        if response.status_code == 200:
            if not os.path.isdir(savePath):
                with open(savePath,'wb')as f:
                    f.write(response.content)
                    print(image_info.get('title'), '-》ok\n')
                    COUNT += 1
    except requests.ConnectionError:
        print('Failed to Save Image.')

picType, dpi = get_wallPaperTypeAndDpi()
for num in range(0, 90, 15):
    imageUrl = get_imageUrl(get_url(dpi, num, picType))
    for x in imageUrl:
        saveimage(x)
print('总共下载%d张' % COUNT)


