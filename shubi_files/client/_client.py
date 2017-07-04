import sys
from PyQt5.QtCore import QObject, QUrl, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType, QQmlComponent, QQmlEngine
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEvent, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtQuick import QQuickView

# from core import path

style_path = 'style.qml'


# import sys
# from PyQt5 import QtWidgets, QtCore
#
#
# class Imputer(QtWidgets.QMainWindow):
#     def __init__(self):
#         QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
#         self.editor = QtWidgets.QLineEdit(self)
#         self.editor.setFocusPolicy(QtCore.Qt.StrongFocus)
#         self.editor.move(25, 40)
#
#         self.setFocusPolicy(QtCore.Qt.StrongFocus)
#         self.setWindowFlags(
#             QtCore.Qt.WindowStaysOnTopHint |
#             QtCore.Qt.FramelessWindowHint |
#             QtCore.Qt.X11BypassWindowManagerHint
#         )
#
#         self.setGeometry(QtWidgets.qApp.desktop().width() - 20 - 200 + 50,
#                          QtWidgets.qApp.desktop().height() - 40 - 20 - 100,
#                          150,
#                          100)
#
#         self.installEventFilter(self)
#
#     def eventFilter(self, obj, event):
#         if event.type() == QtCore.QEvent.WindowDeactivate:
#             self.terminate()
#             return True
#         if event.type() == QtCore.QEvent.KeyPress:
#             key = event.key()
#             if key == QtCore.Qt.Key_Return:
#                 self.terminate()
#         return False
#
#     def terminate(self):
#         self.deleteLater()
#         tag = self.editor.text()
#         print(tag)
#         exit()
#
#
# app = QtWidgets.QApplication(sys.argv)
# imputer = Imputer()
# imputer.show()
#
# app.exec_()
# exit(app.exec_())
mutex = QMutex()

class Imputer(QObject):
    def __init__(self):
        super(Imputer, self).__init__()
        app.installEventFilter(self)

    def eventFilter(self, onj, event):
        # print(event.type())
        if event.type() == QEvent.WindowDeactivate:
            self.terminate()
            return True
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return:
                self.terminate()

        return False

    def terminate(self):

        tag = win.findChild(QObject, 'textField')

        # tag = self.editor.text()
        entered_text = tag.property('text')
        print(entered_text)
        quit()

initlialized = False
entered_text = None



# win.textUpdated.connect(lambda x: print('KlikuKluku!', x))
# win.onClosing = lambda: print(1)
# status = win.findChild(QObject, 'textField')
# status.onActiveFocusChanged.connect(lambda: print('KlikuKluku!'))
# Show the Label
# appLabel.show()

# Execute the Application and Exit


def run():
    global app, win
    app = QApplication(sys.argv)

    engine = QQmlEngine()
    component = QQmlComponent(engine, QUrl('style.qml'))
    win = component.create()
    # con = QWidget.createWindowContainer(component)
    imputer = Imputer()
    imputer.win = win
    win.show()
    exit(app.exec_())

def show():
    global win, mutex
    mutex.lock()
    win.show()

def wait_for_end():
    global win, mutex
    mutex.lock()
    mutex.unlock()

def hide():
    global win, mutex
    win.hide()
    mutex.unlock()

if __name__ == '__main__':
    run()



