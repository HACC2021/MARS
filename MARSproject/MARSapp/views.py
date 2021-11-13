from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
from PIL import Image
from decouple import config
import gridfs
import codecs


# Create your views here.

client = MongoClient(config('DB_HOST'))
database = client["hacc_sample_database"]
collection = database["hacc_upload_collection"] #for all data
upload = database["hacc_upload_collection"] #for report submissions
grid_database = client["gridfs_database"]

fs = gridfs.GridFS(grid_database)

def home(request):
    return render(request, 'homepage_final2.html', )


def emergency(request):
    return render(request, 'emergency_final.html')


def login(request):
    return render(request, 'login.html')


def sealform(request):
    return render(request, 'sightingform_final2.html')

def whichform(request):
    return render(request, 'pickform.html')

def turtleform(request):
    return render(request, 'copysightingform_turtle.html')

def birdform(request):
    return render(request, 'copysightingform_turtle.html')

def submitform(request):
   result = upload.find({}, {"_id": 1})
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
   comment = request.POST.get('commment')
   humans = request.POST.get('humans')
   coordinates = request.POST.get('valuenow')
   coord2 = request.POST.get('valuenow2')
   print(coordinates)
   print("hi")
   print(coord2)
   try:
       submission_dict["_id"] = len(objectID)
       submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3]
       submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
       submission_dict["Ticket_Number"] = "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
       submission_dict["Observer"] = fname + " " + lname
       submission_dict["Observer_Contact_Number"] = pnumber
       submission_dict["Observer_Initals"] = fname[0] + lname[0]
       submission_dict["animal characteristics"] = animalcharacteristics
       submission_dict["island"] = island
       submission_dict["comment"] = comment
       submission_dict["humans"] = humans

       mongoID = len(objectID)
       if request.method == 'POST' and request.FILES['filename']:
           myfile = request.FILES['filename']
           fs = gridfs.GridFS(grid_database)
           filename = fs.put(myfile, _id = mongoID, filename= "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15])
       submission_dict["imageID"] = mongoID
       upload.insert_one(submission_dict)


   except IndexError:
       print()


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
    for i in upload.find({}):
       if i.get("Ticket_Number") == ID:
           theID = i.get("_id")
       else:
           theID = ""
    if i.get("Ticket_Number") == ID:
        base64_data = codecs.encode(fs.get(file_id = theID).read(), 'base64')
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
    return render(request, 'viewspecificreport_new.html', context=context)



def editform(request, ID):
    context = {
        "report_data": collection.find({ "Ticket_Number": ID})
    }

    return render(request, 'editform_new.html', context)


