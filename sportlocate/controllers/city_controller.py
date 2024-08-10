from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

from sportlocate.models.city_model import CityModel


class CityController(QObject):
    """Handles the city ComboBox cities."""

    cities_changed = pyqtSignal(name="citiesChanged")

    def __init__(self):
        """Init."""
        super().__init__()
        self._city_model = CityModel()

    @pyqtProperty(list, notify=cities_changed)
    def cities(self):
        """Gets the city objects from CityModel and returns
        those to the view.
        """
        return self._city_model.cities
