from django.urls import path, include
from movies.api.v1 import views

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]