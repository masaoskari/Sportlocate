from __future__ import annotations
import pandas as pd
from pathlib import Path


class CityModel:
    """CityModel singleton that stores city and city code information and
    serves that for SportVenue factory and also to UI side.

    Reads city/citycode information from .csv file. In the future that
    can be read for example using requests.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create and return a new instance of CityModel.

        This method ensures that only a single instance of CityModel is created.
        If an instance already exists, it is returned; otherwise, a new instance is created.
        """
        if not cls._instance:
            cls._instance = super(CityModel, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        """Init the model."""
        self._cities = []
        self._cities_and_city_codes = {}
        self._load_cities()

    @property
    def cities(self) -> list[object]:
        """Returns object list {name: "", code: ""}.
        Qml can apply these objects straight for example to
        ComboBox
        """
        return self._cities

    @property
    def cities_and_city_codes(self) -> dict:
        """Returns dict where the city name is key and the
        code is value.
        """
        return self._cities_and_city_codes

    def _load_cities(self):
        """Load cities information from csv-file. The file is from https://www.stat.fi/en/luokitukset/kunta/."""
        self._cities_and_city_codes = self.read_cities_and_city_codes()
        self._cities = [
            {"name": key.capitalize(), "code": value}
            for key, value in self._cities_and_city_codes.items()
        ]

    @staticmethod
    def read_cities_and_city_codes() -> dict:
        """
        Read city codes from a CSV file and return them as a dictionary.
        Returns:
            dict: A dictionary where city names are keys and their codes are values.
        """
        city_codes_file = Path(__file__).parent.parent / "data" / "city_codes.csv"
        # Using pandas to read .csv-file
        df = pd.read_csv(
            city_codes_file,
            sep=";",
            encoding="ISO-8859-1",
            converters={
                "code": lambda x: int(
                    x.replace("'", "")
                ),  # Removing extra '-marks from data
                "classificationItemName": lambda x: x.lower(),  # city names to lowercase
            },
        )
        return df.set_index("classificationItemName")["code"].to_dict()
