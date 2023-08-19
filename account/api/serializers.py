from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from account.models import Profile
from rest_framework import serializers


# class PhoneNumberSerializer(serializers.Serializer):
#     number = PhoneNumberField(region="IE")


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
