version = '1.0.0'

import os
import sys

main_file_path = ''

def is_packaged():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return True
    else:
        return False

def get_program_dir():
    return os.path.dirname(sys.executable if is_packaged() else main_file_path)

def get_program_basename():
    return os.path.basename(sys.executable if is_packaged() else main_file_path)

def has_touchpad_speed_support():
    flag = True
    try:
        sys_win_ver = sys.getwindowsversion()
        if not sys_win_ver.build or sys_win_ver.build < 26000:
            flag = False
    except AttributeError:
        flag = False
    return flag
