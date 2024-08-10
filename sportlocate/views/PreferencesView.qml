import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

//
// PreferencesView
//

Rectangle {
    width: parent.width
    height: parent.height
    color: "white"

    Text {
        horizontalAlignment: Text.AlignHCenter
        text: "Choose the categories of venues you'd like to view on the map"
        font.pixelSize: 30
        width: parent.width
    }

    Rectangle {
        y: 50
        width: parent.width
        height: parent.height - 100

        ScrollView {
            anchors.fill: parent
            width: parent.width
            height: parent.height
            clip: true
            Grid {
                columns: 2
                columnSpacing: 10
                rowSpacing: 10
                Repeater {
                    model: PreferencesController ? PreferencesController.getPreferences() : undefined
                    delegate: CheckBox {
                        font.pixelSize: 15
                        onCheckedChanged: {
                            PreferencesController.setPreference(modelData.name, checked);
                            MapController.showCurrentVenues();
                        }
                        checked: modelData.value
                        text: qsTr(modelData.name)
                    }
                }
            }
        }
    }

    BackToMapButton {}
}
