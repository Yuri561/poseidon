import requests
from PIL import Image, ImageTk
import io

API_KEY = "897cb7af93dc77cc8639d0935e34a4d6"  # Replace with your API key
CITY = "Fayetteville"


def fetch_detailed_weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_details = {
            "temp": round(data["main"]["temp"] * 9 / 5 + 32, 1),  # Convert to Fahrenheit
            "feels_like": round(data["main"]["feels_like"] * 9 / 5 + 32, 1),
            "description": data["weather"][0]['description'].capitalize(),
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "humidity": data["main"]["humidity"],
            "clouds": data["clouds"]["all"],
            "pressure": data["main"]["pressure"],
            "icon_url": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"  # Full icon URL
        }
        return weather_details
    else:
        return None


def fetch_weather_icon(icon_url):
    response = requests.get(icon_url)
    if response.status_code == 200:
        icon_data = response.content
        icon_image = Image.open(io.BytesIO(icon_data))
        return icon_image.resize((100, 100))  # Resize the icon
    return None
