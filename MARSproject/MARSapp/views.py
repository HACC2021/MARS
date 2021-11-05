from django.shortcuts import render
from pymongo import MongoClient
# Create your views here.

client = MongoClient("mongodb+srv://Payton_Ikeda:mililanihs@cluster0.lrsp5.mongodb.net/hacc_sample_database?retryWrites=true&w=majority")
database = client["hacc_sample_database"]
collection = database["hacc_sample_collection"]


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
        animalcharacteristics = (request.POST.get('AnimalCharacteristics'))
        island = (request.POST.get('Island'))
        behavior = (request.POST.get('behavior'))
        interaction = (request.POST.get('interaction1'))
        humans = (request.POST.get('humans'))
        filename = (request.POST.get('filename'))
        latitude = (request.POST.get('latitude'))
        print(fname)
        print(type((fname)))
        submission_dict["first name"].append(fname)
        print(submission_dict)
        submission_dict["first name":fname]
        submission_dict["last name":lname]
        submission_dict["phone number":pnumber]
        submission_dict["datetime":datetime]
        submission_dict["animal characteristics":animalcharacteristics]
        submission_dict["island":island]
        submission_dict["behavior":behavior]
        submission_dict["interaction":interaction]
        submission_dict["humans":humans]
        submission_dict["filename":filename]
        print(submission_dict)


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
