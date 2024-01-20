from django import forms
from django.db import models
from Admin.models import user, feedback
from Admin.models import area
from Admin.models import gallery
from Admin.models import pgdetails
from Admin.models import facility
from Admin.models import inquiry
from Admin.models import wishlist, pgowner
# from parsley.decorators import parsleyfy

class userFrom(forms.ModelForm):
    class Meta:
        model = user
        fields = ['user_name','password','email','contact', 'area_id','is_admin']


class pgownerForm(forms.ModelForm):
    class Meta:
        model = pgowner
        fields = ["owner_name", "email","password", "contact", "area_id"]



class areaForm(forms.ModelForm):
    class Meta:
        model = area
        fields = ["area_name", "pincode"]


class galleryForm(forms.ModelForm):
    gallery_name = forms.FileField()
    class Meta:
        model = gallery
        fields = ["gallery_name", "pg_id"]


class pgdetailsForm(forms.ModelForm):
    img = forms.FileField()

    class Meta:
        model = pgdetails
        fields = ["pg_name", "pg_type", "description", "img" ,"address", "area_id","owner_id","amount"]



class facilityForm(forms.ModelForm):
    class Meta:
        model = facility
        fields = ["facility_name", "description"]



class inquiryForm(forms.ModelForm):
    class Meta:
        model = inquiry
        fields = ["inquiry_title", "inquiry_type", "user_id", "email", "contact"]


class feedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ["feedback_id", "user_id", "pg_id" , "des","rate", "date"]



class wishlistForm(forms.ModelForm):
    class Meta:
        models = wishlist
        fields = ["date", "user_id", "pg_id"]

