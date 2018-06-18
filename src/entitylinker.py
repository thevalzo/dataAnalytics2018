# -*- coding: utf-8 -*-
import requests
import MySQLdb
import json
import urllib
from geopy.geocoders import Nominatim

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
        cursor.execute("select articles.url, articles.article_clean from articles where articles.url not in "
                       "(select articles_entities.url from articles_entities where source='Dandelion');")
        results = cursor.fetchall()
        print(" **Loading from DB done**")

        #Build the request for Dandelion API
        url = "https://api.dandelion.eu/datatxt/nex/v1/"

        for row in results:
            article_url = str(row[0])
            text = str(row[1].encode('utf8')).replace('#', '')
            text= text[:3489]


            print(" ** Send request for article " + str(article_url) + " **")

            r = requests.get(url=url, params={'token': self.access_token, 'lang': 'it', 'text': text})
            r.encoding = 'utf-8'
            text = r.text
            resources_count=0
            #extract every resource found
            jsonresponse = json.loads(text)
            if 'annotations' in jsonresponse:
                resources=jsonresponse['annotations']
                for resource in resources:
                    resources_count=resources.__len__()
                    URI = urllib.unquote(resource['uri'].encode("utf8")).replace('\"', '\\\"').replace('\'', '\\\'')
                    confidence = resource['confidence']
                    surfaceForm = resource['spot'].encode("utf8").replace('\"', '\\\"').replace('\'','\\\'')
                    offset = resource['start']

                    #Save entities in the DB
                    cursor = self.db.cursor()
                    query = "INSERT INTO articles_entities(uri, url, source, surfaceForm, confidence, offset, type)" \
                            " VALUES  (\'" + URI + "\', \'" + str(article_url) + "\', \'Dandelion\', \'" + str(surfaceForm) + "\', \'" + str(confidence) + "\',  \'" + str(offset) + "\' , 'generic_entity');"
                    cursor.execute(query)

                    cursor = self.db.cursor()
                    query = "SELECT * FROM entities WHERE uri=\'" + URI + "\' and type=\'generic_entity\';"
                    cursor.execute(query)

                    if(cursor.rowcount==0):
                        cursor = self.db.cursor()
                        query = "INSERT INTO entities(uri, type, checked)" \
                                " VALUES  (\'" + URI + "\', 'generic_entity', '0');"
                        cursor.execute(query)
                    else:
                        print(" ** Resource "+URI+" was already in DB**")
                        resources_count-=1

                    self.db.commit()

                print(" ** Inserted " + str(resources_count) + " new entities for article " + str(article) + " **")

            elif 'error' in jsonresponse:
                print(" ** "+jsonresponse['code']+" : "+jsonresponse['message']+" ** ")
            else:
                print(" ** Article " + str(article) + " has no entities for Dandelion api **")

    def set_wd_ids_entities(self, limit):

        #Extract entities from DB
        cursor = self.db.cursor()
        query = "select uri from (select entities.uri, count(url) as num from entities, articles_entities where entities.uri=articles_entities.uri and entities.uri like '%wikipedia%' and  entities.wikidata_id is null group by uri having num>"+str(limit)+" order by num desc) as n;"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            #For every entity save wikipedia url and wikipedia page name
            uri=row[0].encode('utf-8')
            page_name = row[0].split("/")[-1]
            page_name = page_name.encode('utf-8')

            #use wikiWrapper to get the wiki_id of the page
            wiki = WikiWrapper()
            response=wiki.get_wiki_id(page_name)
            print(response['message'])

            #If the response is positive insert the value
            if(response['code']==200):
                #Save extracted id
                cursor = self.db.cursor()
                query = "update entities set wikidata_id=\'"+str(response['wd_id'])+"\' where uri=\'"+str(uri).replace('\"', '\\\"').replace('\'','\\\'')+"\';"
                cursor.execute(query)

                cursor = self.db.cursor()
                query = "update articles_entities, entities set articles_entities.wikidata_id = entities.wikidata_id where articles_entities.uri = entities.uri;"
                cursor.execute(query)
                self.db.commit()

    def detect_places(self):

        # Extract entities from DBplaces
        cursor = self.db.cursor()
        query = "select entities.wikidata_id, entities.uri, similarityScore, surfaceForm, source, confidence, offset, url from entities, articles_entities where entities.uri like '%wikipedia%' and checked=FALSE and  entities.wikidata_id is not null limit 1000;"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:

            wd_id=row[0]
            uri=row[1].encode('utf-8')

            # use wikiWrapper to get info on one entity: is it a place?
            wiki = WikiWrapper()
            response=wiki.get_place_info(wd_id)

            print("Checked element " + uri )

            if(response['in_provincia']==1 or response['in_brescia']==1 or response['has_coordinates']==1):
                # Insert info for the entity
                cursor = self.db.cursor()
                query = "INSERT INTO places (wikidata_id, type, uri, in_brescia, in_provincia, has_coordinates, latitude, longitude) " \
                        "VALUES (\'" + str(wd_id) + "\', 'generic_entity', \'" + str(uri).replace('\"', '\\\"').replace('\'','\\\'') + "\',\'" + str(response['in_brescia']) + "\',\'" + str(response['in_provincia']) + "\', \'" + str(response['has_coordinates']) + "\',\'" + str(response['latitude']) + "\',\'" + str(response['longitude']) + "\') ;"
                cursor.execute(query)

                print("Inserted element " + uri + " :\n is in Brescia:" + str(response['in_brescia']) + "\n is in Provincia:" + str(
                response['in_provincia']) + "\n has coordinates:" + str(response['has_coordinates']) + " - " + str(response['latitude']) + " - " + str(
                response['longitude']) + "\n")

            #check the entity to not repeat the same task
            cursor = self.db.cursor()
            query = "UPDATE entities SET checked=TRUE WHERE wikidata_id= \'" + wd_id + "\';"
            cursor.execute(query)
            self.db.commit()

    def correct_places(self):

        # Select the entities where the url end like "place_in_more_cities_(not_in_brescia)"
        cursor = self.db.cursor()
        query = "select uri from places where uri like '%(%)%' and uri not like '%(Brescia)%' and has_coordinates=1 and in_brescia=0 and in_provincia=0 and checked=0;"
        cursor.execute(query)
        results = cursor.fetchall()

        url = 'https://it.wikipedia.org/w/api.php'
        wiki_url = 'https://it.wikipedia.org/wiki/'

        for row in results:
            uri = row[0]

            # get the last part of the url string
            page_name = row[0].split("/")[-1]
            page_name = page_name.encode('utf-8')

            # split the string to replace the word between parethesis with Brescia
            page_name_split = page_name.split('(')
            part1 = page_name_split[0]
            part2 = page_name_split[1].split(')')[1]
            page_with_brescia = part1 + "(Brescia)" + part2

            # check if uri exist
            new_uri = 'http://it.wikipedia.org/wiki/' + page_with_brescia.replace('\"', '\\\"').replace('\'', '\\\'')

            wiki = WikiWrapper()
            response = wiki.get_wiki_id(page_with_brescia)
            print(response['message'])

            # If the response is positive insert the value
            if (response['code'] == 200):
                wd_id=response['wd_id']
                print(part1 + " item is in Brescia with id " + str(wd_id))

                # insert a new annotation on the same position of the old one
                cursor = self.db.cursor()
                query = "insert into articles_entities select '" + new_uri + "', type, '" + wd_id + "', similarityScore, surfaceForm, source, confidence, offset, url from articles_entities where uri = \'" + uri.replace(
                    '\"', '\\\"').replace('\'', '\\\'') + "\';"
                cursor.execute(query)

                #set the old place checked to not check it again
                cursor = self.db.cursor()
                query = "update places set  checked=1 where uri = \'" + uri.replace('\"', '\\\"').replace(
                    '\'', '\\\'') + "\';"
                cursor.execute(query)

                #self.db.commit()

                # check if the annotated place already exists
                cursor = self.db.cursor()
                query = "select * from places where uri = '" + new_uri + "';"
                cursor.execute(query)

                if (cursor.rowcount == 0):

                    # if not exists has to be created
                    response1 = wiki.get_wiki_id(page_with_brescia)
                    print(response1['message'])

                    if (response1['code'] == 200):
                        wd_id1 = response1['wd_id']
                        response = wiki.get_place_info(wd_id1)

                        # Insert info for the new entity
                        cursor = self.db.cursor()
                        query = "INSERT INTO places (wikidata_id, type, uri, in_brescia, in_provincia, has_coordinates, latitude, longitude) " \
                                "VALUES (\'" + str(
                            wd_id1) + "\', 'generic_entity', \'" + new_uri + "\',\'" + str(
                            response['in_brescia']) + "\',\'" + str(
                            response['in_provincia']) + "\', \'" + str(
                            response['has_coordinates']) + "\',\'" + str(
                            response['latitude']) + "\',\'" + str(
                            response['longitude']) + "\') ;"
                        cursor.execute(query)
                        self.db.commit()
                else:
                    print(new_uri + " was already saved")
            else:
                print(part1 + " item is not in Brescia")

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
        torre_count = 0
        contrada_count = 0

        #Extract saved named entities and articles where entities has been found
        cursor = self.db.cursor()
        cursor.execute("select articles.url, articles.article_clean, articles_entities.offset, articles_entities.uri, articles_entities.surfaceForm from articles, articles_entities where articles.url=articles_entities.url;")
        results = cursor.fetchall()


        for row in results:
            url = row[0].encode("utf8").replace('\"', '\\\"').replace('\'','\\\'')
            article = row[1]
            offset = row[2]
            uri= row[3].encode("utf8").replace('\"', '\\\"').replace('\'','\\\'')
            surfaceForm = row[4].encode("utf8").replace('\"', '\\\"').replace('\'','\\\'')

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

                elif (article[offset - 6:offset] == "torre "):
                    # print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type = "torre"
                    place_offset = offset - 6
                    torre_count += 1

                elif (article[offset - 9:offset] == "contrada "):
                    # print(url+" : "+uri + " = " + article[offset - 11:offset_end])
                    type = "contrada"
                    place_offset = offset - 9
                    contrada_count += 1

                if(type!="none"):
                    # Check for already inserted places
                    cursor = self.db.cursor()
                    query = "SELECT uri, similarityScore, source, confidence, offset, url from articles_entities WHERE url =\'" + url.encode('utf8') + "\' AND offset=\'" + str(offset) + "\' AND  uri=\'" + str(uri) + "\'AND type='" + str(type) + "';"
                    cursor.execute(query)
                    cursor.fetchone()

                    #Update all the references
                    if (cursor.rowcount == 0):
                        #select all the old references
                        cursor = self.db.cursor()
                        query = "SELECT similarityScore, source, confidence, wikidata_id from articles_entities WHERE url =\'" + url.encode(
                            'utf8') + "\' AND uri=\'" + str(uri) + "\'AND offset=\'" + str(offset) + "\' AND surfaceForm=\'" + str(surfaceForm) + "\'AND type='generic_entity';"
                        cursor.execute(query)
                        results = cursor.fetchall()


                        for row in results:
                            # create new references
                            similarityScore = row[0]
                            source = row[1]
                            confidence = row[2]
                            wd_id = row[3]

                            cursor = self.db.cursor()
                            query = "INSERT INTO articles_entities(uri, url, type, offset, surfaceForm, source, confidence, wikidata_id)" \
                                    " VALUES  (\'" + uri.decode('utf8') + "\', \'" + url.decode('utf8') + "\', \'" +    type.decode('utf8') + "\', \'" + str(offset) + "\', \'" + surfaceForm.decode('utf8') + "\' , \'" + source.decode('utf8') + "\' , \'" + str(confidence) + "\', \'" + str(wd_id)+ "\');"
                            cursor.execute(query)

                        # Check if the place already exists
                        cursor = self.db.cursor()
                        query = "SELECT * FROM places WHERE uri =\'" + uri + "\' AND type=\'" + str(type) + "\';"
                        cursor.execute(query)
                        cursor.fetchone()

                        if (cursor.rowcount == 0):
                            # Insert new place
                            cursor = self.db.cursor()
                            query = "INSERT INTO places(uri, type, wikidata_id)" \
                                    " VALUES  (\'" + uri + "\', \'" + str(type) + "\', \'" + str(wd_id) + "\');"

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
            +str(galleria_count) + " gallerie \n"
            +str(torre_count) + " torri \n"
            + str(contrada_count) + " torri \n"
              )

            #Future adds: contrada, corsetto, piazzetta, spalto, strada privata

    def set_places_type(self):

        # Extract from db places with basic label
        cursor = self.db.cursor()
        query = "select wikidata_id, uri from places where wikidata_id is not NULL and type='generic_entity';"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            # For every entity save wikipedia url and wikipedia page name
            wd_id = row[0]
            uri = row[1].encode('utf-8').replace('\"', '\\\"').replace('\'','\\\'')

            #ask to wikipedia for place's type
            wiki = WikiWrapper()
            response = wiki.get_place_type(wd_id)


            if (response['code'] == 200):
                #if exists save tipe
                type=response['value'].encode('utf-8').replace('\"', '\\\"').replace('\'','\\\'')
                cursor = self.db.cursor()
                query = "update places set type=\'" + str(type) + "\' where wikidata_id=\'" + str(wd_id) + "\' and type='generic_entity';"
                cursor.execute(query)

                print(" Updated "+str(uri)+" with new label : " +str(type))

        cursor = self.db.cursor()
        query = "update articles_entities, places set articles_entities.type = places.type where articles_entities.uri = places.uri and" \
                " articles_entities.type='generic_entity'and places.type!='via' and places.type!='contrada' and places.type!='piazza' and places.type!='corso'" \
                " and places.type!='piazzetta' and places.type!='viale'  and places.type!='villaggio' and places.type!='piazzale' and places.type!='torre' and places.type!='galleria';"
        cursor.execute(query)
        self.db.commit()

    def set_roads_coordinates(self):
        # Extract roads from db
        cursor = self.db.cursor()
        query = "select distinct articles_entities.uri, articles_entities.surfaceForm, articles_entities.type from articles_entities where type='via' or type='corso' or type='viale' or type='piazza' or type='piazzetta' or type='cavalcavia' or type='piazzale' or type='galleria' or type='contrada';"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            uri=row[0].replace('\"', '\\\"').replace('\'','\\\'')
            surfaceForm=row[1]
            type=row[2]

            #compose adress string
            address=type+" "+surfaceForm+", Brescia, BS, 25121"
            print(address)
            #calculate location
            geolocator = Nominatim()
            location = geolocator.geocode(address, timeout=10)

            #check if location in city or provincia
            if(location):

                in_brescia = 0
                in_provincia = 0
                if("Brescia" in location.address):
                    in_brescia=1
                else:
                    in_provincia=1

                #update places
                cursor = self.db.cursor()
                query = "update places set has_coordinates=1, latitude=\'"+str(location.longitude)+"\', longitude=\'"+str(location.latitude)+"\', in_brescia=\'"+str(in_brescia)+"\', in_provincia=\'"+str(in_provincia)+"\' where type=\'"+type+"\' and uri=\'"+uri+"\';"
                cursor.execute(query)
                self.db.commit()

                print(" ** updated places "+type+" "+surfaceForm+" with coordinates "+ str(location.latitude)+" , "+str(location.longitude))

