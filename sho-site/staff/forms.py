from django import forms
from shobiz.models import Customer

class CustomerForm(forms.ModelForm):


    name = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    romaji = forms.CharField(max_length=100)
    birthday = forms.DateTimeField(widget = forms.DateInput)
    post_code = forms.CharField(max_length=8)
    address1 = forms.CharField(max_length=100)
    address2 = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=13)
    email = forms.CharField(max_length=35)
    note = forms.CharField(widget = forms.Textarea,
                                       max_length = 150,
                                       help_text="Note about customer")

    entry_date = forms.DateTimeField(widget = forms.DateTimeInput)
    last_edited = forms.DateTimeField(widget = forms.DateTimeInput)
    birthday = forms.DateTimeField(widget = forms.DateTimeInput)
    valid_profile = forms.BooleanField()
    picture = forms.ImageField()

    class Meta:
        model = Customer
        fields = ('name', 'lastname', 'romaji', 'birthday', 'post_code', 'address1', 'address2', 'phone', 'email', 'note')
