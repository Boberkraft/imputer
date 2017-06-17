import sys
from PyQt5 import QtGui, QtCore, QtWidgets, QtCore
import requests
from clipboard import ClipBoard


class Imputer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
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
            typed_text = self.qle.text()
            print('You typed:', typed_text)
            if typed_text:
                # self.paste_image(typed_text)
                pass

            self.terminate()
            return True
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Return:
                print('Enter pressed')
                self.terminate()
        return False

    def terminate(self):
        self.deleteLater()

        r = requests.get('http://localhost:5000/get_image/{}'.format(tag))

        if r.status_code == 200 and r.text:
            path = r.text
            ClipBoard.paste(path, tag)


def create():
    app = QtWidgets.QApplication(sys.argv)
    imputer = Imputer()
    imputer.show()

    app.exec_()


create()
