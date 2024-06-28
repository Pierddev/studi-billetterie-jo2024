from django.shortcuts import render


def index(request):
    return render(request, 'jo2024/index.html')