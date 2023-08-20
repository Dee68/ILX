from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from account.models import Profile
from rest_framework import serializers


# class PhoneNumberSerializer(serializers.Serializer):
#     number = PhoneNumberField(region="IE")


class ProfileSerializer(serializers.ModelSerializer):
    user_applications = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    def get_user_applications(self, obj):
        queryset = Product.objects.filter(seller=obj.user)
        applications = ProductSerializer(queryset, many=True)
        return applications.data
        
    def get_user_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = '__all__'
