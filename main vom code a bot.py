import discord
import os
import asyncio
import json
import datetime as dt
import time
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    global startTime
    startTime = time.time()
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------------------------')
    print('Bot running.')
    bot.loop.create_task(status_task())
    start_time = time.time()


async def status_task():
    while True:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"at {len(set(bot.users))} users"))
        await asyncio.sleep(13)
        await bot.change_presence(activity=discord.Game(f'In {len(bot.guilds)} Servers'), status=discord.Status.online)
        await asyncio.sleep(13)


bot.launch_time = dt.datetime.utcnow()


@slash.slash(name="uptime", description="Show uptime from Bot ")
async def _uptime(ctx):
    delta_uptime = dt.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    with open("channel.json", "r") as f:
        data = json.load(f)
    if data[str(ctx.author.id)]["language"] == ["En"]:
        embed = discord.Embed(title="Uptime", color=0x7a7aff)
        embed.add_field(name="Bot online since", value=f"{days}d, {hours}h, {minutes}m, {seconds}s")
        embed.set_footer(text=f'Asked by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif data[str(ctx.author.id)]["language"] == ["De"]:
        embed = discord.Embed(title="Uptime", color=0x7a7aff)
        embed.add_field(name="Bot online seit", value=f"{days}t, {hours}s, {minutes}m, {seconds}sec")
        embed.set_footer(text=f'Gefragt von: {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@slash.slash(name="switch-language", description="Up to now you can have: 'DE', 'EN'")
async def _language(ctx):
    with open("channel.json", "r") as f:
        data = json.load(f)
    if data[str(ctx.author.id)]["language"] == ["De"]:
        data[str(ctx.author.id)]["language"] = ["En"]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Switch-language", description="Your Language has been changed to **English**",
                              color=0x7a7aff)
        await ctx.send(embed=embed)
    elif data[str(ctx.author.id)]["language"] == ["En"]:
        data[str(ctx.author.id)]["language"] = ["De"]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Switch-language", description="Deine Sprache wurde zu **Deutsch** gewechselt",
                              color=0x7a7aff)
        await ctx.send(embed=embed)


@slash.slash(name="profile", description="See your Profile")
async def _profile(ctx):
    with open("channel.json", "r") as f:
        data = json.load(f)
    if not str(ctx.author.id) in data:
        data[str(ctx.author.id)] = {}
        data[str(ctx.author.id)]["lvl"] = [1]
        data[str(ctx.author.id)]["language"] = ["En"]
        data[str(ctx.author.id)]["mistakes"] = 0
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
    mistakes=data[str(ctx.author.id)]["mistakes"]
    level = data[str(ctx.author.id)]["lvl"]
    test = ", ".join([f'{c - 2}' for c in level])
    if int(test) <= 0:
        embed = discord.Embed(name="Profile", description=f"{ctx.author.mention}", color=0x7a7aff)
        embed.add_field(name="Level:", value=f"0")
        if data[str(ctx.author.id)]["language"] == ["De"]:
          embed.add_field(name="Fehler:", value="0")
          embed.add_field(name="Sprache:", value="Deutsch")
        elif data[str(ctx.author.id)]["language"] == ["En"]:
          embed.add_field(name="Mistakes:", value="0")
          embed.add_field(name="Language:", value="Englisch")
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(name="Profile", description=f"{ctx.author.mention}", color=0x7a7aff)
    if data[str(ctx.author.id)]["lvl"] <= [14]:
      embed.add_field(name="Level:", value=f", ".join([f'{c - 2}' for c in level]))
    if data[str(ctx.author.id)]["lvl"] >= [15] and data[str(ctx.author.id)]["lvl"] <= [24]:
      embed.add_field(name="Level:", value=f", ".join([f'{c - 3}' for c in level]))
    elif data[str(ctx.author.id)]["lvl"] >= [24]:
      embed.add_field(name="Level:", value=f", ".join([f'{c - 4}' for c in level]))
    if data[str(ctx.author.id)]["language"] == ["De"]:
      embed.add_field(name="Mistakes:", value=f"{mistakes}")
      embed.add_field(name="Sprache:", value="Deutsch")
    elif data[str(ctx.author.id)]["language"] == ["En"]:
      embed.add_field(name="Mistakes:", value=f"{mistakes}")
      embed.add_field(name="Language:", value="Englisch")
    await ctx.send(embed=embed)


@slash.slash(name="help", description="See all commands")
async def _help(ctx: SlashContext):
    with open("channel.json", "r") as f:
        data = json.load(f)
    if data[str(ctx.author.id)]["language"] == ["En"]:
        embed = discord.Embed(title="Help", color=0x7a7aff)
        embed.add_field(name="Learn commands:",
                        value="```/start-<option> - Start a new discord  Tutorial\n/resume-<option> - resume your "
                              "tutorial\n```"
                              "\nMORE IS COMING SOON",
                        inline=True)
        embed.add_field(name="Other Commands:", value="```/switch-language - 'DE' or 'En'\n/profile - See your Profile\n/uptime - see bot uptime\n/credits - see Bot Developer```")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/682/682055.png")
        await ctx.send(embed=embed)
    elif data[str(ctx.author.id)]["language"] == ["De"]:
        embed = discord.Embed(title="Hilfe", color=0x7a7aff)
        embed.add_field(name="Lern Commands:",
                        value="```/start-python - startet ein neues Python Tutorial\n/resume-python - führt dein "
                              "vorhandenes Tutorial fort\n```"
                              "\nMehr ist in Planung",
                        inline=True)
        embed.add_field(name="Andere Commands:",
                        value="```/switch-language - 'DE' oder 'En'\n/profile - Siehe deine Profil Informationen\n/uptime - Siehe die Online Zeit des bots\n/credits - sehe die Bot Entwickler```")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/682/682055.png")
        await ctx.send(embed=embed)


