from discord.ext import commands
from utils import DATA, round_time


def setup(bot):
    bot.add_cog(Information(bot))


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='what-is', aliases=['who-is', 'what-are', 'who-are'])
    async def what_is(self, ctx):
        """Learn how to use `what-is`."""
        if len(ctx.message.content.split()) == 1:
            await self.bot.cogs['Help'].help_command(ctx, 'what-is')
    

    @what_is.command(name='downtime')
    async def downtime(self, ctx):
        """Get the downtime the owner has set."""
        await ctx.send('Downtime is from {} to {}'.format(*DATA['downtime'].values()))


    @what_is.command(name='cooldown')
    async def cooldown(self, ctx):
        """Get the notify command cooldown."""
        await ctx.send('The command cooldown is {}'.format(round_time(DATA['cooldown'])))


    @what_is.command(name='owner')
    async def owner(self, ctx):
        """Inquire of whom my owner may be."""
        await ctx.send('The current owner of me is <@!{}>'.format(DATA['owner_id']))


    @what_is.command(name='owner-status')
    async def owner_status(self, ctx):
        """Learn whether my owner is blocking your notifications or not."""
        await ctx.send('My owner is{} blocking notifications.'.format("" if DATA['block'] else "n't"))
