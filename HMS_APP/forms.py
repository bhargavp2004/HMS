from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, UserProfile
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

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
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

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
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_in < datetime.now().date():
            raise ValidationError(("Check-in date cannot be in the past."))

        if check_in and check_out and check_out < check_in:
            raise ValidationError(("Check-out date cannot be before check-in date."))

class RoomForm(forms.ModelForm):
    class Meta :
        model = Room
        fields = '__all__'
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Room Number'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Room Capacity'}),
            'room_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Room Description'}),
            'room_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price Per Day'}),
        }

class UpdateInformationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['category', 'capacity', 'room_description', 'room_picture', 'room_price']

        ROOM_CATEGORIES = [        ('WithAc', 'AC'),        ('WithoutAc', 'NON-AC'),        ('Deluxe', 'DELUXE'),    ]
        category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
        capacity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        room_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
        room_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
        room_price = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserUpdateInformationForm(forms.Form):
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    mobile_number = forms.CharField(max_length = 10)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    profile_picture = forms.ImageField()
    new_password = forms.CharField(widget=forms.PasswordInput)

class ImageForm(forms.Form):
    image = forms.ImageField()