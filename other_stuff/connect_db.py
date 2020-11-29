import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://vadimpk:lz921skm0001p@cluster0-bawxm.mongodb.net/cr_stats?retryWrites=true&w=majority")

db = client["cr_stats"]

