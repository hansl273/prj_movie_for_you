import pandas as pd
from konlpy.tag import Okt
import matplotlib.pyplot as plt
import re

df = pd.read_csv('./crawling_data/reviews_2018.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['영화','연출','관객','개봉','개봉일','주인공','출연','배우','리뷰',
                         '촬영','각본','극장','감독','네이버','박스','오피스','박스오피스',
                         '장면','관람','연기','되어다']
# count = 0 생략가능

# 형태소 분리
cleaned_sentences = []
for review in df.reviews:
    # count += 1                생략가능
    # if count % 10 == 0:
    #     print(',', end='')
    # if count % 100 == 0:
    #     print()
    review = re.sub('[^가-힝 ]', ' ', review) # ^ 지정단어 제외하고 삭제
    # review = review.split()
    # words = []
    # for word in review:               이언정
    #     if len(word) > 20:
    #         word = ' '
    #     words.append(word)
    # review = ' '.join(words)
    token = okt.pos(review, stem=True)

    df_token = pd.DataFrame(token, columns=['word','class'])
    df_token = df_token[(df_token['class'] == 'Noun') |     #명사
                        (df_token['class'] == 'Verb') |     #동사
                        (df_token['class'] == 'Adjective')] #형용사만 남김

# 불용어 처리
    words=[]
    for word in df_token.word:

        if len(word) > 1:
            if word not in stopwords :
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
df.dropna(inplace=True)

# 리뷰 길이 분포 확인
print('리뷰의 최대 길이 :',max(len(cleaned_sentences) for cleaned_sentences in df))
print('리뷰의 평균 길이 :',sum(map(len, df))/len(df))
plt.hist([len(cleaned_sentences) for cleaned_sentences in df], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

df.to_csv('./crawling_data/cro/cleaned_review_2018.csv', index=False)
df.info()






