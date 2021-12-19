import json
from data.monkey_template import MonkeyTemplate
from data.upgrade import Upgrade


def load_upgrades(upgrades_dict):
    upgrades_list = []
    path_number = 0
    for upgrade_path in upgrades_dict:
        upgrades_list.append([])
        path_number += 1
        tier_number = 0
        for upgrade in upgrade_path:
            tier_number += 1
            upgrades_list[-1].append(
                Upgrade(
                    name=upgrade["name"],
                    cost=upgrade["cost"],
                    tier=tier_number,
                    path=path_number
                )
            )
    return upgrades_list


def load_monkey_templates(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        monkeys = []

        for monkey_class in data:
            for monkey in data[monkey_class]:
                monkeys.append(
                    MonkeyTemplate(
                        clas=monkey_class,
                        name=monkey["name"],
                        cost=monkey["cost"],
                        hotkey=monkey["key"],
                        upgrades=load_upgrades(monkey["upgrades"])
                    )
                )

    return monkeys