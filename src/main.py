# -*- coding: utf-8 -*-
from entitylinker import EntityLinker
from utility import Utility
from cleaner import Cleaner
from sentiment import Sentiment

def main():

    #istantiate all the useful classes
    linker=EntityLinker()
    cleaner=Cleaner()
    sentiment=Sentiment()
    utility= Utility()


    #-----PREPARE TEXT-----

    #--copy the baseline 'article_raw' to 'article_clean': in this field we can clean the text
    #cleaner.copy_article()

    #--after the text has been cleaned, the last step is to tokenize it
    #cleaner.tokenize()

    # -----EXTRACT NAMED ENTITIES-----

    #Use Dandelion API to do NER and NEL
    #--Extract with Dandelion
    #linker.dandelify()

    # --Filter and integrate results
    #linker.set_wd_ids_entities(10)
    #linker.detect_places()

    # --Disambiguate and correct
    #linker.correct_places()
    #linker.search_roads()
    #linker.set_places_type()
    #linker.set_roads_coordinates()

    #utility.set_places_aggregated_type()
    #utility.set_articles_dates()

    # -----COMPUTE NAMED ENTITIES SENTIMENT-----
    #sentiment.set_places_sentiment()
    

if __name__ == "__main__":
    main()