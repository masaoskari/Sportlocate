import QtQuick 2.15
import QtQuick.Controls 2.15

//
// Recommendation button
//

Button {
    id: button

    text: "Recommend sport venue"
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.bottomMargin: 10
    anchors.leftMargin: 10

    background: Rectangle {
        border.color: "#008080"
        border.width: 2
        radius: 5
        color: "white"
        width: parent.width
        height: parent.height
    }

    // Two states for button
    //  current: the state when user can do recommendation by clicking that button
    //  recommendation: like backwards state to that current state
    states: [
        State {
            name: "current"
            PropertyChanges { target: button; text: "Recommend sport venue" }
        },
        State {
            name: "recommendation"
            PropertyChanges { target: button; text: "Show all venues" }
        }
    ]

    // Default state
    state: "current"

    // Button events
    onClicked: {
        if (button.state === "current") {
            // Change to recommendation state
            button.state = "recommendation";
            MapController.showRecommendation();
        } else {
            // Change to current state
            button.state = "current";
            MapController.showCurrentVenues();
        }
    }

    // Connection to that situation when CityBox changes the
    // map to show all venues based on user preferences.
    Connections {
        target: MapController
        function onCurrentVenuesRequested(){
            button.state = "current";

        }
    }
}
