from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from account.models import Profile
from rest_framework import serializers
from product.models import Product
from product.serializers import ProductSerializer


User = get_user_model()

# class PhoneNumberSerializer(serializers.Serializer):
#     number = PhoneNumberField(region="IE")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user_applications = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    user_date = serializers.SerializerMethodField()

    def get_user_applications(self, obj):
        queryset = Product.objects.filter(seller=obj.user)
        applications = ProductSerializer(queryset, many=True)
        return applications.data
       
    def get_user_username(self, obj):
        return obj.user.username

    def get_user_date(self, obj):
        return obj.user.created_at

    class Meta:
        model = Profile
        fields = '__all__'
