"""
weathermodel.py

This module defines classes related to weather data modeling and retrieval.

Classes:
- WeatherData: Abstract base class representing weather data with common attributes.
- ClearSkyWeather: Subclass of WeatherData for clear sky weather conditions.
- CloudyWeather: Subclass of WeatherData for cloudy weather conditions.
- FoggyWeather: Subclass of WeatherData for foggy weather conditions.
- RainWeather: Subclass of WeatherData for rainy weather conditions.
- SnowWeather: Subclass of WeatherData for snowy weather conditions.
- ThunderstormWeather: Subclass of WeatherData for thunderstorm weather conditions.
- WeatherFactory: Factory class for creating specific weather instances based on data.
- WeatherDescriptions: Class providing weather condition descriptions based on codes.
- weatherService: Service class for retrieving weather information.
"""
import ssl
import geopy.geocoders
import certifi
from geopy.geocoders import Nominatim
from abc import ABCMeta, abstractmethod

from sportlocate.utils.apiclient import ApiClient

WEATHER_API_URL = "https://api.open-meteo.com"


class WeatherData(metaclass=ABCMeta):
    """
    Abstract base class representing common attributes for weather data.

    Attributes:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        temperature (float): The temperature at the location.
        windspeed (float): The wind speed at the location.
        weathercode (int): The code representing the weather condition.

    Methods:
        warningInfo(self) -> str: Abstract method to be implemented by subclasses.
    """

    def __init__(self, latitude, longitude, temperature, windspeed, weathercode):
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.windspeed = windspeed
        self.weathercode = weathercode

    @abstractmethod
    def warningInfo(self) -> str:
        """Warnings info property."""
        pass


class ClearSky(WeatherData):
    """ClearSky weather."""

    def warningInfo(self) -> str:
        return "Clear sky conditions. Enjoy the sunshine!"


class PartlyCloudy(WeatherData):
    """PartlyCloudy weather."""

    def warningInfo(self) -> str:
        return "Partly cloudy conditions."


class FoggyWeather(WeatherData):
    """FoggyWeather."""

    def warningInfo(self) -> str:
        return "Foggy conditions. Drive safely and use headlights."


class RainWeather(WeatherData):
    """RainWeather."""

    def warningInfo(self) -> str:
        return "Rainy weather. Grab your raincoat or umbrella."


class SnowWeather(WeatherData):
    """SnowWeather."""

    def warningInfo(self) -> str:
        return "Snowfall expected. Bundle up and drive cautiously."


class ThunderstormWeather(WeatherData):
    """ThunderstormWeather."""

    def warningInfo(self) -> str:
        return "Thunderstorm alert. Stay indoors and away from windows."


class WeatherFactory:
    """Weather data factory."""

    @staticmethod
    def create_weather_data(data: dict) -> WeatherData:
        """
        Factory method to create a WeatherData instance based on input data.

        Parameters:
            data (dict): Weather data containing latitude, longitude, temperature, windspeed, and weathercode.

        Returns:
            WeatherData: An instance of the appropriate WeatherData subclass.
        """
        latitude = data["latitude"]
        longitude = data["longitude"]
        temperature = data["current_weather"]["temperature"]
        windspeed = data["current_weather"]["windspeed"]
        weathercode = data["current_weather"]["weathercode"]

        condition_categories = {
            (0,): "ClearSky",
            (1, 2, 3): "PartlyCloudy",
            (45, 48): "FoggyWeather",
            (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82): "RainWeather",
            (71, 73, 75, 77, 85, 86): "SnowWeather",
            (95, 96, 99): "ThunderstormWeather",
            # Add more conditions as needed
        }
        # Check if weathercode falls within a range
        weather_category = next(
            (
                category
                for codes, category in condition_categories.items()
                if weathercode in codes
            ),
            "WeatherData",
        )
        if weather_category == "ClearSky":
            return ClearSky(latitude, longitude, temperature, windspeed, weathercode)
        elif weather_category == "PartlyCloudy":
            return PartlyCloudy(
                latitude, longitude, temperature, windspeed, weathercode
            )
        elif weather_category == "FoggyWeather":
            return FoggyWeather(
                latitude, longitude, temperature, windspeed, weathercode
            )
        elif weather_category == "RainWeather":
            return RainWeather(latitude, longitude, temperature, windspeed, weathercode)
        elif weather_category == "ThunderstormWeather":
            return ThunderstormWeather(
                latitude, longitude, temperature, windspeed, weathercode
            )


class WeatherModel:
    """
    Weather Model class for retrieving weather information.

    Methods:
        get_weather_info(self, city_name: str): Get weather information for a given city.
        get_lat_long(city_name): Get latitude and longitude for a given city.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of WeatherModel.

        Parameters:
            cls (type): The class type.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            WeatherModel: The singleton instance of WeatherModel.

        This method ensures that only a single instance of WeatherModel is created.
        If an instance already exists, it is returned; otherwise, a new instance is created.
        """
        if not cls._instance:
            cls._instance = super(WeatherModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Init."""
        self._api_client = ApiClient(WEATHER_API_URL)
        self._weather_factory = WeatherFactory()
        self._current_weather = None

    @property
    def current_weather(self) -> WeatherData:
        """Getter for current weather."""
        return self._current_weather

    def get_weather_info(self, city_name: str) -> WeatherData:
        """
        Get weather information for a given city.

        Parameters:
            city_name (str): Name of the city.

        Returns:
            WeatherData: An instance of WeatherData representing the current weather conditions.
        """
        latitude, longitude = self.get_lat_long(city_name)
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": "auto",
        }
        raw_weather_data = self._api_client.get("/v1/forecast", params=params)
        weather_data = self._weather_factory.create_weather_data(raw_weather_data)
        self._current_weather = weather_data
        return self._current_weather

    @staticmethod
    def get_lat_long(city_name: str):
        """
        Get latitude and longitude for a given city.

        Parameters:
            city_name (str): Name of the city.

        Returns:
            tuple: A tuple containing latitude and longitude.
        """
        ctx = ssl.create_default_context(cafile=certifi.where())
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        geopy.geocoders.options.default_ssl_context = ctx
        geolocator = Nominatim(user_agent="software_project")
        location = geolocator.geocode(city_name)

        if location:
            return location.latitude, location.longitude
        else:
            return None
