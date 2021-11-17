from django.shortcuts import render
from pymongo import MongoClient
import pymongo
from decouple import config
import gridfs
import codecs
import math
import reverse_geocoder as rg
import numpy as np


client = MongoClient(config('DB_HOST'))
database = client["hacc_sample_database"]
collection = database["hacc_sample_seal_data"] #for all data
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


def home(request):
    return render(request, 'homepage.html', )


def emergency(request):
    return render(request, 'emergency.html')


def login(request):
    return render(request, 'login.html')


def formselect(request):
    return render(request, 'formselect.html')


def sealreport(request):
    return render(request, 'sealsightingform.html')


def turtlereport(request):
    return render(request, 'turtlesightingform.html')


def birdreport(request):
    return render(request, 'birdsightingform.html')


def sealsubmit(request):
    result = sealupload.find({}, {"_id": 1})
    objectID = []
    for i in result:
        p = i.get("_id")
        objectID.append(p)
    submission_dict = {}
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    pnumber = request.POST.get('pnumber')
    datetime = request.POST.get('datetime')
    animalcharacteristics = request.POST.getlist('Animal Characteristics[]')
    island = request.POST.get('island')
    comment = request.POST.get('comment')
    humans = request.POST.get('humans')
    Longitude = request.POST.get('Longitude')
    Latitude = request.POST.get('Latitude')
    try:
        submission_dict["_id"] = len(objectID)
        submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + datetime[3]
        submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Ticket_Number"] = "OS" + datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + \
                                           datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Observer"] = fname + " " + lname
        submission_dict["Observer_Contact_Number"] = pnumber
        submission_dict["Observer_Initals"] = fname[0] + lname[0]
        submission_dict["animal characteristics"] = animalcharacteristics
        submission_dict["island"] = island
        submission_dict["comment"] = comment
        submission_dict["humans"] = humans
        submission_dict["Latitude"] = Latitude
        submission_dict["Longitude"] = Longitude

        mongoID = len(objectID)
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = gridfs.GridFS(sealimages)
            filename = fs.put(myfile, _id=mongoID,
                              filename="OS" + datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] +
                                       datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
        submission_dict["imageID"] = mongoID
    except IndexError:
        print(" ")

    user_lat = 21.6415
    user_long = -158.0671

    diff_of_lat = 0
    diff_of_long = 0

    compare_dict = {}
    for_min = []

    '''pulling options using beach name'''
    def reverseGeocode(coordinates):
        result = rg.search(coordinates)
        for data in result:
            locale_name = (data["name"])
            # print(locale_name)

        # pulling coords with same name
        myDoc = collectioncoordinates.find({"Name": locale_name})
        for data in myDoc:
            # print(data)

            # for squaring
            loc_lat = data["Latitude"]
            loc_lat = float(str(loc_lat))
            diff_of_lat = user_lat - loc_lat

            loc_long = data["Longitude"]
            loc_long = float(str(loc_long))
            diff_of_long = user_long - loc_long

            # print(diff_of_lat, diff_of_long)

            distance = math.sqrt(math.pow(diff_of_lat, 2) + math.pow(diff_of_long, 2))
            print(distance)

            # creating dict with beach name as key, then append distance
            beach_name = data["Location"]

            temp = {beach_name: distance}
            compare_dict.update(temp)

        # print(compare_dict)

        # now find smallest distance and print key
        for value in compare_dict.values():
            # print(value)
            for_min.append(value)

        closest_distance = min(for_min)
        # print("close", closest_distance)
        # print("beach distances", for_min)

        # create 0.0001 range around closest_distance, check if all values are within
        # #  if in, print key
        for key, value in compare_dict.items():
            range = 0.0005  # 0.001 = 40 feet
            if (closest_distance - range) <= value <= (closest_distance + range):
                submission_dict["Location"] = key
            else:
                submission_dict["Location"] = ""

    coordinates = (user_lat, user_long)
    reverseGeocode(coordinates)
    sealupload.insert_one(submission_dict)
    return render(request, 'thankyoupage.html')


