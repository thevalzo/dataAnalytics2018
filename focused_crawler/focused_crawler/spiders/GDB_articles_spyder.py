import scrapy
import unidecode
import MySQLdb
import re
from bs4 import BeautifulSoup

class GDBSpider(scrapy.Spider):

    # Spyder name
    name = "GDB_articles"
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
        #cursor.execute("select  distinct url from results where tooLong=0 and url not in (select url from articles);")
        cursor.execute("select url from articles where tooLong=0;")
        results = cursor.fetchall()

        # Make a request for every link's page
        for row in results:

            # meta contains some variables for the response's processing
            yield scrapy.Request(url=row[0], callback=self.parse, meta={'dont_merge_cookies': True, 'url': row[0]})

    def parse(self, response):

        # Extract text
        body = response.body

        # Save variables for the response's processing
        url = response.meta.get('url')

        # Do the html parse
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='utf8')
        [s.extract() for s in soup("ul", {"class": "article-service"})]
        [s.extract() for s in soup("div", {"class": "adv-inset"})]
        [s.extract() for s in soup("p", {"class": "copyright"})]
        [s.extract() for s in soup("div", {"class": "caption-text"})]
        [s.extract() for s in soup("script")]
        [s.extract() for s in soup("img")]
        results = soup.find("div", {"class": "article-base-body"})

        # Apply the correct codification
        #text=unidecode.unidecode(results.get_text())
        text=results.get_text()
        text = filter(lambda x: not re.match(r'^\n*$', x), text)
        text=text.replace('\"', '\\\"').replace('\'','\\\'')
        text=text.encode('utf8')
        # Insert the article in the db
        cursor = self.db.cursor()
        #query = "insert into articles (url, article_raw) values (\'"+url.decode('utf8')+"\',\'"+text.decode('utf8')+"\');"
        query = "update articles set article_raw=\'" + text.decode('utf8') + "\' where url=\'" + url.decode('utf8') + "\';"
        cursor.execute(query)
        self.db.commit()





