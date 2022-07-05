import glob
import pandas as pd


df = pd.DataFrame()
# data_paths = glob.glob('./crawling_data/reviews_2018/*')
data_paths = glob.glob('./crawling_data/one/*')
# print(data_paths)

# for i in range(1, 20) : # 페이지 38+1
for path in data_paths:  # 경로지정으로
    # df_temp = pd.read_csv('./crawling_data/reviews_2022_{}page.csv'.format(i)) # 년도 수정
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)  # nan값 제거
    df_temp.drop_duplicates(inplace=True) # 중복값 제거
    df = pd.concat([df, df_temp], ignore_index=True)

df.drop_duplicates(inplace=True) # 합친 파일 중복값 제거
df.info()

my_year = 2022 # 년도 체크
# df.to_csv("./crawling_data/reviews_{}.csv".format(my_year), index=False)
df.to_csv("./crawling_data/reviews_2017_2022.csv", index=False) #6개년도