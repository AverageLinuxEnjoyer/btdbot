import pexpect
import re

def get_window_data():
    p = pexpect.spawn("xwininfo -name BloonsTD6")
    p.expect("BloonsTD6")
    text = str(p.read())

    
    all_values = re.findall(r"\d+", text)
    return {
        "x": int(all_values[0]), 
        "y": int(all_values[1]),
        "width": int(all_values[4]), 
        "height": int(all_values[5]),
    }
    
# import time
# import pyautogui

# while True:
#     x,y = pyautogui.position()
#     data = get_window_data()
#     x-=data["x"]
#     y-=data["y"]
#     print(f"x:{x}, y:{y}")
#     time.sleep(2)
    