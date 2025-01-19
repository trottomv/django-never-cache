from django.http import HttpResponse
from django.urls import path


def view(_request):
    return HttpResponse()


urlpatterns = [path("", view)]
