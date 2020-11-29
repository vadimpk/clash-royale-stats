import pymongo
from pymongo import MongoClient
import ssl

client = MongoClient("mongodb+srv://vadimpk:lz921skm0001p@cluster0-bawxm.mongodb.net/cr_stats?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)

db = client["cr_stats"]

