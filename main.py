# -*- coding: utf-8 -*-
from entitylinker import EntityLinker
from cleaner import Cleaner
from sentiment import Sentiment

def main():

    #istantiate all the useful classes
    linker=EntityLinker()
    cleaner=Cleaner()
    sentiment=Sentiment()

    #-----PREPARE TEXT-----
    #copy the baseline 'article_raw' to 'article_clean': in this field we can clean the text
    #cleaner.copy_article()

    #after the text has been cleaned, the last step is to tokenize it
    #cleaner.tokenize()

    # -----EXTRACT NAMED ENTITIES-----
    #Use Dandelion API to do NER and NEL
    linker.dandelify()

    #Identify wich named entities are roads
    #linker.search_roads()

    # -----COMPUTE NAMED ENTITIES SENTIMENT-----
    #places=linker.get_places()
    #sentiment.places_word_frequency(places)

if __name__ == "__main__":
    main()