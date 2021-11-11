from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
from PIL import Image
from decouple import config
import gridfs


# Create your views here.

client = MongoClient(config('DB_HOST'))
database = client["hacc_sample_database"]
collection = database["hacc_sample_seal_data"] #for all data
upload = database["hacc_upload_collection"] #for report submissions
grid_database = client["gridfs_database"]

fs = gridfs.GridFS(grid_database)

def home(request):
    return render(request, 'homepage_final.html', )


def emergency(request):
    return render(request, 'emergency_final.html')


def login(request):
    return render(request, 'login_final.html')


def sighting(request):
    return render(request, 'sightingform_final.html')


def submitform(request):
    '''
    submit = (request.POST.get('submit'))
    submission_dict = {}

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
        # upload.insert_one(submission_dict)
        if request.method == "POST" and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = gridfs.GridFS(grid_database)
            filename = fs.put(myfile, filename = "OS"+ datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
    except IndexError:
        print()'''
    return render(request, 'thankyou_new.html')


def hmar(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html')
    context = {
    "all_data" : collection.find({})
    }
    #print(type(context["all_data"]))
    return render(request, 'hmarlanding_new.html',context)


def specificreport(request,ID):
    print(ID)
    # print(collection.find({"Ticket_Number": ID}))
    context = {
        "ticket_ID": {"Identification":ID},
        "report_data" : collection.find({ "Ticket_Number": ID})
    }
    # for i in context["report_data"]:
    #     print(i)

    # for i in context["ticket_ID"]:
        # print(i["Identification"])
    # print(context["ticket_ID"]["Identification"])
    return render(request, 'viewspecificreport_new.html', context)


def editform(request, ID):
    context = {
        "report_data": collection.find({ "Ticket_Number": ID})
    }

    return render(request, 'editform_new.html', context)


