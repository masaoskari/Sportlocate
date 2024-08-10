import pytest

from sportlocate.models.venuemodel import VenueModel
from sportlocate.models.venuefactory import SportVenue
from sportlocate.models.sportvenuecategorymodel import SportVenueCategoryModel
from sportlocate.models.weathermodel import WeatherModel, WeatherData


@pytest.fixture
def venue_model():
    return VenueModel('sport')

def test_sport_venue_model_singleton(venue_model):
    model2 = VenueModel('sport')
    assert venue_model == model2

def test_get_filtered_sport_venues(venue_model):
    category_model = SportVenueCategoryModel()
    all_categories = category_model.sport_venue_categories
    some_categories = all_categories[0:3]
    filtered_sport_venues = venue_model.get_filtered_venues("akaa", some_categories)
    assert len(filtered_sport_venues) != 0

def test_get_sport_venue_recommendation(venue_model):
    weather_model = WeatherModel()
    weather_info = weather_model.get_weather_info("Tampere")
    # Before recommendation some city venues should be get from API
    category_model = SportVenueCategoryModel()
    all_categories = category_model.sport_venue_categories
    venue_model.get_filtered_venues("Tampere", all_categories)
    recommendation = venue_model.get_recommendation(weather_info)
    assert isinstance(recommendation, SportVenue)

def test_get_weather_info():
    weather_model = WeatherModel()
    weather_info = weather_model.get_weather_info("Tampere")
    assert isinstance(weather_info, WeatherData)
