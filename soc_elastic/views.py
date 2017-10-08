from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def show_siem_alerts(request):
    return render(request, 'offenses_from_elastic.html')