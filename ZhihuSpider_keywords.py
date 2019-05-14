#!/user/bin/python
#-*-coding:utf-8-*-
#author：luoxiaoxu
#blog:xiaoxu.online
#Filename: ZhihuAnswerDowload.py
#Function: 爬取知乎问题中含有特定关键词的回答

from bs4 import BeautifulSoup
import requests
import os
import re
import time
import csv
import json

def GetAnswer(*Question_ID):
    if len(Question_ID)==0:
        Question_ID=input("请输入问题编号：")
    keyword=input('请输入关键字(同时含有以空格间隔，或含有用+间隔)：')  # 例如，必须含有杭州，同时含有武汉或南京，输入“杭州 武汉+南京”
    keywords=keyword.split()                                            #下载全部答案，直接enter
    if keyword=='':
        keyword='无'
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
               " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    limit=10  #每次显示的答案个数
    offset=0  #下一次显示的回答偏移量
    total_num=10  #答案个数，初始设为limit
    browse_num=0  #已经遍历的回答个数
    record_num=0  #含关键字的回答个数
    title=''
    if not os.path.exists('知乎下载/'):
        os.makedirs('知乎下载/')
    print('\n正在爬取……\n')
    while browse_num<total_num:
        url = "https://www.zhihu.com/api/v4/questions/{Question_ID}/answers?include=content&limit="\
              "{limit}&offset={offset}&platform=desktop&sort_by=default"\
               .format(Question_ID=str(Question_ID),limit=str(limit),offset=str(offset))
        res=requests.get(url,headers=headers)
        try:
            res=json.loads(res.content)
        except:
            print('问题编号输入错误！\n')
            return None
        total_num=res['paging']['totals']
        cons=res['data']

        if cons is not None:
            if total_num<=0:
                print('该问题暂时无答案！')
                break
            if title=='':
                    title=cons[0]['question']['title']
                    path_csv,path_txt=CreativeFile(title,keyword)  #创建csv和txt文件，csv文件为保存所有含有关键词回答的链接列表
            for con in cons:
                browse_num+=1
                Re=re.compile(r'<[^>]+>',re.S)
                answer_detail=Re.sub('',con['content'])   #获取具体回答内容
                flag=True
                if len(keywords)>0:
                   flag=HasKeywords(answer_detail,keyword)  #查询是否有关键词
                if flag:
                    record_num+=1
                    author_name=con['author']['name']
                    author_url='https://www.zhihu.com/people/'+con['author']['url_token'] if not author_name=='匿名用户' else ' '
                    answer_url='https://www.zhihu.com/question/'+str(Question_ID)+'/answer/'+str(con['id'])
                    Save2File_csv(path_csv,[str(record_num)+'.',author_name,answer_url,author_url])
                    answer_txt=[str(record_num)+'.',author_name+'   主页:'+author_url]
                    answer_txt.append('\n\n链接:'+answer_url+'\n')
                    answer_txt.append('\n'+answer_detail+\
                        '\n-------------------------------------------------------------------------------\n')
                    Save2File_txt(path_txt,answer_txt)
                    print('已保存第%d个回答\n'%record_num)
            offset+=len(cons)
            if len(cons)<limit:  #已爬取到最后一页
                break
    if len(keywords)==0:
        print('爬取完成，已保存全部%d个回答！\n'%record_num)
    elif record_num>0:
        print('爬取完成，已保存%d个与关键词有关的回答！\n'%record_num)
    else:
        os.remove(path_csv)
        os.remove(path_txt)
        print('未找到与关键词有关的答案\n')
                


def Save2File_csv(path,content):
    f=open(path,'a+')
    writer=csv.writer(f)
    writer.writerow(content)
    f.close()

def Save2File_txt(path,contents):
    f=open(path,'a+',encoding='utf-8')
    for content in contents:
        f.writelines(content)
    f.writelines('\n')

def HasKeywords(answer_detail,keyword):   #判断是否含有所有关键词
    flag=True
    for key in keyword.split():    
        flag2=False
        for sub_key in key.split('+'):
            flag2=flag2 or answer_detail.find(sub_key)>0
            if flag2:
                break
        flag=flag and flag2
        if not flag:
            return False
    return True

def CreativeFile(title,keyword):
    path_csv='知乎下载/'+title+'.csv'
    path_txt='知乎下载/'+title+'.txt'
    if os.path.exists(path_csv):   #若文件存在，清空
        f=open(path_csv,'w')
        f.seek(0)
        f.truncate()
        f.close()
    if os.path.exists(path_txt):
        f=open(path_txt,'w')
        f.seek(0)
        f.truncate()
        f.close()
    Save2File_csv(path_csv,[title])
    Save2File_csv(path_csv,['关键字：'+keyword])
    Save2File_csv(path_csv,['序号','作者昵称','回答链接','主页链接'])
    Save2File_txt(path_txt,[title,'关键字：'+keyword+'\n'])
    return path_csv,path_txt


if __name__=='__main__':
    GetAnswer()
