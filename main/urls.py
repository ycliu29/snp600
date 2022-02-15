from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('ticker/<str:ticker>',views.detailed_view,name='detailed_view')
]