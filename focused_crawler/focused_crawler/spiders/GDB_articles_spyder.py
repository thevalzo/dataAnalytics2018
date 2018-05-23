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
                                  db="data_analytics")

        # Retrieve all inserted links
        cursor = self.db.cursor()
        cursor.execute("SELECT idarticle, url  from articles where article is null;")
        results = cursor.fetchall()

        # Make a request for every link's page
        for row in results:
            self.actualUrlID=row[0]
            # meta contains some variables for the response's processing
            yield scrapy.Request(url=row[1], callback=self.parse, meta={'dont_merge_cookies': True, 'id': row[0]})

    def parse(self, response):

        # Extract text
        body = response.body

        # Save variables for the response's processing
        id = response.meta.get('id')

        # Do the html parse
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='ISO-Latin-1')
        [s.extract() for s in soup("ul", {"class": "article-service"})]
        [s.extract() for s in soup("div", {"class": "adv-inset"})]
        [s.extract() for s in soup("p", {"class": "copyright"})]
        results = soup.find("div", {"class": "article-base-body"})

        # Apply the correct codification
        text=unidecode.unidecode(results.get_text())
        text = filter(lambda x: not re.match(r'^\n*$', x), text)
        text=text.replace('\"', '\\\"').replace('\'','\\\'')

        # Insert the article in the db
        cursor = self.db.cursor()
        query = "UPDATE articles SET article=\'"+text+"\' WHERE idarticle=\'"+str(id)+"\';"
        cursor.execute(query)
        self.db.commit()





