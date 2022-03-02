from django.urls import path

from . import views

urlpatterns = [
    # account functions
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('create_account/',views.create_account,name='create_account'),
    # site content
    path('',views.index,name='index'),
    path('ticker/<str:ticker>',views.detailed_view,name='detailed_view'),
    path('following/',views.following,name='following'),
    # db update apis
    path('update_follow/',views.update_follow,name='update_follow'),
    path('update_notification_list/',views.update_notification_list,name='update_notification_list'),
    path('test_notification/',views.test_notification,name='test_notification')
]