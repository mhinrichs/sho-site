from django import forms
from shobiz.models import Reservation, SurveyItem

class ReservationForm(forms.ModelForm):

    name = forms.CharField(max_length = 50, help_text="Enter your name.")
    phone = forms.CharField(max_length = 13, help_text="Enter your phone number.")
    services = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple(),                                                           queryset=SurveyItem.objects.all(),
                                              required=False,
                                              help_text="Select the services you are interested in:")
    customer_comment = forms.CharField(widget = forms.Textarea,
                                       max_length = 255,
                                       help_text="Personal message for Sho:")

    class Meta:
        model = Reservation
        fields = ('name', 'phone', 'services', 'customer_comment')
