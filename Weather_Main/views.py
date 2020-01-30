from django.shortcuts import render, redirect
import requests
from .models import City
from .Form import CityForm


def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=ce822893aade93d25a251bf7307612f1'
    cities = City.objects.all()
    form = CityForm()
    message_class = ""
    msg = ""
    error_msg = ""

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=new_city).count()

            if existing_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = "City Dose Not Exists in the world."
            else:
                error_msg = "City already exists."

        if error_msg:
            msg = error_msg
            message_class = "alert-danger"
        else:
            msg = "City Added Successfully"
            message_class = "alert-success"

    Weather_Data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'City': city,
            'Temperature': r['main']['temp'],
            'Description': r['weather'][0]['description'],
            'Icon': r['weather'][0]['icon']
        }
        Weather_Data.append(city_weather)

    context = {
        'Weather_Detail': Weather_Data,
        'Form': form,
        'Msg': msg,
        'Msg_Class': message_class
    }

    return render(request, 'Wather_Main/Main.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
