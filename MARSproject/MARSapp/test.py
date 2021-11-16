from django.shortcuts import render
from pymongo import MongoClient
import pymongo
from decouple import config
import gridfs
import codecs

client = MongoClient(config('DB_HOST'))
database = client["hacc_sample_database"]
collection = database["hacc_sample_seal_data"] #for all data
collectioncoordinates = database["hacc_coordinates_collection"]
upload = database["hacc_upload_collection"] #for report submissions
grid_database = client["gridfs_database"]
fs = gridfs.GridFS(grid_database)





