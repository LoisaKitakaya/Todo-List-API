from pyexpat import model
from rest_framework import serializers
from .models import TodoList
from django.contrib.auth.models import User

class TodoListSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = TodoList

        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ['username', 'email', 'first_name', 'last_name', 'password']

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):

        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user