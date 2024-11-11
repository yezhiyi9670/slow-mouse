import ctypes
from app.touchpad_params import TOUCHPAD_PARAMETERS
from app import app_env

def set_sys_value(key, value): 
    ctypes.windll.user32.SystemParametersInfoA(key, value, value, 0)

def get_sys_value(key):
    ptr = ctypes.c_void_p(1)
    ctypes.windll.user32.SystemParametersInfoA(key, 0, ctypes.byref(ptr), 0)
    val = ptr.value
    if val == None:
        return 0
    if(val < 1): return 1
    if(val > 20): return 20
    return val

class ValueInterface:
    def name(self) -> str:
        return '?'
    def menu_entry(self) -> str:
        return self.name()
    def is_available(self) -> bool:
        return True
    def get(self) -> int:
        raise NotImplemented()
    def set(self, value) -> None:
        raise NotImplemented()

class ValueInterfaceMouseSpeed(ValueInterface):
    def name(self):
        return 'mouse_speed'
    def menu_entry(self) -> str:
        return 'Reduced &Mouse Speed'
    def get(self):
        return get_sys_value(112)
    def set(self, value):
        set_sys_value(113, value)
        
class ValueInterfaceHScroll(ValueInterface):
    def name(self):
        return 'hscroll_speed'
    def menu_entry(self) -> str:
        return 'Reduced &H-scroll Speed'
    def get(self):
        return get_sys_value(0x6C)
    def set(self, value):
        set_sys_value(0x6D, value)

class ValueInterfaceVScroll(ValueInterface):
    def name(self):
        return 'vscroll_speed'
    def menu_entry(self) -> str:
        return 'Reduced &V-scroll Speed'
    def get(self):
        return get_sys_value(0x68)
    def set(self, value):
        set_sys_value(0x69, value)

class ValueInterfaceTouchpadSpeed(ValueInterface):
    def name(self):
        return 'touchpad_speed'
    def menu_entry(self) -> str:
        return 'Reduced &Touchpad Speed'
    def is_available(self):
        return super().is_available() and app_env.has_touchpad_speed_support()
    def get(self):
        params = TOUCHPAD_PARAMETERS()
        params.versionNumber = 1
        ctypes.windll.user32.SystemParametersInfoA(0xAE, ctypes.sizeof(params), ctypes.byref(params), 0)
        return params.cursorSpeed
    def set(self, value):
        params = TOUCHPAD_PARAMETERS()
        params.versionNumber = 1
        ctypes.windll.user32.SystemParametersInfoA(0xAE, ctypes.sizeof(params), ctypes.byref(params), 0)
        params.cursorSpeed = value
        ctypes.windll.user32.SystemParametersInfoA(0xAF, ctypes.sizeof(params), ctypes.byref(params), 0)
