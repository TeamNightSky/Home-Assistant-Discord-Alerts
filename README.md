# Home Alert System

Notifies you when you have notifications from discord.

## ENVIRONMENT:

``DISCORD_TOKEN=<Discord Bot Token>``

``HOMEASSISTANT_TOKEN=<Long Lived Home Assistant Token>``

## data.json
```json
{
    "owner_id": <your discord user id>,
    "cooldown": <command cooldown in seconds>,
    "api-endpoint": <external api endpoint of your homeassistant>,
    "block": <bool>,
    "downtime": {
        "start": "10:00pm",
        "end": "7:00am"
    }
}
```

## Run
Make sure to install dependencies first before using the following command.
```
$ python -m hotline
```