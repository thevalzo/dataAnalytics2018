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

Il database è costituito dalle tabelle materializzabili con queste istruzioni:
	'articles': 'CREATE TABLE `articles` (\n  `idarticle` int(11) NOT NULL AUTO_INCREMENT,\n  `url` varchar(250) DEFAULT NULL,\n  `keyword` varchar(45) DEFAULT NULL,\n  `article` mediumtext,\n  `location` varchar(45) DEFAULT NULL,\n  `date` varchar(45) DEFAULT NULL,\n  `section` varchar(45) DEFAULT NULL,\n  `tooLong` tinyint(4) DEFAULT \'0\',\n  PRIMARY KEY (`idarticle`)\n) ENGINE=InnoDB AUTO_INCREMENT=27068 DEFAULT CHARSET=utf8'
	'entities': 'CREATE TABLE `entities` (\n  `idEntities` int(11) NOT NULL AUTO_INCREMENT,\n  `uri` varchar(150) DEFAULT NULL,\n  `similarityScore` decimal(17,16) DEFAULT NULL,\n  `types` varchar(300) DEFAULT NULL,\n  `surfaceForm` varchar(45) DEFAULT NULL,\n  `source` varchar(45) DEFAULT NULL,\n  `idArticle` int(11) DEFAULT NULL,\n  `confidence` decimal(17,16) DEFAULT NULL,\n  `offset` int(11) DEFAULT NULL,\n  PRIMARY KEY (`idEntities`)\n) ENGINE=InnoDB AUTO_INCREMENT=70857 DEFAULT CHARSET=utf8'

**** ESECUZIONE
	
		1 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB

		2 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB_articles
	
		3 - Posizionarsi in DataAnalytics\
		Eseguire entity_linker.py
		




