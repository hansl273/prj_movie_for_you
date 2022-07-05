import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from job07_TFIDF import df_reviews, Tfidf_matrix

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[1:11]
    movieIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mts.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb')  as f:
    Tfidf = pickle.load(f)

# 영화제목 / 인덱스를 이용
movie_idx =1003
movie_idx = df_reviews[df_reviews['titles']=='범죄도시2 (the roundup)'].index[0]
# print(movie_idx)
# print(df_reviews.iloc[1228, 1])

cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)