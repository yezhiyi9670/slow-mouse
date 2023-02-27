import threading
from pynput import keyboard
from tkinter import Tk
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import json
import os
import psutil
import ctypes
import sys

version = '0.1.2'

# ======= Self detect =======
class SelfDetect:
	path: str = ''
	def detect(self):
		self.path = os.path.join('', 'pid.log')
		if os.path.exists(self.path):
			fp = open(self.path,'r')
			pid = fp.read().strip()
			try:
				pid1 = int(pid)
				fp.close()
				running_pid = psutil.pids()
				if pid1 in running_pid:
					return True
				return False
			except:
				return False
		else:
			return False
	def write(self):
		pid = os.getpid()
		fp = open(self.path,'w')
		fp.write(str(pid))
		fp.close()
	def clean(self):
		if os.path.exists(self.path):
			os.unlink(self.path)

selfDetect = SelfDetect()
if selfDetect.detect():
	exit(-1)
selfDetect.write()

# ======= Mouse speed =======
def change_speed(speed): 
	set_mouse_speed = 113 # 0x0071 for SPI_SETMOUSESPEED 
	ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0) 
def get_speed():
	get_mouse_speed = 112
	ptr = ctypes.c_void_p(1)
	ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(ptr), 0)
	val = ptr.value
	if(val < 1): return 1
	if(val > 20): return 20
	return val

# ======= Config utils =======
class Config:
	'FIle path'
	path: str = ''
	'Data'
	data = {}
	'Read or initialize data'
	def __init__(self):
		self.path = os.path.join('', 'config.json')
		if not os.path.exists(self.path):
			open(self.path, 'w').write(json.dumps({
				'standardSpeed': get_speed(),
				'lowSpeed': 1,
				'key': 'RightAlt'
			}))
		self.data = json.load(open(self.path, 'r'))
	'Write data'
	def write(self):
		open(self.path, 'w').write(json.dumps(self.data))
	'Get item'
	def get(self, key):
		return self.data[key]
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
	def on_press(self, key):
		if(key == self.get_key() and self.keyState == False):
			self.keyState = True
			change_speed(configManager.get('lowSpeed'))
	def on_release(self, key):
		if(key == self.get_key()):
			self.keyState = False
			change_speed(configManager.get('standardSpeed'))
	def start(self):
		self.listener.start()
	def stop(self):
		self.listener.stop()

keyboardListener = KeyboardListener()

# ======= Icon, also main loop =======
def icon_loop():
	def handle_quit(icon: pystray.Icon):
		global selfDetect
		selfDetect.clean()
		keyboardListener.stop()
		icon.stop()
	def set_standard_speed(val: int):
		global configManager
		configManager.set('standardSpeed', val)
		configManager.write()
	def set_slow_speed(val: int):
		global configManager
		configManager.set('lowSpeed', val)
		configManager.write()
	def set_key(val: str):
		global configManager
		configManager.set('key', val)
		configManager.write()

	global configManager
	menu = (
		MenuItem('Slow Mouse v' + version, action=lambda item: None),
		Menu.SEPARATOR,
		MenuItem('Standard Speed', Menu(*(
			list(map(
				lambda i: MenuItem(str(i), action=lambda item: set_standard_speed(i), checked=lambda item: configManager.get('standardSpeed') == i),
				range(1, 21)
			)) + [
				MenuItem('Auto Detect', lambda item: set_standard_speed(get_speed()))
			]
		))),
		MenuItem('Low Speed', Menu(*map(
			lambda i: MenuItem(str(i), action=lambda item: set_slow_speed(i), checked=lambda item: configManager.get('lowSpeed') == i),
			range(1, 21)
		))),
		MenuItem('Modifier Key', Menu(*map(
			lambda k: MenuItem(k, action=lambda item: set_key(k), checked=lambda item: configManager.get('key') == k),
			['LeftShift', 'LeftCtrl', 'LeftAlt', 'RightShift', 'RightCtrl', 'RightAlt', 'RightAlt2']
		))),
		Menu.SEPARATOR,
		MenuItem('Exit', action=handle_quit),
	)
	if getattr(sys, 'frozen', False):
		image = Image.open(os.path.join(sys._MEIPASS, "icon/main.png"))
	else:
		image = Image.open(os.path.join('.', "icon/main.png"))
	icon = pystray.Icon("icon", image, "Slow Mouse", menu)

	keyboardListener.start()

	icon.run()

'Start'
if __name__ == '__main__':
	icon_loop()
