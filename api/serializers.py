from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['usrname'] = user.username
        # ...

        return token

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'password2']

    def create(self, validated_data):
        user=User.objects.create_user(validated_data['username'].lower(), validated_data['email'].lower(), validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        userprofile = Profile.objects.create(user=user)
        userprofile.save()

        return validated_data
    
    def validate_email(self, email):
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email is already used')

        return email
    
    def validate_username(self, username):
        allowed_charahteres = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.']

        if (not (i in allowed_charahteres for i in username)):
            raise serializers.ValidationError('Username can only contain a-z 0-9 and .')
        
        username=username.lower()
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username is taken')
        
        return username
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password':'Password must match'})
        return data