**** OVERVIEW

Il codice è composto da due spyder e uno script python indipendenti che estraggono testo di articoli del Giornale di Brescia 
e utilizzano vari servizi per fare NERL
Questo l'ordine di esecuzione:
	1- "focused_crawler\focused_crawler\spiders\GDB_spyder.py"
	Si occupa di estrarre i link degli articoli dal motore di ricerca del giornale, inserendoli nella tabella articles
	2- "focused_crawler\focused_crawler\spiders\GDB_articles_spyder.py"
	Questo spyder recupera i link degli articoli, estrare il relativo testo e lo salva ancora nella tabella articles.
	3- "entity-linker.py"
	Lo script si occupa di caricare dal database i testi degli articoli e interrogare i vari servizi di entity linking,
	salvandone il  risultato nella tabella entities

**** SETTAGGIO DELL'AMBIENTE

 E' necessario installare le seguenti librerie utilizzando i comandi da un punto qualsiasi:
	- pip install scrapy
	- pip install unidecode
	- pip install MySQL-python
	- pip install re
	- pip install bs4

Il database è costituito dalle tabelle 
	- `data_analytics`.`entities`
		(`idEntities`,
		`uri`,
		`similarityScore`,
		`types`,
		`surfaceForm`,
		`source`,
		`idArticle`,
		`confidence`,
		`offset`)

	-`data_analytics`.`articles`
		(`idarticle`,
		`url`,
		`keyword`,
		`article`,
		`location`,
		`date`,
		`section`,
		`tooLong`)

**** ESECUZIONE
	
		1 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB

		2 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB_articles
	
		3 - Posizionarsi in DataAnalytics\
		Eseguire entity_linker.py
		




