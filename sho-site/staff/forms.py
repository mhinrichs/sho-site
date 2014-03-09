from datetime import datetime
from django import forms
from shobiz.models import Customer

class CustomerForm(forms.ModelForm):

    name = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    romaji = forms.CharField(max_length=100)
    post_code = forms.CharField(max_length=8)
    address1 = forms.CharField(max_length=100)
    address2 = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=13)
    email = forms.CharField(max_length=35)
    note = forms.CharField(
        required=False,
        widget = forms.Textarea,
        max_length = 150)
    created = forms.DateTimeField(required=False)
    modified = forms.DateTimeField(required=False)
    birthday = forms.DateTimeField(required=False)
    valid_profile = forms.BooleanField()
    picture = forms.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ('name', 'lastname', 'romaji', 'birthday', 'post_code', 'address1', 'address2', 'phone', 'email', 'note')
