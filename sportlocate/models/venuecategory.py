from __future__ import annotations
from dataclasses import dataclass
from abc import ABC


@dataclass
class VenueCategory(ABC):
    """
    Base class for different venue categories.

    Attributes:
        name (str): The name of the category.
    """

    name: str


@dataclass
class SportVenueCategory(VenueCategory):
    """
    Data class representing a sport venue category.

    Attributes:
        category_code (int): A unique code representing the sport venue category.
        sport_venue_types (list[int]): A list of sub-categories or types within the sport venue category.
    """

    category_code: int
    sport_venue_types: list[int]
