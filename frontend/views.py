from django.shortcuts import render


def index(request):
    return render(request, "index.html")  # Name of your HTML file here


def tasks(request):
    return render(request, "tasks.html")
