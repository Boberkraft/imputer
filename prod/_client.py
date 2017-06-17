import sys
from PyQt5 import QtWidgets, QtCore


class Imputer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.editor = QtWidgets.QLineEdit(self)
        self.editor.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.editor.move(25, 40)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )

        self.setGeometry(QtWidgets.qApp.desktop().width() - 20 - 200 + 50,
                         QtWidgets.qApp.desktop().height() - 40 - 20 - 100,
                         150,
                         100)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.terminate()
            return True
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Return:
                self.terminate()
        return False

    def terminate(self):
        self.deleteLater()
        tag = self.editor.text()
        print(tag)
        exit()
        # r = requests.get('http://localhost:5000/get_image/{}'.format(tag))
        #
        # if r.status_code == 200 and r.text:
        #     path = r.text
        #     ClipBoard.paste(path, tag)


app = QtWidgets.QApplication(sys.argv)
imputer = Imputer()
imputer.show()

app.exec_()
exit(app.exec_())