@slash.slash(name="start-python", description="Start a new python tutorial")
async def _start(ctx):
  with open("channel.json", "r") as f:
        data = json.load(f)
  if not str(ctx.author.id) in data:
      data[str(ctx.author.id)] = {}
      data[str(ctx.author.id)]["lvl"] = [1]
      data[str(ctx.author.id)]["language"] = ["En"]
      data[str(ctx.author.id)]["mistakes"] = 0
      with open("channel.json", "w") as f:
          json.dump(data, f, indent=4)
  if data[str(ctx.author.id)]["language"] == ["De"]:
        with open("channel.json", "r") as f:
            data = json.load(f)
        if data[str(ctx.author.id)]["lvl"] == [1]:
            embed = discord.Embed(title="Start-python", description="Ändere deine Sprache mit /switch-language",
                                  color=0x2bff00)
            embed.add_field(name=f"Python Tutorial:",
                            value=f"Hi {ctx.author.mention}, \nmein Name ist Code-a-Bot und das nicht ohne Grund. \nDu hast dich dazu entschlossen deinen ersten Bot \nzu Programmieren oder bist neu in Python? \nMit dieser Schritt für schritt Anleitung kann gar nichts \nschief gehen. Wenn du jetzt **/resume-python** im Chat eingibst, \nfängst du mit deinem Tutorial an. Das wird in \neiner Dm Message an dich gesendet. Wenn du \nirgendwo noch Fragen haben solltest, dann adde: \n_@Tadanosenshi#1054_ und stelle sie gerne oder joine dem: \n[Melion Codin Support](https://discord.com/melion)\nViel Erfolg :)")
            embed.set_footer(text="Fortschritt zurücksetzbar mit /start-python")
            await ctx.send(embed=embed)
            data[str(ctx.author.id)]["lvl"] = [2]
            with open("channel.json", "w") as f:
                json.dump(data, f, indent=4)
            return
        elif data[str(ctx.author.id)]["lvl"] >= [1]:
            embed = discord.Embed(title="Start-python", color=0x2bff00)
            embed.add_field(name="Python Tutorial", value="Willst du deinen Fortschritt wirklich zurücksetzen?")
            embed.set_footer(text="COMMAND DEAKTIVIERT")
            await ctx.send(embed=embed)
  elif data[str(ctx.author.id)]["language"] == ["En"]:
        with open("channel.json", "r") as f:
            data = json.load(f)
        if not str(ctx.author.id) in data:
            data[str(ctx.author.id)] = {}
            data[str(ctx.author.id)]["lvl"] = [1]
            data[str(ctx.author.id)]["language"] = ["De"]
            with open("channel.json", "w") as f:
                json.dump(data, f, indent=4)
        if data[str(ctx.author.id)]["lvl"] == [1]:
            embed = discord.Embed(title="Start-python", description="Switch language with /switch-language",
                                  color=0x2bff00)
            embed.add_field(name=f"Python Tutorial:",
                            value=f"Hi {ctx.author.mention}, \nmy name is Code-a-Bot.\nYou decided to build your first bot \nor you're new to python...\nWith these step-by-step instructions, nothing can \ngo wrong. If you now enter **/resume-python** in the chat, you \nstart with your tutorial. This will be sent to you in \na DM message. If you should have any questions \nhere, then add: \n_@Tadanosenshi#1054_ and ask him or join the: \n[Melion Codin Support] (https://discord.com/melion)\nGood Luck :)")
            embed.set_footer(text="Use /start-python again to reset your progress ")
            await ctx.send(embed=embed)
            data[str(ctx.author.id)]["lvl"] = [2]
            with open("channel.json", "w") as f:
                json.dump(data, f, indent=4)
            return
        elif data[str(ctx.author.id)]["lvl"] >= [1]:
            embed = discord.Embed(title="Start-python", color=0x2bff00)
            embed.add_field(name="Python Tutorial", value="Do you really wanna reset your progress?")
            embed.set_footer(text="COMMAND DEACTIVATED")
            await ctx.send(embed=embed)

@slash.slash(name="credits", description="Who programmed this Bot?")
async def _credits(ctx):
  embed=discord.Embed(title="Credits", color=0x2bff00)
  embed.add_field(name="Häuptling:", value="```Tadanosenshi#1054```", inline=False)
  embed.add_field(name="Helferlein:", value="```/```", inline=False)
  embed.add_field(name="Python:", value="```Tadanosenshi#1054```", inline=False)
  embed.add_field(name="Javascript:", value="```/```", inline=False)
  embed.add_field(name="Kotlin:", value="```/```", inline=False)
  embed.set_footer(text="Vielen Dank an das ganze Team :)")
  await ctx.send(embed=embed)

