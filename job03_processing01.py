import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_2018.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords = list(df_stopwords['stopword'])

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
    # for word in review:
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
df.to_csv('./crawling_data/cleaned_review_2018.csv', index=False)
df.info()




