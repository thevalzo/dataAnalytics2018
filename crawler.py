from pymongo import MongoClient
import requests
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = MongoClient("127.0.0.1:27017")
#db=client.admin
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

access_token="AIzaSyBC42AcO9sSmxbzyTUvm7Mx0NBS9uUN4zA"
CSE_id="009340605044712161504:3r4vwijr9ik"
query="Brescia"
r = requests.get("https://www.googleapis.com/customsearch/v1?key="+access_token+"&cx="+CSE_id+"&q="+query)
response = r.json()
print response