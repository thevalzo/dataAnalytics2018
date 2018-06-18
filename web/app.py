# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import sys, os, subprocess
import pandas as pd
import numpy as np
# same as cd /web/ --> cd ../ --> cd src
lib_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(lib_path)
from entitylinker import EntityLinker
from entitylinker import WikiWrapper
from cleaner import Cleaner
from sentiment import Sentiment
from utility import Utility
from collections import Counter
import urllib
app = Flask(__name__)
mysql = MySQL(app)

#set up mysql options
app.config['MYSQL_HOST'] = '127.0.0.1' # <-- db if docker
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'experiments'


@app.route('/')
def index():

	return render_template('index.html')

@app.route('/dataset_entities')
def dataset_entities():
	utility = Utility()
	entities=utility.get_entities_count(15)
	return render_template('dataset_entities.html', entities=entities)

@app.route('/dataset_places')
def dataset_places():
	utility = Utility()
	places_brescia=utility.get_places(1,0,15)
	places_provincia = utility.get_places(0,1,15)
	places_mondo = utility.get_places(0,1,15)
	return render_template('dataset_places.html', places_brescia=places_brescia, places_provincia=places_provincia, places_mondo=places_mondo)

@app.route('/dataset_places_sentiment')
def dataset_places_sentiment():
	utility = Utility()
	worst=utility.get_worst_places()
	best = utility.get_best_places()
	return render_template('dataset_places_sentiment.html', worst=worst, best=best)


@app.route('/brescia_provincia')
def mappa_provincia():
	utility=Utility()
	places=utility.get_places(1,1, 10000)

	params=dict()
	params['zoom']=9
	params['circle_size'] = 2
	params['counters']="map.addLayer(circlesLayer);"
	return render_template('mappa.html',places=places, zoom=9)

@app.route('/brescia', methods=['POST', 'GET'])
def mappa_brescia():
	utility=Utility()
	places=utility.get_places(1,0, 10000)

	params=dict()
	params['zoom']=13
	params['circle_size'] = 2
	params['counters']="map.addLayer(circlesLayer);"
	return render_template('mappa.html',places=places, params=params)

@app.route('/brescia_filtered', methods=['POST', 'GET'])
def mappa_brescia_filtered():
	utility = Utility()
	query=""
	count=0
	if(urllib.unquote(str(request.args.get('elemento_stradale'))) =="1"):
		query=query+" or aggregated_type = \'elemento stradale\'"

	if (urllib.unquote(str(request.args.get('sede_scolastica'))) =="1"):
		query = query + " or aggregated_type = \'sede scolastica/culturale\'"

	if (urllib.unquote(str(request.args.get('luogo_turistico'))) =="1"):
		query = query + " or aggregated_type = \'luogo turistico/monumento\'"

	if (urllib.unquote(str(request.args.get('edificio_religioso'))) =="1"):
		query = query + " or aggregated_type = \'edificio religioso\'"

	if (urllib.unquote(str(request.args.get('suddivisione_cittadina'))) =="1"):
		query = query + " or aggregated_type = \'suddivisione cittadina'"

	if (urllib.unquote(str(request.args.get('edifici_civili'))) =="1"):
		query = query + " or aggregated_type = \'edificio civile\'"

	if (urllib.unquote(str(request.args.get('fermata_tpl'))) =="1"):
		query = query + " or aggregated_type = \'fermata tpl\'"

	if (urllib.unquote(str(request.args.get('edificio_sanitario'))) =="1"):
		query = query + " or aggregated_type = \'edificio sanitario\'"

	if (urllib.unquote(str(request.args.get('edificio_sportivo'))) =="1"):
		query = query + " or aggregated_type = \'edificio sportivo\'"

	n_citations = urllib.unquote(str(request.args.get('citations')))
	places = utility.get_places_filtered(1, 0, n_citations, query)

	circle_size = urllib.unquote(str(request.args.get('circle_size')))
	show_counters = urllib.unquote(str(request.args.get('show_counters')))

	elemento_stradale = 1
	sede_scolastica = 1
	luogo_turistico = 1
	edificio_religioso = 1
	suddivisione_cittadina = 1
	edifici_civili = 1
	fermata_tpl = 1
	edificio_sanitario = 1
	edificio_sportivo = 1

	params=dict()
	params['zoom']=13
	params['circle_size']=circle_size
	if(show_counters=="1"):
		params['counters']="map.addLayer(circlesLayer);"
	else:
		params['counters']="0"

	return render_template('mappa.html', places=places, params=params)

@app.route('/place_sentiment', methods=['POST', 'GET'])
def place_sentiment():
	wd_id = urllib.unquote(str(request.args.get('wd_id')))
	type = urllib.unquote(request.args.get('type')).encode('utf8')

	utility=Utility()
	sentiment=Sentiment()

	place=utility.get_place(wd_id=wd_id, type=type)
	place['label']=place['uri'].split("/")[-1].replace("_"," ")
	if(place['wikidata_id']!="None"):
		place['surfaceForm']=utility.get_surfaceForm(place['wikidata_id'])
	elements=sentiment.get_place_word_frequency(wd_id=wd_id, type=type, pos_tag="a")

	words = elements['words']
	most = words.most_common()
	array = []
	for i in range(0, min(15,most.__len__())):
		new_dict = {}
		elem = most[i]
		new_dict['word'] = elem[0].decode('utf-8')
		new_dict['num'] = elem[1]
		array.append(new_dict)

	words['words']= array
	pos_neg_words=sentiment.get_best_worst_words(wd_id, type, "a")

	return render_template('place_sentiment.html',place=place,words=words, pos_words=pos_neg_words['pos'], neg_words=pos_neg_words['neg'])

