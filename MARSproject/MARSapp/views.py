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


def home(request):
    return render(request, 'homepage_final.html', )


def emergency(request):
    return render(request, 'emergency.html')

from django.views.decorators.cache import never_cache

@never_cache
def login(request):
    return render(request, 'login.html')


def formselect(request):
    return render(request, 'animalselect.html')


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
    island = request.POST.get('Island')
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

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = config("SENDER_EMAIL")
        receiver_email = config("RECEIVER_EMAIL")
        password = config("EMAIL_PASSWORD")
        message = """\
        Subject: Hi there

        This is an email."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except IndexError:
        print(" ")
#This is were the Lat and Long from the form will actually go (Temp values for uploading manually)
    user_lat = Latitude
    user_long = Longitude

    diff_of_lat = 0
    diff_of_long = 0

    compare_dict = {}
    for_min = []

    '''pulling options using beach name'''
    def reverseGeocode(coordinates):
        try:
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
        except:
            submission_dict["Location"] = "Not Near Beach"

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
    island = request.POST.get('Island')
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
        submission_dict["Phone_number"] = pnumber
        submission_dict["Observer_Initials"] = fname[0] + lname[0]
        submission_dict["animal_characteristics"] = animalcharacteristics
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

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = config("SENDER_EMAIL")
        receiver_email = config("RECEIVER_EMAIL")
        password = config("EMAIL_PASSWORD")
        message = """\
        Subject: Hi there

        This is an email."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except IndexError:
        print(" ")

    user_lat = Latitude
    user_long = Longitude

    diff_of_lat = 0
    diff_of_long = 0

    compare_dict = {}
    for_min = []

    '''pulling options using beach name'''

    def reverseGeocode(coordinates):
        try:
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
        except:
            submission_dict["Location"] = "Not Near Beach"

    coordinates = (user_lat, user_long)
    reverseGeocode(coordinates)

    birdupload.insert_one(submission_dict)
    return render(request, 'thankyoupage.html')