def birdsubmit(request):
    result = birdupload.find({}, {"_id": 1})
    objectID = []
    for i in result:
        p = i.get("_id")
        objectID.append(p)
    print("YES")
    submission_dict = {}
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    pnumber = request.POST.get('pnumber')
    datetime = request.POST.get('datetime')
    animalcharacteristics = request.POST.getlist('Animal Characteristics[]')
    island = request.POST.get('island')
    comment = request.POST.get('comment')
    humans = request.POST.get('humans')
    Longitude = request.POST.get('Longitude')
    Latitude = request.POST.get('Latitude')
    try:
        submission_dict["_id"] = len(objectID)
        submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + datetime[3]
        submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Ticket_Number"] = "OB" + datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + \
                                           datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Observer"] = fname + " " + lname
        submission_dict["Observer_Contact_Number"] = pnumber
        submission_dict["Observer_Initals"] = fname[0] + lname[0]
        submission_dict["animal characteristics"] = animalcharacteristics
        submission_dict["island"] = island
        submission_dict["comment"] = comment
        submission_dict["humans"] = humans
        submission_dict["Latitude"] = Latitude
        submission_dict["Longitude"] = Longitude

        mongoID = len(objectID)
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = gridfs.GridFS(birdimages)
            filename = fs.put(myfile, _id=mongoID,
                              filename="OB" + datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] +
                                       datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
        submission_dict["imageID"] = mongoID
    except IndexError:
        print(" ")

    # Old geolocation function
    #  compare_lat = []
    #  compare_long = []
    #
    # # add invalid something so if coord is way too off, beach is invalid
    #
    #  user_lat = 21.639158
    #  user_long = -158.064262
    #  try:
    #     import reverse_geocoder as rg
    #
    #     def reverseGeocode(coordinates):
    #         result = rg.search(coordinates)
    #         for data in result:
    #             locale_name = (data["name"])
    #
    #
    #         # pulling coords with same name
    #         myDoc = collectioncoordinates.find({"Name": locale_name})
    #         for data in myDoc:
    #             print(data)
    #             compare_lat.append(data["Latitude"])
    #             compare_long.append(data["Longitude"])
    #
    #     coordinates = (user_lat, user_long)
    #     reverseGeocode(coordinates)
    #
    #     # function for latitude
    #     import numpy as np
    #     def find_nearest_lat(lat_list, latitude):
    #         lat_list = np.asarray(lat_list)
    #         idx = (np.abs(lat_list - latitude)).argmin()
    #         return lat_list[idx]
    #
    #
    #     lat_list = np.random.random(10)
    #
    #     lat_list = []
    #
    #     x = 0
    #     for i in compare_lat:
    #         bob = (compare_lat[x])
    #         lat_list.append(float(bob))
    #         x += 1
    #
    #     closest_lat = (find_nearest_lat(lat_list, user_lat))
    #     # print(closest_lat)
    #
    #     # same function for longitude
    #     import numpy as np
    #     def find_nearest_long(long_list, longitude):
    #         long_list = np.asarray(long_list)
    #         idx = (np.abs(long_list - longitude)).argmin()
    #         return long_list[idx]
    #
    #     long_list = np.random.random(10)
    #
    #     long_list = []
    #     x = 0
    #     for i in compare_long:
    #         bob = (compare_long[x])
    #         long_list.append(float(bob))
    #         x += 1
    #     closest_long = (find_nearest_long(long_list, user_long))
    #
    #
    #     closest_lat = str(closest_lat)
    #     closest_set = (collectioncoordinates.find_one({"Latitude": closest_lat}))
    #     closest_beach_lat = closest_set["Location"]
    #     print(closest_beach_lat)
    #
    #     closest_long = str(closest_long)
    #     closest_set_long = (collectioncoordinates.find_one({"Longitude": closest_long}))
    #     closest_beach_long = closest_set_long["Location"]
    #     print(closest_beach_long)
    #
    #
    #     #if closest_beach_lat == closest_beach_long:
    #         #submission_dict["Location"] = closest_beach_long
    #
    #     #if closest_beach_lat != closest_beach_long:
    #         #submission_dict["Location"] = "invalid"

    except:
        print(" ")
    birdupload.insert_one(submission_dict)
    return render(request, 'thankyoupage.html')


