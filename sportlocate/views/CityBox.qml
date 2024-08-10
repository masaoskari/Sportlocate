import QtQuick 2.15
import QtQuick.Controls 2.15

//
// MapView's city combo box element defined here
//

ComboBox {
    id: cityComboBox

    textRole: "name"
    implicitWidth: 200
    implicitHeight: 30

    anchors.horizontalCenter: webview.horizontalCenter
    anchors.top: webview.top
    anchors.topMargin: 10

    model: CityController && CityController.cities

    background: Rectangle {
        border.color: "#008080"
        border.width: 2
        radius: 5
        color: "white"
        width: parent.width
        height: parent.height
    }

    // Changes the city in ComboBox
    currentIndex: {
        var city = PreferencesController && PreferencesController.get_city();
        if (model){
          for (var i = 0; i < model.length; ++i) {
            if (model[i].name === city) {
                return i;
            }
          }
        }
        return -1;
    }

    // When user has clicked the ComboBox city the weather and map is updated.
    onActivated: {
        if (currentIndex >= 0 && currentIndex < model.length) {
            var city_name = model[currentIndex].name;
            WeatherController.get_and_display_weather(city_name);
            PreferencesController.set_city(city_name);
            MapController.showCurrentVenues();

        }
    }

}
