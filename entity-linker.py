# -*- coding: utf-8 -*-
import requests
from urllib import urlencode
import MySQLdb
import unidecode
import re

from xml.dom import minidom

db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                    charset = 'utf8')
#LAST 22892
#Retrive all articles
cursor = db.cursor()
cursor.execute("select articles.idArticle, articles.article from articles where articles.idArticle not in "
               "(select DISTINCT articles.idArticle from articles,entities where articles.idArticle = entities.idArticle ) and articles.tooLong=0;")
results = cursor.fetchall()
print(" **Loading from DB done**")


for row in results:

    idArticle=row[0]
    text=str(row[1].encode('utf8')).replace('#','')
    confidence="0.8"

    # Make a request for every article
    print(" ** Send request for article "+str(idArticle)+" **")
    params=urlencode({'text': text, 'confidence':confidence})
    url="https://api.dbpedia-spotlight.org/en/annotate?"+params
    r = requests.get(url=url)
    r.encoding = 'utf-8'
    text=r.text

    if(text[:6] == "<html>" or text[:14] == "<!DOCTYPE HTML"):

        # If the service return the html message "data too long" skip article and annotate it
        print(" ** Article " + str(idArticle) + " is too long for DBPedia api **")
        cursor = db.cursor()
        cursor.execute("UPDATE articles SET tooLong=1 where idArticle=\'" + str(idArticle)+ "\';")
        db.commit()
    else:
        text = filter(lambda x: not re.match(r"&#([0-9]+);|&#x([0-9a-fA-F]+);", x), text)
        text=text.replace('&#2;','')

        #If the aswer is correct, parse the xml code and extract values
        xmldoc = minidom.parseString(text)
        resources=xmldoc.getElementsByTagName('Resource')

        if(resources.__len__()==0):
            #tooLong is set at error value 2 when article has no enitities
            print(" ** Article " + str(idArticle) + " has no entities for DBPedia api **")
            cursor = db.cursor()
            cursor.execute("UPDATE articles SET tooLong=2 where idArticle=\'" + str(idArticle) + "\';")
            db.commit()

        for element in resources:

            #extract values of every ne/concept found
            URI = element.attributes['URI'].value.replace('\"', '\\\"').replace('\'','\\\'').encode("utf8")
            similarityScore = element.attributes['similarityScore'].value
            surfaceForm = element.attributes['surfaceForm'].value.replace('\"', '\\\"').replace('\'','\\\'').encode("utf8")
            types = element.attributes['types'].value.replace('\"', '\\\"').replace('\'','\\\'').encode("utf8")
            offset= element.attributes['offset'].value

            #check if the entities has been already iserted
            cursor = db.cursor()
            query = "SELECT uri, idArticle, offset FROM entities " \
                    "WHERE uri =\'" + str(URI) + "\' AND idArticle=\'" + str(idArticle) + "\'AND offset=\'" + str(offset) + "\';"
            cursor.execute(query)
            cursor.fetchall()

            if (cursor.rowcount == 0):

                #if the entities are new, insert thme into the db
                cursor = db.cursor()
                query = "INSERT INTO entities(uri, idArticle, source, similarityScore, surfaceForm, types, confidence, offset)" \
                        " VALUES  (\'" + URI + "\', \'" + str(idArticle) + "\', \'DBPedia_Spotlight\', \'" + str(similarityScore) + "\', \'" + surfaceForm + "\', \'" + types + "\', \'" + str(confidence) + "\', \'" + str(offset) + "\');"
                results = cursor.execute(query)


            else:
                print(" ** Already have entities for article " + str(idArticle)+" **")
                break
        print(" ** Inserted "+str(resources.__len__())+" entities for article " + str(idArticle) + " **")
        db.commit()
