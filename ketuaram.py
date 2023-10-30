import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    try:
        print(f'{bot.user.name} has connected to Discord!')
        print(f"Registered commands: {bot.commands}")
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def ping(ctx):
    try:
        await ctx.send('pong')
    except discord.errors.Forbidden:
        print(f"Error: I don't have permission to send messages in {ctx.channel.name}")
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def pong(ctx):
    try:
        await ctx.send('ping')
    except discord.errors.Forbidden:
        print(f"Error: I don't have permission to send messages in {ctx.channel.name}")
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def teams(ctx):
    message = await ctx.send("React to join a team!")
    # Replace with your actual emoji and role names
    emoji1 = "1️⃣"
    emoji2 = "2️⃣"
    await message.add_reaction(emoji1)
    await message.add_reaction(emoji2)

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.message_id == message.id:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if str(payload.emoji) == emoji1:
                role = discord.utils.get(guild.roles, name='Team 1')
            elif str(payload.emoji) == emoji2:
                role = discord.utils.get(guild.roles, name='Team 2')
            else:
                # Ignore all other emojis
                return
            if role is not None:
                await member.add_roles(role)

    @bot.event
    async def on_raw_reaction_add(payload):
        if payload.message_id == message.id:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if str(payload.emoji) == emoji1:
                role = discord.utils.get(guild.roles, name='Team 1')
            elif str(payload.emoji) == emoji2:
                role = discord.utils.get(guild.roles, name='Team 2')
            else:
                # Ignore all other emojis
                return
            if role is not None:
                await member.add_roles(role)
                # Check if the member has both 'Team 1' and 'Team 2' roles
                if discord.utils.get(guild.roles, name='Team 1') in member.roles and discord.utils.get(guild.roles, name='Team 2') in member.roles:
                    # Remove the most recently added role
                    if str(payload.emoji) == emoji1:
                        await member.remove_roles(discord.utils.get(guild.roles, name='Team 2'))
                    else:
                        await member.remove_roles(discord.utils.get(guild.roles, name='Team 1'))
                    await ctx.send(f'{member.mention} that\'s cheating that\'s cheating you\'re literally cheating')

@bot.command()
async def aram(ctx):
    # Run the ~teams command
    await ctx.invoke(bot.get_command('teams'))

    # Create the channels
    team1_role = discord.utils.get(ctx.guild.roles, name='Team 1')
    team2_role = discord.utils.get(ctx.guild.roles, name='Team 2')
    if team1_role is None or team2_role is None:
        await ctx.send("Error: One or both of the roles 'Team 1' and 'Team 2' do not exist.")
        return

    # Create overwrites for team 1 channel
    overwrites_team1 = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        team1_role: discord.PermissionOverwrite(read_messages=True),
        team2_role: discord.PermissionOverwrite(read_messages=False),
    }
    channel1 = await ctx.guild.create_text_channel('team-1-champs', overwrites=overwrites_team1)

    # Create overwrites for team 2 channel
    overwrites_team2 = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        team1_role: discord.PermissionOverwrite(read_messages=False),
        team2_role: discord.PermissionOverwrite(read_messages=True),
    }
    channel2 = await ctx.guild.create_text_channel('team-2-champs', overwrites=overwrites_team2)

    # List of Champion Names
    champions = ["Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "Aurelion Sol", "Azir",
                 "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", "Corki",
                 "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio",
                 "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna",
                 "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "K'Sante", "Kai'Sa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle",
                 "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu",
                 "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Milio", "Miss Fortune", "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus",
                 "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
                 "Quinn", "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani",
                 "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas",
                 "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch",
                 "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong",
                 "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"]

    num_champs = 15
    try:
        team1_champs = random.sample(champions, num_champs)
        champions = [champ for champ in champions if champ not in team1_champs]
        team2_champs = random.sample(champions, num_champs)
    except ValueError:
        await ctx.send("Error: Not enough champions to choose from.")
        return

    # Format the champions as a list and print each one on a new line
    team1_champs_str = "\n".join(f"- {champ}" for champ in team1_champs)
    team2_champs_str = "\n".join(f"- {champ}" for champ in team2_champs)

    # Send a message in each channel
    await channel1.send(f'Welcome to Team 1! Here are your champions:\n{team1_champs_str}')
    await channel2.send(f'Welcome to Team 2! Here are your champions:\n{team2_champs_str}')


@bot.command()
async def end(ctx):
    # Delete the channels
    channel1 = discord.utils.get(ctx.guild.channels, name='team-1-champs')
    channel2 = discord.utils.get(ctx.guild.channels, name='team-2-champs')
    if channel1 is not None:
        await channel1.delete()
    if channel2 is not None:
        await channel2.delete()

    # Remove the roles from all users
    team1_role = discord.utils.get(ctx.guild.roles, name='Team 1')
    team2_role = discord.utils.get(ctx.guild.roles, name='Team 2')
    if team1_role is not None:
        for member in team1_role.members:
            if member != bot.user:
                await member.remove_roles(team1_role)
    if team2_role is not None:
        for member in team2_role.members:
            if member != bot.user:
                await member.remove_roles(team2_role)


bot.run('token')