import platform

system = platform.system()

print(f"Using {system} specific functions")

ctrl = 0
lmb = 0
rmb = 0

if system == 'Windows':

    F2 = 0x71
    F3 = 0x72

    import ctypes
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


    # Load user32.dll for Windows API calls
    user32 = ctypes.windll.user32

 


    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010

    MOUSEEVENTF_WHEEL = 0x0800
    # ctrl
    VK_CONTROL = 0x11
    # F2
    VK_VOL_UP = F3
    # F3
    VK_VOL_DOWN = F2

    VK_L = 0x4C

    KEYEVENTF_KEYDOWN = 0x0000
    KEYEVENTF_KEYUP = 0x0002

    # Function to move the mouse to (x, y)
    def move_mouse(x, y):
        user32.SetCursorPos(x, y)

    def move_mouse_relative(dx, dy):
        user32.mouse_event(0x0001, ctypes.c_long(dx), ctypes.c_long(dy), 0, 0)

    def hold_lmb():
        global lmb
        if not lmb:
            lmb = 1 
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    # Function to release the left mouse button
    def release_lmb():
        global lmb
        if lmb:
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            lmb = 0

    def hold_rmb():
        global rmb
        if not rmb:
            rmb = 1
            user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            
    def release_rmb(): 
        global rmb
        if rmb:
            user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            rmb = 0

    def press_L():
        user32.keybd_event(VK_L, 0, KEYEVENTF_KEYDOWN, 0)
        user32.keybd_event(VK_L, 0, KEYEVENTF_KEYUP, 0)

    def hold_ctrl():
        global ctrl
        if not ctrl:
            ctrl = 1
            user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYDOWN, 0)

    def release_ctrl():
        global ctrl
        if ctrl:
            user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
            ctrl = 0

    def setup_vol():
        global vol
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))



    vol = setup_vol() 

    # requires control to be hold
    def volume(level):
        global vol
        vol.SetMasterVolumeLevelScalar(level, None)
    
    # requires control to be hold
    def zoom(delta = 0):
        hold_ctrl()
        delta = delta * 120
        user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, delta, 0)


elif system == 'Darwin':

    # Mac volume control not working. Author doesn't own a Mac.

    from pynput.mouse import Button, Controller as MouseController
    from pynput.keyboard import Controller as KbController, Key
    # from Quartz.CoreAudio import (
    #     kAudioHardwarePropertyDefaultOutputDevice,
    #     kAudioDevicePropertyVolumeScalar,
    #     kAudioObjectPropertyElementMaster,
    #     kAudioDevicePropertyScopeOutput,
    #     AudioObjectPropertyAddress,
    #     AudioObjectGetPropertyData,
    #     AudioObjectSetPropertyData,
    #     AudioObjectPropertyAddress,
    #     AudioDeviceID
    # )
    # import objc

    # Initialize the mouse controller
    mouse = MouseController()
    kb = KbController()



    # def setup_vol():
    #     address = AudioObjectPropertyAddress(
    #         mSelector=kAudioHardwarePropertyDefaultOutputDevice,
    #         mScope=kAudioObjectPropertyScopeGlobal,
    #         mElement=kAudioObjectPropertyElementMaster
    #     )
    #     device_id = AudioDeviceID()
    #     size = ctypes.sizeof(device_id)
    #     status = AudioObjectGetPropertyData(
    #         kAudioObjectSystemObject, address, 0, None, size, device_id)
    #     if status != 0:
    #         raise OSError(f"Error {status} getting default device")
        
    #     volume_address = AudioObjectPropertyAddress(
    #         mSelector=kAudioDevicePropertyVolumeScalar,
    #         mScope=kAudioDevicePropertyScopeOutput,
    #         mElement=kAudioObjectPropertyElementMaster
    #     )
    #     return device_id.value, volume_address

    
    # vol, address = setup_vol()

    # def volume(level):
    #     global vol
    #     global address

    #     level = ctypes.c_float(level)
    #     size = ctypes.sizeof(level)
    #     status = AudioObjectSetPropertyData(
    #         vol,
    #         address,
    #         0,
    #         None,
    #         size,
    #         ctypes.byref(level)
    #     )
    #     if status != 0:
    #         print("Failed to set volume")

    def volume(level):
        print("Not implemented for MAC")
        print(f"level: {level}")

    def move_mouse(x, y):
        mouse.position = (x, y)

    def move_mouse_relative(dx, dy):
        current_x, current_y = mouse.position
        mouse.position = (current_x + dx, current_y + dy)

    def hold_lmb():
        global lmb
        if not lmb:
            lmb = 1 
            mouse.press(Button.left)

    def release_lmb():
        global lmb
        if lmb:
            mouse.release(Button.left)
            lmb = 0

    def hold_rmb():
        global rmb
        if not rmb:
            rmb = 1
            mouse.press(Button.right)
            
    def release_rmb(): 
        global rmb
        if rmb:
            mouse.release(Button.right)
            rmb = 0


    def press_L():
        kb.press('l')
        kb.release('l')

    def hold_ctrl():
        global ctrl
        if not ctrl:
            ctrl = 1
            kb.press(Key.cmd)
    
    def release_ctrl():
        global ctrl
        if ctrl:
            kb.release(Key.cmd)
            ctrl = 0
        
    def zoom(delta = 0):
        hold_ctrl()
        mouse.scroll(0, delta)
        
else:
    raise Exception("Unsupported Operating System")
