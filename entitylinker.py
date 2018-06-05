# -*- coding: utf-8 -*-
import requests
from urllib import urlencode
import MySQLdb
import json

class EntityLinker:

    db=[]
    access_token=""

    def __init__(self):

        # Set up db connection
        self.db = MySQLdb.connect(   host="127.0.0.1",
                                user="root",
                                passwd="root",
                                db="data_analytics",
                                charset = 'utf8')

        #Extract access token from DB
        cursor = self.db.cursor()
        cursor.execute("SELECT access_token from credentials where service = 'Dandelion'")
        result=cursor.fetchone()
        self.access_token=result[0]

    def dandelify(self):

        # Retrive all articles we want to do NERL
        cursor = self.db.cursor()
        cursor.execute("select articles.url, articles.article_clean from articles, results where articles.url=results.url and results.keyword='città' and articles.url not in "
                       "(select entities.url from entities where entities.source='Dandelion') limit 10;")
        results = cursor.fetchall()
        print(" **Loading from DB done**")

        #Build the request for Dandelion API
        url = "https://api.dandelion.eu/datatxt/nex/v1/"

        for row in results:
            text = str(row[1].encode('utf8')).replace('#', '')
            text= text[:3489]
            article = str(row[0])

            print(" ** Send request for article " + str(article) + " **")

            r = requests.get(url=url, params={'token': self.access_token, 'lang': 'it', 'text': text})
            r.encoding = 'utf-8'
            text = r.text

            #extract every resource found
            jsonresponse = json.loads(text)
            if 'annotations' in jsonresponse:
                resources=jsonresponse['annotations']
                for resource in resources:

                    URI = resource['uri'].replace('\"', '\\\"').replace('\'', '\\\'').encode("utf8")
                    confidence = resource['confidence']
                    surfaceForm = resource['spot'].replace('\"', '\\\"').replace('\'','\\\'').encode("utf8")
                    offset = resource['start']

                    #Save entities in the DB
                    cursor = self.db.cursor()
                    query = "INSERT INTO entities(uri, url, source, surfaceForm, confidence, offset)" \
                            " VALUES  (\'" + str(URI) + "\', \'" + str(article) + "\', \'Dandelion\', \'" + str(surfaceForm) + "\', \'" + str(confidence) + "\',  \'" + str(offset) + "\');"
                    cursor.execute(query)
                    self.db.commit()

                print(" ** Inserted " + str(resources.__len__()) + " entities for article " + str(article) + " **")

            elif 'error' in jsonresponse:
                print(" ** "+jsonresponse['code']+" : "+jsonresponse['message']+" ** ")
            else:
                print(" ** Article " + str(article) + " has no entities for Dandelion api **")

    def search_roads(self):

        #We want to recognize roads, places ecc entitles to Named Entities
        via_count = 0
        corso_count = 0
        viale_count = 0
        villaggio_count = 0
        piazza_count = 0
        piazzetta_count = 0
        cavalcavia_count = 0
        piazzale_count = 0
        galleria_count = 0

        #Extract saved named entities and articles where entities has been found
        cursor = self.db.cursor()
        cursor.execute("select articles.url, articles.article_clean, entities.offset,entities.uri, entities.surfaceForm from articles, entities, results where articles.url=results.url and articles.url=entities.url and results.keyword='città' limit 10000;")
        results = cursor.fetchall()


        for row in results:
            url = row[0]
            article = row[1]
            offset = row[2]
            uri= row[3]
            surfaceForm = row[4].replace('\"', '\\\"').replace('\'','\\\'').encode("utf8")

            #for every entities check if in the article is preceded by a place prefix
            if(not (surfaceForm=="e-mail" or surfaceForm=='WhatsApp' or surfaceForm=="email")):
                type="none"
                place_offset=0
                offset_end=offset+surfaceForm.__len__()

                if(article[offset-4:offset]=="via "):
                    #print(url+" : "+uri + " = " +article[offset-4:offset_end])
                    type="via"
                    place_offset=offset-4
                    via_count+=1

                elif (article[offset - 6:offset] == "corso "):
                    #print(url+" : "+uri + " = " + article[offset - 6:offset_end])
                    type="corso"
                    place_offset=offset-6
                    corso_count += 1

                elif (article[offset - 7:offset] == "piazza "):
                    #print(url+" : "+uri + " = " + article[offset - 7:offset_end])
                    type="piazza"
                    place_offset=offset-7
                    piazza_count += 1

                elif (article[offset - 6:offset] == "viale "):
                    #print(url+" : "+uri + " = " + article[offset - 6:offset_end])
                    type="viale"
                    place_offset=offset-6
                    viale_count += 1

                elif (article[offset - 10:offset] == "villaggio "):
                    # print(url+" : "+uri + " = " + article[offset - 10:offset_end])
                    type = "villaggio"
                    place_offset = offset - 10
                    villaggio_count += 1

                elif (article[offset - 11:offset] == "cavalcavia "):
                    #print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type="cavalcavia"
                    place_offset=offset-11
                    cavalcavia_count += 1

                elif (article[offset - 9:offset] == "piazzale "):
                    #print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type="piazzale"
                    place_offset=offset-9
                    piazzale_count += 1

                elif (article[offset - 10:offset] == "piazzetta "):
                    #print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type="piazzetta"
                    place_offset=offset-10
                    piazzetta_count += 1

                elif (article[offset - 9:offset] == "galleria "):
                    #print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type="galleria"
                    place_offset=offset-9
                    galleria_count += 1


                if(type!="none"):
                    # Check for already inserted places
                    cursor = self.db.cursor()
                    query = "SELECT uri, url, type, offset, surfaceForm from places WHERE url =\'" + url.encode('utf8') + "\' AND type=\'" + str(type) + "\'AND offset=\'" + str(place_offset) + "\'AND surfaceForm=\'" + surfaceForm + "\';"

                    cursor.execute(query)
                    cursor.fetchall()

                    if (cursor.rowcount == 0):
                        # Insert place
                        cursor = self.db.cursor()
                        query = "INSERT INTO places(uri, url, type, offset, surfaceForm)" \
                                " VALUES  (\'" + str(uri) + "\', \'" + url.encode('utf8') + "\', \'" + str(type) + "\', \'" + str(place_offset) + "\', \'" + surfaceForm + "\');"

                        cursor.execute(query)
                        self.db.commit()

        print("Founded: \n"
            +str(via_count)+" vie \n"
            +str(corso_count)+" corsi \n"
            +str(viale_count)+" viali \n"
            +str(villaggio_count)+" villaggio \n"
            +str(piazza_count)+" piazze \n"
            +str(piazzetta_count) + " piazzette \n"
            +str(piazzale_count) + " piazzali \n"
            +str(cavalcavia_count)+" cavalcavia \n"
            +str(galleria_count) + " gallerie \n")

            #Future adds: contrada, corsetto, piazzetta, spalto, strada privata

    def get_places(self):
        #Create a dict with saved places
        cursor = self.db.cursor()
        query = "Select uri, type, surfaceForm from places group by uri;"
        cursor.execute(query)
        results = cursor.fetchall()

        places = []
        for row in results:
            place = dict()
            place['uri'] = row[0]
            place['type'] = row[1]
            place['surfaceForm'] = row[2]
            places.append(place)

        return places


