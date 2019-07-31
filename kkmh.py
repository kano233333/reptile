# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import re
import json
import ast
from PIL import Image
from io import BytesIO
import base64
import os

def getContent(url,xp,type):
    response = requests.get(url)
    html_doc = response.content.decode("utf-8")
    if(type==1):
        return html_doc
    tree = etree.HTML(html_doc)
    xcontent = tree.xpath(xp)
    return xcontent

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                  
		os.makedirs(path)

print("快看目标漫画url:")
flagUrl = input()
print("\n导出目录:")
flagCatalog = input()
basisUrl = 'https://www.kuaikanmanhua.com'
xptitle = '/html/body//div[@class="cover fl"]//a/@href'
xpimg = '//script/text()'
titleHref = getContent(flagUrl,xptitle,0)


for titleItem in titleHref:
    titleIndex = titleHref.index(titleItem)
    htmlStr = getContent(basisUrl+titleHref[titleIndex],xpimg,1)
    imgs = re.search('{status:200,comicInfo:(.*?),nextComicInfo:',htmlStr) 
    imgsObj = re.findall('url:"(.*?)"',imgs.group(1))
    file = flagCatalog + '\\' + str(titleIndex)
    mkdir(file)
    print(str(titleIndex+1)+'话\n')
    for item in imgsObj:
        index = imgsObj.index(item)
        src = item.replace('\\u002F','/')
        res = requests.get(src)
        image = Image.open(BytesIO(res.content))
        image.save(file + '\\' + str(index) +'.jpg')
        
# pic = open("D:/9.jpg", "rb")
# pic_base64 = base64.b64encode(pic.read())
# pic.close()
# f = open('D:/test.txt','w')
# f.write(pic_base64.decode())
# f.write('\n')\

# f.close()
# os.remove('D:/9.jpg')
# print(pic_base64.decode())