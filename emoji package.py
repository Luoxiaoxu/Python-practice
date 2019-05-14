from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import urllib.parse
import os
import re

def GetEmoji():
    keyword=input("请输入所查询的表情名称：")
    input_num=int(input("\n请输入要下载的数量："))
    num=input_num
    i=0
    page=0
    while i<num:
        page+=1
        image_url='http://www.doutula.com/search?type=photo&more=1&keyword='+urllib.parse.quote(keyword)+'&page='+str(page)  #表情来源于斗图啦网
        path='表情/'+keyword
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req=urllib.request.Request(url=image_url, headers=headers)
            con=urlopen(req)
            soup=BeautifulSoup(con.read(),'lxml')
        except HTTPError as e:
             print(e)
        else:    
            imageLoca=soup.find_all('a',{'class':'col-xs-6 col-md-2'})
            if len(imageLoca)<72 and len(imageLoca)+i<num:
                num=len(imageLoca)+i
            if num==0:
                print('\n未找到该表情！\n')
                break
            if not os.path.exists(path):
                os.makedirs(path)
            for con in imageLoca:
                name=con.text 
                con2=con.find_all('img')
                imageDow=con2[0]['data-original'] if len(con2)<2 else con2[1]['data-original']
                name_new = re.sub('[!\/:*?"<>|]', '', name)
                i+=1
                urlretrieve(imageDow,path+'/'+str(i)+name_new.replace('\n','')+imageDow[-4:]) 
                print('第%d张表情下载完成!\n'%i)
                if i>=num:
                    print("下载已完成！" if num==input_num else "当前仅找到"+str(num)+"表情，已下载完成！\n")
                    break

if __name__=='__main__':
    GetEmoji()


