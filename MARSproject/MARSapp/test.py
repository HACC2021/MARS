from django.shortcuts import render
from pymongo import MongoClient
import pymongo
from decouple import config
import gridfs
import codecs
import math
import reverse_geocoder as rg
import numpy as np
import smtplib, ssl

client = MongoClient(config('DB_HOST'))
database = client["hacc_sample_database"]
seal_collection = database["hacc_sample_seal_data"] #for all data
bird_collection = database["hacc_sample_bird_data"]
collectioncoordinates = database["hacc_coordinates_collection"]

# sealupload = database.hacc_upload_collection #for report submissions

sealupload = database["hacc_seal_upload"]
birdupload = database["hacc_bird_upload"]
turtleupload = database["hacc_turtle_upload"]

# GRID FS databases for images
birdimages = client["bird_images"]
sealimages = client["seal_images"]
turtleimages = client["turtle_images"]
birdFS = gridfs.GridFS(birdimages)
sealFS = gridfs.GridFS(sealimages)
turtleFS = gridfs.GridFS(turtleimages)

x = sealupload.find({"Ticket_Number": 'OS1204410041'})

print(x)