def turtlesubmit(request):
    result = turtleupload.find({}, {"_id": 1})
    objectID = []
    for i in result:
       p = i.get("_id")
       objectID.append(p)
    print("YES")
    submission_dict = {}
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    pnumber = request.POST.get('pnumber')
    datetime = request.POST.get('datetime')
    animalcharacteristics = request.POST.getlist('Animal Characteristics[]')
    island = request.POST.get('island')
    comment = request.POST.get('comment')
    humans = request.POST.get('humans')
    Longitude = request.POST.get('Longitude')
    Latitude = request.POST.get('Latitude')
    try:
        submission_dict["_id"] = len(objectID)
        submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + datetime[3]
        submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Ticket_Number"] = "OT" + datetime[5] + datetime[6] + datetime[8] + datetime[9] + datetime[2] + \
                                           datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Observer"] = fname + " " + lname
        submission_dict["Observer_Contact_Number"] = pnumber
        submission_dict["Observer_Initals"] = fname[0] + lname[0]
        submission_dict["animal characteristics"] = animalcharacteristics
        submission_dict["island"] = island
        submission_dict["comment"] = comment
        submission_dict["humans"] = humans
        submission_dict["Latitude"] = Latitude
        submission_dict["Longitude"] = Longitude

        mongoID = len(objectID)
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = gridfs.GridFS(turtleimages)
            filename = fs.put(myfile, _id = mongoID, filename= "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
        submission_dict["imageID"] = mongoID
    except IndexError:
        print(" ")

    # Old geolocation function
    #  compare_lat = []
    #  compare_long = []
    #
    # # add invalid something so if coord is way too off, beach is invalid
    #
    #  user_lat = 21.639158
    #  user_long = -158.064262
    #  try:
    #     import reverse_geocoder as rg
    #
    #     def reverseGeocode(coordinates):
    #         result = rg.search(coordinates)
    #         for data in result:
    #             locale_name = (data["name"])
    #
    #
    #         # pulling coords with same name
    #         myDoc = collectioncoordinates.find({"Name": locale_name})
    #         for data in myDoc:
    #             print(data)
    #             compare_lat.append(data["Latitude"])
    #             compare_long.append(data["Longitude"])
    #
    #     coordinates = (user_lat, user_long)
    #     reverseGeocode(coordinates)
    #
    #     # function for latitude
    #     import numpy as np
    #     def find_nearest_lat(lat_list, latitude):
    #         lat_list = np.asarray(lat_list)
    #         idx = (np.abs(lat_list - latitude)).argmin()
    #         return lat_list[idx]
    #
    #
    #     lat_list = np.random.random(10)
    #
    #     lat_list = []
    #
    #     x = 0
    #     for i in compare_lat:
    #         bob = (compare_lat[x])
    #         lat_list.append(float(bob))
    #         x += 1
    #
    #     closest_lat = (find_nearest_lat(lat_list, user_lat))
    #     # print(closest_lat)
    #
    #     # same function for longitude
    #     import numpy as np
    #     def find_nearest_long(long_list, longitude):
    #         long_list = np.asarray(long_list)
    #         idx = (np.abs(long_list - longitude)).argmin()
    #         return long_list[idx]
    #
    #     long_list = np.random.random(10)
    #
    #     long_list = []
    #     x = 0
    #     for i in compare_long:
    #         bob = (compare_long[x])
    #         long_list.append(float(bob))
    #         x += 1
    #     closest_long = (find_nearest_long(long_list, user_long))
    #
    #
    #     closest_lat = str(closest_lat)
    #     closest_set = (collectioncoordinates.find_one({"Latitude": closest_lat}))
    #     closest_beach_lat = closest_set["Location"]
    #     print(closest_beach_lat)
    #
    #     closest_long = str(closest_long)
    #     closest_set_long = (collectioncoordinates.find_one({"Longitude": closest_long}))
    #     closest_beach_long = closest_set_long["Location"]
    #     print(closest_beach_long)
    #
    #
    #     #if closest_beach_lat == closest_beach_long:
    #         #submission_dict["Location"] = closest_beach_long
    #
    #     #if closest_beach_lat != closest_beach_long:
    #         #submission_dict["Location"] = "invalid"

    except:
        print(" ")
    turtleupload.insert_one(submission_dict)
    return render(request, 'thankyoupage.html')



# def submitform(request, animal):
#      #temporarily turning off image to prove concept
#      # result = sealupload.find({}, {"_id": 1})
#      # objectID = []
#      # for i in result:
#      #    p = i.get("_id")
#      #    objectID.append(p)
#      print("YES")
#      submission_dict = {}
#      fname = request.POST.get('fname')
#      lname = request.POST.get('lname')
#      pnumber = request.POST.get('pnumber')
#      datetime = request.POST.get('datetime')
#      animalcharacteristics = request.POST.getlist('Animal Characteristics[]')
#      island = request.POST.get('island')
#      comment = request.POST.get('comment')
#      humans = request.POST.get('humans')
#      Longitude = request.POST.get('Longitude')
#      Latitude = request.POST.get('Latitude')
#      try:
#         submission_dict["_id"] = len(objectID)
#         submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3]
#         submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
#         submission_dict["Ticket_Number"] = "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
#         submission_dict["Observer"] = fname + " " + lname
#         submission_dict["Observer_Contact_Number"] = pnumber
#         submission_dict["Observer_Initals"] = fname[0] + lname[0]
#         submission_dict["animal characteristics"] = animalcharacteristics
#         submission_dict["island"] = island
#         submission_dict["comment"] = comment
#         submission_dict["humans"] = humans
#         submission_dict["Latitude"] = Latitude
#         submission_dict["Longitude"] = Longitude
#
#         # mongoID = len(objectID)
#         # if request.method == 'POST' and request.FILES['filename']:
#         #     myfile = request.FILES['filename']
#         #     fs = gridfs.GridFS(grid_database)
#         #     filename = fs.put(myfile, _id = mongoID, filename= "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
#         # submission_dict["imageID"] = mongoID
#      except IndexError:
#         print(" ")
#
#     #Old geolocation function
#     #  compare_lat = []
#     #  compare_long = []
#     #
#     # # add invalid something so if coord is way too off, beach is invalid
#     #
#     #  user_lat = 21.639158
#     #  user_long = -158.064262
#     #  try:
#     #     import reverse_geocoder as rg
#     #
#     #     def reverseGeocode(coordinates):
#     #         result = rg.search(coordinates)
#     #         for data in result:
#     #             locale_name = (data["name"])
#     #
#     #
#     #         # pulling coords with same name
#     #         myDoc = collectioncoordinates.find({"Name": locale_name})
#     #         for data in myDoc:
#     #             print(data)
#     #             compare_lat.append(data["Latitude"])
#     #             compare_long.append(data["Longitude"])
#     #
#     #     coordinates = (user_lat, user_long)
#     #     reverseGeocode(coordinates)
#     #
#     #     # function for latitude
#     #     import numpy as np
#     #     def find_nearest_lat(lat_list, latitude):
#     #         lat_list = np.asarray(lat_list)
#     #         idx = (np.abs(lat_list - latitude)).argmin()
#     #         return lat_list[idx]
#     #
#     #
#     #     lat_list = np.random.random(10)
#     #
#     #     lat_list = []
#     #
#     #     x = 0
#     #     for i in compare_lat:
#     #         bob = (compare_lat[x])
#     #         lat_list.append(float(bob))
#     #         x += 1
#     #
#     #     closest_lat = (find_nearest_lat(lat_list, user_lat))
#     #     # print(closest_lat)
#     #
#     #     # same function for longitude
#     #     import numpy as np
#     #     def find_nearest_long(long_list, longitude):
#     #         long_list = np.asarray(long_list)
#     #         idx = (np.abs(long_list - longitude)).argmin()
#     #         return long_list[idx]
#     #
#     #     long_list = np.random.random(10)
#     #
#     #     long_list = []
#     #     x = 0
#     #     for i in compare_long:
#     #         bob = (compare_long[x])
#     #         long_list.append(float(bob))
#     #         x += 1
#     #     closest_long = (find_nearest_long(long_list, user_long))
#     #
#     #
#     #     closest_lat = str(closest_lat)
#     #     closest_set = (collectioncoordinates.find_one({"Latitude": closest_lat}))
#     #     closest_beach_lat = closest_set["Location"]
#     #     print(closest_beach_lat)
#     #
#     #     closest_long = str(closest_long)
#     #     closest_set_long = (collectioncoordinates.find_one({"Longitude": closest_long}))
#     #     closest_beach_long = closest_set_long["Location"]
#     #     print(closest_beach_long)
#     #
#     #
#     #     #if closest_beach_lat == closest_beach_long:
#     #         #submission_dict["Location"] = closest_beach_long
#     #
#     #     #if closest_beach_lat != closest_beach_long:
#     #         #submission_dict["Location"] = "invalid"
#
#      except:
#          print(" ")
#      # sealupload.insert_one(submission_dict)
#      if animal == "seal":
#          print("seal")
#      if animal == "bird":
#          print("bird")
#      if animal == "turtle":
#          print("turtle")
#
#      return render(request, 'thankyoupage.html')


def hmar(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html')

    context = {
    "all_data" : collection.find({})
    }
    #print(type(context["all_data"]))
    return render(request, 'activereports.html',context)


def archive(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html')

    context = {
        "all_data": collection.find({})
    }
    # print(type(context["all_data"]))
    return render(request, 'archivereports.html', context)


def specificreport(request,ID):
    for i in sealupload.find({}):
       if i.get("Ticket_Number") == ID:
           theID = i.get("_id")
       else:
           theID = ""
    if i.get("Ticket_Number") == ID:
        base64_data = codecs.encode(sealFS.get(file_id = theID).read(), 'base64')
        image = base64_data.decode('utf-8')
    else:
        image = ""

    for i in turtleupload.find({}):
       if i.get("Ticket_Number") == ID:
           theID = i.get("_id")
       else:
           theID = ""
    if i.get("Ticket_Number") == ID:
        base64_data = codecs.encode(turtleFS.get(file_id = theID).read(), 'base64')
        image = base64_data.decode('utf-8')
    else:
        image = ""

    for i in birdupload.find({}):
       if i.get("Ticket_Number") == ID:
           theID = i.get("_id")
       else:
           theID = ""
    if i.get("Ticket_Number") == ID:
        base64_data = codecs.encode(birdFS.get(file_id = theID).read(), 'base64')
        image = base64_data.decode('utf-8')
    else:
        image = ""

    x = {
       "grid_data": {"photo": image}
    }
    y = x["grid_data"].get("photo")
    context = {
       "report_data" : collection.find({ "Ticket_Number": ID}),
       "grid_data" : y
    }
    return render(request, 'viewspecificreport.html', context=context)



def editform(request, ID):
    context = {
        "report_data": collection.find({ "Ticket_Number": ID})
    }

    return render(request, 'editform.html', context)


