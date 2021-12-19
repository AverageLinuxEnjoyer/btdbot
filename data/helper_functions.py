from data.monkey_template import MonkeyTemplate

def get_monkey_template(templates: list[MonkeyTemplate], name: str) -> MonkeyTemplate:
    for template in templates:
        if template.name == name:
            return template

    return None