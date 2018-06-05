# -*- coding: utf-8 -*-
import MySQLdb
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import string

class Cleaner:

    db = []

    def __init__(self):

        #Set up db connection
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                  charset='utf8')

    def copy_article(self):

        #Copy article text from article_raw to article_clean
        cursor = self.db.cursor()
        query = "UPDATE articles SET article_clean=article_raw"
        cursor.execute(query)
        self.db.commit()


    def tokenize(self):

        #extract cleaned text
        cursor = self.db.cursor()
        query = "select url, article_clean from articles;"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            url = row[0]
            article = row[1]

            #remove puntuaction
            for c in string.punctuation:
                article = article.replace(c, ' ')

            #remove more puntuaction
            article = article.replace('«'.decode('utf8'), '')
            article = article.replace('»'.decode('utf8'), '')
            article = article.replace('’'.decode('utf8'), ' ')

            #set up and remove stopwords
            stops = set(stopwords.words("italian"))
            article = [word for word in article.lower().split() if word not in stops]
            article = ''.join(t+' ' for t in article)

            #save tokenized article
            cursor = self.db.cursor()
            query = "UPDATE articles SET article_token=\'" + article + "\' WHERE url=\'" + url + "\';"
            print(" ** updated  article " + url + " ** ")
            cursor.execute(query)
            self.db.commit()
