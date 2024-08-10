import os
import sys

from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from controllers.mapcontroller import MapController
from controllers.preferences_controller import PreferencesController
from controllers.city_controller import CityController
from controllers.weather_controller import WeatherController


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QGuiApplication(sys.argv)
    app.setApplicationDisplayName("Sportlocate")
    engine = QQmlApplicationEngine()

    # Set controllers to available to qml side
    preferences = PreferencesController()
    engine.rootContext().setContextProperty("PreferencesController", preferences)

    mapController = MapController()
    engine.rootContext().setContextProperty("MapController", mapController)

    city_controller = CityController()
    engine.rootContext().setContextProperty("CityController", city_controller)

    weather_controller = WeatherController()
    engine.rootContext().setContextProperty("WeatherController", weather_controller)

    # Load qml to engine
    qml_file = os.fspath(Path(__file__).parent / "views" / "main.qml")
    engine.load(QUrl.fromLocalFile(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
