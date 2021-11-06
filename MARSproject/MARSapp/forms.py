from django import forms
from .models import formdata

class formdata(forms.ModelForm):
    class Meta:
        model = formdata
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'date',
            'island',
            'longitude',
            'identifying_characteristics',
            'animal_behavior',
            'number_of_beach_goers',
            'picture',
        ]
