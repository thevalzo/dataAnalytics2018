# -*- coding: utf-8 -*-
import MySQLdb
from collections import Counter

class Sentiment:

    db = []

    def __init__(self):

        # Set up db connection
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                  charset='utf8')

    def places_word_frequency(self, places):
        places_wf=[]
        for place in places:

            #istantiate a new word-counter
            words = Counter()

            #extract every article cointaining the place
            cursor = self.db.cursor()
            query = "select distinct articles.article_token from articles, entities where articles.url=entities.url and entities.uri = \'" + place['uri'] + "\';"
            cursor.execute(query)
            results = cursor.fetchall()

            # for every tokenized article add words to counter
            for row in results:
                tokens = row[0]
                words.update(tokens.split())

            #remove the prefix of the place from words
            place_type=place['type'].encode('utf8').lower()
            if place_type in words:
                words.pop(place_type)

            # remove the name of the place from words
            for word in place['surfaceForm'].split():
                word=word.encode('utf8').lower()
                if word in words:
                    words.pop(word)

            print("most common words for " + place['type'] + " " + place['surfaceForm'] + " with uri " + place['uri'] + " \n " + str(
                words.most_common())[:500])

