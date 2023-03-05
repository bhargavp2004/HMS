from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room

class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES = (
        ('WithAc', 'AC'),
        ('WithoutAc', 'NON-AC'),
        ('Deluxe', 'DELUXE'),
    )
    room_category = forms.ChoiceField(choices = ROOM_CATEGORIES, required=True)
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)

    def __str__(self):
        return f'{self.room_category}'
    
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RoomSearchForm(forms.Form):
    ROOM_CATEGORIES = (
        ('WithAc', 'AC'),
        ('WithoutAc', 'NON-AC'),
        ('Deluxe', 'DELUXE'),
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES)
    check_in = forms.DateField()
    check_out = forms.DateField()

class RoomForm(forms.ModelForm):
    class Meta :
        model = Room
        fields = '__all__'
    ROOM_CATEGORIES = [
        ('WithAc', 'AC'),
        ('WithoutAc', 'NON-AC'),
        ('Deluxe', 'DELUXE'),
    ]
    number = forms.IntegerField()
    category = forms.ChoiceField(choices = ROOM_CATEGORIES, required=True)
    capacity = forms.IntegerField()
    room_description = forms.Textarea()

