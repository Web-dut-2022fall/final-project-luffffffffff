from django.urls import path
from . import views

urlpatterns = [
    path(r'management/', views.BuildListAPIView.as_view()),
    path(r'house/', views.HouseAPIView.as_view()),
    path(r'cateList/', views.BuildList.as_view()),
    path(r'search/', views.BuildSearchAPIView.as_view()),
    path(r'search_house/', views.HouseSearchAPIView.as_view()),
    path(r'', views.BuildManageViewSet.as_view({
        'post': 'add',
        'patch': 'show',
        'delete': 'del_build',
        'put': 'change_build',
    })),
    path(r'House/', views.HouseManageViewSet.as_view({
        'post': 'add',
        'patch': 'show',
        'delete': 'del_house',
        'put': 'change_house',
    })),
]
