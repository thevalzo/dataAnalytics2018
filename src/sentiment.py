# -*- coding: utf-8 -*-
import MySQLdb
from collections import Counter
from utility import Utility
import operator
from itertools import takewhile
class Sentiment:

    db = []
    sentix_polarity=dict()
    sentix_pos = dict()

    def __init__(self):

        # Set up db connection
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                  charset='utf8')

        #load lexicon from DB
        cursor = self.db.cursor()
        query = "SELECT token, avg(polarity), pos_tag FROM data_analytics.sentix where token not like'%\_%' group by token;"
        cursor.execute(query)
        results = cursor.fetchall()

        #save lexicon in dict
        for row in results:
            self.sentix_polarity[row[0]]=row[1]
            self.sentix_pos[row[0]] = row[2]

        print("  ***  Lexicon Loaded  ***  ")


    def get_linked_entities(self, wd_id, type):
        # extract every article cointaining the place
        cursor = self.db.cursor()
        # query = "Select articles_entities.uri, surfaceForm, count(*) as n from 	articles_entities where articles_entities.url in  (select distinct articles_entities.url from articles_entities where articles_entities.wikidata_id =\'"+wd_id+"\' and articles_entities.type = \'"+type+"\') and articles_entities.uri in (select uri from entities where uri not in (select uri from places)) group by uri order by n desc limit 15;"
        query = "SELECT B.uri, B.surfaceForm, count(*) as n FROM ARTICLES_ENTITIES A ,ARTICLES_ENTITIES B WHERE A.wikidata_id = \'" + wd_id + "\' AND A.TYPE = \'" + type.replace('\"', '\\\"').replace('\'', '\\\'') + "\' AND A.URL    = B.URL AND NOT EXISTS (SELECT 1  FROM PLACES P WHERE B.URI = P.URI) group by b.uri order by n desc limit 15;"
        cursor.execute(query)
        print(query)
        results = cursor.fetchall()

        list = []
        for row in results:
            element = dict()
            element['uri'] = row[0]
            element['uri_short'] = row[0].split("/")[-1]
            element['surfaceForm'] = row[1]
            element['count'] = row[2]
            print(str(element))
            list.append(element)

        return list

    def get_linked_places(self, wd_id, type):
        # extract every article cointaining the place
        cursor = self.db.cursor()
        query = "Select places.uri, places.type, surfaceForm, count(*) as n from articles_entities, places where url in (select distinct articles_entities.url from articles_entities where articles_entities.wikidata_id =\'" + wd_id + "\' and articles_entities.type = \'" + type.replace('\"', '\\\"').replace('\'', '\\\'') + "\') and places.wikidata_id!='Q4006292' and places.uri=articles_entities.uri and places.type=articles_entities.type and places.wikidata_id!=\'" + wd_id + "\'  and (places.in_brescia=1 or places.in_provincia=1) group by uri order by n desc limit 15;"
        cursor.execute(query)
        print(query)
        results = cursor.fetchall()

        list = []
        for row in results:
            element = dict()
            element['uri'] = row[0]
            element['uri_short'] = row[0].split("/")[-1]
            element['surfaceForm'] = row[2]
            element['count'] = row[3]
            list.append(element)

        return list

    def get_place_word_frequency(self, wd_id, type, pos_tag):

        #istantiate a new word-counter
        uri=""
        words = Counter()
        place_wf=dict()
        surfaceForms=[]
        #extract every article cointaining the place
        cursor = self.db.cursor()
        query = "select distinct articles.article_token, articles_entities.surfaceForm, articles_entities.uri from articles, articles_entities where articles.url=articles_entities.url and articles_entities.wikidata_id = \'" + str(wd_id) + "\'and articles_entities.type = \'" + type.replace('\"', '\\\"').replace('\'','\\\'') + "\';"
        cursor.execute(query)
        n_articles = cursor.rowcount
        results = cursor.fetchall()
        tokens_to_add=[]
        # for every tokenized article add words to counter
        for row in results:
            surfaceForms.append(row[1])
            tokens = row[0].encode('utf-8').split()
            uri = row[2]
            for token in tokens:
                if(token in self.sentix_pos ):
                    if(self.sentix_pos[token]==pos_tag):
                        tokens_to_add.append(token)


        words.update(tokens_to_add)

        #remove the prefix of the place from words
        place_type=type.lower()
        if place_type in words:
            words.pop(place_type)

        # remove the name of the place from words
        for word in surfaceForms:
            word=word.lower()
            word_s=word.split('\'')
            for word1 in word_s:
                if word1.lower() in words:
                    words.pop(word1.lower())

        # remove the wikipedia name of the place from words
        t_uri=uri.split("/")[-1].replace("_"," ").split(" ")

        for word2 in t_uri:
            if word2.lower() in words:
                words.pop(word2.lower())

        t_uri=uri.split("/")[-1].replace("_"," ").split("\'")

        for word2 in t_uri:
            if word2.lower() in words:
                words.pop(word2.lower())


       # set up structure with all data
        place_wf['words'] = words
        place_wf['n_articles']= n_articles
        #print("most common words for " + str(type) + " with uri " + str(uri.encode('utf8')) + " \n " + str(words.most_common())[:500])

        return place_wf

    def get_best_worst_words(self, wd_id, type, pos_tag):
        place_wf = self.get_place_word_frequency(wd_id, type, pos_tag)
        # retrive place and word dict for every place
        words = place_wf['words']

        # compute sentimen from sentix

        pos_words=dict()
        neg_words=dict()
        pos_neg_words=dict()
        for word in words.keys():
            if word in self.sentix_polarity:
                # print("sentiment for word :" +word+ " is "+str(self.sentix[word]*wf[word]))
                word_sentiment = self.sentix_polarity[word] * words[word]
                if( word_sentiment>0):
                    pos_words[word]=word_sentiment
                if (word_sentiment < 0):
                    neg_words[word] = word_sentiment
        pos_ord_words=sorted(pos_words.items(), key=operator.itemgetter(1))
        pos_ord_words=reversed(pos_ord_words)
        neg_ord_words=sorted(neg_words.items(), key=operator.itemgetter(1))



        negs=[]
        for elem in neg_ord_words:
            new_neg = dict()
            new_neg['word']=elem[0]
            new_neg['sent']=round(elem[1],2)
            negs.append(new_neg)


        poss = []
        for elem in pos_ord_words:
            new_pos = dict()
            print(elem)
            new_pos['word'] = elem[0]
            new_pos['sent'] = round(elem[1],2)
            poss.append(new_pos)

        pos_neg_words['pos']=poss
        pos_neg_words['neg']=negs

        return pos_neg_words

    def calc_place_sentiment(self, place, normalize):

        place_wf = self.get_place_word_frequency(place['wikidata_id'], place['type'], "a")
        # retrive place and word dict for every place
        words = place_wf['words']

        # compute sentimen from sentix
        total_sentiment = 0
        total_words = 0
        for word in words:
            total_words += words[word]

        word_sentiment = dict()
        for word in words.keys():
            if word in self.sentix_polarity:
                # print("sentiment for word :" +word+ " is "+str(self.sentix[word]*wf[word]))
                word_sentiment[word] = self.sentix_polarity[word] * words[word]
                total_sentiment += self.sentix_polarity[word] * words[word]
        if (int(normalize) == 1 and total_words != 0):
            total_sentiment = total_sentiment / total_words

        # build dict for output
        place_sentiment = dict()
        place_sentiment['type'] = place['type']
        place_sentiment['uri'] = place['uri']
        place_sentiment['wikidata_id'] = place['wikidata_id']
        place_sentiment['in_brescia'] = place['in_brescia']
        place_sentiment['in_provincia'] = place['in_provincia']
        place_sentiment['has_coordinates'] = place['has_coordinates']
        place_sentiment['latitude'] = place['latitude']
        place_sentiment['longitude'] = place['longitude']
        place_sentiment['n_articles'] = place['n_articles']
        place_sentiment['uri_short'] = place['uri_short']
        place_sentiment['words_sentiment'] = word_sentiment
        place_sentiment['total_sentiment'] = total_sentiment

        return place_sentiment

    def calc_places_sentiment(self, places, normalize):
        places_sentiment=[]

        for place in places:
            place_sentiment=self.calc_place_sentiment(place, normalize)
            places_sentiment.append(place_sentiment)
            #print("total sentiment for "+place['uri']+" is "+str(total_sentiment))
        return places_sentiment

    def set_places_sentiment(self):
        utility=Utility()
        places=utility.get_places(1,0,100000)

        places_sentiment=self.calc_places_sentiment( places, 1)
        for place in places_sentiment:
            #print(str(round(place['total_sentiment']*1000,2))+" - "+place['uri'])
            cursor = self.db.cursor()
            query = "UPDATE places set sentiment_norm='"+str(round(place['total_sentiment']*1000,2))+"' where uri='"+place['uri'].replace('\"', '\\\"').replace('\'', '\\\'')+"' and type='"+place['type'].replace('\"', '\\\"').replace('\'', '\\\'') + "\';"
            cursor.execute(query)

        self.db.commit()

        places_sentiment=self.calc_places_sentiment( places, 0)
        for place in places_sentiment:
            #print(str(round(place['total_sentiment'],3))+" - "+place['uri'])
            cursor = self.db.cursor()
            query = "UPDATE places set sentiment='"+str(round(place['total_sentiment'],2))+"' where uri='"+place['uri'].replace('\"', '\\\"').replace('\'', '\\\'')+"' and type='"+place['type'].replace('\"', '\\\"').replace('\'', '\\\'') + "\';"
            cursor.execute(query)
        self.db.commit()


