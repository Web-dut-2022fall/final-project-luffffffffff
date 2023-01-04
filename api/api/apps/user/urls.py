from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from . import views

urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path(r'', views.UserAPIView.as_view()),
    path(r'management/', views.UserListAPIView.as_view()),
    path(r'search/', views.UserSearchAPIView.as_view()),
    path(r'info/', views.SaveAPIView.as_view({
        'post': 'add',
        'patch': 'show',
        'delete': 'del_user',
        'put': 'change_user',
    })),
]