@app.route('/place', methods=['POST', 'GET'])
def place_info():
	wd_id = urllib.unquote(str(request.args.get('wd_id')))
	type = urllib.unquote(request.args.get('type')).encode('utf8')

	utility=Utility()
	sentiment=Sentiment()

	place=utility.get_place(wd_id=wd_id, type=type)
	place['label']=place['uri'].split("/")[-1].replace("_"," ")
	if(place['wikidata_id']!="None"):
		place['surfaceForm']=utility.get_surfaceForm(place['wikidata_id'])
	elements=sentiment.get_place_word_frequency(wd_id=wd_id, type=type, pos_tag="n")

	words = elements['words']
	n_articles = str(elements['n_articles'])

	linked_entities=sentiment.get_linked_entities(wd_id=wd_id, type=type)


	#CLEAN WORDS FROM ENTITIES
	for element in linked_entities:
		for word in element['surfaceForm']:
			word = word.lower()
			word_s = word.split('\'')
			for word1 in word_s:
				if word1.lower() in words:
					words.pop(word1.lower())

		t_uri = element['uri'].split("/")[-1].replace("_", " ").split(" ")

		for word2 in t_uri:
			if word2.lower() in words:
				words.pop(word2.lower())

		t_uri = element['uri'].split("/")[-1].replace("_", " ").split("\'")

		for word2 in t_uri:
			if word2.lower() in words:
				words.pop(word2.lower())

	linked_places = sentiment.get_linked_places(wd_id=wd_id, type=type)

	# CLEAN WORDS FROM PLACES
	for element in linked_places:
		for word in element['surfaceForm']:
			word = word.lower()
			word_s = word.split('\'')
			for word1 in word_s:
				if word1.lower() in words:
					words.pop(word1.lower())

		t_uri = element['uri'].split("/")[-1].replace("_", " ").split(" ")

		for word2 in t_uri:
			if word2.lower() in words:
				words.pop(word2.lower())

		t_uri = element['uri'].split("/")[-1].replace("_", " ").split("\'")

		for word2 in t_uri:
			if word2.lower() in words:
				words.pop(word2.lower())
	#linked_places=sentiment.get_linked_places(wd_id=wd_id, type=type)

	most = words.most_common()

	#len = most.__len__()
	#for i in range(0, len - 1):
		#word4 = most[i]
		#if (most.__len__() == i + 1):
		#	break
		#if (str(word4[0]).__len__() == 1):
		#	most.pop(i)

	# create dict from word frequency
	array = []
	#most=words['most']

	# most = list(takewhile(lambda x: x[1] > 5, words.most_common()))
	for i in range(0, min(15,most.__len__())):
		new_dict = {}
		elem = most[i]
		new_dict['word'] = elem[0].decode('utf-8')
		new_dict['num'] = elem[1]
		array.append(new_dict)

	words['words']= array
	return render_template('place.html',place=place,words=words, n_a=n_articles, places=linked_places, entities= linked_entities)

# 404 error handler
#@app.errorhandler(404)
#def page_not_found(e):
#	return render_template('404.html'), 404

@app.route('/brescia_sentiment', methods=['POST', 'GET'])
def mappa_brescia_sentiment():
	utility=Utility()

	places=utility.get_places(1,0, 10000)

	params=dict()
	params['zoom']=13
	params['circle_size'] = 2
	params['counters']="map.addLayer(circlesLayer);"
	params['sentiment'] = "1"
	return render_template('mappa_sentiment.html',places=places, params=params)


@app.route('/brescia_filtered_sentiment', methods=['POST', 'GET'])
def mappa_brescia_filtered_sentiment():
	utility = Utility()
	sentiment=Sentiment()
	query=""
	count=0
	if(urllib.unquote(str(request.args.get('elemento_stradale'))) =="1"):
		query=query+" or aggregated_type = \'elemento stradale\'"

	if (urllib.unquote(str(request.args.get('sede_scolastica'))) =="1"):
		query = query + " or aggregated_type = \'sede scolastica/culturale\'"

	if (urllib.unquote(str(request.args.get('luogo_turistico'))) =="1"):
		query = query + " or aggregated_type = \'luogo turistico/monumento\'"

	if (urllib.unquote(str(request.args.get('edificio_religioso'))) =="1"):
		query = query + " or aggregated_type = \'edificio religioso\'"

	if (urllib.unquote(str(request.args.get('suddivisione_cittadina'))) =="1"):
		query = query + " or aggregated_type = \'suddivisione cittadina'"

	if (urllib.unquote(str(request.args.get('edifici_civili'))) =="1"):
		query = query + " or aggregated_type = \'edificio civile\'"

	if (urllib.unquote(str(request.args.get('fermata_tpl'))) =="1"):
		query = query + " or aggregated_type = \'fermata tpl\'"

	if (urllib.unquote(str(request.args.get('edificio_sanitario'))) =="1"):
		query = query + " or aggregated_type = \'edificio sanitario\'"

	if (urllib.unquote(str(request.args.get('edificio_sportivo'))) =="1"):
		query = query + " or aggregated_type = \'edificio sportivo\'"

	n_citations = urllib.unquote(str(request.args.get('citations')))
	norm = urllib.unquote(str(request.args.get('normalize')))
	circle_size = urllib.unquote(str(request.args.get('circle_size')))

	places = utility.get_places_filtered(1, 0, n_citations, query)


	params=dict()
	params['zoom']=13
	params['circle_size']=circle_size
	params['counters']="map.addLayer(circlesLayer);"
	params['sentiment'] = norm
	return render_template('mappa_sentiment.html', places=places, params=params)

if __name__ == '__main__':
	app.run()
