**** OVERVIEW

Il codice è composto da due spyder e diversi script python indipendenti tra loro che estraggono testi di articoli del Giornale di Brescia, utilizzano le Dandelion API per fare NERL e calcolano il sentiment dei luoghi individuati
Questo l'ordine di esecuzione:
	1- "focused_crawler\focused_crawler\spiders\GDB_spyder.py"
	Si occupa di estrarre i link degli articoli dal motore di ricerca del giornale, inserendoli nella tabella articles
	2- "focused_crawler\focused_crawler\spiders\GDB_articles_spyder.py"
	Questo spyder recupera i link degli articoli, estrare il relativo testo e lo salva ancora nella tabella articles.
	3- "main.py"
	Utilizza le classi:
		- Cleaner.py : ripulische il testo degli articoli e lo tokenizza
		- EntityLinker.py : Interroga le Dandelion Api, le Wikidata Api, ed effettua operazioni di disambiguazione col fine di individuare i luoghi di Brescia
		- Sentiment.py : Calcola le parole più frequenti per ogni luogo e il  sentiment
		- Utility.py :fornisce metodi di supporto alle precedenti

**** SETTAGGIO DELL'AMBIENTE
 La versione utilizzata di python è la 2.7
 E' necessario installare le seguenti librerie utilizzando i comandi da un punto qualsiasi:
	- pip install scrapy
	- pip install unidecode
	- pip install MySQL-python
	- pip install re
	- pip install bs4
	- ..

Il database è costituito dalle tabelle materializzabili con queste istruzioni:
	'articles': 'CREATE TABLE `articles` (\n  `idarticle` int(11) NOT NULL AUTO_INCREMENT,\n  `url` varchar(250) DEFAULT NULL,\n  `keyword` varchar(45) DEFAULT NULL,\n  `article` mediumtext,\n  `location` varchar(45) DEFAULT NULL,\n  `date` varchar(45) DEFAULT NULL,\n  `section` varchar(45) DEFAULT NULL,\n  `tooLong` tinyint(4) DEFAULT \'0\',\n  PRIMARY KEY (`idarticle`)\n) ENGINE=InnoDB AUTO_INCREMENT=27068 DEFAULT CHARSET=utf8'
	'entities': 'CREATE TABLE `entities` (\n  `idEntities` int(11) NOT NULL AUTO_INCREMENT,\n  `uri` varchar(150) DEFAULT NULL,\n  `similarityScore` decimal(17,16) DEFAULT NULL,\n  `types` varchar(300) DEFAULT NULL,\n  `surfaceForm` varchar(45) DEFAULT NULL,\n  `source` varchar(45) DEFAULT NULL,\n  `idArticle` int(11) DEFAULT NULL,\n  `confidence` decimal(17,16) DEFAULT NULL,\n  `offset` int(11) DEFAULT NULL,\n  PRIMARY KEY (`idEntities`)\n) ENGINE=InnoDB AUTO_INCREMENT=70857 DEFAULT CHARSET=utf8'
	..

La cartella data contiene:
	-il file di testo sorgente del lessico Sentix
	-lo script python con cui è stato creato il lo script sql di popolamento
	-lo script sql di popolamento 
	- il file sql con il database completo

**** ESECUZIONE
	
		1 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB

		2 - Posizionarsi in DataAnalytics\focused_crawler\focused_crawler
		Da linea di comando digitare scrapy crawl GDB_articles
	
		3 - Posizionarsi in DataAnalytics\src
		Eseguire main.py

		3 - Posizionarsi in DataAnalytics\src
		Eseguire app.py per azionare il server web , visibile a http://127.0.0.1:5000/
		




