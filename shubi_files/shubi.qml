import QtQuick.Window 2.2
import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3


ApplicationWindow  {
    id: window
    visible: true
    width: 300
    height: 480
    title: qsTr("Shubi")
    maximumHeight: height
    maximumWidth: width

    minimumHeight: height
    minimumWidth: width

    signal clicked(string id)
    Text {
        id: text1
        x: 27
        y: 0
        width: 247
        height: 74
        text: qsTr("Shubi")
        anchors.horizontalCenter: parent.horizontalCenter
        font.bold: true
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 40
    }

    ColumnLayout {
        id: columnLayout
        x: 26
        y: 75
        width: 247
        height: 380


        SwitchDelegate {
            id: switchServer
            objectName: "switchServer"
            text: qsTr("Server")
            font.pointSize: 19
            transformOrigin: Item.Center
            Layout.fillWidth: true
            onClicked: {
                shubi.click_switch("server", this.checked)
            }
        }

        Button {
            id: buttonWebsite
            width: 147
            height: 28
            text: qsTr("website")
            font.pointSize: 12
            Layout.fillWidth: true
            onClicked: {
                shubi.click_button("website")
            }
        }

        SwitchDelegate {
            id: switchClient
            objectName: "switchClient"
            text: qsTr("Client")
            font.pointSize: 19
            transformOrigin: Item.Center
            Layout.fillWidth: true
            onClicked: {
                shubi.click_switch("client", this.checked)
            }
        }


        SwitchDelegate {
            id: switchAutostart
            objectName: "switchAutostart"
            text: qsTr("Autostart")
            font.pointSize: 19
            transformOrigin: Item.Center
            Layout.fillWidth: true
            onClicked: {
                shubi.click_switch("autostart", this.checked)
            }
        }


        Button {
            id: buttonUpdate
            text: qsTr("Check for updates")
            font.pointSize: 12

            Layout.fillWidth: true
            onClicked: {
                shubi.click_button("update")
            }
        }




    }

 Connections {
        target: shubi

    }


onClosing: {
        close.accepted = false;
        shubi.exiting()
    }

}
