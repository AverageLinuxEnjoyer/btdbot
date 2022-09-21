from os_info.scanmem import MemoryScanner
from monkey_placer import MonkeyPlacer
import time
from logger import log
from collections import deque
from os_info.window import get_window_data
import pyautogui
from map_selector import  MapSelector

class App:
    def __init__(self):
        self.win_data = get_window_data()
        
        self.memory_scanner = MemoryScanner()
        self.monkey_placer = MonkeyPlacer(self.win_data)
        self.map_selector = MapSelector(self.win_data)
        self.current_map = None

    def run(self):
        while True:
            self.current_map = self.map_selector.run()
            self.monkey_placer.reset(f"strategies/{self.current_map}.json")
            self.memory_scanner.reset()
            
            if self.current_map == "sanctuary":
                time.sleep(2)
                pyautogui.click(633,502)
                time.sleep(2)
                
            self.playMap()
            
    def check_for_win(self):
        found = pyautogui.locateOnScreen(
            "res/victory2.png",
            region=(
                465 + self.win_data["x"],
                76 + self.win_data["y"],
                800 + self.win_data["x"],
                170 + self.win_data["y"]
            )
        )
        
        if found is None:
            return False
        else:
            return True
        
    def exit_map(self):
        # click next after win ~(630, 600)
        pyautogui.moveTo(630 + self.win_data["x"], 600 + self.win_data["y"], 0.2)
        pyautogui.click()
        
        # click home after next ~(470, 560)
        pyautogui.moveTo(470 + self.win_data["x"], 560 + self.win_data["y"], 0.2)
        pyautogui.click()
        
        
        
    def playMap(self):
        log("Looking for money address...")
        if self.current_map == "sanctuary":
            starting_money = 40400
        else:
            starting_money = 1700
            
        located = self.memory_scanner.locate_money(value=starting_money)

        if not located:
            fallback_monkey_cost = self.monkey_placer.place_fallback_monkey()
            

            remaining_money = starting_money-fallback_monkey_cost
            located = self.memory_scanner.locate_money(value=remaining_money)
            
            if not located:
                raise RuntimeError("The money can't be located.")

        log("Money located.")

        last_5_money = deque([2,3,20,45,81])
        while True:
            money = self.memory_scanner.get_money()
            
            last_5_money.rotate(-1)
            last_5_money[4] = money
            if last_5_money.count(last_5_money[0]) == len(last_5_money):
                if self.check_for_win():
                    self.exit_map()
                    time.sleep(2)
                    return
            
            self.monkey_placer.update_strategy(money)
            time.sleep(1)