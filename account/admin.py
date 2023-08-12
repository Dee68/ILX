from django.contrib import admin
from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']
    exclude = ['password1']


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'county', 'phone_number', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
