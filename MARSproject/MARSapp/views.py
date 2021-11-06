from django.shortcuts import render
from pymongo import MongoClient
# Create your views here.

client = MongoClient("mongodb+srv://Payton_Ikeda:mililanihs@cluster0.lrsp5.mongodb.net/hacc_sample_database?retryWrites=true&w=majority")
database = client["hacc_sample_database"]
collection = database["hacc_sample_collection"]
upload = database["hacc_upload_collection"]


def home(request):
    return render(request, 'home.html', )
'''
def hmar(request):
    return render(request, 'hmar.html')
'''

def emergency(request):
    return render(request, 'emergency.html')

def login(request):
    return render(request, 'login.html')

def sighting(request):
    return render(request, 'sighting.html')

def submitform(request):
    submit = (request.POST.get('submit'))
    submission_dict = {}
    if (submit == "submitted"):
        fname = (request.POST.get('fname'))
        lname = (request.POST.get('lname'))
        pnumber = (request.POST.get('pnumber'))
        datetime = (request.POST.get('datetime'))
        animalcharacteristics = (request.POST.getlist('Animal Characteristics[]'))
        island = (request.POST.get('Island'))
        behavior = (request.POST.get('behavior'))
        interaction = (request.POST.get('interaction1'))
        humans = (request.POST.get('humans'))
        filename = (request.POST.get('filename'))
        latitude = (request.POST.get('latitude'))
        try:
            submission_dict["Date"] = datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3]
            submission_dict["Time"] = datetime[11] + datetime[12] + datetime[14] + datetime[15]
            submission_dict["Ticket_Number"] = "OS" +  datetime[5] + datetime[6] + datetime[8]+datetime[9]+datetime[2]+datetime[3] + datetime[11] + datetime[12] + datetime[14] + datetime[15]
            submission_dict["Observer"] = fname + " " + lname
            submission_dict["Observer_Contact_Number"]= pnumber
            submission_dict["Observer_Initals"] = fname[0] + lname[0]
            submission_dict["animal characteristics"] = animalcharacteristics
            submission_dict["island"]=island
            submission_dict["behavior"]=behavior
            submission_dict["interaction"]= interaction
            submission_dict["humans"]= humans
            submission_dict["filename"]=filename
            upload.insert_one(submission_dict)
        except IndexError:
            print()


    return render(request, 'thankyou.html')




def hmar(request):
    context = {
    "all_data" : collection.find({})
    }
    print(context)
    return render(request, 'hmarlanding.html',context)

def editform(request):
    return render(request, 'editform.html')

def viewspecificreport(request):
    return render(request, 'viewspecificreport.html')

