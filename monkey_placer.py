from data.load_strategy import load_strategy
from data.load_monkey_templates import load_monkey_templates
from data.helper_functions import get_monkey_template
from logger import log
import pyautogui
from copy import deepcopy


class MonkeyPlacer:
    def __init__(self, win_data, filename):
        self.monkey_templates = load_monkey_templates("monkey_templates.json")
        self.monkeys = dict()
        self.strategy: list = load_strategy(filename)

        self.xOffset = win_data["x"]
        self.yOffset = win_data["y"]

        self.clear_spot = (900, 30)
        self.upgrade_ongoing = None
        
        self.game_started = False

    def reset(self, filename):
        self.monkeys = dict()
        self.strategy: list = load_strategy(filename)
        self.upgrade_ongoing = None
        self.game_started = False

    def clear_popups(self):
        pyautogui.moveTo(
            self.clear_spot[0] + self.xOffset,
            self.clear_spot[1] + self.yOffset,
            0.2)

        pyautogui.click(clicks=3, interval=0.1)

    def place(self, x, y, name, id, money) -> bool:
        template = get_monkey_template(self.monkey_templates, name)

        if template.cost > money:
            return False

        self.clear_popups()

        pyautogui.moveTo(x + self.xOffset, y + self.yOffset, 0.2)
        pyautogui.press(template.hotkey)
        pyautogui.click()

        self.monkeys[id] = {
            "x": x,
            "y": y,
            "name": name,
            "upgrades": "000"
        }

        log(f"{name} with id {id} placed at ({x},{y}).")
        return True

    def upgrade(self, id, upgrades, money) -> bool:
        monkey = self.monkeys[id]
        template = get_monkey_template(self.monkey_templates, monkey["name"])

        for i in range(3):
            if i == 0:
                hotkey = ','
            elif i == 1:
                hotkey = '.'
            elif i == 2:
                hotkey = '/'

            if monkey["upgrades"][i] < upgrades[i]:
                cost = template.upgrades[i][int(monkey["upgrades"][i])].cost
                name = template.upgrades[i][int(monkey["upgrades"][i])].name

                if cost <= money:
                    money -= cost
                    self.clear_popups()
                    pyautogui.moveTo(
                        monkey["x"] + self.xOffset,
                        monkey["y"] + self.yOffset,
                        0.2
                    )
                    pyautogui.click()
                    pyautogui.press(hotkey)
                    self.clear_popups()

                    lst = list(monkey["upgrades"])
                    lst[i] = str(int(monkey["upgrades"][i]) + 1)
                    monkey["upgrades"] = ''.join(lst)
                    
                    log(f"{monkey['name']} with ID {id} got \"{name}\" upgrade bought at {cost}. Current upgrades: : [{monkey['upgrades']}].")

        if monkey["upgrades"] == upgrades:
            self.upgrade_ongoing = None
            self.strategy.pop(1)

    def update_strategy(self, money):
        if len(self.strategy) == 1:
            return

        if self.upgrade_ongoing is not None:
            self.upgrade(*self.upgrade_ongoing, money)
            return

        current = self.strategy[1]

        if "name" in current:
            x = current["position"]["x"]
            y = current["position"]["y"]
            name = current["name"]
            id = current["id"]

            if self.place(x, y, name, id, money):
                self.strategy.pop(1)

        elif "upgrades" in current:
            id = current["id"]
            upgrades = current["upgrades"]

            self.upgrade_ongoing = (id, upgrades)
            self.upgrade(id, upgrades, money)
                
        elif "hero" in current and money >= current["hero"]:
            self.clear_popups()

            x = current["position"]["x"]
            y = current["position"]["y"]
            pyautogui.moveTo(x + self.xOffset, y + self.yOffset, 0.2)
            pyautogui.press("u")
            pyautogui.click()
            
            self.strategy.pop(1)
            
        if not self.game_started:
            self.game_started = True
            self.clear_popups()
            pyautogui.press("space")
            pyautogui.press("space")
                        
                        

    def place_fallback_monkey(self):
        if len(self.strategy) == 0:
            raise Exception("No fallback monkey specified.")

        fallback = self.strategy[0]

        x = fallback["position"]["x"]
        y = fallback["position"]["y"]
        name = fallback["name"]
        id = fallback["id"]

        template = get_monkey_template(self.monkey_templates, name)

        pyautogui.moveTo(x + self.xOffset, y + self.yOffset, 0.5)
        pyautogui.press(template.hotkey)
        pyautogui.click()

        log(f"Fallback {name} with id {id} placed at ({x},{y}).")

        if template.name == "Sniper Monkey":
            return 215

        return template.cost
