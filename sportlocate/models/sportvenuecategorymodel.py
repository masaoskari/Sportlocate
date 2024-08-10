from __future__ import annotations
from sportlocate.utils.apiclient import ApiClient
from sportlocate.models.venuecategory import SportVenueCategory

SPORT_VENUE_API_URL = "http://lipas.cc.jyu.fi/api"

# THis division is done so that we can categorize
# categories to indoor and outdoor categories
INDOOR_CATEGORY_CODES = [2000, 3000]
OUTDOOR_CATEGORY_CODE = [0, 1000, 4000, 5000, 6000]


class SportVenueCategoryModel:
    """SportVenueCategoryModel that handles sport venue categories.
    When model is created it fetches the category data from LIPAS API.

    Outdoor and indoor categories are used in sport venue recommendation and
    in general categories are used in sport venue filtering based on user input."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SportVenueCategoryModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Constructor for SortVenueCategoryModel"""
        self._api_client = ApiClient(SPORT_VENUE_API_URL)
        # All categories
        self._sport_venue_categories = []
        self._indoor_categories = []
        self._outdoor_categories = []
        # Fetch types to model when instance is created
        self._parse_sport_venue_categories()

    @property
    def indoor_categories(self) -> list[SportVenueCategory]:
        """Getter for indoor categories."""
        return self._indoor_categories

    @property
    def outdoor_categories(self) -> list[SportVenueCategory]:
        """Getter for outdoor categories."""
        return self._outdoor_categories

    @property
    def sport_venue_categories(self) -> list[SportVenueCategory]:
        """Getter for all categories."""
        return self._sport_venue_categories

    def _parse_sport_venue_categories(self):
        """Parses API data to model datastructures."""
        try:
            categories_data = self._api_client.get(f"/categories?lang=en")
            for category in categories_data:
                if category["typeCode"] in INDOOR_CATEGORY_CODES:
                    for sub_category in category["subCategories"]:
                        sport_venue_category = SportVenueCategory(
                            category_code=sub_category["typeCode"],
                            name=sub_category["name"],
                            sport_venue_types=sub_category["sportsPlaceTypes"],
                        )
                        self._indoor_categories.append(sport_venue_category)
                else:
                    for sub_category in category["subCategories"]:
                        sport_venue_category = SportVenueCategory(
                            category_code=sub_category["typeCode"],
                            name=sub_category["name"],
                            sport_venue_types=sub_category["sportsPlaceTypes"],
                        )
                        self._outdoor_categories.append(sport_venue_category)
                self._sport_venue_categories = (
                    self._indoor_categories + self._outdoor_categories
                )
        except Exception as e:
            print(f"An error occurred while parsing sport venue categories: {e}")
