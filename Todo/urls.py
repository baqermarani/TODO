from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path( '' , TaskList.as_view() , name = 'Task'),
    path("Task/<int:pk>" , TaskDetail.as_view() , name = 'Detail'),
    path('Task-create/' , TaskCreate.as_view() , name = 'Create'),
    path('Task-update/<int:pk>' , TaskUpdate.as_view() , name = 'Update' ),
    path('Task-delete/<int:pk>' , TaskDelete.as_view() , name = 'Delete' ),
    path('login/', Login.as_view(), name ='Login'),
    path('logout/', LogoutView.as_view(next_page = 'Login') , name = 'Logout'),
    path('rgister/' , RegisterPage.as_view() , name = 'register')
]