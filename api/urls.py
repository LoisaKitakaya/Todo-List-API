from django.urls import path
from api import views

urlpatterns = [
    path('todo-list/admin/', views.TodoListView.as_view()),
    path('create-account/', views.create_account),
    path('generate-token/', views.generate_token),
    path('todo-list/', views.todo_list),
    path('todo-item/<str:id>/', views.todo_item),
]