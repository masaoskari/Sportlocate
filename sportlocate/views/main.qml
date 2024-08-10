import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.0

//
// The base view defined here. This should be kept as small as possible with generating
// own components like CityBox.qml is.
//

ApplicationWindow {
    id: main
    visible: true
    width: 1024
    height: 720

    StackLayout {
        id: stackLayout
        width: parent.width
        height: parent.height
        MapView{}
        PreferencesView{}
    }
}