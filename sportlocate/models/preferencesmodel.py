from __future__ import annotations

import json

from sportlocate.models.sportvenuecategorymodel import SportVenueCategoryModel
from sportlocate.models.venuecategory import VenueCategory

# Default city
DEFAULT_CITY = "Tampere"


class PreferencesModel:
    """Preferences model is singleton class that handles and stores user given preferences like
    last city that user has search and venue categories that user has chosen not to be shown on map.

    Stores only minimal amount of data (only those categories that user have checked out) to JSON file.

    Write to disc is done everytime when user changes preferences so that those are always correct
    if something happens for example program crashes.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create and return a new instance of PreferenceModel.

        This method ensures that only a single instance of PreferencesModel is created.
        If an instance already exists, it is returned; otherwise, a new instance is created.
        """
        if not cls._instance:
            cls._instance = super(PreferencesModel, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        """Init preferences model.
        1. Gets the all sport venue categories from SportVenueCategoryModel
        2. Reading user preferences from a disc.
        """
        self._all_categories = SportVenueCategoryModel().sport_venue_categories
        self._overrides = dict()
        self._city = DEFAULT_CITY
        self.read_from_disk()

    @property
    def all_categories(self) -> list[VenueCategory]:
        """Returns all categories so that those can be shown in preferences view."""
        return self._all_categories

    @property
    def current_city(self) -> str:
        """Current city that is stored in user preferences."""
        return self._city

    @current_city.setter
    def current_city(self, city: str):
        """Current city setter."""
        self._city = city
        self.write_to_disk()

    def get_preferences(self) -> list[VenueCategory]:
        """Getter for current venue categories that user wants to show in the map."""
        current_categories = []
        for category in self._all_categories:
            if category.name not in self._overrides:
                current_categories.append(category)
        return current_categories

    def set_preferences(self, name: str, value: bool):
        """Setting and saving user preferences (which type of venues user want to be shown in map)."""
        # Saving to overrides those values that are unchecked
        if not value:
            self._overrides[name] = value
        else:
            # If the value is true and an override exists, remove it
            if name in self._overrides:
                del self._overrides[name]

        self.write_to_disk()

    def write_to_disk(self):
        """Writes user preferences to disc."""
        # Ensuring that the city cannot be never nothing
        if self._city == "":
            self._city = DEFAULT_CITY
        serialized_data = {"overrides": self._overrides, "city": self._city}
        with open("preferences.json", "w") as f:
            json.dump(serialized_data, f)

    def read_from_disk(self):
        """Reads user preferences to disc."""
        try:
            with open("preferences.json", "r") as f:
                deserialized_data = json.load(f)
                self._overrides = deserialized_data.get("overrides", {})
                self._city = deserialized_data.get("city", {})
                # If city doesn't exist in preferences.json using default city.
                if self._city == "":
                    self._city = DEFAULT_CITY

        except FileNotFoundError:
            # If preferences.json file not found writes that to user disc with default settings.
            self.write_to_disk()
            print(
                "preferences.json not found, making that file and using default settings."
            )

        except json.JSONDecodeError:
            # If decode error resets the preferences and write those to disc.
            self._overrides = {}
            self._city = DEFAULT_CITY
            self.write_to_disk()
            print(
                "Error decoding preferences.json, resetting preferences.json and using default settings."
            )
