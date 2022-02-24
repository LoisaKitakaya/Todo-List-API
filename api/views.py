from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import TodoList
from .serializers import TodoListSerializer, UserSerializer

# Create your views here.
# class based views
class TodoListView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = TodoList.objects.all()

    serializer_class = TodoListSerializer


# function based views
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response({'Action status': 'Account created successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'Action status': 'Error.'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_token(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:

        return Response({'Error': 'Please provide required credentials.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:

        return Response({'Error': 'Could not authenticate. Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    token = Token.objects.create(user=user)

    return Response({'Token': token.key}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):

    if request.method == 'GET':

        todo_list = TodoList.objects.filter(owner=request.user)

        serializer = TodoListSerializer(todo_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        serializer = TodoListSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(owner=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def todo_item(request, id):

    try:

        todo_item = TodoList.objects.get(id=id)

    except TodoList.DoesNotExist:

        return Response({'Error': 'Todo-List item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = TodoListSerializer(todo_item)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':

        serializer = TodoListSerializer(todo_item, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response({'Error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':

        todo_item.delete()

        return Response({'Action status': 'Todo-List item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)