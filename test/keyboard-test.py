from pynput import keyboard
from threading import Thread

def listen():
	keyState = False
	def on_press(key):
		nonlocal keyState
		if(key == keyboard.Key.alt_r and keyState == False):
			keyState = True
			print('attack')
	def on_release(key):
		nonlocal keyState
		if(key == keyboard.Key.alt_r):
			keyState = False
			print('release')
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

if __name__ == '__main__':
	lt = Thread(target=listen)
	lt.start()
