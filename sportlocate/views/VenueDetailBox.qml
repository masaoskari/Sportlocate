import QtQuick 2.15
import QtQuick.Controls 2.15

//
// Venue detail pop up box
//

Rectangle {
    id: venueDetail

    visible: MapController && MapController.selected_venue_id != -1
    width: parent ? parent.width - parent.width / 3 : 0
    height: parent.height / 3
    anchors.bottom: parent.bottom
    color: "#FAFAFA"

    Component {
        id: detailRowComponent
        Row {
            width: parent.width
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5
            Text {
                horizontalAlignment: Text.AlignHCenter
                width: parent.width * 0.2       
                text: label
                font.pixelSize: 24
                color: "black"
                wrapMode: Text.WordWrap
            }
            Text {
                width: parent.width * 0.8     
                wrapMode: Text.WordWrap
                text: MapController && MapController.selected_venue_id != 0 
                ? ((venue => venue && venue[value])(MapController.venues.find(v => v.id == MapController.selected_venue_id)) || "")
                : ""
                font.pixelSize: 24
                color: "black"
            }
        }

    }    
    BackToMapButton {}
    // Here repeater moves the right venue field information to right list element
    Column {
        anchors.topMargin: 20
        anchors.fill: parent
        spacing: 5
        Repeater {
            model: ListModel {
                ListElement { label: "Name: "; value: "name"}
                ListElement { label: "Id: "; value: "id"}
                ListElement { label: "City: "; value: "city_name"}
                ListElement { label: "Info: "; value: "info"}
            }
            delegate: detailRowComponent
        }
    }


}