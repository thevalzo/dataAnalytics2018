
import requests
import MySQLdb
import unidecode
import re

from xml.dom import minidom

db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics")
#LAST 22892
#Retrive all articles
cursor = db.cursor()
cursor.execute("select articles.idArticle, articles.article from articles where articles.idArticle not in (select DISTINCT articles.idArticle from articles,entities where articles.idArticle = entities.idArticle ) and articles.tooLong=0;")
results = cursor.fetchall()
print(" **Loading from DB done**")
for row in results:

    idArticle=row[0]
    text=str(row[1]).replace('#','')
    confidence="0.8"

    # Make a request for every article
    print(" ** Send request for article "+str(idArticle)+" **")
    url="https://api.dbpedia-spotlight.org/en/annotate?"+"text="+text+"&confidence="+confidence
    #print(url)
    r = requests.get(url=url)
    text=r.text
    print(text)


    if(r.text[:6] == "<html>"):

        # If the service return the html message "data too long" skip article and annotate it
        print(" ** Article " + str(idArticle) + " is too long for DBPedia api **")
        cursor = db.cursor()
        cursor.execute("UPDATE articles SET tooLong=1 where idArticle=\'" + str(idArticle)+ "\';")
        db.commit()
    else:
        text = filter(lambda x: not re.match(r"&#([0-9]+);|&#x([0-9a-fA-F]+);", x), text)
        text=text.replace('&#2;','')
        print(text)
        #If the aswer is correct, parse the xml code and extract values
        xmldoc = minidom.parseString(text.encode("utf-8"))
        resources=xmldoc.getElementsByTagName('Resource')

        if(resources.__len__()==0):
            #tooLong is set at error value 2 when article has no enitities
            print(" ** Article " + str(idArticle) + " has no entities for DBPedia api **")
            cursor = db.cursor()
            cursor.execute("UPDATE articles SET tooLong=2 where idArticle=\'" + str(idArticle) + "\';")
            db.commit()

        for element in resources:

            #extract values of every ne/concept found
            URI = element.attributes['URI'].value.replace('\"', '\\\"').replace('\'','\\\'')
            similarityScore = element.attributes['similarityScore'].value
            surfaceForm = element.attributes['surfaceForm'].value.replace('\"', '\\\"').replace('\'','\\\'')
            types = element.attributes['types'].value.replace('\"', '\\\"').replace('\'','\\\'')
            offset= element.attributes['offset'].value

            #check if the entities has been already iserted
            cursor = db.cursor()
            query = "SELECT uri, idArticle, offset FROM entities " \
                    "WHERE uri =\'" + str(URI.encode("utf-8")) + "\' AND idArticle=\'" + str(idArticle) + "\'AND offset=\'" + str(offset) + "\';"
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
