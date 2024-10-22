from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include('accounts.urls')),
    path('api/v1/', include('cards.urls')),
]
