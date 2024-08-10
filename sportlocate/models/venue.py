from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, asdict


@dataclass
class Coordinates:
    """Coordinates dataclass for handling venue's coordinates."""

    lon: float
    lat: float


@dataclass
class Venue(ABC):
    """
    Represents a venue with basic information.

    Attributes:
        id (int): The unique identifier of the venue.
        name (str): The name of the venue.
        coordinates (Coordinates): The coordinates of the venue.
        city_name (str): The name of the city where the venue is located.
        info (str): Additional information about the venue.
    """

    coordinates: Coordinates
    id: int = -100
    name: str = ""
    city_name: str = ""
    info: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class SportVenue(Venue):
    """
    SportVenue dataclass for storing sport venue information.

    Attributes:
        type_code (int): The code representing the type of sport played at the venue.

        Other attributes that are inherited from Venue class:
                id (int): The unique identifier of the venue.
                name (str): The name of the venue.
                coordinates (Coordinates): The coordinates of the venue.
                city_name (str): The name of the city where the venue is located.
                info (str): Additional information about the venue.

    """

    type_code: int = -100
