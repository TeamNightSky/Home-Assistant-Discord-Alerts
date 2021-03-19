import time
from discord.ext import commands
from .utils import DATA, COOLDOWNS, round_time, between_times
from .logic import message_logic


class Hotline(commands.Bot):
    async def on_ready(self):
        self.extra_exts = {
            'Notify': f'Mention <@!{DATA["owner_id"]}> to violently notify them of your intent to urgently contact them.'
        }
        print(f'{self.user.name} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        owner_mention = f'<@!{DATA["owner_id"]}>'
        user_id = message.author.id
		
        if owner_mention in message.content:
            if DATA["block"]:
                await message.channel.send("Owner has blocked notifications", delete_after=10)
                return

            start = DATA['downtime']['start']
            end = DATA['downtime']['end']
            
            if start and end:
                if between_times(start, end, message.created_at, DATA['time_zone']):
                    await message.channel.send("You cannot notify owner during downtime.", delete_after=30)
                    return
    
            now = time.time()
            if now > COOLDOWNS[user_id]['last-used'] + DATA['cooldown']:
                await message.channel.send('You notified my owner.')
                COOLDOWNS[user_id]['last-used'] = now
                COOLDOWNS[user_id]['use-count'] += 1
            else:
                time_left = COOLDOWNS[user_id]['last-used'] + DATA['cooldown'] - now
                await message.channel.send("You can't notify owner for another {}".format(round_time(time_left)))
            
            message_logic(COOLDOWNS)
        if f'<@!{self.user.id}>' in message.content or f'<@{self.user.id}>' in message.content:
            await self.cogs['Help'].help_command(type('Context', (), {'send': message.channel.send, 'message': message}))
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.BadArgument):
            await ctx.send('`{}`'.format(error.__name__))
        raise error