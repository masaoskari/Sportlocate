from __future__ import annotations

from sportlocate.models.venue import Venue
from sportlocate.models.venuefactory import SportVenueFactory
from sportlocate.models.venuecategory import VenueCategory
from sportlocate.models.weathermodel import WeatherData


class VenueModel:
    """Venue model singleton class to handle venues in the map. Uses venue factories
    to create venues."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of VenueModel.

        Parameters:
            cls (type): The class type.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            VenueModel: The singleton instance of VenueModel.

        This method ensures that only a single instance of VenueModel is created.
        If an instance already exists, it is returned; otherwise, a new instance is created.
        """
        if not cls._instance:
            cls._instance = super(VenueModel, cls).__new__(cls)
        return cls._instance

    def __init__(self, venue_type):
        """
        Initialize a VenueModel instance.

        Args:
            venue_type (str): The type of venue for which to manage factories.

        Raises:
            ValueError: If the provided venue_type is not supported.

        Usage:
            The VenueModel is designed to manage different types of venues by selecting the appropriate
            factory class based on the venue_type. You can use this instance to retrieve venue categories,
            venues, filtered venues, and recommendations specific to the chosen venue type.
        """
        self._venue_type = venue_type
        self._factory_mapping = {
            "sport": SportVenueFactory(),
            # Add other venue types and their respective factory classes here
        }
        if self._venue_type not in self._factory_mapping:
            raise ValueError(f"Unsupported venue type: {self._venue_type}")
        self._venue_factory = self._factory_mapping[self._venue_type]
        self._current_venues = []  # Venues that are currently shown on map
        self._current_recommendation = None
        self._selected_venue_id = -1

    def get_venue_categories(self) -> list[VenueCategory]:
        """
        Get a list of venue categories specific to the managed venue type.

        Returns:
            list[VenueCategory]: A list of venue categories for the selected venue type.
        """
        return self._venue_factory.create_venue_categories()

    def get_filtered_venues(
        self, city: str, accepted_categories: list[VenueCategory]
    ) -> list[Venue]:
        """
        Get a list of venues in a city filtered by accepted categories.

        Args:
            city (str): The name of the city for which to fetch venues.
            accepted_categories (list[VenueCategory]): A list of accepted venue categories.

        Returns:
            list[Venue]: A list of venues in the specified city that match the accepted categories.
        """
        self._current_venues = self._venue_factory.create_filtered_venues(
            city, accepted_categories
        )
        return self._current_venues

    def get_recommendation(self, weather: WeatherData) -> Venue:
        """
        Get a venue recommendation based on weather conditions.

        Args:
            weather (WeatherData): Weather data used to make a venue recommendation.

        Returns:
            Venue: A recommended venue based on the provided weather data.
        """

        self._current_recommendation = self._venue_factory.create_recommendation(
            weather, self._current_venues
        )
        if self._current_recommendation is not None:
            self._current_venues = [self._current_recommendation]
        return self._current_recommendation

    @property
    def selected_venue(self) -> int:
        """Getter for selected venue id in venue list view."""
        return self._selected_venue_id

    @selected_venue.setter
    def selected_venue(self, venue_id: int):
        """Setter for selected venue id in venue list view."""
        self._selected_venue_id = venue_id

    @property
    def current_venues(self) -> list[Venue]:
        """Getter for current venues that are shown on the map."""
        return self._current_venues
