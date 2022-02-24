from django.shortcuts import render
from weather import models
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=32c8edf6d58415301925443283d480a6'
    if request.method == "POST":
        name = request.POST.get('name')
        models.City.objects.create(name=name)
        
    cities = models.City.objects.all()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        # print(city_weather)
        weather = {
            'city': city,
            'temperature':city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    
    context = {'weather_data': weather_data}
    return render(request, 'weather/index.html', context)