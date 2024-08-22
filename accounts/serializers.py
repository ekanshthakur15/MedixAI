from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

class ProfileSerialzer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)
    user = UserSerializer()
    gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES)
    
    class Meta:
        model = Profile
        fields = "__all__"
    
    def create(self, validated_data):

        user_data = validated_data.pop("user")
        profile = Profile.objects.create(**validated_data)
        User.objects.create(**user_data)

        return profile
    def update(self,instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.dob('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance