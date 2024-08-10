from __future__ import annotations

import random

from typing import Dict, Any
from abc import ABC, abstractmethod

from sportlocate.models.city_model import CityModel
from sportlocate.utils.apiclient import ApiClient
from sportlocate.models.venue import Venue, SportVenue, Coordinates
from sportlocate.models.weathermodel import WeatherData, ClearSky, PartlyCloudy
from sportlocate.models.sportvenuecategorymodel import SportVenueCategoryModel
from sportlocate.models.venuecategory import VenueCategory, SportVenueCategory

# Urls for venue apis:
SPORT_VENUE_API_URL = "http://lipas.cc.jyu.fi/api"
# add other urls here...


class VenueFactory(ABC):
    """
    Abstract factory base class for creating and managing venues different types
    of venues for example: sportvenues, reastaurants, cinemas, etc...

    Methods:
    - create_venue_categories(): Retrieve a list of venue categories.
    - create_venues(city: str): Retrieve a list of venues in a specified city.
    - create_filtered_venues(city: str, categories: list[VenueCategory]): Retrieve a
        list of venues filtered by categories.
    - create_recommendation(weather: WeatherData): Get a venue recommendation based on weather
        conditions.

    These methods are designed to be implemented by concrete subclasses for specific types of venues.
    """

    @abstractmethod
    def create_venue_categories(self) -> list[VenueCategory]:
        """
        Fetch/creates a list of venue categories.

        Returns:
            list[VenueCategory]: A list of venue categories for the specific venue type.
        """
        raise NotImplementedError

    @abstractmethod
    def create_venues(self, city: str) -> list[Venue]:
        """
        Creates a list of venues in a specified city.

        Args:
            city (str): The name of the city for which to fetch venues.

        Returns:
            list[Venue]: A list of venues in the specified city.
        """
        raise NotImplementedError

    @abstractmethod
    def create_filtered_venues(
        self, city: str, categories: list[VenueCategory]
    ) -> list[Venue]:
        """
        Creates a list of venues filtered by categories in a specified city.

        Args:
            city (str): The name of the city for which to fetch venues.
            categories (list[VenueCategory]): A list of accepted venue categories.

        Returns:
            list[Venue]: A list of venues in the specified city that match the accepted categories.
        """
        raise NotImplementedError

    @abstractmethod
    def create_recommendation(
        self, weather: WeatherData, current_venues: list[Venue]
    ) -> Venue:
        """
        Creates a venue recommendation based on weather conditions.

        Args:
            weather (WeatherData): Weather data used to make a venue recommendation.
            current_venues: list of venues which is taken along when recommendation is created.

        Returns:
            Venue: A recommended venue based on the provided weather data.
        """
        raise NotImplementedError


