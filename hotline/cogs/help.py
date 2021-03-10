from discord.ext import commands
from utils import DATA
import random
import discord


GREENS = [
    0x3cb043, 0xaef359, 0x74b72e, 0x234f1e, 0x597d35, 0xB0fc38, 0xfdbb63,
    0x566d1d, 0x03c04a, 0xb2d3c2, 0x3a5311, 0x98bf64, 0x03ac13, 0x99edc3,
    0x32612d, 0x728c69, 0x02a80f, 0x3ded97, 0x354a21, 0x607d3b
]

HELP_MESSAGES = [
    'The help you requested!', 'Really you want help? Ok.',
    'Sure glad to help.', "Help has arrived!"
]

HELP_MESSAGES = [
    msg + ' (Psst. Use `help {command}` to see more!)' for msg in HELP_MESSAGES
]


def setup(bot):
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    async def help_command(self, ctx, command: str = None):
        """Get help for commands."""
        embed = discord.Embed(title=random.choice(HELP_MESSAGES),
                              color=random.choice(GREENS))
        owner = await self.bot.fetch_user(DATA['owner_id'])
        embed.set_author(name=owner, icon_url=owner.avatar_url)
        if command is None:
            await ctx.send(f'**``My prefix is "{self.bot.command_prefix}".``**')
            await self.all_help(ctx, embed)
        else:
            await self.command_help(ctx, embed, command)

    async def all_help(self, ctx, embed):    
        for name, cog in self.bot.cogs.items():
            val = ""
            for cmd in cog.walk_commands():
                if not cmd.hidden:
                    val += f"`{' '.join([str(x) for x in cmd.parents]) + ' ' * int(len(cmd.parents) == 1)}{cmd.name}`: {cmd.help}\n"

            if bool(val):
                embed.add_field(name=name, value=val.strip(), inline=False)
        
        val = ""
        for name, docs in self.bot.extra_exts.items():
            val += f'`{name}`: {docs}\n'
        embed.add_field(name='Other Help', value=val, inline=False)
        
        
        await ctx.send(embed=embed)

    async def command_help(self, ctx, embed, *command: str):
        command = " ".join(command)
        for name, cog in self.bot.cogs.items():
            if command in [
                    com.qualified_name for com in cog.walk_commands()
                    if not com.hidden
            ]:
                com = [
                    com for com in cog.walk_commands()
                    if com.qualified_name == command
                ][0]
                embed.add_field(name=f"`{command}` help.",
                                value=f"*{com.help}*",
                                inline=False)
                embed.add_field(name="Aliases",
                                value=" | ".join([
                                    "`%s`" % name
                                    for name in [com.name, *com.aliases]
                                ]),
                                inline=False)
                embed.add_field(
                    name="Arguments",
                    value=
                    f"`<>` means required, `[]` means optional.\n**`{com.name} {com.signature}`**",
                    inline=False)
                await ctx.send(embed=embed)
                return
        await ctx.send("Sorry, but I couldn't find that command. Try again?")
