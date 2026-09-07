from django import forms
from django.forms import ModelForm
from .models import Buyer, Vendor, Profile, Order
from django.contrib.auth.forms import UserCreationForm


class VendorForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = Vendor
        fields = ('name', 'email', 'phone', 'age', 'company')


class BuyerForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    name = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ('name', 'email', 'phone', 'age')


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('location', 'info', )


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ('address', )