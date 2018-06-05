import scrapy
import unidecode
import MySQLdb
import re
from bs4 import BeautifulSoup

class GDBSpider(scrapy.Spider):

    # Spyder name
    name = "test"
    db = ""

    def start_requests(self):

        # Connect to DB
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics",
                                  charset = 'utf8')

        # Retrieve all inserted links
        cursor = self.db.cursor()
        cursor.execute("select  url from articles where article_raw like '%www.giornaledibrescia.it%' limit 10;")
        results = cursor.fetchall()
        i=0
        # Make a request for every link's page
        for row in results:
            i+=1
            # meta contains some variables for the response's processing
            yield scrapy.Request(url=row[0], callback=self.parse, meta={'dont_merge_cookies': True, 'url': row[0], 'i':i})

    def parse(self, response):
        # Save variables for the response's processing
        url = response.meta.get('url')
        i = response.meta.get('i')

        page = response.url.split("/")[-2]+str(i)

        #save file with page's html
        filename = 'before-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        f.close

        # Extract text
        body = response.body

        # Do the html parse
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='utf8')
        [s.extract() for s in soup("ul", {"class": "article-service"})]
        [s.extract() for s in soup("div", {"class": "adv-inset"})]
        [s.extract() for s in soup("p", {"class": "copyright"})]
        [s.extract() for s in soup("div", {"class": "caption-text"})]
        [s.extract() for s in soup("script")]
        [s.extract() for s in soup("img")]
        results = soup.find("div", {"class": "article-base-body"})

        #save the file with only extracted html
        filename = 'after-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(str(results))
        self.log('Saved file %s' % filename)
        f.close







