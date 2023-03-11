from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, UserProfile

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
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=10)
    address = forms.Textarea()
    username = forms.CharField(max_length = 200)
    profile_picture = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "mobile_number", "address", "username", "email", "profile_picture", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.mobile_number = self.cleaned_data['mobile_number']
        user.profile_picture = self.cleaned_data['profile_picture']
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

