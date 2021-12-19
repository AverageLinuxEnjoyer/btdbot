import pyautogui
import time


class MapSelector():
    def __init__(self, win_data):
        self.win_data = win_data

    def run(self):
        icon = pyautogui.locateOnScreen(
            "res/icon.png",
            region=(
                0 + self.win_data["x"],
                0 + self.win_data["y"],
                100 + self.win_data["x"],
                100 + self.win_data["y"]),
            confidence=0.9
        )

        # we are in the collection event lobby
        if icon is None:
            # click collect
            pyautogui.moveTo(
                640 + self.win_data["x"], 450 + self.win_data["y"], 0.2)
            pyautogui.click()
            time.sleep(0.5)

            # click on the insta monkeys
            for i in range(8):
                pyautogui.moveTo(
                    375 + self.win_data["x"] + i * 75,
                    375 + self.win_data["y"], 0.2
                )
                pyautogui.click()
                time.sleep(0.5)

            # back after insta monkeys collection
            pyautogui.moveTo(
                50 + self.win_data["x"], 40 + self.win_data["y"], 0.2)
            pyautogui.click()

        # main menu
        # click on play button
        pyautogui.moveTo(
            550 + self.win_data["x"], 630 + self.win_data["y"], 0.2)
        pyautogui.click()

        while True:
            # click on expert
            pyautogui.moveTo(
                900 + self.win_data["x"], 650 + self.win_data["y"], 0.2)
            pyautogui.click()

            time.sleep(0.5)

            # locate event icon 1
            event_icon = pyautogui.locateOnScreen(
                "res/event_icon.png",
                region=(
                    200 + self.win_data["x"],
                    50 + self.win_data["y"],
                    950 + self.win_data["x"],
                    550 + self.win_data["y"]
                ),
                confidence=0.9
            )

            print(event_icon)

            if event_icon is None:
                continue
            else:
                break

        if event_icon is None:
            raise Exception("Event map couldn't be found")

        x = event_icon.left
        y = event_icon.top

        # check what map has the bonus on it
        expert_maps = [
            "sanctuary", "ravine", "flooded_valley", "infernal",
            "bloody_puddles", "workshop", "quad", "dark_castle",
            "muddy_puddles", "ouch"
        ]

        event_map = None

        for expert_map in expert_maps:
            map_location = pyautogui.locateOnScreen(
                f"res/maps/{expert_map}.png",
                region=(x - 300, y - 200, x, y),
                confidence=0.9
            )

            if map_location is not None:
                event_map = expert_map
                break

        # click the map with the event icon
        pyautogui.moveTo(x, y, 0.2)
        pyautogui.click()

        if event_map == "sanctuary":
            # TODO
            pass

        # click the medium difficulty
        pyautogui.moveTo(
            635 + self.win_data["x"], 377 + self.win_data["y"], 0.2)
        pyautogui.click()

        # click standard
        pyautogui.moveTo(
            420 + self.win_data["x"], 400 + self.win_data["y"], 0.2)
        pyautogui.click()

        time.sleep(4)

        return event_map


# play button 550, 630
# expert button 900, 650
# next after win 630 600
# home after next 470 560
# EVENT COLLECT 640 450
# Back after event collection 50 40
