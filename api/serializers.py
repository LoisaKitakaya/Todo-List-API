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
        fields = ['username', 'email', 'password']