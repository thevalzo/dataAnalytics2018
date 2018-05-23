
import requests
import MySQLdb
import unidecode

from xml.dom import minidom
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = MongoClient("127.0.0.1:27017")
#db=client.admin
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)


db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics")

#Retrive all articles
cursor = db.cursor()
cursor.execute("SELECT idarticle, article  from articles;")
results = cursor.fetchall()

for row in results:

    idArticle=row[0]
    text=str(row[1])
    confidence="0.8"

    #Make a request for every article
    r = requests.get(url="https://api.dbpedia-spotlight.org/en/annotate?"+"text="+text+"&confidence="+confidence)
    #print(r.text)


    if(r.text[:6] == "<html>"):

        # If the service return the html message "data too long" skip article and annotate it
        cursor = db.cursor()
        cursor.execute("UPDATE articles SET tooLong=1 where idArticle=\'" + str(idArticle)+ "\';")
        db.commit()
    else:

        #If the aswer is correct, parse the xml code and extract values
        xmldoc = minidom.parseString(r.text.encode("utf-8") )
        resources=xmldoc.getElementsByTagName('Resource')
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
            print(query)
            cursor.execute(query)
            cursor.fetchall()
            if (cursor.rowcount == 0):

                #if the entities are new, insert thme into the db
                cursor = db.cursor()
                query = "INSERT INTO entities(uri, idArticle, source, similarityScore, surfaceForm, types, confidence, offset)" \
                        " VALUES  (\'" + URI + "\', \'" + str(idArticle) + "\', \'DBPedia_Spotlight\', \'" + str(similarityScore) + "\', \'" + surfaceForm + "\', \'" + types + "\', \'" + str(confidence) + "\', \'" + str(offset) + "\');"
                results = cursor.execute(query)
                print("Inserted entities for article " + str(idArticle))

            else:
                print("already have entities for article " + str(idArticle))
                break
        db.commit()
