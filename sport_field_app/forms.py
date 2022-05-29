from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import SportDiscipline, SportFieldReservation


OPTIONS = []
sport_disciplines = SportDiscipline.objects.all()
for sd in sport_disciplines:
    OPTIONS.append((sd.id, sd.name))


class AddSportFieldForm(forms.Form):
    name = forms.CharField(max_length=128, label="Sport Field Name")
    size = forms.CharField(max_length=32, label="Sport Field Size (in meters)")
    disciplines = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=OPTIONS)
    lighting = forms.BooleanField(required=False, label="Lighting")
    latitude = forms.DecimalField(max_digits=8, decimal_places=6, label="Latitude",
                                  help_text="Click at the field on the map")
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, label="Longitude",
                                   help_text="Click at the field on the map")


class EditSportFieldForm(AddSportFieldForm):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)


class SportFieldReservationForm(forms.ModelForm):
    class Meta:
        model = SportFieldReservation
        fields = ["date", "comment"]


class SearchByNameForm(forms.Form):
    name = forms.CharField(label="Sport Field Name", max_length=128,
                           help_text="Search for fields containing given text string")


class SearchByDisciplineForm(forms.Form):
    discipline = forms.ChoiceField(choices=OPTIONS)


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=64)
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
