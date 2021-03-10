import json, time, pytz
from collections import defaultdict
from datetime import datetime, timedelta


class Json(dict):
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as f:
            load = json.load(f)
            for key in load:
                self[key] = load[key]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self, f, indent=4)


def round_time(amount: float):
    if amount < 60:
        return '{:.2f} seconds'.format(amount)
    elif amount < 3600:
        return '{:.2f} minutes'.format(amount / 60)
    elif amount < 3600 * 24:
        return '{:.2f} hours'.format(amount / 3600)
    elif amount < 3600 * 24 * 7:
        return '{:.2f} days'.format(amount / (3600 * 24))
    elif amount < 3600 * 24 * 30:
        return '{:.2f} weeks'.format(amount / (3600 * 24 * 7))
    elif amount < 3600 * 24 * 30 * 12:
        return '{:.2f} months'.format(amount / (3600 * 24 * 30))


def between_times(start, end, now, timezone):
    if start is None or end is None or now is None:
        return False
    tz = pytz.timezone(timezone)
    start = datetime.strptime(start.upper(), '%I:%M%p')
    end = datetime.strptime(end.upper(), '%I:%M%p')
    now = now.replace(tzinfo=pytz.utc).astimezone(tz=tz).replace(tzinfo=None)
    now = now.replace(year=start.year, month=start.month, day=start.day)
    
    if start > end:
        end += timedelta(days=1)
    return start < now < end


START = time.time()
DATA = Json('data.json')
COOLDOWNS = defaultdict(lambda: {'last-used': START, 'use-count': 0})


now = datetime.fromisoformat('1900-01-01 20:17:47.905901')
tz = 'America/Chicago'
vals = [
    [between_times('9:00pm', '10:00pm', now, tz), False],
    [between_times('1:00pm', '10:00pm', now, tz), True],
    [between_times('1:00pm', '2:00pm', now, tz), False],
    [between_times('10:00pm', '1:00am', now, tz), False],
    [between_times('1:00pm', '11:00am', now, tz), True],
]

for value, expected in vals:
    assert value == expected