class SportVenueFactory(VenueFactory):
    """
    Factory for creating and managing sport venues. Factory fetches sport
    venue data from Lipas API.
    """

    def __init__(self):
        """Initialize a new instance of SportVenueFactory."""
        self._api_client = ApiClient(SPORT_VENUE_API_URL)
        # Factory stores fetched sportvenues to dict so that new api calls are not
        # nesseccary if user wants to see already fetched sportvenue information.
        self._sport_venues = {}
        self._cities = CityModel().cities_and_city_codes
        self._category_model = SportVenueCategoryModel()

    def create_venue_categories(self) -> list[SportVenueCategory]:
        """Fetch a list of sport venue categories from Lipas API."""
        return self._category_model.sport_venue_categories

    def create_venues(self, city: str) -> list[SportVenue]:
        """
        Fetch and return sport venues for a specific city.

        This method retrieves sport venue data for the specified city from the Lipas API.
        It first checks if the sport venues for the city are already cached, and if so,
        it returns the cached data. If not, it makes an API request to fetch the data,
        processes it, caches it, and returns the sport venues.

        Parameters:
            city (str): The name of the city.

        Returns:
            list: A list of SportVenue objects representing the sport venues for the city.
                  Returns an empty list if no sport venues are found.

        Raises:
            Exception: If an unexpected error occurs during the API request.

        """
        city = city.lower()
        if city in self._sport_venues:
            return self._sport_venues[city]
        else:
            try:
                sport_venue_list = self._api_client.get(
                    f"/sports-places?cityCodes={self._cities[city]}"
                )
                city_sport_venues = []

                for item in sport_venue_list:
                    sport_venue_data = self._api_client.get(
                        f"/sports-places/{item['sportsPlaceId']}?lang=en"
                    )
                    sport_venue = self._parse_sport_venue_data(sport_venue_data)
                    city_sport_venues.append(sport_venue)

                self._sport_venues.update({city: city_sport_venues})
                return city_sport_venues

            except Exception as e:
                raise (
                    f"An unexpected error occurred when trying to get city sports places: {e}"
                )

    def create_filtered_venues(
        self, city: str, venue_categories: list[SportVenueCategory]
    ) -> list[SportVenue]:
        """
        Get filtered sport venues for a specific city based on venue categories.

        Parameters:
            city (str): The name of the city.
            venue_categories (list[SportVenueCategory]): A list of SportVenueCategory instances
                specifying allowed sport venue types.

        Returns:
            list[SportVenue]: A list of SportVenue instances representing the filtered sport venues.
        """
        # Fetch city all sport venues
        city_sport_venues = self.create_venues(city)

        # Takes all allowed (based on filters) sport venue type codes to set
        sport_venue_type_codes = set()
        for venue_category in venue_categories:
            sport_venue_type_codes.update(venue_category.sport_venue_types)

        # Collecting filtered sport venues and keeping in track
        # that those are now current sport venues that are showed in map.
        filtered_sport_venues = []
        for sport_venue in city_sport_venues:
            if sport_venue.type_code in sport_venue_type_codes:
                filtered_sport_venues.append(sport_venue)
        return filtered_sport_venues

    def create_recommendation(
        self, weather: WeatherData, current_sport_venues: list[SportVenue]
    ) -> SportVenue:
        """
        Get a sport venue recommendation based on weather conditions.

        Parameters:
            weather: An object representing the current weather conditions.
            current_sport_venues: list of venues which is taken along when recommendation is created.

        Returns:
            SportVenue: A randomly selected SportVenue instance based on the weather conditions.

        Raises:
            Exception: If no suitable sport venue is found based on the weather conditions.

        """
        allowed_sport_venue_type_codes = set()
        # If weather is something else that clearsky or partlycloudy recommending the
        # indoor sports.
        if not isinstance(weather, ClearSky) and not isinstance(weather, PartlyCloudy):
            for category in self._category_model.indoor_categories:
                allowed_sport_venue_type_codes.update(category.sport_venue_types)
        # If the weather is good all categories are acceptable.
        else:
            for venue_type in self._category_model.sport_venue_categories:
                allowed_sport_venue_type_codes.update(venue_type.sport_venue_types)
        allowed_sport_venues = []
        for sport_venue in current_sport_venues:
            if sport_venue.type_code in allowed_sport_venue_type_codes:
                allowed_sport_venues.append(sport_venue)
        if len(allowed_sport_venues) == 0:
            return None
        else:
            # Taking random from list and setting it also to current sport venue
            recommendation = random.choice(allowed_sport_venues)
            return recommendation

    @staticmethod
    def _parse_sport_venue_data(sport_venue_data: Dict[str, Any]) -> SportVenue:
        """
        Parse sport venue data from JSON data.

        Parameters:
            sport_venue_data (dict): A dictionary containing sport venue data (keys are strings and
            data can be any type.

        Returns:
            SportVenue: An instance of the SportVenue class representing the parsed sport place data.
        """
        coordinates = Coordinates(
            lon=sport_venue_data["location"]["coordinates"]["wgs84"]["lon"],
            lat=sport_venue_data["location"]["coordinates"]["wgs84"]["lat"],
        )
        properties = sport_venue_data.get("properties", {})
        # Adjusting the long names to be smaller
        name = sport_venue_data["type"]["name"]
        if len(name.split(" ")) > 5:
            name = " ".join(name.split(" ")[0:5])
        return SportVenue(
            id=int(sport_venue_data["sportsPlaceId"]),
            name=name,
            type_code=int(sport_venue_data["type"]["typeCode"]),
            coordinates=coordinates,
            city_name=sport_venue_data["location"]["city"]["name"],
            info=properties.get("infoFi", ""),
        )
