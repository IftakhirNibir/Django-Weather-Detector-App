from django.shortcuts import render
import json
import urllib.request
from urllib.error import HTTPError 

# Create your views here.

import urllib.parse

def index(request):
    cityname = ""
    data = {}
    if request.method == "POST":
        cityname = request.POST['city']
        if cityname:
            try:
                # Encode the city name to handle spaces
                cityname_encoded = urllib.parse.quote(cityname)
                result  = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + cityname_encoded + '&appid=93ae6791d326edf8776513658aff39bf').read()
                json_data = json.loads(result)
                temp = float(json_data['main']['temp'])
                feels_like = float(json_data['main']['feels_like'])
                feels_like_C = feels_like - 273.15
                temp_C = temp - 273.15
                if feels_like_C < 0:
                    info = "Freezing"
                elif feels_like_C >=0 and feels_like_C <10:
                    info = "Cold"
                elif feels_like_C >=10 and feels_like_C <20:
                    info = "Mild"
                elif feels_like_C >=20 and feels_like_C <30:
                    info = "Warm"
                else:
                    info = "Hot"

                data = {
                    "temp" : f'{round(temp_C,2)}°C',
                    "feels_like" : f'{round(feels_like_C,2)}°C',
                    "short": str(json_data["sys"]["country"]),
                    "info": info,
                }
            except HTTPError as e:
                # Handle the HTTPError here
                error_message = "City name is not found. Please enter a valid city name."
                data = {"error_message": error_message}

    return render(request, 'index.html', {'cityname': cityname, 'data': data})


