import sys
from PyQt5.QtCore import QObject, QUrl, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, Qt
import webbrowser
import configparser
import subprocess
import time
from PyQt5.QtCore import QEvent

# I have no idea why this worked.
# Qt5 have quite good documentaton - 7/10
# i use Python - 5/10
# everything on the web is referring to Qt4.8 - 3/10
# i use qml - 0 tutorials. http://i.imgur.com/evAFq1T.png
# http://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html


config_file_path = 'shubi_config.ini'
config = configparser.ConfigParser()
config.read(config_file_path)
is_exited_from_tray = False
is_autostart_on = 0
server_process = None
client_process = None


def str2bool(val):
    return val in ['True', 'true']


class Processes:
    server, client = None, None


def set_config():
    config['server'] = {}
    config['server']['toggled'] = str(False)
    config['server']['file'] = 'server.py'
    config['client'] = {}
    config['client']['toggled'] = str(False)
    config['client']['file'] = 'client.py'
    config['autostart'] = {}
    config['autostart']['toggled'] = str(False)
    config['autostart']['file'] = 'config.py'
    with open(config_file_path, 'w') as f:
        config.write(f)


# set_config()


class Toggler:
    def __init__(self):
        pass

    def start(self, process, save=False):

        setattr(Processes, process, subprocess.Popen('pythonw {}.py'.format(process)))
        if save:
            config[process]['toggled'] = str(True)
            with open(config_file_path, 'w') as f:
                config.write(f)

    def terminate(self, process, save=False):
        try:
            getattr(Processes, process).terminate()
            if save:
                config[process]['toggled'] = str(False)
                with open(config_file_path, 'w') as f:
                    config.write(f)
        except:
            print('Error durning closing {}'.format(process))

    def auto_start(self):
        for process in 'server client'.split():
            print(str2bool(config[process]['toggled']))
            if str2bool(config[process]['toggled']):
                self.start(process)
                print('turning on', process)
            else:
                print(process, 'is turned off')

    def update_switches(self):
        switches = 'switchServer switchClient switchAutostart'.split()
        names = 'server client autostart'.split()
        for switch, name in zip(switches, names):
            x = win.findChild(QObject, switch)
            if str2bool(config[name]['toggled']):
                x.setProperty('checked', True)


toggler = Toggler()
toggler.auto_start()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu()
        exitAction = menu.addAction("Exit")

        self.activated.connect(self.from_tray)
        # print(exitAction.text())
        exitAction.triggered.connect(self.do_exit)
        self.setContextMenu(menu)

    def from_tray(self):
        win.show()

    def do_exit(self):
        global is_exited_from_tray
        is_exited_from_tray = True
        win.close()


# TODO: add statusbar

class Shubi(QObject):
    clicked = pyqtSignal()
    exiting = pyqtSignal()

    def __init__(self):
        super(Shubi, self).__init__()
        self.exiting.connect(self.delete_view)

    @pyqtSlot(str)
    def click_button(self, what):
        if what == 'updates':
            print('checking updates')
        elif what == 'website':
            # lunching website
            webbrowser.open("http://localhost:5000/")

    @pyqtSlot(str, bool)
    def click_switch(self, what, is_checked):
        """is_checked: bool"""
        # TODO: add a lot of exceptions if termination or running failed
        # print(what, is_checked)
        if what == 'autostart':
            subprocess.call('pythonw autostart.py {}'.format(int(is_checked)))
            config['autostart']['toggled'] = str(is_checked)
            with open(config_file_path, 'w') as f:
                config.write(f)
        else:
            if is_checked:
                toggler.start(what, True)
            else:
                toggler.terminate(what, True)

    def delete_view(self):
        global is_exited_from_tray
        if is_exited_from_tray:
            print('Aplication terminated')
            toggler.terminate('server')
            toggler.terminate('client')
            QApplication.quit()
        else:
            print('Minimalized')
            win.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    shubi = Shubi()
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("shubi", shubi)

    # TODO: this is showing and closing. I dont want that
    engine.load('shubi.qml')

    win = engine.rootObjects()[0]

    # win.setFlags(Qt.FramelessWindowHint)
    win.tray_icon = SystemTrayIcon(QIcon('web.png'), win)
    win.tray_icon.show()
    toggler.update_switches()
    # app.aboutToQuit.connect(Shubi.exit_click)
    # win.hide()
    sys.exit(app.exec_())
