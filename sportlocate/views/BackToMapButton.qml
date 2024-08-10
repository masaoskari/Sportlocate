import QtQuick 2.15
import QtQuick.Controls 2.15

//
// Preferences views back to map button
//

Button {
    id: button
    text: "Switch to map"
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

    onClicked: () => {
        stackLayout.currentIndex = 0;
        MapController.set_selected_venue_id(-1);
    }
}
