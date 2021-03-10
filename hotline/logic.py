from .api import run_script


def message_logic(COOLDOWNS):
    messages = sum([COOLDOWNS[x]['use-count'] for x in COOLDOWNS])

    if messages < 1:
        run_script('light_off')
    elif messages == 1:
        run_script('light_green')
    elif 1 < messages < 10:
        run_script('light_yellow')
    else:
        run_script('light_red')
        