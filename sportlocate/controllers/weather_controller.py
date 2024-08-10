from __future__ import annotations

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QThreadPool

from sportlocate.utils.qmlworker import Worker
from sportlocate.models.weathermodel import WeatherModel, WeatherData


class WeatherController(QObject):
    """Controller class for managing weather information."""

    # Signals
    temperature_changed = pyqtSignal(name="temperatureChanged")
    wind_speed_changed = pyqtSignal(name="windspeedChanged")
    weather_condition_changed = pyqtSignal(name="weatherconditionChanged")
    warning_info_changed = pyqtSignal(name="warningInfoChanged")
    start_indicator = pyqtSignal(name="startIndicator")

    def __init__(self):
        """Init."""
        super().__init__()
        self._weather_model = WeatherModel()
        self._temperature = ""
        self._windspeed = ""
        self._weathercondition = ""
        self._warning_info = ""

    @pyqtProperty(str, notify=temperature_changed)
    def temperature(self) -> str:
        """Returns temperature property (for qml side)."""
        return self._temperature

    @pyqtProperty(str, notify=wind_speed_changed)
    def windspeed(self) -> str:
        """Returns wind speed property (for qml side)."""
        return self._windspeed

    @pyqtProperty(str, notify=weather_condition_changed)
    def weather_condition(self) -> str:
        """Returns weather condition property (for qml side)."""
        return self._weathercondition

    @pyqtProperty(str, notify=warning_info_changed)
    def warning_info(self) -> str:
        """Returns warning info property (for qml side)."""
        return self._warning_info

    @pyqtSlot(str)
    def get_and_display_weather(self, city_name: str):
        """
        Fetch weather information for the specified city and update properties.

        Args:
            city_name (str): The name of the city for which weather information is fetched.
        """
        self.start_indicator.emit()
        worker = Worker(self._weather_model.get_weather_info, city_name)
        worker.signals.result.connect(self.update_weather)
        QThreadPool.globalInstance().start(worker)

    @pyqtSlot(object)
    def update_weather(self, weather_data: WeatherData):
        """
        Update properties with the fetched weather information. Also
        Signals qml that properties have changed.

        Args:
            weather_data (object): Object containing weather information.
        """
        if weather_data:
            self._temperature = str(weather_data.temperature)
            self._windspeed = str(weather_data.windspeed)
            self._warning_info = weather_data.warningInfo()
            self.temperature_changed.emit()
            self.wind_speed_changed.emit()
            self.weather_condition_changed.emit()
            self.warning_info_changed.emit()
        else:
            print("Failed to fetch weather data.")
