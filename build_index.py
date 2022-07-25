#创建倒排索引文件,计算相关度
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

import os
DOC_NUM=438

def BuildCorpus(path):
    '''将路径下的所有文档读进字符串'''
    corpus=[]
    for i in range(0,DOC_NUM+1):
        #print(i)

        f = open(path + '/' + str(i)+'.txt', 'rb')
        content = f.read().decode('utf-8')
        corpus.append(content)
        f.close()
    #print('Over')
    return corpus

def GetTFIDF(corpus):
    '''生成TFIDF矩阵'''
    vectorizer=CountVectorizer()        #将文本中的词语转换为词频矩阵
    X=vectorizer.fit_transform(corpus)      #计算每个词语出现的次数
    words = vectorizer.get_feature_names()
    #print(word)
    #print(X.toarray())
    transformer=TfidfTransformer()
    M=transformer.fit_transform(X)      #将词频矩阵X统计成TF-IDF值
    #print(M.toarray())
    return words,M.toarray()

def GetPos(words,corpus):
    '''生成倒排索引文件'''
    f = open('index.txt', 'w', encoding='utf-8')

    for word in words:
        f.write(word)       #每行开头写单词
        print(word)
        for doc in corpus:
            count=0     #word在doc中出现的次数
            p=0       #索引起始位置
            pos=[]      #存储所有位置
            p=doc.find(word,p,len(doc))       #此次找出单词的位置
            while(p!=-1):
                count+=1
                pos.append(p)
                p=doc.find(word,p+len(word),len(doc))

            '''输出每个单词的倒排索引在文档中'''
            f.write(' '+str(count))
            for each in pos:
                f.write(','+str(each))
        f.write('\n')
    f.close()

def CalSim(M,words):
    '''计算相关度'''
    Sim=[]
    for i in range(1,len(M)):
        sim=cosine_similarity([M[0]],[M[i]])        #计算余弦相似度

        '''找到文档标题'''
        f=open('docs_utf8\\'+str(i)+'.txt','r',encoding='utf-8')
        head=f.readline()
        while(not ('【 标  题 】'in head)):
            head=f.readline()

        f.close()

        '''文件标题中每有一个关键词，则相关度加一'''
        for word in words:
            if word in head:
                sim[0][0]+=1

        Sim.append((i,sim))
    Sim.sort(key=lambda x:x[1][0][0],reverse=True)        #按相关度从大到小排序
    return Sim

# Sim=[]
# clean_doc=BuildCorpus('E:\CODE\pycharm\InfoSearch\clean_data')
# words,M=GetTFIDF(clean_doc)       #word为所有单词，M为TFIDF矩阵
# raw_doc=BuildCorpus('E:\CODE\pycharm\InfoSearch\docs_utf8')
# GetPos(words,raw_doc)
# CalSim()
# print(Sim)