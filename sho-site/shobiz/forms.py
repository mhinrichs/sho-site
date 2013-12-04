from django import forms
from shobiz.models import Reservation

class ReservationForm(forms.ModelForm):

    name = forms.CharField(max_length = 50, help_text="Enter your name.")
    phone = forms.CharField(max_length = 13, help_text="Enter your phone number.")

    class Meta(self):
        model = Reservation
        fields = ('name', 'phone')

class SurveyForm(forms.ModelForm):

    services = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)

    class Meta(self):
        model = Reservation
        fields = ('services')
