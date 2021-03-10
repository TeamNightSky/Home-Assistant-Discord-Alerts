from api import run_script


def message_logic(COOLDOWNS):
    messages = sum([COOLDOWNS[x]['use-count'] for x in COOLDOWNS])

    if messages < 1:
        run_script('dog_light_off')
    elif messages == 1:
        run_script('dog_light_green')
    elif 1 < messages < 10:
        run_script('dog_light_yellow')
    else:
        run_script('dog_light_red')
        