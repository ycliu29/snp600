from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('create_account/',views.create_account,name='create_account'),
    path('',views.index,name='index'),
    path('ticker/<str:ticker>',views.detailed_view,name='detailed_view'),
]