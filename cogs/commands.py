
import discord
from discord.ext import commands
import platform
import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

# displays the server stats
    @commands.command()
    async def stats(self, ctx):
        """
        A usefull command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@DEEErab>")

        embed.set_footer(text=f"DEEErab | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

# owner only command for forceing the bot to log out
    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()


# allows admins to speak as the bot
    @commands.command()
    @commands.has_role('Baby Dyno admins')
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)


# bans people from being able to use the bot
    @commands.command()
    @commands.has_role('Baby Dyno admins')
    async def blacklist(self, ctx, user: discord.Member):
        """
        Ban users form useing bot commands
        """
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")


# un-ban users from useing the bot commands
    @commands.command()
    @commands.has_role('Baby Dyno admins')
    async def unblacklist(self, ctx, user: discord.Member):
        """
        un-bans people from useing the bot
        """
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")


# command to send baby dyno links to the discord
    @commands.command()
    async def links(self, ctx):
        """
        links everything for BabyDyno
        """
        await ctx.send('https://y.at/%F0%9F%90%A3%F0%9F%8C%88%F0%9F%9A%80%F0%9F%8C%95')



    @commands.command()
    async def dip(self, ctx):
        """
        BUT THE DIP!!!
        """
        await ctx.send(file=discord.File('discord-bot\images\dip.png'))



def setup(bot):
    bot.add_cog(Commands(bot)) # adds the commands cog to the bot