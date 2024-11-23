import requests
from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City
from decouple import config


def fetch_weather_data(city_name, token_key):
    """
    Fetch weather data for a given city from OpenWeatherMap API.

    Parameters:
        city_name (str): The name of the city.
        token_key (str): API key for OpenWeatherMap.

    Returns:
        dict or None: Weather data if successful, otherwise None.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={token_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def index(request):
    """
    Handle adding new cities and display weather data for saved cities.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: Rendered index page with weather data.
    """
    token_key = config('TOKEN_KEY', '')
    message = ''
    message_class = ''

    # Handle POST request to add a new city
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            if not City.objects.filter(name__iexact=new_city).exists():
                weather_data = fetch_weather_data(new_city, token_key)
                if weather_data:
                    form.save()
                    message = "City added successfully!"
                    message_class = "alert-success"
                else:
                    message = "City does not exist!"
                    message_class = "alert-danger"
            else:
                message = "City already exists in the database!"
                message_class = "alert-danger"

    # Retrieve weather data for all saved cities
    form = CityForm()
    cities = City.objects.all()
    weather_data_list = []

    for city in cities:
        weather_data = fetch_weather_data(city.name, token_key)
        if weather_data:
            weather_data_list.append({
                'city': city.name,
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'icon': weather_data['weather'][0]['icon'],
            })

    # Prepare the context
    context = {
        'weather_data': weather_data_list,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather/weather.html', context)


def about(request):
    """
    Render the about page.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: The rendered about page.
    """
    return render(request, 'weather/about.html')


def delete_city(request, city_name):
    """
    Delete a city from the database.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.
        city_name (str): The name of the city to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the index page after deletion.
    """
    City.objects.filter(name__iexact=city_name).delete()
    return redirect('home')


def help(request):
    """
    Render the help page.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: The rendered help page.
    """
    return render(request, 'weather/help.html')
