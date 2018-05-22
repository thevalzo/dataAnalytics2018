import scrapy
import unidecode
import MySQLdb
import re
import datetime

from bs4 import BeautifulSoup


class GDBSpider(scrapy.Spider):
    name = "GDB_articles"
    db = ""

    def start_requests(self):

        # Connect to DB
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics")

        cursor = self.db.cursor()
        cursor.execute("SELECT idarticle, url  from articles where article is null;")
        results = cursor.fetchall()

        for row in results:
            self.actualUrlID=row[0]
            yield scrapy.Request(url=row[1], callback=self.parse, meta={'dont_merge_cookies': True, 'id': row[0]})

    def parse(self, response):

        body = response.body
        id = response.meta.get('id')
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='ISO-Latin-1')
        #text=soup.prettify()
        [s.extract() for s in soup("ul", {"class": "article-service"})]
        [s.extract() for s in soup("div", {"class": "adv-inset"})]
        [s.extract() for s in soup("p", {"class": "copyright"})]
        results = soup.find("div", {"class": "article-base-body"})
        text=unidecode.unidecode(results.get_text())
        text = filter(lambda x: not re.match(r'^\n*$', x), text)
        text=text.replace('\"', '\\\"').replace('\'','\\\'')

        # Save page
        #page = response.url.split("/")[-2]+str(id)
        #filename = 'raw-file-%s.html' % page
       # with open(filename, 'wb') as f:
        #    f.write(unidecode.unidecode(text))
        #f.close

        cursor = self.db.cursor()
        query = "UPDATE articles SET article=\'"+text+"\' WHERE idarticle=\'"+str(id)+"\';"
        #print(query)
        cursor.execute(query)
        self.db.commit()





