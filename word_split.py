import chardet
import os
import jieba.posseg as pseg
import re
import operator
import math
import codecs

DOC_NUM=438     #文档总数

'''读取停用词文件'''
f_stop=codecs.open("stop_words.txt",'rb','utf-8')
stop_words=[each.replace('\n','') for each in f_stop.readlines()]

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def wordSplit(path):
    '''将文档进行分词，创建新目录存储分词后的结果'''
    for i in range(1, DOC_NUM + 1):
        print(i)

        f = open(path + '/' + str(i) + '.txt', 'rb')
        p=f.read().decode('utf-8')

        p=p.replace(" ","")     #去空格
        words=pseg.cut(p)       #分词

        f.close()
        r=open('clean_data/'+str(i)+'.txt','w',encoding='utf-8')
        flag=0

        for w in words:
            if flag==0 and w.word!='正文':     #只用正文计算
                continue
            elif w.word=='正文':
               flag=1
            elif (not w.word in stop_words) and is_Chinese(w.word):        #去停用词
                r.write(w.word+'\n')
        r.close()


def GetInput(q):
    #q = input("Enter the query here:")
    res=[]
    q = q.replace(" ", "")  # 去空格
    words = pseg.cut(q)  # 分词

    '''将用户输入分词后写入文档中'''
    f = open( 'clean_data\\0.txt', 'w', encoding='utf-8')
    for w in words:
        if (not w.word in stop_words) and is_Chinese(w.word):  # 去停用词
            f.write(w.word + '\n')
            res.append(w.word)
    f.close()
    return list(set(res))

# def idf(path):
#     idf={}
#     for file in os.listdir(path):
#         f=open(path+'\\'+file,'r',encoding='utf-8')
#         print(file)
#
#         '''该词出现的文档数计数'''
#         rf=set([each.replace('\n','') for each in f.readlines()])
#         f.close()
#         for each in rf:
#             if each in idf.keys():
#                 idf[each]+=1
#             else:
#                 idf[each]=1
#
#     '''输出到文件中'''
#     f=open('idf.txt','w',encoding='utf-8')
#     for (word,count) in idf.items():
#         s='%s %7lf'%(word,math.log((DOC_NUM)/count,10))
#         f.write(s+'\n')
#     f.close()

path_doc='E:\CODE\pycharm\InfoSearch\docs_utf8'     #原始文档存储目录
#wordSplit(path_doc)
# idf('E:\CODE\pycharm\InfoSearch\clean_data')


