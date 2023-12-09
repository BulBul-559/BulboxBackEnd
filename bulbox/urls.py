from django.urls import path

from . import views

urlpatterns = [
    path('getToken/', views.getToken),
    path('postYouAskMe/', views.postYouAskMe),
    path('getYouAskMe/', views.getYouAskMe),
    path('postIAskYou/', views.postIAskYou),
    path('getIAskYouQues/', views.getIAskYouQues),
    path('getIAskYouDetails/', views.getIAskYouDetails),
    # path('sendMess/', views.sendMess),
]
