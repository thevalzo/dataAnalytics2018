import scrapy
import unidecode
import MySQLdb


from bs4 import BeautifulSoup


class GDBSpider(scrapy.Spider):
    # Spyder name
    name = "GDB"
    db = ""

    def start_requests(self):

        #Keywords to search in the search engine of GDB
        keywords=["brescia"]
        actualKeyword=""

        # Location for filtering the search results
        locations=["brescia","Brescia","BRESCIA"]
        actualLocation=""

        # Sections for filtering the search results
        sections=["Brescia e Hinterland"]
        actualSection=""

        # Url of GDB
        url="https://www.giornaledibrescia.it/ricerca-nel-portale?fq=tag_dimension.Location:"

        # Connect to DB
        self.db = MySQLdb.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="data_analytics")

        # Make a request to the search engine for every keyword, location and result page (default 1-500)
        for i in range(0, keywords.__len__()):
            actualKeyword = keywords[i]
            for j in range(0, locations.__len__()):
                actualLocation = locations[j]
                for k in range(1, 500):
                    #meta contains some variables for the response's processing
                    yield scrapy.Request(url=url+str(actualLocation)+"&fq=tag_gdb.categ.root:"+sections[0]+"&q="+str(actualKeyword)+"&page="+str(k), callback=self.parse, meta={'dont_merge_cookies': True, 'keyword': actualKeyword, 'location': actualLocation, 'section': sections[0]})

    def parse(self, response):

        # Extract text
        body = response.body

        # Save variables for the response's processing
        actualLocation=response.meta.get('location')
        actualSection = response.meta.get('section')
        actualKeyword=response.meta.get('keyword')

        # Do the html parse
        soup = BeautifulSoup(body, 'html.parser' ,  from_encoding='ISO-Latin-1')
        soup.prettify()
        [s.extract() for s in soup("div", {"class": "text-center"})]
        dates = soup.findAll("span", {"class": "date"})
        [s.extract() for s in soup("div", {"class": "list-item"})]
        results = soup.find("ul", {"class": "panel-articles-list"})

        # Filter all the links
        results = results.findAll("a")


        for i in range(0, len(results)):

            # Build complete link
            url = "https://www.giornaledibrescia.it"+results[i].get("href")

            # Check for already inserted links
            cursor = self.db.cursor()
            query = "SELECT url, keyword, location FROM articles WHERE url =\'" + str(url) + "\' AND keyword=\'" + str(actualKeyword) + "\'AND location=\'" + str(actualLocation) + "\';"
            cursor.execute(query)
            cursor.fetchall()

            if (cursor.rowcount == 0 ):
                # Insert link
                cursor = self.db.cursor()
                query = "INSERT INTO articles (url, keyword, location, section, date) VALUES  (\'"+url+"\', \'"+actualKeyword+"\', \'"+actualLocation+"\', \'"+actualSection+"\', \'"+str(dates[i].get_text())+"\');"
                cursor.execute(query)
        self.db.commit()