@slash.slash(name="resume-python", description="Resume your Python Tutorial")
@commands.dm_only()
async def resumepy(ctx: SlashContext):
    with open("channel.json", "r") as f:
        data = json.load(f)
    if not str(ctx.author.id) in data:
        embed = discord.Embed(title="Fehler", description="Du musst erst mit \n**/start-python** das Tutorial starten")
        await ctx.send(embed=embed)
        return
    if data[str(ctx.author.id)]["lvl"] == [2]:
        data[str(ctx.author.id)]["lvl"] = [3]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 1/30", color=0x2bff00)
        embed.add_field(name="Coding Umgebung:",
                        value="Bevor du anfangen kannst brauchst du ein Programm um \ndeinen Bot schreiben zu können. Installiere dafür **[Python](https://www.python.org/downloads/)**\nDas ist die Sprache mit der wir den Bot Coden werden. \nDann brauchst du auch noch **[Pycharm](https://www.jetbrains.com/de-de/pycharm/download/)**. \nPycharm ist das Programm in den wir den code \nimplementieren werden.")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [3]:
        data[str(ctx.author.id)]["lvl"] = [4]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 2/30", color=0x2bff00)
        embed.add_field(name="Imports:",
                        value="Wenn Pycharm geöffnet ist musst du ins Teminal, und gibst dort:\n```pip install discord.py```\nein, damit wir mit der library arbeiten können. Als \nnächstes schreibst du den Import in deinen Code: \n```py\nimport discord```\nzusätzlich nutzen wir noch  einen weiteren import:\n```py\nfrom discord.ext import commands``` \nDamit werden die commands aus der discord Datei abgerufen")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [4]:
        data[str(ctx.author.id)]["lvl"] = [5]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 3/30", color=0x2bff00)
        embed.add_field(name="Definition:",
                        value="Nun ist es an der Zeit deinen \nBot zu definieren und ihm einen Prefix zu \ngeben. Hierfür nutzen wir _bot.commands_ aus der _discord.ext_ \ndie wir importiert haben und nennen die Variable \nmal Bot (Der Name kann beliebig sein):\n```py\nbot = commands.Bot(command_prefix='!')```\nWir haben dem Bot soeben das Prefix ``!`` gegeben, \nwelches du aber auch durch dein eigenes ersetzen kannst. Mit \ndem Prefix geben wir dem Bot zu verstehen \ndass wir ihn meinen, wenn wir einen \nCommand ausführen wollen")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [5]:
        data[str(ctx.author.id)]["lvl"] = [6]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 4/30", color=0x2bff00)
        embed.add_field(name="Konsolen print:",
                        value="Damit der Bot etwas in die Konsole (terminal) \nschreibt nutzen wir ``print('TEXT')``. In diesem Fall \nwollen wir dass der Bot in die Konsole \nschreibt wenn er Online geht. dazu nutz du folgendes: \n```py\n@bot.event\nasync def on_ready():\n  print('Logged in as:')\n  print(bot.user.name)```\nMit ``bot.user.name`` bekommst du den Namen des \nBots, mit _on ready_ gibst du an dass \nder Bot was machen soll wenn er gestartet ist\nSchau mal was passiert wenn du den zweiten print in String setzt, also ``print('bot.user.name')``")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [6]:
        data[str(ctx.author.id)]["lvl"] = [7]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 5/30", color=0x2bff00)
        embed.add_field(name="Bot starten:",
                        value="Was bringt uns das Coden wenn der Bot \nnicht angeht? Um den Bot starten zu können \nbrauchen wir die _run_ methode: \n```py\nbot.run('TOKEN')```\nDa wo ``TOKEN`` drinne steht muss du deinen \nBot Token einfügen. Den findest du im [Discord Developer Portal](https://discord.com/developers/applications)\n unter der Kategorie: _Bot_. Jetzt kannst du deinen \nBot starten und er wird online gehen")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [7]:
        data[str(ctx.author.id)]["lvl"] = [8]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 6/30", color=0x2bff00)
        embed.add_field(name="On_message",
                        value="Mit _on message_ checkt der Bot ständig \nob was bestimmtes in deinem Server passiert bzw \ngeschrieben wird. Hier ein Beispiel Code: ```py\n@bot.event\nasync def on_message(message):\n  if message.author.bot:\n    return\n  if message.content.startswith('test'):\n    message.channel.send('Test Bestanden')```\n Mit ``if message.author.bot`` schauen wir ob \nder Bot diese Nachricht geschrieben hat. Wenn ja, \ndann returnen wir, heißt der Bot schaut nicht \nweiter im code. Mit ``message.content.startswith`` schaut \nder Bot ob eine Nachricht in einem channel \nmit _test_ startet. Wenn ja, dann sendet er \nin diesen channel dass der Test bestanden wurde")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [8]:
        data[str(ctx.author.id)]["lvl"] = [9]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 7/30", color=0x2bff00)
        embed.add_field(name="Command",
                        value="Ein Command ist eine Reaktion vom Bot wenn \ndu ihn mit dem **Prefix** aufrufst. Wir brauchen \ndafür auch nicht mehr _bot.event_ sondern \n**bot.command()**: \n```py\n@bot.command\nasync def test(ctx):\n  await ctx.send('Command Test Bestanden')```\n Mit ctx geben wir den Kontext der Nachricht \nan, also den Inhalt. Mit await geben wir \nan dass der Bot was tun soll, in \nunserem Fall sendet er den Kontext den du \nihm im String gegeben hast also _Command Test Bestanden_")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [9]:
        data[str(ctx.author.id)]["lvl"] = [10]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 8/30", color=0x2bff00)
        embed.add_field(name="Embed-text",
                        value="Wusstest du dass diese Nachricht hier auch ein \nEmbed ist? Das verschönert deine Nachricht kann allerdings \noft auch nervig sein wenn es zu groß wird. \nEmbeds kannst du auch im on_message event nutzen, \naber wir werden hier einen Command wieder erstellen:\n```py\n@bot.command()\nasync def embed(ctx):\n  embed=discord.Embed(title='Überschrift', description='Beschreibung'\n  embed.add_field(name='Name', value='Text',inline=True)\n  embed.add_field(name='Name2', value='False', inline=False)\n  await ctx.send(embed=embed)```\n Mit **embed=disco...** geben wir an was gesendet \nwerden soll in der await Funktion. Wir brauchen\n in der Definition einen Titel und eine Beschreibung, \naber im **add_field** brauchen wir Name \nund Value. add_field ist nicht anderes als \nein weiterer Block im Embed. Siehst du was  \ninline=True und inline=False für einen Unterschied \nbewirken? Probiere es aus")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [10]:
        data[str(ctx.author.id)]["lvl"] = [11]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 9/30", color=0x2bff00)
        embed.add_field(name="Embed-Bilder",
                        value="Ja, Embeds können risig werden, und dabei habe ich schon \nembed.set_footer bzw embed.set_author weggelassen. Wir wollen \nBilder, also machen wir Bilder. In diesem Schritt gibt \nes 2 verschiedene Arten von Bilder. Einmal ein großes unter \ndem Text und einmal ein kleines oben rechts neben \ndem text. Füge das Beispiel in deinen Code vom Embed \nüber dem await ein: \n```py\nembed.set_thumbnail(url='https://images-na.ssl-images-amazon.com/images/I/51lpm9SpsJL.png')\nembed.set_thumbnail(url='https://www.basicthinking.de/blog/wp-content/uploads/2021/03/discord-foto-pixabay-com-b_zocholl.jpg')```\n**set_image** ist das große Bild unter deinem Text und **set_thumbnail** \ndas kleine oben rechts neben deinem Text. Probiere es gerne \naus und versuche auch mal andere Bilder")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [11]:
        data[str(ctx.author.id)]["lvl"] = [12]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 10/30", color=0x2bff00)
        embed.add_field(name="Bot Status",
                        value="Du willst deinen Bot status selber bestimmen? Das kommt ins on_ready rein welches wir bereits gemacht haben: ```py\nactivity = discord.Game(name='Ich bin ein Status', type=3)\nawait bot.change_presence(status=discord.Status.online, activity=activity)```\n **discord.Game** kann man auch zu **discord.Streaming** wechseln, dann sagt der Bot halt nicht mehr _spielt Bot Status_ sondern _streamt Bot Status_")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [12]:
        data[str(ctx.author.id)]["lvl"] = [13]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 11/30", color=0x2bff00)
        embed.add_field(name="Mitglieder Kicken",
                        value="Mitglieder zu kicken ist eine einfache Angelegenheit. Der folgende Code \nist dafür am besten geeignet: \n```py\n@bot.command()\n@commands.has_permissions(kick_members=True)\nasync def kick(ctx, member: discord.Member):\n  await ctx.send('{ctx.member.mention} wurde aus dem Server geschmissen')\n  await member.kick()```\n**@commands.has_permissions** fragt ab ob der User der den \nCommand ausführt (in diesem Fall) die Rechte hat Mitglieder \nzu kicken. Mit **await member.kick** schmeißt der Bot \nden User aus dem Server")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [13]:
        data[str(ctx.author.id)]["lvl"] = [14]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 12/30", color=0x2bff00)
        embed.add_field(name="Mitglieder Bannen",
                        value="Hierfür musst du eigentlich nur das gleiche machen wie beim kick User Command. Nur dass du diesesmal alles wo kick steht durch ban ersetzt. Dieses mal bekommst du keinen Code von mir sondern probierst es einfach mal selber. Viel Erfolg, die Lösung findest du auf der nächsten Seite :)")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [14]:
        data[str(ctx.author.id)]["lvl"] = [15]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 12.5/30", color=0x2bff00)
        embed.add_field(name="Mitglieder Bannen",
                        value="Hier ist die Lösung für den Bann Command:\n```py\n@bot.command()\n@commands.has_permissions(ban_members=True)\nasync def ban(ctx, member: discord.Member):\n  await ctx.send('{ctx.member.mention} wurde aus dem Server gebannt')\n  await member.ban()```\nIch hoffe natürlich dass du das genaus so hattest!")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [15]:
        data[str(ctx.author.id)]["lvl"] = [16]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 13/30", color=0x2bff00)
        embed.add_field(name="Slow Modus",
                        value="Hier für brauchst du nicht viel code. Der Bot muss \neigentlich nur eine Sache machen: Den Channel editieren, damit \ndu einen Slowmode hast, und zwar so wie du ihn \nwillst. Hier mal wieder der perfekte Beispielcode: \n```py\n@bot.command()\n@command.has_permissions(administrator=True)\nasync def slowmode(ctx, seconds:int):\n  ctx.send(f'Der Channel wurde auf {seconds} Sekunden gestellt')\n  await ctx.channel.edit(slowmode_delay=seconds)```\nDiesesmal schaut der Bot nach ob du Admin rechte hast. \nIm _async def_ sehen wir dass _seconds_ in ``int``gespeichert \nwerden, also ohne String. Das ist weil die Nachricht die \ndu in Discord schickst immer als String rauskommt. \nMit (f'{seconds}') bekommen wir die Sekunden eingabe die du gemacht \nhast. Und das war auch schon alles was den Slowmode betrifft.")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [16]:
        data[str(ctx.author.id)]["lvl"] = [17]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 14/30", color=0x2bff00)
        embed.add_field(name="Userinfo",
                        value="Um einen Userinfo Command zu erstellen braucht es eigentlich nur \nein bisschen Wissen über die Funktionen die man aufrufen kann: \n```{member.mention} - Erwähnt einen User\n{member.avatar_url} - Profilbild vom User\n{member.status} - zeigt den Online Status\n{member.activity} - zeigt die Profilinfo```Ein Beispiel um einen Info command für einen User anzeigen zu lassen: ```py\n@bot.command()\nasync def userinfo(ctx,member:discord.Member):\n  embed=discord.Embed(title='Userinfo')\n  embed.add_field(name='Name:', value=f'{member.mention})'\n  embed.add_field(name='Status:', value=f'{member.status}')\n  embed.add_field(name='Activity:', value=f'{member.activity}')\n  embed.set_thumbnail(url=member.avatar_url)\n  await ctx.send(embed=embed)```\nDen Command rufst du nun auf indem du ``!userinfo @member`` \nalso für member einen account angibst, jemanden quasi pingst")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [17]:
        embed = discord.Embed(title="Resume-pyton", description="Level 15/30", color=0x2bff00)
        embed.add_field(name="Aufgabe",
                        value="**Frage:** Als was sind Nachrichten die du in Discord eingibst gespeichert?\n\n**Antworten:** ``a. Als String`` oder ``b. Als Int`` \n\n**Sendemöglichkeiten:** a oder b in den Chat eingeben")
        embed.set_footer(text="Du hast 40 Sekunden Zeit")
        await ctx.send(embed=embed)
        try:
            responseDesc = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=40)
            description = responseDesc.content
            if description == "a":
                embed = discord.Embed(title="Resume-pyton", description="Level 15/30", color=0x2bff00)
                embed.add_field(name="Aufgabe", value="Sehr gut, du hast diese frage richtig beantwortet!")
                embed.set_footer(text="Nutze /resume-python um weiter zu machen")
                await ctx.send(embed=embed)
                data[str(ctx.author.id)]["lvl"] = [18]
                with open("channel.json", "w") as f:
                    json.dump(data, f, indent=4)
            elif description == "b":
                with open("channel.json", "r") as f:
                  data = json.load(f)
                data[str(ctx.author.id)]["mistakes"] += 1
                with open("channel.json", "w") as f:
                  json.dump(data, f, indent=4)
                embed = discord.Embed(title="Resume-pyton", description="Level 15/30", color=0x2bff00)
                embed.add_field(name="Aufgabe", value="GESCHEITERT. Diese Antwort war leider Falsch")
                embed.set_footer(text="Nutze /resume-python um es nochmal zu versuchen")
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            with open("channel.json", "r") as f:
                    data = json.load(f)
            data[str(ctx.author.id)]["mistakes"] += 1
            with open("channel.json", "w") as f:
              json.dump(data, f, indent=4)
            embed = discord.Embed(title="Resume-pyton", description="Level 15/30", color=0x2bff00)
            embed.add_field(name="Aufgabe", value="GESCHEITERT. Du hast keine Eingabe getätigt.")
            embed.set_footer(text="Nutze /resume-python um es nochmal zu versuchen")
            await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [18]:
        data[str(ctx.author.id)]["lvl"] = [19]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 16/30", color=0x2bff00)
        embed.add_field(name="If Abfrage",
                        value="Mit der Abfrage kannst du abfragen ob das gewünschte \nErgebniss gegeben ist oder nicht (in unserem Fall). Dafür \nerstellen wir einen einfachen command: \n```py\n@bot.command()\nasync def if(ctx):\n  await ctx.send('Schreibe a oder b')\n  answer=await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=40)\n  if answer=='a':\n    await ctx.send('Das war 1')\n  elif answer=='b':\n    await ctx.send('Das war 2')```\nAnswer ist die Nachricht die der User sendet \nund die der Bot abfängt. Mit ``answer=='a':`` schaut \nder Bot ob du a gesendet hat und \nwenn ja dann sendet er die Antwort. Timeout=40 bedeutet \ndass er 40 Sekunden wartet, bis er einen error \nsendet und keine Eingabe mehr aufnimmt, der Command also abbricht.")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [19]:
        data[str(ctx.author.id)]["lvl"] = [20]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 17/30", color=0x2bff00)
        embed.add_field(name="Try-Except",
                        value="Mit einer try-except abfrage versucht (try) der Bot zum Beispiel in unserem Fall eine Nachricht versucht per DM an den zu senden der den Command ausführt. Angenommen die Person hat Dm Nachrichten von Nicht-Freunden aus, dann kann der Bot keine Nachricht senden und hierbei kommt das except ins spiel. Das ist dafür da wenn was schief geht, der try also nicht funktioniert hat. Wir bekommen also keinen error Code in Pycharm in die Konsole, sondern können wir dem Bot befehlen einfach error zu senden: ```py\n@bot.command()\nasync def try(ctx):\n  try:\n    await ctx.author.send('Dm Message')\n  except:\n     await ctx.send('Error')```")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [20]:
        data[str(ctx.author.id)]["lvl"] = [21]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 18/30", color=0x2bff00)
        embed.add_field(name="Dm Nachricht",
                        value="Es gibt verschiedene Möglichkeiten einem User, Owner eines Servers oder dir selber eine Nachricht zusenden. In unserem Beispiel können wir theoretisch folgendes einsetzem: ```ctx.author\nguild.owner\nmember```\nDenk daran dass du die guild bzw den member angeben musst wenn du was an jemand bestimmtes senden willst. Hier der Code um dir selber also dem der den Command nutzt eine Dm Nachricht zu senden:\n```py\n@bot.command()\nasync def dm(ctx):\n   await ctx.author.send('Deine Nachricht')```\nMit ctx.author erkennt der Bot dass er den jenigem welcher den Command ausgeführt hat eine Nachricht senden soll. Wenn wir jetzt die ``async def`` und ``await`` Zeile duch folgendes ändert: ```py\nasync def dm(ctx,member: discord.Member)\n-------------------------------\nawait member.send('Deine Nachricht')```dann sendet er die Nachricht an den member den du pingst im Zusammenhang mit dem Command, also ``!dm @member``. Probiere es jetzt mal alleine mit der **ctx.guild.owner**")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [21]:
        data[str(ctx.author.id)]["lvl"] = [22]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 19/30", color=0x2bff00)
        embed.add_field(name="Doppelt",
                        value="Eine wichtige Funktion um das bei uns definierte **ctx** im **async def** zu verstehen ist das Wiederholen deines Kontexts: ```py\n@bot.command()\nasync def say(ctx, *, text):\n  await ctx.send(text)```Das ``*`` gibt an dass er alles also auch das was du nach dem Leerzeichen tippst wiederholt. Nimm es mal raus und probiere aus was passiert!")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [22]:
        data[str(ctx.author.id)]["lvl"] = [23]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 20/30", color=0x2bff00)
        embed.add_field(name="Profilbild",
                        value="Um demjenigen der den Command ausführt sein Bild groß anzeigen zu können benötigen wir ein embed. Da du aber bereits weißt wie man eins macht liegt es an dir es in einem **@bot.command** zu definieren. Das Bild eines Users bekommst du hiermit:``ctx.author.avatar_url``\nAlso du bekommst eine Sache von mir vorgegeben:```py\nembed.set_image(url=ctx.author.avatar_url)```\nDie Lösung findest du auf der nächsten Seite.")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [23]:
        data[str(ctx.author.id)]["lvl"] = [24]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 20.5/30", color=0x2bff00)
        embed.add_field(name="Profilbild",
                        value="Hier die Musterlösung: ```py\n@bot.command()\nasync def avatar(ctx):\n  embed=discord.Embed(title='Avatar')\n  embed.set_image(url=ctx.author.avatar_url)\n  await ctx.send(embed=embed)```\nSehr gut, auf der nächsten Seite gehts weiter!")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [24]:
        data[str(ctx.author.id)]["lvl"] = [25]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 21/30", color=0x2bff00)
        embed.add_field(name="random.choice",
                        value="Für dieses Beispiel eignet es sich perfekt eine List anzulegen, aus der wir nur ein Ergebniss haben wollen. Für uns reicht erstmal ``ja`` und ``nein``. Nach diesem Prinzip codet man auch einen 8ball command, welcher dir auf deine Frage eine zufällige Antwort gibt. Unsere Liste bauen wir wie folgt auf: \n```Antworten=['Ja', 'Nein']```\nPraktisch kannst du so viele Sachen rein machen wie du willst, aber für uns reicht erstmal das hier. Jetzt coden wir unseren Command: ```py\n@bot.command()\nasync def random(ctx):\n  answer=random.choice(Antworten)\n  await ctx.send(f'Der Zufall entscheidet sich für{answer}!')```\nMit answer haben wir nur abgekürtzt, dass wir nicht candom.choice(Antworten) ins ctx.send rein packen mussten. Mit {...} gibt der Bot den Inhalt der Variable wieder. Vuch mal ``answer=3`` anstelle vom random.choice und sehe was passiert")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [25]:
        data[str(ctx.author.id)]["lvl"] = [26]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 22/30", color=0x2bff00)
        embed.add_field(name="random.choice",
                        value="Für dieses Beispiel eignet es sich perfekt eine List anzulegen, aus der wir nur ein Ergebniss haben wollen. Für uns reicht erstmal ``ja`` und ``nein``. Nach diesem Prinzip codet man auch einen 8ball command, welcher dir auf deine Frage eine zufällige Antwort gibt. Unsere Liste bauen wir wie folgt auf: \n```Antworten=['Ja', 'Nein']```\nPraktisch kannst du so viele Sachen rein machen wie du willst, aber für uns reicht erstmal das hier. Jetzt coden wir unseren Command: ```py\n@bot.command()\nasync def random(ctx):\n  answer=random.choice(Antworten)\n  await ctx.send(f'Der Zufall entscheidet sich für{answer}!')```\nMit answer haben wir nur abgekürtzt, dass wir nicht candom.choice(Antworten) ins ctx.send rein packen mussten. Mit {...} gibt der Bot den Inhalt der Variable wieder. Vuch mal ``answer=3`` anstelle vom random.choice und sehe was passiert")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [26]:
        data[str(ctx.author.id)]["lvl"] = [27]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 23/30", color=0x2bff00)
        embed.add_field(name="Links Verstecken",
                        value="Sicherlich hast du bei einem Invite Command keine Lust den ganzen riesigen Link in das Embed zu schreiben. Ähnlich wie in **css** und **html** kannst  du das aber ganz einfach verstecken. Deine Aufgabe ist es nun folgendes zu tun: Erstelle einen Command, welcher einen Link in einem Embed erstellt. Der command soll den Namen ``Link`` besitzen. ich gebe dir ein Embed.add_field vor: ```py\nembed.add_field(name='Deinen Namen', value=f'[DEIN TEXT HIER REIN]('DEINEN LINK HIER REIN'))```")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [27]:
        data[str(ctx.author.id)]["lvl"] = [28]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 24/30", color=0x2bff00)
        embed.add_field(name="Replace",
                        value="Mit ``.replace`` ersetzt du Wörter, Buchstaben oder Sonderzeichen durch das was du willst. Ein ziemlich unpraktischer Command für einen Bot, aber ein ziemlich guter für ein Tutorial ist ein folgender: ```py\n@bot.command()\nasync def replace(ctx, *,text):\n  text2=(f'{text}'.replace(' ','+'))\n  await ctx.send(f'{text2})```\nMit diesem Code ersetzt der Bot `` `` (Leerzeichen), durch ``+`` (Plus). Also wenn du !replace **hallo welt** eingibst, wird der Bot **hallo+welt** dir wieder zurückgeben")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [28]:
        data[str(ctx.author.id)]["lvl"] = [29]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 25/30", color=0x2bff00)
        embed.add_field(name="asyncio.sleep",
                        value="Wenn du willst dass der Bot eine Nachricht erst nach 4 Sekunden sendet, dann brauchst du dafür asyncio.sleep. Du kannst eine beliebige Zeit rein setzen. Wenn du einen Command nutzt den wir bereits gemacht haben und dann darunter ``asyncio.sleep(5)`` einsetzt, dann wird der Bot erst nach 5 Sekunden das embed oder den Text senden")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [29]:
        data[str(ctx.author.id)]["lvl"] = [30]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 26/30", color=0x2bff00)
        embed.add_field(name="error-handler",
                        value="Das kannst du nutzen wenn du von einem command keine errors mehr haben willst oder allgemein was gegen errors hast. Wir nutzen unseren error handler für den kick command. Ganz allgemein können wir also folgendes machen: ```py\n@kick.error\nasync def _error(ctx, error):\n  if isinstance(error, commands.MissingPermissions):\n  ctx.send('Fehlende Permissions!'```\nMit **kick.error** gibst du an dass der Error handler für den kick command ist. Dann haben wir den error angegeben dass man wenn man keine kick permissions hat einen Text vom Bot gesendet bekommst")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [30]:
        data[str(ctx.author.id)]["lvl"] = [31]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 27/30", color=0x2bff00)
        embed.add_field(name="Json",
                        value="Eine Json ist sowas wie eine ganz normale Textdatei, nur dass der Bot da sachen rein schreiben oder auch die Json lesen kann und abrufen. Erstelle eine Json mit dem Namen: ``test.json``. Wir erstellen einen code der etwas in die json schreibt: ```py\n@bot.command()\nasync def json(ctx):\n  with open('test.json', 'r') as f:\n    data=json.load(f)```Jetzt haben wir gemacht dass die json zum lesen geöffnet wurde ('r'=read) und in f gespeichert wird. Jetzt wollen wir dass er was rein schreibt also fügen wir folgendes hinzu: ```py\n  data[str(ctx.author.id)] = {}\n  data[str(ctx.author.id)]['zahl'] = 1\n  with open('test.json', 'w') as f:\n    json.dump(data, f, indent=4)```Hiermit schreibt er die Id von dir (deinem Profil) in die Json rein. Mit indent=4 geben wir eine Formatierung des Textes an, du kannst es ja auch gerne mal aus den Code nehmen und schauen was passiert. Den Inhalt der Json bekommst du mit einem einfachen: **print(data)**")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [31]:
        data[str(ctx.author.id)]["lvl"] = [32]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 28/30", color=0x2bff00)
        embed.add_field(name="read-json",
                        value="Wenn wir nun den Inhalt von einer Json datei lesen wollen fügen wir einfach folgendes hinzu: ```py\ninhalt = data[ctx.author.id]['zahl']\nctx.send(f'{inhalt}')```\nWir hätten auch das was wir in inhalt definiert haben in die geschweifte Klammer setzen können, das wäre aber zu unübersichtlich und daher ist es besser en großen Code in einer kleinen Variable zu verstecken")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [32]:
        data[str(ctx.author.id)]["lvl"] = [33]
        with open("channel.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Resume-pyton", description="Level 29/30", color=0x2bff00)
        embed.add_field(name="global-var",
                        value="Eine Globale Variable ist eine Variable die solange so bleibt wie du es codest, bis du den Bot neu startest. Wenn du z.b. zählen willst wie oft ein Command genutze wurde, kann er einfach immer +1 in die globale Variable schreiben und du könntest einen simplen Command machen um dir die Zahl welche die Globale Variable aktuell beinhaltet senden zu lassen")
        embed.set_footer(text="Nutze /resume-python um weiter zu machen")
        await ctx.send(embed=embed)
        return
    elif data[str(ctx.author.id)]["lvl"] == [33]:
          data[str(ctx.author.id)]["lvl"] = [34]
          with open("channel.json", "w") as f:
              json.dump(data, f, indent=4)
          embed = discord.Embed(title="Resume-pyton", description="Level 30/30", color=0x2bff00)
          embed.add_field(name="Gratulation!",
                          value="Hiermit hast du die Basics gelernt um einen Bot für Discord in der Sprache Python zu Programmieren. Wenn dir dieses Tutorial gefallen hat dann kannst du auch noch zusätzlich die basics füt **Kotlin** und **Javascript** lernen.\n\nWürdige auch gerne die Entwickler dieses Bots mit **/credits**\n\nWenn du das Tutorial nochmal starten möchtest, dann kannst du nochmal **/start-python** eingeben.")
          embed.set_footer(text="Nutze /resume-python um weiter zu machen")
          await ctx.send(embed=embed)
          return
    elif data[str(ctx.author.id)]["lvl"] == [34]:
          embed = discord.Embed(title="Resume-pyton", description="Level 30/30", color=0x2bff00)
          embed.add_field(name="Du bist bereits fertig",
                          value="Du hast bereits gelernt einen Bot in Python für Discord zu Programmieren. Wenn dir dieses Tutorial gefallen hat dann kannst du auch noch zusätzlich die basics füt **Kotlin** und **Javascript** lernen.\n\nWürdige auch gerne die Entwickler dieses Bots mit **/credits**\n\nWenn du das Tutorial nochmal starten möchtest, dann kannst du nochmal **/start-python** eingeben.")
          embed.set_footer(text="Nutze /resume-python um weiter zu machen")
          await ctx.send(embed=embed)
          return

