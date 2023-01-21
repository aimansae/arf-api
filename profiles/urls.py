from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view())
]   # as_view because its a clas based view