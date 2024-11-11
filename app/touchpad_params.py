import ctypes

# More info on this: https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-systemparametersinfoa
# https://github.com/ntdiff/headers/blob/ebe89c140e89b475005cd8696597ddf7406dfb8a/Win11_2409_24H2/x64/System32/ole32.dll/Standalone/TOUCHPAD_PARAMETERS.h#L17

# <ai-assisted-content>

# Define the enums with actual values
class LEGACY_TOUCHPAD_FEATURES(ctypes.c_uint):
    LEGACY_TOUCHPAD_FEATURE_NONE = 0
    LEGACY_TOUCHPAD_FEATURE_ENABLE_DISABLE = 1
    LEGACY_TOUCHPAD_FEATURE_REVERSE_SCROLL_DIRECTION = 4

class TOUCHPAD_SENSITIVITY_LEVEL(ctypes.c_uint):
    TOUCHPAD_SENSITIVITY_LEVEL_MOST_SENSITIVE = 0
    TOUCHPAD_SENSITIVITY_LEVEL_HIGH_SENSITIVITY = 1
    TOUCHPAD_SENSITIVITY_LEVEL_MEDIUM_SENSITIVITY = 2
    TOUCHPAD_SENSITIVITY_LEVEL_LOW_SENSITIVITY = 3
    TOUCHPAD_SENSITIVITY_LEVEL_LEAST_SENSITIVE = 4

# Define the structure for the bitfields
class TouchpadFlags1(ctypes.Structure):
    _fields_ = [
        ("touchpadPresent", ctypes.c_int, 1),
        ("legacyTouchpadPresent", ctypes.c_int, 1),
        ("externalMousePresent", ctypes.c_int, 1),
        ("touchpadEnabled", ctypes.c_int, 1),
        ("touchpadActive", ctypes.c_int, 1),
        ("feedbackSupported", ctypes.c_int, 1),
        ("clickForceSupported", ctypes.c_int, 1),
        ("Reserved1", ctypes.c_int, 25),
    ]

class TouchpadFlags2(ctypes.Structure):
    _fields_ = [
        ("allowActiveWhenMousePresent", ctypes.c_int, 1),
        ("feedbackEnabled", ctypes.c_int, 1),
        ("tapEnabled", ctypes.c_int, 1),
        ("tapAndDragEnabled", ctypes.c_int, 1),
        ("twoFingerTapEnabled", ctypes.c_int, 1),
        ("rightClickZoneEnabled", ctypes.c_int, 1),
        ("mouseAccelSettingHonored", ctypes.c_int, 1),
        ("panEnabled", ctypes.c_int, 1),
        ("zoomEnabled", ctypes.c_int, 1),
        ("scrollDirectionReversed", ctypes.c_int, 1),
        ("Reserved2", ctypes.c_int, 22),
    ]

# Define the main structure
class TOUCHPAD_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ("versionNumber", ctypes.c_uint),
        ("maxSupportedContacts", ctypes.c_uint),
        ("legacyTouchpadFeatures", LEGACY_TOUCHPAD_FEATURES),
        ("flags1", TouchpadFlags1),
        ("flags2", TouchpadFlags2),
        ("sensitivityLevel", TOUCHPAD_SENSITIVITY_LEVEL),
        ("cursorSpeed", ctypes.c_uint),
        ("feedbackIntensity", ctypes.c_uint),
        ("clickForceSensitivity", ctypes.c_uint),
        ("rightClickZoneWidth", ctypes.c_uint),
        ("rightClickZoneHeight", ctypes.c_uint),
    ]

# </ai-assisted-content>
