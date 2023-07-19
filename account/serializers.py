from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from account.models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=20,
        min_length=6,
        write_only=True)
    password1 = serializers.CharField(
        max_length=20,
        min_length=6,
        write_only=True)
    username = serializers.CharField(
        max_length=20,
        min_length=2,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        password1 = attrs.get('password1', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                {
                    'error'
                    : 'Only alphanumeric characters allowed in username field.'
                }
                )
        if password != password1:
            raise serializers.ValidationError({
                'error': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
