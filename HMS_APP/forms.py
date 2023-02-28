from django import forms

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
    


