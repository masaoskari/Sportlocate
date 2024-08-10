from __future__ import annotations

import folium

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QThreadPool

from sportlocate.models.venue import Venue
from sportlocate.models.venuemodel import VenueModel
from sportlocate.models.weathermodel import WeatherModel
from sportlocate.models.preferencesmodel import PreferencesModel
from sportlocate.utils.qmlworker import Worker


class MapController(QObject):
    """Controls the events on the mapview. Fetch data from needed models and provides that
    to qml side.
    """

    # Signals to qml side
    venues_changed = pyqtSignal(name="venuesChanged")
    map_updated = pyqtSignal(name="mapUpdated")
    no_recommendation = pyqtSignal(name="noRecommendation")
    current_venues_requested = pyqtSignal(name="currentVenuesRequested")
    venue_selected = pyqtSignal(name="venueSelected")
    start_indicator = pyqtSignal(name="startIndicator")
    stop_indicator = pyqtSignal(name="stopIndicator")

    def __init__(self, parent=None):
        """Init the map controller."""
        super().__init__(parent)
        self._map_html = ""
        self._current_map = None
        self._venue_model = VenueModel("sport")
        self._weather_model = WeatherModel()
        self._pref_model = PreferencesModel()
        self._last_lat = 0
        self._last_lon = 0
        self._painting_marker = False

    @pyqtProperty(str, constant=True)
    def map_html(self) -> str:
        """Map property for qml WebengineView."""
        return self._map_html

    @pyqtSlot(name="showRecommendation")
    def show_recommendation(self):
        """Handles the recommendation with models and Shows the recommendation on map."""
        weather = self._weather_model.current_weather
        recommendation = self._venue_model.get_recommendation(weather)
        if recommendation is None:
            self.no_recommendation.emit()
        else:
            self._draw_map([recommendation])

    @pyqtSlot(name="showCurrentVenues")
    def show_current_venues(self):
        """Handles the venue showing (based on user preferences) on the map."""
        # Starting indicator because this is heavy process (many API calls needs to be done)
        self.start_indicator.emit()
        preferences = self._pref_model.get_preferences()

        # Create a Worker instance
        worker = Worker(
            self._venue_model.get_filtered_venues,
            self._pref_model.current_city,
            preferences,
        )

        # Connect result signal to map drawing
        worker.signals.result.connect(self._draw_map)

        # Start the worker in the thread pool
        QThreadPool.globalInstance().start(worker)

        # Signaling to qml side that current venues are requested
        self.current_venues_requested.emit()

    @pyqtProperty(list, notify=venues_changed)
    def venues(self) -> list[object]:
        """Providing the venues to VenueDetailBox (view where venue details are shown).

        Venues must be converted to object format {"id": id, "name": name...} like so that qml side can
        show those straight.
        """
        return [venue.to_dict() for venue in self._venue_model.current_venues]

    @pyqtProperty(int, notify=venue_selected)
    def selected_venue_id(self) -> int:
        """User can select venue from VenueList. Method fetches the selected venue id
        from VenueModel and then provides it to qml side."""
        return self._venue_model.selected_venue

    @pyqtSlot(int)
    def set_selected_venue_id(self, venue_id: int):
        """Stores the user selected venue id to venue model and also paints the selected
        venue marker to the map.

        Args:
            venue_id (int): Selected venue id.

        """
        # Store selected venue id
        self._venue_model.selected_venue = venue_id
        self.venue_selected.emit()
        # Setting the selected venue marker paint flag true
        self._painting_marker = True
        # Draw map
        self._draw_map(self._venue_model.current_venues)

    def _draw_map(self, venues: list[Venue]):
        """Draws the map with updated information.

        Args:
            venues (list[Venue]): List of venues that needs to be drawn to map.
        """
        # Calculating map center coordinates based on venues that needs to be drawn to map.

        # If painting marker flag is set using selected venue coordinates as map center point.
        if self._painting_marker and self._venue_model.selected_venue > 0:
            for venue in venues:
                if venue.id == self._venue_model.selected_venue:
                    self._last_lat = venue.coordinates.lat
                    self._last_lon = venue.coordinates.lon
        # If there are more than 0 venues calculating venues middle point coordinates
        # If there is 0 venues last coordinates are used in center point.
        elif len(venues) > 0:
            self._last_lat = sum(venue.coordinates.lat for venue in venues) / len(
                venues
            )
            self._last_lon = sum(venue.coordinates.lon for venue in venues) / len(
                venues
            )

        # Creating map
        self._current_map = folium.Map(
            location=[self._last_lat, self._last_lon], zoom_start=10
        )

        # Adding markers to map
        for venue in venues:
            self._draw_marker_to_map(venue)

        # Rendering the map when all markers are drawn.
        self._map_html = self._current_map.get_root().render()

        # Signaling to qml that map venues are changed
        self.map_updated.emit()
        # this needs to be prevented so that list view position is not reset when painting marker.
        if not self._painting_marker:
            self.venues_changed.emit()
        self._painting_marker = False

        # Signaling to loader that software is ready.
        self.stop_indicator.emit()

    def _draw_marker_to_map(self, venue: Venue):
        """Helper that draws venue marker to map.
        Args:
            venue (Venue): Venue that marker is asked to draw to map.
        """
        # Tooltip font size
        font_size = "16px"

        # Writing the tooltip content with html
        tooltip_content = (
            f"<div style='font-size: {font_size}'>"
            f"<b>{venue.name}</b><br>"
            f"Coordinates:<br>"
            f"    lat: {venue.coordinates.lat:.2f}<br>"
            f"    lon: {venue.coordinates.lon:.2f} <br>"
            f"City: {venue.city_name}<br>"
            f"Info: {venue.info}</div>"
        )

        marker_color = "blue"
        if self._venue_model.selected_venue == venue.id:
            marker_color = "red"

        folium.Marker(
            [venue.coordinates.lat, venue.coordinates.lon],
            tooltip=tooltip_content,
            icon=folium.map.Icon(icon="star", color=marker_color),
        ).add_to(self._current_map)
