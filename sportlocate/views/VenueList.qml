import QtQuick 2.15
import QtQuick.Controls 2.15

//
// VenueList
//

ListView {
    clip: true
    width: parent.width / 3 - 40
    height: parent.height - 150
    anchors.rightMargin: 20
    anchors.bottom: parent.bottom
    
    model: ListModel {
        id: venueModel
    }

    anchors.right: parent.right
    orientation: ListView.Vertical
    spacing: 10

    delegate: MouseArea {
        width: parent ? parent.width : 0
        height: 100
        onClicked: {
            MapController.set_selected_venue_id(model.id);
        }

        Rectangle {
            id: venueRectangle

            width: parent ? parent.width : 0
            height: 100
            border.color: "#008080"
            border.width: 2
            radius: 8

            // Text to display the venue name
            Text {
                id: venueText
                anchors.centerIn: parent
                text: model.name
                font.pixelSize: 16
            }

            // Define two states for those venue "cards" that are shown in the webview.
            states: [
                State {
                    name: "selected"
                    when: MapController && MapController.selected_venue_id === model.id
                    PropertyChanges {
                        target: venueRectangle
                        color: "#008080"
                    }
                    PropertyChanges {
                        target: venueText
                        color: "white"
                    }
                },
                State {
                    name: "unselected"
                    when: MapController && MapController.selected_venue_id !== model.id
                    PropertyChanges {
                        target: venueRectangle
                        color: "white"
                    }
                    PropertyChanges {
                        target: venueText
                        color: "black"
                    }
                }
            ]
        }
    }

    // Connecting the update signal to webview
    Connections {
        target: MapController
        function onVenuesChanged() {
            var venues = MapController.venues;
            venueModel.clear();
            for (var i = 0; i < venues.length; ++i) {
                venueModel.append(venues[i]);
            }
        }

    }
}
