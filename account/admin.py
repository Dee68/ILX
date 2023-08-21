from django.contrib import admin
from .models import User, Profile
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']
    exclude = ['password1']


admin.site.register(User, UserAdmin)


class PhoneForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='IE'),
        }


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'county', 'phone_number', 'image_tag']
    #form = PhoneForm
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
