#!/user/bin/python
#coding=gbk
#author��luoxiaoxu
#blog:xiaoxu.online
#Filename: ZhihuAnswerDowload.py
#Function: ��ȡ֪�������к����ض��ؼ��ʵĻش�

from bs4 import BeautifulSoup
import requests
import os
import re
import time
import csv
import json

def GetAnswer(*Question_ID):
    if len(Question_ID)==0:
        Question_ID=input("�����������ţ�")
    keyword=input('������ؼ���(ͬʱ�����Կո�����������+���)��')  # ���磬���뺬�к��ݣ�ͬʱ�����人���Ͼ������롰���� �人+�Ͼ���
    keywords=keyword.split()                                            #����ȫ���𰸣�ֱ��enter
    if keyword=='':
        keyword='��'
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
               " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    limit=10  #ÿ����ʾ�Ĵ𰸸���
    offset=0  #��һ����ʾ�Ļش�ƫ����
    total_num=10  #�𰸸�������ʼ��Ϊlimit
    browse_num=0  #�Ѿ������Ļش����
    record_num=0  #���ؼ��ֵĻش����
    title=''
    if not os.path.exists('֪������/'):
        os.makedirs('֪������/')
    print('\n������ȡ����\n')
    while browse_num<total_num:
        url = "https://www.zhihu.com/api/v4/questions/{Question_ID}/answers?include=content&limit="\
              "{limit}&offset={offset}&platform=desktop&sort_by=default"\
               .format(Question_ID=str(Question_ID),limit=str(limit),offset=str(offset))
        res=requests.get(url,headers=headers)
        try:
            res=json.loads(res.content)
        except:
            print('�������������\n')
            return None
        total_num=res['paging']['totals']
        cons=res['data']

        if cons is not None:
            if total_num<=0:
                print('��������ʱ�޴𰸣�')
                break
            if title=='':
                    title=cons[0]['question']['title']
                    path_csv,path_txt=CreativeFile(title,keyword)  #����csv��txt�ļ���csv�ļ�Ϊ�������к��йؼ��ʻش�������б�
            for con in cons:
                browse_num+=1
                Re=re.compile(r'<[^>]+>',re.S)
                answer_detail=Re.sub('',con['content'])   #��ȡ����ش�����
                flag=True
                if len(keywords)>0:
                   flag=HasKeywords(answer_detail,keyword)  #��ѯ�Ƿ��йؼ���
                if flag:
                    record_num+=1
                    author_name=con['author']['name']
                    author_url='https://www.zhihu.com/people/'+con['author']['url_token'] if not author_name=='�����û�' else ' '
                    answer_url='https://www.zhihu.com/question/'+str(Question_ID)+'/answer/'+str(con['id'])
                    Save2File_csv(path_csv,[str(record_num)+'.',author_name,answer_url,author_url])
                    answer_txt=[str(record_num)+'.',author_name+'   ��ҳ:'+author_url]
                    answer_txt.append('\n\n����:'+answer_url+'\n')
                    answer_txt.append('\n'+answer_detail+\
                        '\n-------------------------------------------------------------------------------\n')
                    Save2File_txt(path_txt,answer_txt)
                    print('�ѱ����%d���ش�\n'%record_num)
            offset+=len(cons)
            if len(cons)<limit:  #����ȡ�����һҳ
                break
    if len(keywords)==0:
        print('��ȡ��ɣ��ѱ���ȫ��%d���ش�\n'%record_num)
    elif record_num>0:
        print('��ȡ��ɣ��ѱ���%d����ؼ����йصĻش�\n'%record_num)
    else:
        os.remove(path_csv)
        os.remove(path_txt)
        print('δ�ҵ���ؼ����йصĴ�\n')
                


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

def HasKeywords(answer_detail,keyword):   #�ж��Ƿ������йؼ���
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
    path_csv='֪������/'+title+'.csv'
    path_txt='֪������/'+title+'.txt'
    if os.path.exists(path_csv):   #���ļ����ڣ����
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
    Save2File_csv(path_csv,['�ؼ��֣�'+keyword])
    Save2File_csv(path_csv,['���','�����ǳ�','�ش�����','��ҳ����'])
    Save2File_txt(path_txt,[title,'�ؼ��֣�'+keyword+'\n'])
    return path_csv,path_txt


if __name__=='__main__':
    GetAnswer()
