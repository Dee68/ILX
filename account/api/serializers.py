from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from account.models import Profile
from rest_framework import serializers


class PhoneNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(region="IE")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'first_name',
            'last_name',
            'user',
            'street_address1',
            'city',
            'county',
            'phone_number',
            'postcode',
            'avatar',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user=user,
            street_address1=validated_data['street_address1'],
            city=validated_data['city'],
            county=validated_data['county'],
            phone_number=validated_data['phone_number'],
            postcode=validated_data['postcode'],
            avatar=validated_data['avatar']
        )
        return profile
