from re import split
import threading
from pynput import keyboard
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import os
import sys
import json
import psutil
import ctypes
import signal
from app.config_manager import ConfigManager
from app.touchpad_params import TOUCHPAD_PARAMETERS
from app import app_env
from app import instance_detection
from app.winparam_manager import WinparamManager

app_env.main_file_path = __file__
os.chdir(app_env.get_program_dir())

# ======= Prevent multiple instances =======
self_detect = instance_detection.SelfDetect()
if self_detect.detect():
    sys.exit()
self_detect.write()

# ======= The config utilities =======
winparam_manager = WinparamManager()
config_manager = ConfigManager('config-v2.json', winparam_manager)

# ======= Keyboard detect =======
class KeyboardListener:
    key_state = False
    listener: keyboard.Listener
    def __init__(self):
        def on_press(key):
            self.on_press(key)
        def on_release(key):
            self.on_release(key)
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    def get_key(self):
        dic = {
            'LeftShift': keyboard.Key.shift_l,
            'RightShift': keyboard.Key.shift_r,
            'LeftAlt': keyboard.Key.alt_l,
            'RightAlt': keyboard.Key.alt_gr,
            'RightAlt2': keyboard.Key.alt_r,
            'LeftCtrl': keyboard.Key.ctrl_l,
            'RightCtrl': keyboard.Key.ctrl_r
        }
        key = config_manager.get('key')
        assert isinstance(key, str)
        if(dic.get(key)):
            return dic[key]
        return keyboard.Key.alt_gr
    
    def on_press(self, key):
        if(key == self.get_key() and self.key_state == False):
            winparam_manager.retrieve_initials()
            self.key_state = True
            config_manager.set_winparam_values()
    
    def on_release(self, key):
        if(key == self.get_key()):
            self.key_state = False
            winparam_manager.revert_initials()
    
    def start(self):
        self.listener.start()
    def stop(self):
        self.listener.stop()

keyboardListener = KeyboardListener()

# ======= Icon, also main loop =======
def create_icon():
    def handle_quit(icon):
        global self_detect
        self_detect.clean()
        keyboardListener.stop()
        icon.stop()

    
    menu = (
        MenuItem('Slow Mouse v' + app_env.version, action=lambda item: None),
        Menu.SEPARATOR,
        *map(
            lambda value_obj:
            MenuItem(value_obj.menu_entry(), Menu(*map(
                lambda i: MenuItem(
                    str(i) if i >= 0 else 'Disable',
                    action=lambda item: config_manager.set_and_commit('winparam:' + value_obj.name(), i),
                    checked=lambda item: config_manager.get('winparam:' + value_obj.name()) == i
                ), [-1, *range(1, 21)]))
            ),
            winparam_manager.value_obj_map.values()
        ),
        MenuItem('&Modifier Key', Menu(*map(
            lambda k: MenuItem(
                k,
                action=lambda item: config_manager.set_and_commit('key', k),
                checked=lambda item: config_manager.get('key') == k
            ),
            ['LeftShift', 'LeftCtrl', 'LeftAlt', 'RightShift', 'RightCtrl', 'RightAlt', 'RightAlt2']
        ))),
        Menu.SEPARATOR,
        MenuItem('&Quit', action=handle_quit),
    )
    if app_env.is_packaged():
        meipass = getattr(sys, '_MEIPASS')
        assert meipass != None, '_MEIPASS missing in packaged environment'
        image = Image.open(os.path.join(meipass, "icon/main.png"))
    else:
        image = Image.open(os.path.join('.', "icon/main.png"))
    icon = pystray.Icon("icon", image, "Slow Mouse", menu)

    keyboardListener.start()
    return icon

'Start'
if __name__ == '__main__':
    icon = create_icon()
    def handle_term(signal, frame):
        self_detect.clean()
        icon.stop()
        sys.exit()
    signal.signal(signal.SIGINT, handle_term)
    signal.signal(signal.SIGTERM, handle_term)
    icon.run()
