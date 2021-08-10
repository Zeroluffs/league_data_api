from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from riotwatcher import LolWatcher, ApiError
import pandas as pd
# Create your views here.
import matplotlib.pyplot as plt
import numpy as np
import io
import binascii
import base64
from api_app.plotting.plots import damage_dealt


@method_decorator(csrf_exempt, name="dispatch")
class SummonerData(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        summoner_name = data.get('summoner_name')
        nGames = data.get("nGames")
        region = data.get("region")
        imgdata = damage_dealt(summoner_name, nGames,region)
        return JsonResponse(imgdata, status=201, safe=False)
        # print(HttpResponse(imgdata,content_type="image/svg"))
        # return HttpResponse(imgdata,content_type="image/svg")
