import discord
import atexit
import asyncio

from datetime import datetime
from discord.ext import commands

from ..utils import DATA, COOLDOWNS, between_times, round_time
from ..api import run_script

def setup(bot):
    bot.add_cog(Owner(bot))


def owner_only():
    async def owner_check(ctx):
        return ctx.author.id == DATA['owner_id']
    return commands.check(owner_check)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        atexit.register(run_script, 'dog_light_off')


    @commands.command(name='reset', aliases=['r'])
    @owner_only()
    async def reset_command(self, ctx):
        """[Owner ONLY] Reset your lights."""
        for key in COOLDOWNS:
            COOLDOWNS[key]['use-count'] = 0
        
        embed = discord.Embed(
            title=':white_check_mark: You reset your notifications!',
            color=0x00ff00,
            description="Your lights are now normal."
        )
        run_script('dog_light_off')
        run_script("all_lights_off")
        await ctx.send(embed=embed)

    @commands.command(name='reset-alarm', aliases=['ra'])
    @owner_only()
    async def resetalarm_command(self, ctx):
        """[Owner ONLY] Reset the alarm."""
        
        embed = discord.Embed(
            title=':white_check_mark: The alarm has been stopped',
            color=0x00ff00,
            description="Your lights are now normal."
        )

        run_script("all_lights_off")
        await ctx.send(embed=embed)
    

    @commands.command(name='setcooldown', aliases=['sc'])
    @owner_only()
    async def set_cooldown(self, ctx, cooldown: int):
        """[Owner ONLY] Sets the violent notification cooldown in seconds."""
        
        DATA['cooldown'] = cooldown
        DATA.save()
        embed = discord.Embed(
            title=':white_check_mark:  Success!',
            color=0x00ff00,
            description=f"The cooldown has been changed to {round_time(cooldown)}"
        )
        await ctx.send(embed=embed)

    @commands.command(name='toggle-notifications', aliases=['tn'])
    @owner_only()
    async def block_notifications(self, ctx, block: bool = None):
        """[Owner ONLY] Toggles your notification on or off."""
        
        if block is not None:
            DATA['block'] = block
        else:
            DATA['block'] = not DATA["block"]

        DATA.save()
        if DATA['block']:
            embed = discord.Embed(
                title=':white_check_mark:  Success!',
                color=0x00ff00,
                description="All notifications have been blocked."
            )
        else:
            embed = discord.Embed(
                title=':white_check_mark:  Success!',
                color=0x00ff00,
                description="All notifications have been enabled."
            )
        await ctx.send(embed=embed)

    @commands.command(name='change-color', aliases=['cc'])
    @owner_only()
    async def change_color_command(self, ctx, color="red"):
        """[Owner ONLY] Changes the color of your lights."""
        embed = discord.Embed(
            title=f"Joey\'s lights have changed {color}.",
            color=0x00ff00,
        )
        if color == "blue":
            run_script("all_lights_blue")
        elif color == "green":
            run_script("all_lights_green")
        elif color == "off":
            run_script("all_lights_off")
        else:
            run_script("all_lights_red")
        await ctx.send(embed=embed)
    
    @commands.command(name='downtime', aliases=['dt'])
    @owner_only()
    async def set_downtime(self, ctx, start: str, end: str):
        """[Owner ONLY] Sets your downtime where I will not send you notifications."""
        try:
            datetime.strptime(start.upper(), '%I:%M%p')
        except ValueError:
            embed = discord.Embed(
                    title="Malformed Start time.",
                    color=0xff0000,
                    description=f"{start} is not formatted correctly. Try 9:00pm."
                )
            await ctx.send(embed=embed)
        else:
            try:
                datetime.strptime(end.upper(), '%I:%M%p')
            except ValueError:
                embed = discord.Embed(
                    title="Malformed End time.",
                    color=0xff0000,
                    description=f"{end} is not formatted correctly. Try 6:00am."
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{start.upper()} to {end.upper()}  :last_quarter_moon_with_face:",
                    color=0x4B0082,
                    description=f"Your downtime is now {start.upper()} to {end.upper()}"
                )
                DATA['downtime']["start"] = start
                DATA['downtime']["end"] = end
                DATA.save()
                await ctx.send(embed=embed)
        

    @commands.Cog.listener('on_command_error')
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title=':x:  You aren\'t Owner.',
                description='You are not authorized to run this command.',
                color=0xff0000,
            )
            await ctx.send(embed=embed)
    

    @commands.Cog.listener('on_ready')
    async def status_changer(self):
        while True:
            if between_times(*DATA['downtime'].values(), datetime.now(), DATA['time_zone']) or DATA["block"]:
                await self.bot.change_presence(
                    status=discord.Status.dnd, 
                    activity=discord.Activity(
                        type=discord.ActivityType.listening,
                        name='Notifications Disabled 😌'
                    )
                )
            else:
                await self.bot.change_presence(
                    status=discord.Status.online, 
                    activity=discord.Activity(
                        type=discord.ActivityType.listening,
                        name='Notifications Enabled 😊'
                    )
                )
            await asyncio.sleep(10)
    