# -*- coding: utf-8 -*-
import MySQLdb
import urllib

class Utility:

    db = []
    sentix = dict()

    def __init__(self):
        # Set up db connection
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                  charset='utf8')

    def get_place(self, uri, type):
        place=dict()
        uri=urllib.quote(uri)
        cursor = self.db.cursor()
        query="SELECT type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude, sentiment, sentiment_norm FROM data_analytics.places where uri=\'"+str(uri)+"\' and type=\'"+str(type)+"\';"
        print(query)
        cursor.execute(query)
        result=cursor.fetchone()

        place['type']=result[0]
        place['uri'] = result[1]
        place['wikidata_id'] = result[2]
        place['in_brescia'] = result[3]
        place['in_provincia'] = result[4]
        place['has_coordinates'] = result[5]
        place['latitude'] = result[6]
        place['longitude'] = result[7]
        place['sentiment'] = result[8]
        place['sentiment_norm'] = result[9]
        place['uri_short'] = result[1].split("/")[-1]

        return place

    def get_place(self, wd_id, type):
        place=dict()
        cursor = self.db.cursor()
        query="SELECT type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude, aggregated_type, sentiment, sentiment_norm FROM data_analytics.places where wikidata_id=\'"+str(wd_id)+"\' and type=\'"+str(type).replace('\"', '\\\"').replace('\'', '\\\'')+"\';"
        print(query)
        cursor.execute(query)
        result=cursor.fetchone()

        place['type']=result[0]
        place['uri'] = result[1]
        place['wikidata_id'] = result[2]
        place['in_brescia'] = result[3]
        place['in_provincia'] = result[4]
        place['has_coordinates'] = result[5]
        place['latitude'] = result[6]
        place['longitude'] = result[7]
        place['aggregated_type'] = result[8]
        place['sentiment'] = result[9]
        place['sentiment_norm'] = result[10]
        place['uri_short'] = result[1].split("/")[-1]

        return place

    def get_place_provincia(self, uri, type):
        place = dict()

        cursor = self.db.cursor()
        cursor.execute(
            "SELECT type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude FROM data_analytics.places where uri=\'" + str(
                uri) + "\' and type=\'" + str(type) + "\' and (in_brescia=1 or in_provincia=1);")
        result = cursor.fetchone()

        place['type'] = result[0]
        place['uri'] = result[1]
        place['wikidata_id'] = result[2]
        place['in_brescia'] = result[3]
        place['in_provincia'] = result[4]
        place['has_coordinates'] = result[5]
        place['latitude'] = result[6]
        place['longitude'] = result[7]

        return place

    def get_place_brescia(self, uri, type):
        place = dict()

        cursor = self.db.cursor()
        cursor.execute(
            "SELECT type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude FROM data_analytics.places where uri=\'" + str(
                uri) + "\' and type=\'" + str(type) + "\' and (in_brescia=1 or in_provincia=1);")
        result = cursor.fetchone()

        place['type'] = result[0]
        place['uri'] = result[1]
        place['wikidata_id'] = result[2]
        place['in_brescia'] = result[3]
        place['in_provincia'] = result[4]
        place['has_coordinates'] = result[5]
        place['latitude'] = result[6]
        place['longitude'] = result[7]

        return place

    def get_places(self):
        places = []

        cursor = self.db.cursor()
        cursor.execute(
            "SELECT type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude FROM data_analytics.places;")

        results = cursor.fetchall()

        for result in results:
            place = dict()
            place['type'] = result[0]
            place['uri'] = result[1]
            place['wikidata_id'] = result[2]
            place['in_brescia'] = result[3]
            place['in_provincia'] = result[4]
            place['has_coordinates'] = result[5]
            place['latitude'] = result[6]
            place['longitude'] = result[7]
            places.append(place)

        return places

    def get_places(self, in_brescia,in_provincia, limit):
        places = []

        cursor = self.db.cursor()
        query="SELECT places.type, places.uri, places.wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude,  count(url) as n_articles, sentiment, sentiment_norm FROM data_analytics.places , articles_entities where in_provincia=\'"+str(in_provincia)+"\' and in_brescia=\'"+str(in_brescia)+"\'and has_coordinates=1  and articles_entities.uri = places.uri and articles_entities.type = places.type group by places.uri, places.wikidata_id order by n_articles desc limit "+str(limit)+";"

        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            place = dict()
            place['type'] = result[0]
            place['uri'] = result[1]
            place['wikidata_id'] = result[2]
            place['in_brescia'] = result[3]
            place['in_provincia'] = result[4]
            place['has_coordinates'] = result[5]
            place['latitude'] = result[6]
            place['longitude'] = result[7]
            place['n_articles'] = result[8]
            place['sentiment'] = result[9]
            place['sentiment_norm'] = result[10]
            place['surfaceForm'] = self.get_surfaceForm(result[2])
            place['uri_short'] = result[1].split("/")[-1]
            places.append(place)

        return places


    def get_best_places(self):
        places = []

        cursor = self.db.cursor()
        cursor.execute( "Select type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude, sentiment, sentiment_norm from places where in_brescia=1   order by sentiment_norm desc limit 15;")

        results = cursor.fetchall()

        for result in results:
            place = dict()
            place['type'] = result[0]
            place['uri'] = result[1]
            place['wikidata_id'] = result[2]
            place['in_brescia'] = result[3]
            place['in_provincia'] = result[4]
            place['has_coordinates'] = result[5]
            place['latitude'] = result[6]
            place['longitude'] = result[7]
            place['sentiment'] = result[8]
            place['sentiment_norm'] = result[9]
            place['surfaceForm'] = self.get_surfaceForm(result[2])
            place['uri_short'] = result[1].split("/")[-1]
            places.append(place)

        return places

    def get_worst_places(self):
        places = []

        cursor = self.db.cursor()
        cursor.execute( "Select type, uri, wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude, sentiment, sentiment_norm  from places where in_brescia=1 and sentiment_norm is not null order by sentiment_norm asc limit 15;")

        results = cursor.fetchall()

        for result in results:
            place = dict()
            place['type'] = result[0]
            place['uri'] = result[1]
            place['wikidata_id'] = result[2]
            place['in_brescia'] = result[3]
            place['in_provincia'] = result[4]
            place['has_coordinates'] = result[5]
            place['latitude'] = result[6]
            place['longitude'] = result[7]
            place['sentiment'] = result[8]
            place['sentiment_norm'] = result[9]
            place['surfaceForm'] = self.get_surfaceForm(result[2])
            place['uri_short'] = result[1].split("/")[-1]
            places.append(place)

        return places
    def get_places_filtered(self, in_brescia, in_provincia, n_citations, query_param):
        places = []
        query=""
        if(query_param!=""):
            query_param=query_param[3:]
            query = "SELECT places.type, places.uri, places.wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude,  count(url) as n_articles, sentiment, sentiment_norm FROM data_analytics.places , articles_entities where in_provincia=\'" + str(
                in_provincia) + "\' and in_brescia=\'" + str(
                in_brescia) + "\'and has_coordinates=1  and articles_entities.uri = places.uri and articles_entities.type = places.type and ("+query_param+") group by places.uri, places.wikidata_id having n_articles>" + str(
                n_citations) + ";"
        else:
            query = "SELECT places.type, places.uri, places.wikidata_id, in_brescia, in_provincia, has_coordinates, latitude, longitude,  count(url) as n_articles, sentiment, sentiment_norm FROM data_analytics.places , articles_entities where in_provincia=\'" + str(
                in_provincia) + "\' and in_brescia=\'" + str(
                in_brescia) + "\'and has_coordinates=1  and articles_entities.uri = places.uri and articles_entities.type = places.type group by places.uri, places.wikidata_id having n_articles>" + str(
                n_citations) + ";"

        cursor = self.db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            place = dict()
            place['type'] = result[0].replace('\'','%27')
            place['uri'] = result[1]
            place['wikidata_id'] = result[2]
            place['in_brescia'] = result[3]
            place['in_provincia'] = result[4]
            place['has_coordinates'] = result[5]
            place['latitude'] = result[6]
            place['longitude'] = result[7]
            place['n_articles'] = result[8]
            place['sentiment'] = result[9]
            place['sentiment_norm'] = result[10]
            place['uri_short'] = result[1].split("/")[-1]
            places.append(place)

        return places

    def get_places_with_surfaceForm(self):
        #Create a dict with saved places
        cursor = self.db.cursor()
        query = "Select places.uri, places.type, surfaceForm from places, articles_entities where places.type = articles_entities.type and (places.in_brescia=1 or places.in_provincia=1) and places.uri = articles_entities.uri group by uri;"
        cursor.execute(query)
        results = cursor.fetchall()

        places = []
        for row in results:
            place = dict()
            place['uri'] = row[0].encode('utf-8').replace('\"', '\\\"').replace('\'','\\\'')
            place['type'] = row[1].encode('utf-8')
            place['surfaceForm'] = row[2].encode('utf-8')
            places.append(place)

        return places

    def get_surfaceForm(self, wikidata_id):
        cursor = self.db.cursor()
        query = "select surfaceForm, count(*) as n from articles_entities where wikidata_id = 'Q255375' group by surfaceForm order by n desc limit 1"
        cursor.execute(query)
        row=cursor.fetchone()
        surfaceForm=row[0]

        return surfaceForm

    def get_articles_token(self, uri, type):
        output=dict()
        articles = []
        surfaceForms=[]

        cursor = self.db.cursor()
        cursor.execute(
            "select distinct articles.article_token, url, articles_entities.surfaceForm from articles, articles_entities where articles.url=articles_entities.url and  uri=\'"+str(uri)+"\' and type=\'"+str(type)+"\';")
        results = cursor.fetchall()

        for result in results:
            article = dict()

            article['token'] = result[0]
            article['url'] = result[1]
            articles.append(article)
            if result[2] not in surfaceForms:
                surfaceForms.append(result[2])

        output['articles']=articles
        output['surfaceForms']=surfaceForms

        return output

    def get_entities_count(self, limit):
        entities = []

        cursor = self.db.cursor()
        query="select count(url) as n, entities.uri from entities, articles_entities where entities.wikidata_id= articles_entities.wikidata_id and  entities.type= articles_entities.type AND NOT EXISTS (SELECT 1  FROM PLACES P WHERE entities.URI = P.URI) group by entities.uri order by n desc limit "+str(limit)+";"
        cursor.execute(query)
        results=cursor.fetchall()

        for row in results:
            entity=dict()
            entity['uri_short']=row[1].split("/")[-1]
            entity['uri'] = row[1]
            entity['count'] = row[0]

            entities.append(entity)

        return entities

    def set_places_aggregated_type(self):

        queries=[]

        queries.append("Update places  set  aggregated_type = \'elemento stradale\' where type = \'via\' or type = \'corso\' or type = \'viale\' or type = \'piazza\' or type = \'piazzetta\' or type = \'cavalcavia\' or type = \'piazzale\' or type = \'galleria\' or type = \'contrada\';")

        queries.append("Update places set aggregated_type = \'sede scolastica/culturale\' where type = \'biblioteca\' or type = \'liceo classico' or type = \'teatro\' or type = \'università\';")

        queries.append("Update places set aggregated_type = \'luogo turistico/monumento\' where type = \'castello\' or type = \'museo' or type = \'museo d\\'arte\' or type = \'scultura\' or type = \'sito archeologico\' or uri = \'http://it.wikipedia.org/wiki/Palazzo_Bettoni_Cazzago\';")

        queries.append("Update places set aggregated_type = \'edificio religioso\' where  type = \'chiesa\' or type = \'concattedrale\' or type = \'monastero\' or type = \'cimitero\';")

        queries.append("Update places set aggregated_type = \'suddivisione cittadina\' where type = \'insediamento umano\' or type = \'sobborgo\' or type = \'quartiere di Brescia\' or type = \'frazione\';")

        queries.append("Update places set aggregated_type = \'edificio civile\' where type = \'chiesa sconsacrata\' or type = \'edificio\' or type = \'grattacielo\' or type = \'torre\';")

        queries.append("Update places set aggregated_type = \'fermata tpl\' where type = \'rete di metropolitane\' or type = \'stazione ferroviaria\';")

        queries.append("Update places set aggregated_type = \'edificio sportivo\' where type = \'stadio di calcio\';")

        queries.append("Update places set aggregated_type = \'edificio sanitario\' where type = \'ospedale\';")

        queries.append("Update places set  aggregated_type = \'edificio amministrativo\' where type = 'broletto' or uri = 'http://it.wikipedia.org/wiki/Palazzo_della_Loggia';")

        for query in queries:
            cursor = self.db.cursor()
            cursor.execute(query)

        self.db.commit()
        print("Set aggregated type for places of the city")

    def set_articles_dates(self):

        years=['2018','2017','2016','2015','2014','2013','2012','2011']

        months=['gen','feb','mar','apr','mag','giu','lug','ago','sett','ott','nov','dic']

        for year in years:
            cursor = self.db.cursor()
            query="update articles, results set articles.year=\'"+str(year)+"\' where articles.url=results.url and results.date like '%"+str(year)+"%'"
            cursor.execute(query)
        print("Set year for articles")

        for month in months:
            cursor = self.db.cursor()
            query="update articles, results set articles.month=\'"+str(months.index(month)+1)+"\' where articles.url=results.url and results.date like '%"+str(month)+"%'"
            cursor.execute(query)
        print("Set month for articles")

        self.db.commit()


