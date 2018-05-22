import scrapy
import unidecode
import MySQLdb
import re
import datetime

from bs4 import BeautifulSoup


class GDBSpider(scrapy.Spider):
    name = "GDB"
    db = ""

    def start_requests(self):

        keywords=["brescia"]
        actualKeyword=""
        locations=["brescia","Brescia","BRESCIA"]
        actualLocation=""
        sections=["Brescia e Hinterland"]
        actualSection=""
        url="https://www.giornaledibrescia.it/ricerca-nel-portale?fq=tag_dimension.Location:"

        # Connect to DB
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics")

        for i in range(0, keywords.__len__()):
            actualKeyword = keywords[i]
            for j in range(0, locations.__len__()):
                actualLocation = locations[j]
                for k in range(1, 500):
                    yield scrapy.Request(url=url+str(actualLocation)+"&fq=tag_gdb.categ.root:"+sections[0]+"&q="+str(actualKeyword)+"&page="+str(k), callback=self.parse, meta={'dont_merge_cookies': True, 'keyword': actualKeyword, 'location': actualLocation, 'section': sections[0]})

    def parse(self, response):

        # extract text

        body = response.body
        actualLocation=response.meta.get('location')
        actualSection = response.meta.get('section')
        actualKeyword=response.meta.get('keyword')
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='ISO-Latin-1')
        soup.prettify()
        [s.extract() for s in soup("div", {"class": "text-center"})]
        dates = soup.findAll("span", {"class": "date"})
        [s.extract() for s in soup("div", {"class": "list-item"})]
        results = soup.find("ul", {"class": "panel-articles-list"})

        #print(body)
        #page = response.url.split("/")[-2]
        #filename = 'raw-file-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(str(body))
        #f.close

        results = results.findAll("a")

        #print("dates:"+str(dates.__len__())+" results:"+str(results.__len__()))
        for i in range(0, len(results)):
            url = "https://www.giornaledibrescia.it"+results[i].get("href")
            cursor = self.db.cursor()
            query = "SELECT url, keyword, location FROM articles WHERE url =\'" + str(url) + "\' AND keyword=\'" + str(actualKeyword) + "\'AND location=\'" + str(actualLocation) + "\';"

            cursor.execute(query)
            #print(str(dates[i].get_text()))
            if (cursor.rowcount == 0 ):
                cursor = self.db.cursor()
                query = "INSERT INTO articles (url, keyword, location, section, date) VALUES  (\'"+url+"\', \'"+actualKeyword+"\', \'"+actualLocation+"\', \'"+actualSection+"\', \'"+str(dates[i].get_text())+"\');"
                cursor.execute(query)
        self.db.commit()





