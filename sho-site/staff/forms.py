from django import forms
from shobiz.models import Customer

class CustomerForm(forms.ModelForm):


    name = forms.CharField(max_length=30, help_text="First Name")
    lastname = forms.CharField(max_length=30, help_text="Last Name")
    romaji = forms.CharField(max_length=100, help_text="Romaji")
    birthday = forms.DateTimeField(widget = forms.DateInput, help_text="Birthday")
    post_code = forms.CharField(max_length=8, help_text = "Postal Code: XXX-XXXX")
    address1 = forms.CharField(max_length=100, help_text = "Address 1")
    address2 = forms.CharField(max_length=100, help_text = "Address 2")
    phone = forms.CharField(max_length=13, help_text = "Phone Number")
    email = forms.CharField(max_length=35, help_text = "E-mail Address")
    note = forms.CharField(widget = forms.Textarea,
                                       max_length = 150,
                                       help_text="Note about customer")

    entry_date = forms.DateTimeField(widget = forms.DateTimeInput, help_text = "Entry Date")
    last_edited = forms.DateTimeField(widget = forms.DateTimeInput, help_text="Last Edited")
    valid_profile = forms.BooleanField(help_text="Valid Profile")
    picture = forms.ImageField(help_text="Picture")

    class Meta:
        model = Customer
        fields = ('name', 'lastname', 'romaji', 'birthday', 'post_code', 'address1', 'address2', 'phone', 'email', 'note')