###level klappt nicht ab einer bestimmten anzuahl ist das level falsch!
from discord_slash.utils.manage_commands import create_option, create_choice


@slash.slash(name="error",
             description="See all Errors and get help",
             options=[
              create_option(
                 name="python",
                 description="See Python error and get help",
                 option_type=3,
                 required=False,
                 choices=[
                  create_choice(
                    name="ChoiceOne",
                    value="DOGE!"
                  ),
                  create_choice(
                    name="ChoiceTwo",
                    value="NO DOGE"
                  )
                ]
               ),
               create_option(
                 name="javascript",
                 description="See Javascript error and get help",
                 option_type=3,
                 required=False,
                 choices=[
                  create_choice(
                    name="ChoiceOne",
                    value="DOGE!2"
                  ),
                  create_choice(
                    name="ChoiceTwo",
                    value="NO DOGE2"
                  )
                ]
               )
             ])
async def test(ctx, python: str = False, javascript: str = False):
    if python:
        await ctx.send(f"Wow, you actually chose {python}? :(")
    elif javascript:
        await ctx.send("Worked")


@resumepy.error
async def _resume(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        embed=discord.Embed(title="Fehler", description="Bitte nutze den Command nur per\nDM Nachricht mit dem Bot und nicht hier\n im channel!", color=0x2bff00)
        await ctx.send(embed=embed)


bot.run("ODkwNjM2NDQ0NDUwODE2MTAw.YUyr0w.WItmQic9cszc2qW88jAjQCYjpUs")