class WikiWrapper:

    def get_wiki_id(self, page_name):

        url='https://it.wikipedia.org/w/api.php'
        response=dict()

        # send request to wikipedia for wikidata id
        r = requests.get(url=url,
                         params={'action': 'query', 'prop': 'pageprops', 'format': 'json', 'titles': page_name})
        r.encoding = 'utf-8'
        text = r.text
        jsonresponse = json.loads(text)

        # parse jsonresponse
        if 'query' in jsonresponse:
            query = jsonresponse['query']
            pages = query['pages']
            for page in pages:
                page = pages[page]
                if 'pageprops' in page:
                    pageprops = page['pageprops']
                    if 'wikibase_item' in pageprops:
                        wikidata_id = pageprops['wikibase_item']
                        response['code'] = 200
                        message = "updated entity " + str(page_name) + " with id " + str(wikidata_id)
                        response['message'] = message
                        response['wd_id'] = wikidata_id
                    else:
                        response['code'] = 401
                        message=str(page) + " is not a wikibase item"
                        response['message'] = message
                else:
                    response['code'] = 402
                    message = "non trovo l'id in " + str(page)
                    response['message'] = message

        return response

    def get_place_info(self, wd_id):

        url = 'https://query.wikidata.org/sparql'
        response = dict()

        # situati nel comune
        query = "ASK  { wd:" + wd_id + " wdt:P131 wd:Q6221 }"
        r = requests.get(url=url, params={'query': query, 'format': 'json'})
        r.encoding = 'utf-8'

        json_r = json.loads(r.text)
        if (json_r['boolean'] == True):
            response['in_brescia'] = 1
        else:
            response['in_brescia'] = 0

        # situati nella provincia
        query = "ASK  { wd:" + wd_id + " wdt:P131 wd:Q16144}"
        r = requests.get(url=url, params={'query': query, 'format': 'json'})
        r.encoding = 'utf-8'

        json_r = json.loads(r.text)
        if (json_r['boolean'] == True):
            response['in_provincia'] = 1
        else:
            response['in_provincia'] = 0

        # print(" Uri "+str(uri)+" is in provincia? "+str(in_provincia))

        # situato geograficamente
        query = "SELECT ?o WHERE { wd:" + wd_id + " wdt:P625 ?o }"
        # send request to wikipedia for wikidata id
        r = requests.get(url=url, params={'query': query, 'format': 'json'})
        r.encoding = 'utf-8'
        json_r = json.loads(r.text)
        # print(" uri " + uri+" ha coordinate "+str(json_r))

        has_coordinates = 0
        latitude = 0
        longitude = 0

        results = json_r['results']
        bindings = results['bindings']
        if 'element' in bindings:

            response['has_coordinates'] = 1

            for element in bindings:
                o = element['o']
                coordinates = str(o['value'])
                len_1 = coordinates.__len__() - 1
                coordinates = coordinates[6:len_1]
                coordinates = coordinates.split()

                response['latitude'] = coordinates[0]
                response['longitude'] = coordinates[1]

        else:
            response['has_coordinates'] = 0
            response['latitude'] = 0
            response['longitude'] = 0


        return response

    def get_place_type(self, wd_id):

        url = 'https://query.wikidata.org/sparql'
        response = dict()
        response['code'] = 400

        # situati nel comune
        query = "SELECT ?label where { wd:"+wd_id+"  wdt:P31	?o . ?o rdfs:label ?label . FILTER (LANG(?label) = \"it\")}"
        r = requests.get(url=url, params={'query': query, 'format': 'json'})
        r.encoding = 'utf-8'

        json_r = json.loads(r.text)
        results = json_r['results']
        bindings = results['bindings']

        for element in bindings:
            if('label' in element):
                label=element['label']
                response['value']=label['value']
                response['code'] = 200



        return response
