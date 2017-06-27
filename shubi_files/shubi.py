import sys
import os
import webbrowser
import configparser
import subprocess

# change the cwd to current working directory.
# because invoking with cmd might do trouble
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtCore import QObject, QUrl, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread

sys.path.insert(0, os.path.join(os.getcwd(), 'core'))
sys.path.insert(0, os.path.join(os.getcwd(), 'server'))
sys.path.insert(0, os.path.join(os.getcwd(), 'client'))
# print(sys.path)
from shubi_files.server import server
from core import path
import server
import client



# I have no idea why this worked.
# Qt5 have quite good documentaton - 7/10
# i use Python - 5/10
# everything on the web is referring to Qt4.8 - 3/10
# i use qml - 0 tutorials. http://i.imgur.com/evAFq1T.png
# http://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html


client_path = path.get('client')  # client folder path
shubi_path = path.root  # shubi_files_path

config_file_path = os.path.join(shubi_path, 'shubi_status.cfg')  # file to save user changes to switches
shubi_icon_path = os.path.join(shubi_path, 'web.png')  # app icon
shubi_qml_path = os.path.join(shubi_path, 'shubi.qml')  # qml of root window

is_exited_from_tray = False  # If Tru application is terminated, if False app is minimalized

config = configparser.ConfigParser()
config.read(config_file_path)


def str2bool(val):
    return val in ['True', 'true']


def set_config():
    config['server'] = {}
    config['server']['toggled'] = str(False)
    config['server']['file'] = r'server\server.py'
    config['client'] = {}
    config['client']['toggled'] = str(False)
    config['client']['file'] = r'client\client.py'
    config['autostart'] = {}
    config['autostart']['toggled'] = str(False)
    config['autostart']['file'] = r'client\autostart.py'
    with open(config_file_path, 'w') as f:
        config.write(f)


# set_config()


class Toggler:
    processes = dict(server=server.run, client=client.run)
    processes_status = dict(server=None, clien=None)

    class Process(QThread):
        def __init__(self, what):
            super().__init__()
            self.what = what

        def run(self):
            toggler.processes[self.what]()
            pass

    def __init__(self):
        pass

    def start(self, process, save=False):
        """Starts process with given name.
        :param save: if True. Status is saved to status file"""
        print('{}: ON'.format(process))
        thread = self.Process(process)
        self.processes_status[process] = thread
        thread.start()

        if save:
            config[process]['toggled'] = str(True)
            with open(config_file_path, 'w') as f:
                config.write(f)

    def terminate(self, process, save=False):
        """Terminates process with given name.
         :param save: if True. Status is saved to status file"""
        print('{}: OFF'.format(process))
        try:
            self.processes_status[process].terminate()
            if save:
                config[process]['toggled'] = str(False)
                with open(config_file_path, 'w') as f:
                    config.write(f)
        except:
            # maybe aplication is alredy terminated or something like that.
            # nothing to really do. (TODO: Search window processes and terminate reaming garbage)
            print('Error when closing {}'.format(process))

    def auto_start(self):
        """Checks shubi status file and turns on processes that need to be on"""
        for process in 'server client'.split():
            if str2bool(config[process]['toggled']):
                # start process
                self.start(process)
                print("{}: ON".format(process))
            else:
                # pass
                print("{}: OFF".format(process))

    def update_switches(self):
        """Changes status of switches on GUI"""
        names = 'server client autostart'.split()
        for name in names:
            x = win.findChild(QObject, 'switch' + name.title())
            if str2bool(config[name]['toggled']):
                # toggle it
                x.setProperty('checked', True)


toggler = Toggler()
toggler.auto_start()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu()
        # TODO: Maybe add more Actions? Like go to website
        exitAction = menu.addAction("Exit")

        self.activated.connect(self.from_tray)
        # print(exitAction.text())
        exitAction.triggered.connect(self.do_exit)
        self.setContextMenu(menu)

    def from_tray(self):
        """Shows main window"""
        win.show()

    def do_exit(self):
        """Terminates aplication"""
        global is_exited_from_tray
        is_exited_from_tray = True
        win.close()


# TODO: add statusbar

class Shubi(QObject):
    """Interface to qml"""
    clicked = pyqtSignal()
    exiting = pyqtSignal()

    def __init__(self):
        super(Shubi, self).__init__()
        self.exiting.connect(self.delete_view)

    @pyqtSlot(str)
    def click_button(self, what):
        """Event for changing status of button."""
        if what == 'updates':
            # TODO: implement this
            print('checking updates')
        elif what == 'website':
            # lunching website
            webbrowser.open(path.host_name)

    @pyqtSlot(str, bool)
    def click_switch(self, what, is_checked):
        """Event for changing status of switch"""
        # TODO: add a lot of exceptions if termination or running failed
        # print(what, is_checked)
        if what == 'autostart':
            subprocess.call('{} {} {}'.format(path.pythonw, config[what]['file'], int(is_checked)))
            config['autostart']['toggled'] = str(is_checked)
            with open(config_file_path, 'w') as f:
                config.write(f)
        else:
            if is_checked:
                toggler.start(what, True)
            else:
                toggler.terminate(what, True)

    def delete_view(self):
        """Minimalizes or terminates app.
        Triggered by exit event from QML"""
        global is_exited_from_tray
        if is_exited_from_tray:
            print('Shubi: Aplication terminated')
            toggler.terminate('server')
            toggler.terminate('client')
            QApplication.quit()
        else:
            print('Shubi: Aplication minimalized')
            win.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    shubi = Shubi()
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("shubi", shubi)  # expose class to qml

    # TODO: this is showing and closing. I dont want that
    engine.load(shubi_qml_path)

    win = engine.rootObjects()[0]

    win.tray_icon = SystemTrayIcon(QIcon(shubi_icon_path), win)
    win.tray_icon.show()
    toggler.update_switches()

    sys.exit(app.exec_())
