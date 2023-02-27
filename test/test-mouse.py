import ctypes

def change_speed(speed=10): 
	# 1 - slow 
	# 10 - standard 
	# 20 - fast 
	set_mouse_speed = 113 # 0x0071 for SPI_SETMOUSESPEED 
	ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0) 

change_speed(9)
