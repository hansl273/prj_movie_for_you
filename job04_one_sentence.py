import pandas as pd

df = pd.read_csv('./crawling_data/cro/cleaned_review_2018.csv') #폴더
# df = pd.read_csv('./crawling_data/reviews_2018.csv') #concat파일
df.dropna(inplace=True)
df.info()
one_sentences = []
for title in df['title'].unique():
    temp = df[df['title'] == title]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['cleaned_sentences'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'titles':df['title'].unique(), 'reviews':one_sentences})
print(df_one.head())
# print('debug')

df_one.to_csv('./crawling_data/one/cleaned_review_2018.csv', index=False)
