from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
from PIL import Image
import gridfs
from djongo.storage import GridFSStorage


# Create your views here.

client = MongoClient("mongodb+srv://Payton_Ikeda:mililanihs@cluster0.lrsp5.mongodb.net/hacc_sample_database?retryWrites=true&w=majority")
database = client["hacc_sample_database"]
collection = database["hacc_sample_seal_data"] #for all data
upload = database["hacc_upload_collection"] #for report submissions

fs = gridfs.GridFS(database)

def home(request):
    return render(request, 'home.html', )


def emergency(request):
    return render(request, 'emergency.html')


def login(request):
    return render(request, 'login.html')


def sighting(request):
    return render(request, 'sighting.html')


def submitform(request):
    submit = (request.POST.get('submit'))
    submission_dict = {}
    # if (submit == "submitted") and (request.POST.get('fname') != "")and (request.POST.get('lname') != "" and (request.POST.get('datetime') != "")):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    pnumber = request.POST.get('pnumber')
    datetime = request.POST.get('datetime')
    animalcharacteristics = request.POST.getlist('Animal Characteristics[]')
    island = request.POST.get('Island')
    behavior = request.POST.get('behavior')
    interaction = request.POST.get('interaction1')
    humans = request.POST.get('humans')
    coordinates = request.POST.get('coordinates')
    photo = request.FILES.get('photo')
        #print(type(photo))
        #print(photo)

#grab submission data and build upload dictionary
    try:
        submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3]
        submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Ticket_Number"] = "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
        submission_dict["Observer"] = fname + " " + lname
        submission_dict["Observer_Contact_Number"] = pnumber
        submission_dict["Observer_Initals"] = fname[0] + lname[0]
        submission_dict["animal characteristics"] = animalcharacteristics
        submission_dict["island"] = island
        submission_dict["behavior"] = behavior
        submission_dict["interaction"] = interaction
        submission_dict["humans"] = humans
        #submission_dict["photo"] = photo
        upload.insert_one(submission_dict)
        print(submission_dict)
    except IndexError:
        print("IndexError")

        with open(photo, 'rb') as f:
            contents = f.read()
        fs.put(contents, filename='photo')

    #currently if the entires are empty redirect to the form again (JS script in progress to reset for and check)
    # else:
    #     return render(request, "sighting.html")

    return render(request, 'thankyou.html')


def hmar(request):
    if not request.user.is_authenticated:
        return render(request, 'emergency.html')
    context = {
        "all_data" : collection.find({})
    }
    return render(request, 'hmarlanding.html',context)


def editform(request):
    return render(request, 'editform.html')


def specificreport(request,ID):
    # print(ID)
    # print(collection.find({"Ticket_Number": ID}))
    context = {
        "report_data" : collection.find({ "Ticket_Number": ID})
    }
    return render(request, 'viewspecificreport.html', context)



