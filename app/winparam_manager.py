from app import winparam_values

class WinparamManager:
    value_obj_map: dict[str, winparam_values.ValueInterface] = {}
    initial_value_map: dict[str, int] = {}
    
    def __init__(self):
        values_to_init: list[winparam_values.ValueInterface] = [
            winparam_values.ValueInterfaceMouseSpeed(),
            winparam_values.ValueInterfaceHScroll(),
            winparam_values.ValueInterfaceVScroll(),
            winparam_values.ValueInterfaceTouchpadSpeed()
        ]
        for value in values_to_init:
            if not value.is_available():
                continue
            self.value_obj_map[value.name()] = value
        self.retrieve_initials()
    
    def retrieve_initials(self):
        for name in self.value_obj_map:
            value = self.value_obj_map[name]
            self.initial_value_map[name] = value.get()
        # print('initials', self.initial_value_map)

    def revert_initials(self):
        for name in self.value_obj_map:
            value = self.value_obj_map[name]
            value.set(self.initial_value_map[name])
            
    def set_values(self, value_dict: dict[str, int]):
        for name in self.value_obj_map:
            value = self.value_obj_map[name]
            to_set = value_dict.get(name)
            if to_set == None:
                continue
            value.set(to_set)
        