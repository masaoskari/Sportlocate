from __future__ import annotations

from PyQt5.QtCore import QObject, pyqtSlot

from sportlocate.models.preferencesmodel import PreferencesModel


class PreferencesController(QObject):
    """Handles preferences view preferences. Fetch preferences from preferences model
    and updates those to preferences view."""

    def __init__(self):
        """Init."""
        super().__init__()
        self._preferences_model = PreferencesModel()

    @pyqtSlot(name="getPreferences", result=list)
    def get_preferences(self) -> list[dict]:
        """Current preferences can be fetch with this method from qml."""
        categories = self._preferences_model.all_categories
        preferences = self._preferences_model.get_preferences()
        dict_list = []
        for category in categories:
            if category not in preferences:
                obj_dict = {"name": category.name, "value": False}
            else:
                obj_dict = {"name": category.name, "value": True}

            dict_list.append(obj_dict)

        return dict_list

    @pyqtSlot(str, bool, name="setPreference")
    def set_preference(self, name: str, value: bool):
        """Updates/sets the preferences when user clicks checkboxes on qml side."""
        self._preferences_model.set_preferences(name, value)

    @pyqtSlot(str)
    def set_city(self, name: str):
        """Stores/sets the current city to model."""
        self._preferences_model.current_city = name

    @pyqtSlot(result=str)
    def get_city(self) -> str:
        """Method that can be used to fetch current city to qml side."""
        return self._preferences_model.current_city
