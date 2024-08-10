import QtQuick 2.15
import QtQuick.Controls 2.15

//
// Weather view
//

Rectangle {
    id: weatherBox

    width: parent.width / 3
    height: 150
    anchors.top: parent.top
    anchors.right: parent.right
    anchors.topMargin: 0
    color: "#FFFFFF"

    Column {
        anchors.centerIn: parent
        width: parent.width * 0.9
        spacing: 5

        // Temperature row

        Row {
            spacing: 5
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                text: WeatherController && WeatherController.temperature + "°C"
                font.pixelSize: 24
                font.bold: true
                color: "black"
                verticalAlignment: Text.AlignVCenter
            }
        }

        // Windspeed row

        Row {
            spacing: 5
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                text: WeatherController ? "Windspeed: " + WeatherController.windspeed + " m/s" : ""
                font.pixelSize: 16
                color: "black"
                verticalAlignment: Text.AlignVCenter
            }
        }

        // Warning info row

        Row {
            spacing: 5
            width: parent.width
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                horizontalAlignment: Text.AlignHCenter
                text: WeatherController && WeatherController.warning_info
                font.pixelSize: 16
                color: "black"
                maximumLineCount: 2
                width: parent.width 
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    // Ensuring that the weather is updated when program is started
    Component.onCompleted: {
        var city_name = PreferencesController.get_city();
        WeatherController.get_and_display_weather(city_name);
    }
}
