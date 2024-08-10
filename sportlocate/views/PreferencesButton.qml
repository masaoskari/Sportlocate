import QtQuick 2.15
import QtQuick.Controls 2.15

//
// Map views preferences button
//

Button {
    text: "Preferences"
    anchors.bottom: parent.bottom
    anchors.right: parent.right
    anchors.bottomMargin: 10
    anchors.rightMargin: 10

    background: Rectangle {
        border.color: "#008080"
        border.width: 2
        radius: 5
        color: "white"

        width: parent.width
        height: parent.height
    }

    onClicked: stackLayout.currentIndex = 1
}
