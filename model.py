from rank_bm25 import BM25Okapi
import pandas as pd
import jieba
import dill as pickle
import numpy as np


# # 加载和处理数据
# df = pd.read_csv('songs.csv')  # 确保文件路径正确
# df['纯歌词'] = df['纯歌词'].fillna('')
# tokenized_corpus = [list(jieba.cut(doc)) for doc in df['纯歌词']]

# # 训练 BM25 模型
# bm25 = BM25Okapi(tokenized_corpus)

# # 保存 BM25 模型
# with open('bm25_model.pkl', 'wb') as file:
#     pickle.dump(bm25, file)

# # 保存处理后的 DataFrame
# df.to_pickle('songs_df.pkl')
# 定义搜索相关歌词的函数


def find_most_relevant_lyric(query, lyrics):
    query_words = set(jieba.cut(query))
    sentences = lyrics.split('\n')
    max_score = 0
    most_relevant_sentence = ""
    for sentence in sentences:
        sentence_words = set(jieba.cut(sentence))
        common_words = query_words.intersection(sentence_words)
        score = len(common_words)
        if score > max_score:
            max_score = score
            most_relevant_sentence = sentence
    return most_relevant_sentence


# 定义使用 BM25 进行搜索的函数

# 加载 BM25 模型和 DataFrame
with open('bm25_model.pkl', 'rb') as file:
    bm25_loaded = pickle.load(file)

df_loaded = pd.read_pickle('songs_df.pkl')


def search_with_bm25(query, bm25_model=bm25_loaded, df=df_loaded, top_n=5):
    query_words = list(jieba.cut(query))
    doc_scores = bm25_model.get_scores(query_words)
    top_indexes = np.argsort(doc_scores)[::-1][:top_n]
    results = df.iloc[top_indexes]
    results['最相关歌词'] = results['纯歌词'].apply(
        lambda x: find_most_relevant_lyric(query, x))
    return results

# 执行查询
# query = "我坐在这里"
# results = search_with_bm25(query, bm25_loaded, df_loaded)
# print(results[['歌名', '歌手', '纯歌词', '最相关歌词']])
