
#!/usr/bin/python
# coding=utf-8
# 采用TextRank方法提取文本关键词
import sys
import pandas as pd
import jieba.analyse
"""
       TextRank权重：

            1、将待抽取关键词的文本进行分词、去停用词、筛选词性
            2、以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
            3、计算图中节点的PageRank，注意是无向带权图
"""

# 处理标题和摘要，提取关键词
def getKeywords_textrank(data,topK):
    # idList,titleList,abstractList = data['id'],data['title'],data['abstract']
    idList, titleList, abstractList = data['资源编码'].reset_index().drop(['index'], axis=1).values, data[
        '产品线'].reset_index().drop(['index'], axis=1).values, data['咨询内容'].reset_index().drop(['index'], axis=1).values
    ids, titles, keys = [], [], []
    for index in range(len(idList)):
        # text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        text = abstractList[index]
        jieba.analyse.set_stop_words("data/stopWord.txt") # 加载自停词
        # print "\"",titleList[index],"\"" , " 10 Keywords - TextRank :"
        keywords = jieba.analyse.textrank(text[0], topK=topK, allowPOS=('n','nz','v','vd','vn','l','a','d'))  # TextRank关键词提取，词性筛选
        word_split = " ".join(keywords)
        keys.append(word_split)
        ids.append(idList[index])
        titles.append(titleList[index])

    result = pd.DataFrame({"id": ids, "titles": titles, "key": keys}, columns=['id', 'titles', 'key'])
    result['id'] = result['id'].apply(lambda x:x[0])
    result['titles'] = result['titles'].apply(lambda x: x[0])
    return result


def to_result(cpx,data):
    data = data[data['产品线'] == cpx]
    # tf-idf关键词抽取
    result = getKeywords_textrank(data, 2)
    return result


def main():
    dataFile = 'data/contents.xlsx'
    data = pd.read_excel(dataFile)

    cpx_col = data['产品线'].unique().tolist()[1:]
    df = pd.DataFrame()
    for cpx in cpx_col:
        result = to_result(cpx, data)
        print(f'---------------[{cpx}]，抽取完成------------------------')
        df = pd.concat([df, result], axis=0)
    df.to_csv('result/all_result/contents_keys_textrank.csv', index=False, encoding='utf_8_sig')

if __name__ == '__main__':
    main()
