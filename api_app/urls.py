from django.urls import path
from .views import SummonerData

urlpatterns = [
    path('summoner-data/', SummonerData.as_view())
]