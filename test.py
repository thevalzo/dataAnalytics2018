import requests

import requests
#r = requests.post("http://nerd.eurecom.fr/api/document", data={'key': 'dqdph2hss98qgqt1j2llk16ktslmv0ob', 'text':'Non sono mancati dei fuori programma durante la commemorazione delle vittime della strage di piazza della Loggia. Durante la lettura del messaggio inviato dal presidente della Repubblica, Sergio Mattarella, fischi si sono levati dalla piazza, come pure applausi. Non solo. Proprio durante gli otto rintocchi - tanti quanti le vittime, che appunto ricordano alle 10.12, ora dell\'esplosione della bomba - alcuni antagonisti hanno levato cori dalla piazza, in un momento di commemorazione che è stato sempre accompagnato dal silenzio della folla raccolta. Ne è seguito uno scambio ravvicinato di vedute tra il presidente dell\'associazione dei familiari delle vittime Manlio Milani e una rappresentanza del Magazzino 47. Gli antagonisti hanno rotto il silenzio della piazza durante gli otto rintocchi in memoria delle vittime. Milani si è avvicinato chiedendo loro rispetto, ma senza fortuna.'})
#idDoc=r.json()['idDocument']
#print(idDoc)

#r = requests.post("http://nerd.eurecom.fr/api/annotation", data={'key': 'dqdph2hss98qgqt1j2llk16ktslmv0ob', 'idDocument': idDoc, 'extractor': 'combined'})

#idAnn=r.json()['idAnnotation']
#print(idAnn)

#r = requests.post("http://nerd.eurecom.fr/api/entity", data={'key': 'dqdph2hss98qgqt1j2llk16ktslmv0ob', 'idAnnotation': idAnn})

#idAnn=r.json()['idAnnotation']
#print(r.text)

url="https://api.dandelion.eu/datatxt/nex/v1/"
text="Non sono mancati dei fuori programma durante la commemorazione delle vittime della strage di piazza della Loggia. Durante la lettura del messaggio inviato dal presidente della Repubblica, Sergio Mattarella, fischi si sono levati dalla piazza, come pure applausi. Non solo. Proprio durante gli otto rintocchi - tanti quanti le vittime, che appunto ricordano alle 10.12, ora dell\'esplosione della bomba - alcuni antagonisti hanno levato cori dalla piazza, in un momento di commemorazione che è stato sempre accompagnato dal silenzio della folla raccolta. Ne è seguito uno scambio ravvicinato di vedute tra il presidente dell\'associazione dei familiari delle vittime Manlio Milani e una rappresentanza del Magazzino 47. Gli antagonisti hanno rotto il silenzio della piazza durante gli otto rintocchi in memoria delle vittime. Milani si è avvicinato chiedendo loro rispetto, ma senza fortuna."
token='187d60d6e4c6465d96895b99835d543e'
r = requests.get(url=url, params={'token':'187d60d6e4c6465d96895b99835d543e', 'lang':'it', 'text': text})
print(r)
text=r.text
print(text)