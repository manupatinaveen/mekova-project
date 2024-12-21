from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    is_superadmin = serializers.BooleanField(required=False, default=False)
    is_staff = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'confirm_password', 'profile_picture','is_superadmin', 'is_staff','is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
    
    
class UserGroupAssignmentSerializer(serializers.ModelSerializer):
    group = serializers.CharField()

    class Meta:
        model = User
        fields = ['group']

    def validate(self, attrs):
        group_name = attrs['group']
        if not Group.objects.filter(name=group_name).exists():
            raise serializers.ValidationError('Group does not exist')
        return attrs

    def update(self, instance, validated_data):
        group_name = validated_data['group']
        group = Group.objects.get(name=group_name)
        instance.groups.clear()  # Remove user from all groups
        instance.groups.add(group)
        instance.save()
        return instance