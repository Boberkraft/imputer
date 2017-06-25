"""Sets given path to autostart"""
from PyQt5.QtCore import QSettings
import sys
import os
current_location = os.path.dirname(os.path.abspath(__file__))
program_path = os.path.abspath(os.path.join(current_location, '..'))
shubi_path = os.path.join(program_path, 'start_shubi.bat')

is_checked = bool(int(sys.argv[2]))
boot_up_setting = QSettings("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                                QSettings.NativeFormat)
if is_checked:
    boot_up_setting.remove('Shubi_bat')
else:
    boot_up_setting.setValue('Shubi_bat', shubi_path)
