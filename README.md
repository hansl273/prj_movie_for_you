# prj_movie_for_you
# 영화랭킹 디렉토리 개봉년도 review Data Crawling
https://movie.naver.com/movie/sdb/browsing/bmovie_nation.naver 
D:\work\python\prj_movie_for_you\crawling_data and models 생성
D:\work\python\prj_movie_for_you\crawling_data\ 개봉년도별 폴더, one, cro 생성

job01.crawling 년도별 개봉작 리뷰 페이지 저장

job02.concat 리뷰 페이지 합치기(년도별, 6개년도)

job03.processing01 형태소 분리, 불용어 처리, 결측치 제거, cro 폴더에 저장

job04.one_sentence cleaned_review 데이터를 영화별 리뷰를 한단락으로 one 폴더에 저장, unique(), join()

job05.word2vec  6개년도 영화리뷰 cleaned_tokens, embedding_model

job06.word2vec_visualization word2vec_2017_2022_movies.model 불러서 유사한 단어 embedding_model 생성, 유사한 단어 분류 차트 

job07.TFIDF reviews_2017_2022 불어와서 의미있는 단어들 값 산출
TF-IDF라는 값을 사용하여 CountVectorizer의 단점(문장 내에서 의미심장한 단어를 찾기 곤란)을 보완함.
문서에서 자주 나오는 단어에 대해 높은 가중치를 주되, 모든 문서에서 전반적으로 자주 나타나는 단어에 대해서는 패널티를 주는 방식이다.
해당 단위(문장) 안에서는 많이 등장하고 전체에서는 적게 사용될수록 분별력이 있다는 의미이다.
TF(Term Frequency) : 특정 단어가 하나의 데이터 안에서 등장하는 횟수
DF(Document Frequency) : 특정 단어가 여러 데이터에 자주 등장하는지를 알려주는 지표.
IDF(Inverse Document Frequency) : DF에 역수를 취해(inverse) 구함
TF-IDF : TF와 IDF를 곱한 값. 즉 TF가 높고, DF가 낮을수록 값이 커지는 것을 이용하는 것입니다.

job08.movie_recommendation 영화제목/ 키워드/ 문장이용, pickle불러오기,  word2vec_2017_2022_movies 불러와서 embedding_model 저장 
job09.word_cloud 글꼴지정, 6개년도 영화 불러오기, 영화별 워드클라우드
job10.movie_recommendation_web QT 디자이너 코딩 #pip install PyQt5
