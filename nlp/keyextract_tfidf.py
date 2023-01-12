#!/usr/bin/python
# coding=utf-8
# 采用TF-IDF方法提取文本关键词
# http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting

import sys,codecs
import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
"""
       TF-IDF权重：
           1、CountVectorizer 构建词频矩阵
           2、TfidfTransformer 构建tfidf权值计算
           3、文本的关键字
           4、对应的tfidf矩阵
"""
# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l

# tf-idf获取文本top10关键词
def getKeywords_tfidf(data,stopkey,topK):
    idList, titleList, abstractList = data['资源编码'].reset_index().drop(['index'],axis=1).values, data['产品线'].reset_index().drop(['index'],axis=1).values, data['咨询内容'].reset_index().drop(['index'],axis=1).values
    corpus = [] # 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(abstractList)):
        # text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        text = abstractList[index]
        text = dataPrepos(text[0],stopkey) # 文本预处理
        text = " ".join(text) # 连接成字符串，空格分隔
        corpus.append(text)

    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    # 4、获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    # 5、打印词语权重
    ids, titles, keys = [], [], []
    for i in range(len(weight)):
        print(u"-------这里输出第", i+1 , u"篇文本的词语tf-idf------")
        ids.append(idList[i])
        titles.append(titleList[i])
        df_word,df_weight = [],[] # 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
            # print(word[j],weight[i][j])
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1) # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight",ascending = False) # 按照权重值降序排列
        keyword = np.array(word_weight['word']) # 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0,topK)] # 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)

    result = pd.DataFrame({"id": ids, "titles": titles, "key": keys},columns=['id','titles','key'])
    result['id'] = result['id'].apply(lambda x:x[0])
    result['titles'] = result['titles'].apply(lambda x: x[0])
    return result

def stopwordslist(filepath):
    return [line.strip() for line in open(filepath, 'r').readlines()]

def to_result(cpx,data,stopkey):
    data = data[data['产品线'] == cpx]
    # tf-idf关键词抽取
    result = getKeywords_tfidf(data, stopkey, 2)
    return result

def main():
    # dataFile = 'data/sample_data.csv'
    dataFile = 'data/contents.xlsx'
    data = pd.read_excel(dataFile)
    # 停用词表
    stopkey = stopwordslist('data/stopWord.txt')

    cpx_col = data['产品线'].unique().tolist()[1:]
    df = pd.DataFrame()
    for cpx in cpx_col:
        result = to_result(cpx,data,stopkey)
        df = pd.concat([df, result], axis=0)
    df.to_csv('result/all_result/contents_keys.csv',index=False,encoding='utf_8_sig')


if __name__ == '__main__':
    main()
