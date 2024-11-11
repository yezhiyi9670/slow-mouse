import os, json
from typing import Union

from app.winparam_manager import WinparamManager

class ConfigManager:
    defaults: dict[str, Union[int, str]] = {
        'key': 'RightAlt'
    }
    
    'File path'
    path: str = ''
    
    'Attached winparam manager'
    winparam_manager: WinparamManager
    
    'Data'
    data: dict[str, Union[int, str]] = {}
    
    'Read or initialize data'
    def __init__(self, path: str, winparam_manager: WinparamManager):
        self.path = path
        self.winparam_manager = winparam_manager
        
        for name in winparam_manager.value_obj_map:
            self.defaults['winparam:' + name] = -1
        
        if not os.path.exists(self.path):
            open(self.path, 'w').write(json.dumps(self.defaults))
        self.data = json.load(open(self.path, 'r'))
    
    'Write data'
    def commit(self):
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
        
    def set_and_commit(self, key, val):
        self.set(key, val)
        self.commit()
    
    'Set values on the attached winparam manager using the configuration'
    def set_winparam_values(self):
        for name in self.winparam_manager.value_obj_map:
            value_obj = self.winparam_manager.value_obj_map[name]
            config_val = self.get('winparam:' + name)
            if isinstance(config_val, str) or config_val < 0:
                continue
            value_obj.set(config_val)
