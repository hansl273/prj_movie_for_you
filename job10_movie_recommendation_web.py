import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./movie_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_2017_2022_movies.model')
        # self.comboBox.addItem('2017-2022 영화 리스트')
        self.df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.comboBox.addItem(title)

        model = QStringListModel()              # 자동완성 코딩
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)


    def btn_slot(self):                         # 키워드 추천
        key_word = self.le_keyword.text()
        if key_word in self.titles:
            recommendation = self.recommendation_by_moive_title(key_word)   # 영화제목 키워드 추천
        else:
            recommendation = self.recommendation_by_keyword(key_word)
        if recommendation :
            self.lbl_recommendation.setText(recommendation)

    def getRecommendation(self, cosin_sim):          # 필터 내용(영화리스트)
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        return recMovieList

    def combobox_slot(self):                          # 선택 필터
        title = self.comboBox.currentText()
        recommendation = self.recommendation_by_moive_title(title)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_moive_title(self, title):     # 영화제목 연관 리스트 출력
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        # print('debug06')
        recommendation = '\n'.join(list(recommendation[1:]))
        return recommendation

    def recommendation_by_keyword(self, keyword):       # 키워드 연관 리스트 출력
        if keyword :
            keyword = keyword.split()[0]
            try:
                sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            except:
                self.lbl_recommendation.setText('제가 모르는 단어입니다.')
                return 0
            words = [keyword]
            for word, _ in sim_word:
                words.append(word)
            sentence = []
            count = 10
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            recommendation = '\n'.join(list(recommendation[:10]))
            return recommendation
        else:
            return 0





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())