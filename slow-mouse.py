from re import split
import threading
from pynput import keyboard
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import json
import os
import psutil
import ctypes
import sys
import signal

version = '0.1.7'

def is_packaged():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return True
    else:
        return False

def get_program_dir():
    return os.path.dirname(sys.executable if is_packaged() else __file__)

def get_program_basename():
    return os.path.basename(sys.executable if is_packaged() else __file__)

os.chdir(get_program_dir())

# ======= Self detect =======
class SelfDetect:
    path: str = ''
    def detect(self):
        self.path = os.path.join('', 'pid.log')
        if os.path.exists(self.path):
            fp = open(self.path,'r')
            split_flag = fp.read().strip().split('/')
            if len(split_flag) < 2:
                return False
            pid, identifier = split_flag[0], split_flag[1]
            fp.close()
            try:
                target_pid = int(pid)
                pid_iter = psutil.process_iter()
                for pid in pid_iter:
                    if pid.pid == target_pid and pid.name() == identifier:
                        return True
                return False
            except:
                return False
        else:
            return False
    def write(self):
        pid = os.getpid()
        fp = open(self.path, 'w')
        fp.write(str(pid) + '/' + get_program_basename())
        fp.close()
    def clean(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

selfDetect = SelfDetect()
if selfDetect.detect():
    sys.exit()
selfDetect.write()

# ======= Cursor speed =======
# More info on this: https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-systemparametersinfoa

def set_sys_value(key, value): 
    print('set', key, value)
    ctypes.windll.user32.SystemParametersInfoA(key, value, value, 0) 

def get_sys_value(key):
    ptr = ctypes.c_void_p(1)
    ctypes.windll.user32.SystemParametersInfoA(key, 0, ctypes.byref(ptr), 0)
    val = ptr.value
    if(val < 1): return 1
    if(val > 20): return 20
    return val

def set_sys_cursor_speed(speed): 
    set_sys_value(113, speed)
def get_sys_cursor_speed():
    return get_sys_value(112)
initial_cursor_speed = get_sys_cursor_speed()

def set_sys_hscroll_speed(speed): 
    set_sys_value(0x6D, speed)
def get_sys_hscroll_speed():
    return get_sys_value(0x6C)
initial_hscroll_speed = get_sys_hscroll_speed()

def set_sys_vscroll_speed(speed): 
    set_sys_value(0x69, speed)
def get_sys_vscroll_speed():
    return get_sys_value(0x68)
initial_vscroll_speed = get_sys_vscroll_speed()

def update_initials():
    global initial_cursor_speed, initial_hscroll_speed, initial_vscroll_speed
    initial_cursor_speed = get_sys_cursor_speed()
    initial_hscroll_speed = get_sys_hscroll_speed()
    initial_vscroll_speed = get_sys_vscroll_speed()
    
# ======= Config utils =======
class Config:
    defaults = {
        'lowCursorSpeed': 1,
        'lowHScrollSpeed': 1,
        'lowVScrollSpeed': 1,
        'key': 'RightAlt'
    }
    'FIle path'
    path: str = ''
    'Data'
    data = {}
    'Read or initialize data'
    def __init__(self):
        self.path = os.path.join('', 'config.json')
        if not os.path.exists(self.path):
            open(self.path, 'w').write(json.dumps(self.defaults))
        self.data = json.load(open(self.path, 'r'))
    'Write data'
    def write(self):
        open(self.path, 'w').write(json.dumps(self.data))
    'Get item'
    def get(self, key):
        value = self.data.get(key)
        if value == None:
            return self.defaults[key]
        return value
    'Set item'
    def set(self, key, val):
        self.data[key] = val

configManager = Config()

# ======= Keyboard detect =======
class KeyboardListener:
    keyState = False
    listener: keyboard.Listener = None
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
        key = configManager.get('key')
        if(dic.get(key)):
            return dic[key]
        return keyboard.Key.alt_gr
    
    def try_update_initials(self):
        if self.keyState:
            return
        update_initials()
    
    def on_press(self, key):
        if(key == self.get_key() and self.keyState == False):
            self.try_update_initials()
            self.keyState = True
            set_sys_cursor_speed(configManager.get('lowCursorSpeed'))
            # set_sys_hscroll_speed(configManager.get('lowHScrollSpeed'))
            # set_sys_vscroll_speed(configManager.get('lowVScrollSpeed'))
    
    def on_release(self, key):
        if(key == self.get_key()):
            self.keyState = False
            set_sys_cursor_speed(initial_cursor_speed)
            # set_sys_hscroll_speed(initial_hscroll_speed)
            # set_sys_vscroll_speed(initial_vscroll_speed)
    
    def start(self):
        self.listener.start()
    def stop(self):
        self.listener.stop()

keyboardListener = KeyboardListener()

# ======= Icon, also main loop =======
def create_icon():
    def handle_quit(icon: pystray.Icon):
        global selfDetect
        selfDetect.clean()
        keyboardListener.stop()
        icon.stop()
    def set_config(key: str, val: int):
        global configManager
        configManager.set(key, val)
        configManager.write()
    def set_key(val: str):
        global configManager
        configManager.set('key', val)
        configManager.write()

    global configManager
    menu = (
        MenuItem('Slow Mouse v' + version, action=lambda item: None),
        Menu.SEPARATOR,
        MenuItem('Reduced &Cursor Speed', Menu(*map(
            lambda i: MenuItem(str(i), action=lambda item: set_config('lowCursorSpeed', i), checked=lambda item: configManager.get('lowCursorSpeed') == i),
            range(1, 21)
        ))),
        # MenuItem('Reduced &Vertical Scroll Speed', Menu(*map(
        #     lambda i: MenuItem(str(i), action=lambda item: set_config('lowVScrollSpeed', i), checked=lambda item: configManager.get('lowVScrollSpeed') == i),
        #     range(1, 21)
        # ))),
        # MenuItem('Reduced &Horizontal Scroll Speed', Menu(*map(
        #     lambda i: MenuItem(str(i), action=lambda item: set_config('lowHScrollSpeed', i), checked=lambda item: configManager.get('lowHScrollSpeed') == i),
        #     range(1, 21)
        # ))),
        MenuItem('&Modifier Key', Menu(*map(
            lambda k: MenuItem(k, action=lambda item: set_key(k), checked=lambda item: configManager.get('key') == k),
            ['LeftShift', 'LeftCtrl', 'LeftAlt', 'RightShift', 'RightCtrl', 'RightAlt', 'RightAlt2']
        ))),
        Menu.SEPARATOR,
        MenuItem('&Quit', action=handle_quit),
    )
    if is_packaged():
        image = Image.open(os.path.join(sys._MEIPASS, "icon/main.png"))
    else:
        image = Image.open(os.path.join('.', "icon/main.png"))
    icon = pystray.Icon("icon", image, "Slow Mouse", menu)

    keyboardListener.start()
    return icon

'Start'
if __name__ == '__main__':
    icon = create_icon()
    def handle_term(signal, frame):
        selfDetect.clean()
        icon.stop()
        sys.exit()
    signal.signal(signal.SIGINT, handle_term)
    signal.signal(signal.SIGTERM, handle_term)
    icon.run()
