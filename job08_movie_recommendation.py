import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb')  as f:
    Tfidf = pickle.load(f)

# 영화제목 / 인덱스를 이용
# movie_idx =1003
# movie_idx = df_reviews[df_reviews['titles']=='범죄도시2 (the roundup)'].index[0]
# print(movie_idx)
# print(df_reviews.iloc[1228, 1])

# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# keyword 이용
embedding_model = Word2Vec.load('./models/word2vec_2017_2022_movies.model')
keyword = '겨울'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = [keyword]
for word, _ in sim_word:
    words.append(word)
sentence = []
count = 10
for word in words:
    sentence = sentence + [word] * count
    count -= 1
print(sentence)
sentence = ' '.join(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation[:10])

# 문장 이용
okt = Okt()
# sentence = '견딜 수 없이 촌스런 삼남매의 견딜 수 없이 사랑스러운 행복소생기'
sentence = '당신은 처음부터 결심하고 만난 거니까 머리를 짧게 자른 기정을 보고 당황하는 태훈. ' \
           '왜 자른 걸까...? 우리 관계는 끝일까? 사업 실패로 졌던 빚을 다 갚은 창희. ' \
           '그동안 숨겨둔 묵직한 진실을 밝히는데... 미정은 회사 주변에서 아직도 돈을 갚지 않은 ' \
           '옛 남자친구를 마주친다. 한편, 구씨는 여전히 아침에 눈을 뜰 때마다 괴로운데... ' \
           '두 사람은 해방에 다다르게 될까?'

review = re.sub('[^가-힝 ]', ' ', sentence)  # ^ 지정단어 제외하고 삭제
token = okt.pos(sentence, stem=True)
df_token = pd.DataFrame(token, columns=['word', 'class'])
df_token = df_token[(df_token['class'] == 'Noun') |  # 명사
                    (df_token['class'] == 'Verb') |  # 동사
                    (df_token['class'] == 'Adjective')]  # 형용사만 남김

# 불용어 처리
words=[]
for word in df_token.word:
    if len(word) > 1:
        words.append(word)
cleaned_sentence = ' '.join(words)
print(cleaned_sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation[:10])





