def turtlesubmit(request):
    result = turtleupload.find({}, {"_id": 1})
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
    island = request.POST.get('Island')
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
        submission_dict["Observer_Initials"] = fname[0] + lname[0]
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

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = config("SENDER_EMAIL")
        receiver_email = config("RECEIVER_EMAIL")
        password = config("EMAIL_PASSWORD")
        message = """\
        Subject: Hi there

        This is an email."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    except IndexError:
        print(" ")

    user_lat = Latitude
    user_long = Longitude

    diff_of_lat = 0
    diff_of_long = 0

    compare_dict = {}
    for_min = []

    '''pulling options using beach name'''

    def reverseGeocode(coordinates):
        try:
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

        except:
            submission_dict["Location"] = "Not Near Beach"

    coordinates = (user_lat, user_long)
    reverseGeocode(coordinates)

    turtleupload.insert_one(submission_dict)
    return render(request, 'thankyoupage.html')


#Base submit form function
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
    print(request.user.get_username)
    context = {
        "seal_data" : sealupload.find({}),
        "bird_data" : birdupload.find({}),
        "turtle_data": turtleupload.find({}),
    }
    #print(type(context["all_data"]))
    return render(request, 'activereports.html',context)


# def archive(request):
#     if not request.user.is_authenticated:
#         return render(request, 'error.html')
#
#     context = {
#         "all_data": collection.find({})
#     }
#     # print(type(context["all_data"]))
#     return render(request, 'archivereports.html', context)


def specificreport(request,ID):
    y = ""
    # try:
    if ID == "archive":
        context = {
        "seal_data" : sealupload.find({}),
        "bird_data" : birdupload.find({}),
        "turtle_data": turtleupload.find({}),
        "seal_archive": seal_collection.find({}),
        "bird_archive": bird_collection.find({}),
        }
        return render(request, 'archivereports.html', context)


    if ID == "exportdata":
        context = {
        "seal_data" : sealupload.find({}),
        "bird_data" : birdupload.find({}),
        "turtle_data": turtleupload.find({}),
        "seal_archive": seal_collection.find({}),
        "bird_archive": bird_collection.find({}),
        }
        print("exportdata")
        print(context["seal_archive"])
        return render(request, 'archivescript.html', context)


    else:
        type = ID[0]+ID[1]
        if type == "OS":

            #change to specific upload database
            #later add try except to also search for archived

            for i in sealupload.find({}):

                if i.get("Ticket_Number") == ID:
                    theID = i.get("_id")
                else:
                    theID = ""
                if i.get("Ticket_Number") == ID:
                    base64_data = codecs.encode(sealFS.get(file_id=theID).read(), 'base64')
                    image = base64_data.decode('utf-8')
                    x = {
                        "grid_data": {"photo": image}
                    }
                    y = x["grid_data"].get("photo")


            # context = {
            #     "report_data": seal_collection.find({"Ticket_Number": ID}),
            #     "grid_data": y
            # }
            for i in sealupload.find({}):
                if i["Ticket_Number"] == ID:
                    context = {
                        "report_data": sealupload.find({"Ticket_Number": ID}),
                        "grid_data": y
                    }
                    # print("upload")
                    break
                if i["Ticket_Number"] != ID:
                    context = {
                        "report_data": seal_collection.find({"Ticket_Number": ID}),
                        "grid_data": y
                    }
                    # print("arch")

            return render(request, 'seal_specificreport.html', context=context)
        if type == "OT":

            for i in turtleupload.find({}):
               if i.get("Ticket_Number") == ID:
                   theID = i.get("_id")
               else:
                   theID = ""
               if i.get("Ticket_Number") == ID:
                   base64_data = codecs.encode(turtleFS.get(file_id = theID).read(), 'base64')
                   image = base64_data.decode('utf-8')
                   x = {
                       "grid_data": {"photo": image}
                   }
                   y = x["grid_data"].get("photo")

            # context = {
            #     "report_data": seal_collection.find({"Ticket_Number": ID}),
            #     "grid_data": y
            # }
            return render(request, 'turtle_specificreport.html', context=context)

        if type == "OB":

            for i in birdupload.find({}):
               if i.get("Ticket_Number") == ID:
                   theID = i.get("_id")
               else:
                   theID = ""
               if i.get("Ticket_Number") == ID:
                   base64_data = codecs.encode(birdFS.get(file_id = theID).read(), 'base64')
                   image = base64_data.decode('utf-8')
                   x = {
                       "grid_data": {"photo": image}
                   }
                   y = x["grid_data"].get("photo")

            # context = {
            #     "report_data": bird_collection.find({"Ticket_Number": ID}),
            #     "grid_data": y
            # }
            # print(bird_collection.find({"Ticket_Number": ID}))
            for i in birdupload.find({}):
                if i["Ticket_Number"] == ID:
                    context = {
                        "report_data": birdupload.find({"Ticket_Number": ID}),
                        "grid_data": y
                    }
                    pass
                else:
                    context = {
                        "report_data": bird_collection.find({"Ticket_Number": ID}),
                        "grid_data": y
                    }




            return render(request, 'bird_specificreport.html', context=context)


        #return render(request, 'specificreport_final.html', context=context)
    # except ValueError:
    #     archive(request)



def editform(request, ID):
    # currently only 4 seal need to copy above for all animals
    for i in sealupload.find({}):
        if i["Ticket_Number"] == ID:
            context = {
                "report_data": sealupload.find({"Ticket_Number": ID}),
            }
            print("upload")
            break
        if i["Ticket_Number"] != ID:
            context = {
                "report_data": seal_collection.find({"Ticket_Number": ID}),
            }
            print("arch")

    return render(request, 'seal_edit.html', context)


def editredirect(request, ID):
    if not request.user.is_authenticated:
        return render(request, 'error.html')
    print("ran")
    context = {
        "seal_data" : sealupload.find({}),
        "bird_data" : birdupload.find({}),
        "turtle_data": turtleupload.find({}),
    }
    #Date = request.POST.get('Date')
    #Time = request.POST.get('Time')
    Location = request.POST.get('Location')
    Observer_Contact_Name = request.POST.get('Observer_Contact_Name')
    island = request.POST.get('island')
    comment = request.POST.get('comment')
    humans = request.POST.get('humans')
    Latitude = request.POST.get('Latitude')
    Longitude = request.POST.get('Longitude')
    Hotline_Operator_Initals = request.POST.get('Hotline_Operator_Initials')
    Ticket_Type = request.POST.get('Ticket_Type')
    Sighting = request.POST.get('Sighting')
    Survey = request.POST.get('Survey')
    Observer = request.POST.get('Observer')
    Observer_Initials = request.POST.get('Observer_Initials')
    Observer_Type = request.POST.get('Observer_Type')
    Public = request.POST.get('Public')
    Volunteer_slash_Staff = request.POST.get('Volunteer_slash_Staff')
    Agency = request.POST.get('Agency')
    Sector = request.POST.get('Sector')
    Location_Notes = request.POST.get('Location_Notes')
    Seal_Present = request.POST.get('Seal_Present')
    Seal_Present_Sighting = request.POST.get('Seal_Present_Sighting')
    Seal_Present_Survey = request.POST.get('Seal_Present_Survey')
    Size = request.POST.get('Size')
    Sex = request.POST.get('Sex')
    Beach_Position = request.POST.get('Beach_Position')
    How_Identified = request.POST.get('How_Identified')
    Tag = request.POST.get('Tag')
    Natural_Bleach = request.POST.get('Natural_Bleach')
    Applied_Bleach = request.POST.get('Applied_Bleach')
    Scars_slash_Features = request.POST.get('Scars_slash_Features')
    ID_Temp_Bleach_Number = request.POST.get('ID_Temp_Bleach_Number')
    Tag_Number = request.POST.get('Tag_Number')
    Tag_Side = request.POST.get('Tag_Side')
    Tag_Color = request.POST.get('Tag_Color')
    ID_Perm = request.POST.get('ID_Perm')
    Molt = request.POST.get('Molt')
    Additional_Notes_on_ID = request.POST.get('Additional_Notes_on_ID')
    ID_Verified_By = request.POST.get('ID_Verified_By')
    Seal_Bleached_Today = request.POST.get('Seal_Bleached_Today')
    Seal_Logging = request.POST.get('Seal_Logging')
    Mom_and_Pup_Pair = request.POST.get('Mom_and_Pup_Pair')
    Interaction_With_Human = request.POST.get('Interaction_With_Human')
    Disturbance_to_Seal = request.POST.get('Disturbance_to_Seal')
    Survival_Factor = request.POST.get('Survival_Factor')
    Handling_slash_Take = request.POST.get('Handling_slash_Take')
    SRA_Set_Up = request.POST.get('SRA_Set_Up')
    SRA_Type = request.POST.get('SRA_Type')
    SRA_Disturbance_Type = request.POST.get('SRA_Disturbance_Type')
    SRA_Length = request.POST.get('SRA_Length')
    SRA_Size_Width = request.POST.get('SRA_Size_Width')
    Number_of_Seals_in_SRA = request.POST.get('Number_of_Seals_in_SRA')
    SRA_Set_By = request.POST.get('SRA_Set_By')
    Number_of_Volunteers_Engaged = request.POST.get('Number_of_Volunteers_Engaged')
    Photos_Sent = request.POST.get('Photos_Sent')
    Seal_Depart_Info_Avail = request.POST.get('Seal_Depart_Info_Avail')
    Seal_Departed_Date = request.POST.get('Seal_Departed_Date')
    Seal_Departed_Time = request.POST.get('Seal_Departed_Time')
    Number_of_Calls_Received = request.POST.get('Number_of_Calls_Received')
    Other_Notes = request.POST.get("Other_Notes")
    Animal_Type = request.POST.get("Animal_Type")
    Ticket_Number = request.POST.get('Ticket_Number')


    editdict = {
        "Location": Location,
        "Observer_Contact_Name":Observer_Contact_Name,
        "island" : island,
        "comment":comment,
        "humans":humans,
        "Latitude":Latitude,
        "Longitude": Longitude,
        "Hotline_Operator_Initals":Hotline_Operator_Initals,
        "Ticket_Type":Ticket_Type,
        "Sighting":Sighting,
        "Survey":Survey,
        "Observer":Observer,
        "Observer_Initials":Observer_Initials,
        "Observer_Type": Observer_Type,
        "Public":Public,
        "Volunteer_slash_Staff":Volunteer_slash_Staff,
        "Agency":Agency,
        "Sector":Sector,
        "Location_Notes":Location_Notes,
        "Seal_Present":Seal_Present,
        "Seal_Present_Sighting":Seal_Present_Sighting,
        "Seal_Present_Survey":Seal_Present_Survey,
        "Size":Size,
        "Sex":Sex,
        "Beach_Position":Beach_Position,
        "How_Identified":How_Identified,
        "Tag":Tag,
        "Natural_Bleach":Natural_Bleach,
        "Applied_Bleach":Applied_Bleach,
        "Scars_slash_Features":Scars_slash_Features,
        "ID_Temp_Bleach_Number":ID_Temp_Bleach_Number,
        "Tag_Number":Tag_Number,
        "Tag_Side":Tag_Side,
        "Tag_Color":Tag_Color,
        "ID_Perm":ID_Perm,
        "Molt": Molt,
        "Additional_Notes_on_ID":Additional_Notes_on_ID,
        "ID_Verified_By":ID_Verified_By,
        "Seal_Bleached_Today":Seal_Bleached_Today,
        "Seal_Logging":Seal_Logging,
        "Mom_and_Pup_Pair":Mom_and_Pup_Pair,
        "Interaction_With_Human":Interaction_With_Human,
        "Disturbance_to_Seal":Disturbance_to_Seal,
        "Survival_Factor":Survival_Factor,
        "Handling_slash_Take":Handling_slash_Take,
        "SRA_Set_Up":SRA_Set_Up,
        "SRA_Type":SRA_Type,
        "SRA_Disturbance_Type":SRA_Disturbance_Type,
        "SRA_Length":SRA_Length,
        "SRA_Size_Width":SRA_Size_Width,
        "Number_of_Seals_in_SRA":Number_of_Seals_in_SRA,
        "SRA_Set_By":SRA_Set_By,
        "Number_of_Volunteers_Engaged":Number_of_Volunteers_Engaged,
        "Photos_Sent":Photos_Sent,
        "Seal_Depart_Info_Avail":Seal_Depart_Info_Avail,
        "Seal_Departed_Date":Seal_Departed_Date,
        "Seal_Departed_Time":Seal_Departed_Time,
        "Number_of_Calls_Received":Number_of_Calls_Received,
        "Other_Notes":Other_Notes,
        "Animal_Type":Animal_Type,
        "Ticket_Number":Ticket_Number
    }
    for i in sealupload.find({}):
        if i["Ticket_Number"] == editdict["Ticket_Number"]:
            db = sealupload
            break
        if i["Ticket_Number"] != editdict["Ticket_Number"]:
            db = seal_collection


    # # print(editdict)
    # test = db.find({"Ticket_Number": editdict["Ticket_Number"]})
    # for i in test:
    #     print(i)
    # 
    # db.update({"Ticket_Number": editdict["Ticket_Number"]}, {"$set": {"testfield": "test"}})
    print(db)
    for i in editdict:
        # print(i)
        # post = db.find({"Ticket_Number": editdict["Ticket_Number"]})
        # for i in post:
        #     print(i)
        db.update({"Ticket_Number": editdict["Ticket_Number"]}, {"$set":{i:editdict[i]}} )
        # print(editdict[i])

    return render(request, 'editsubmit.html',context)


#disabled for js only solution
# def csv_list_report(request):
#     print("export")
#     response = HttpResponse(mimetype='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="reports.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
#
#     for i in sealupload.find({}):
#         writer.writerow(i)
#     for i in birdupload.find({}):
#         writer.writerow(i)
#     for i in turtleupload.find({}):
#         writer.writerow(i)
#     for i in seal_collection.find({}):
#         writer.writerow(i)
#     for i in bird_collection.find({}):
#         writer.writerow(i)
#     return response