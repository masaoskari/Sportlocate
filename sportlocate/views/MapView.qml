import QtQuick 2.15
import QtQuick.Controls 2.15
import QtWebEngine 1.0

//
// MapView
//

Rectangle {
    width: parent.width
    height: parent.height
    color: "#F0F0F0"

    // Visualizes the actual map
    WebEngineView {
        id: webview
        width: parent.width * 2/3
        height: parent.height
    }

    // In map view there is those WeatherBox, VenueList, CityBox, VenueDetailBox and button components
    // These components are defined in separate qml files

    // WeatherBox shows the weather
    WeatherBox {}

    // VenueList shows the venue list view on the right hand side off the view
    VenueList {}

    // CityBox shows those cities that are available for user
    CityBox {}

    // Buttons to view
    RecommendationButton {}
    PreferencesButton {}

    // VenueDetailBox is used to like pop up box to show more precise venue details
    VenueDetailBox{}

    // BusyIndicator shows when the app is loading things for example fetching the
    // venue data from APIs.
    BusyIndicator {
        id: busyIndicator

        anchors.centerIn: parent
        width: 100
        height: 100
        running: false
    }

    // Dialog box to show if there are no recommendations available with the
    // user given preferences
    Dialog {
        id: noRecommendationDialog
        
        title: "No Recommendation"
        Text {
            text: "No recommendation available, change preferences!"
        }
        visible: false
    }

    // Connections to different MapController signals
    Connections {
        target: MapController
        function onMapUpdated() {
            webview.loadHtml(MapController.map_html);
        }
        function onNoRecommendation() {
            noRecommendationDialog.open();
        }
       function onStartIndicator() {
            busyIndicator.running = true;
        }
        function onStopIndicator() {
            busyIndicator.running = false;
        }
    }

}