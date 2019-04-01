from pymongo import MongoClient
import os

client = MongoClient("mongodb://360es:Qihoo_360@10.252.32.121:27017/?authSource=admin")
db = client["smartcrawler"]
collection = db["oriented"]
with open('./urls', 'r',encoding="utf-8") as u:
    user_agents = u.read().split('\n')[0:-1]
for url in user_agents:
    print(url)
    print(collection.update({"seed_url":url},{"$set":{"spider":"dynamic","list_spider":"dynamic"}}))