#from keep_alive import keep_alive
import discord
import discord.ext
import requests
#from replit import db
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands

client = discord.Client()

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("Online!")
    r = requests.get("https://api.nitestats.com/v1/epic/staging/fortnite")
    data = r.json()
    FortniteGame_Build = data["FortniteLive"]["version"]
    await client.change_presence(activity=discord.Game(name=f'{FortniteGame_Build}'))
	
footertext = "FNBRInspect"
thumbmail = "https://cdn.discordapp.com/attachments/1037171117330284674/1037186283547656293/Fortnite_-_2022-11-01T201222.344.png"
color = 0x5865F2
fortnite_api_io_key = os.environ["fnio"]
bs = ""
#got dis shit from noteason :>

@slash.slash(name="newid", description="Get All Cosmetic Names And IDS From Latest Version")
async def newid(ctx):
    r = requests.get("https://fortnite-api.com/v2/cosmetics/br/new")
    data = r.json()
    embed = discord.Embed(title="New Cosmetic ID'S", color=discord.Color.blue())
    text = "```md\n"
    lastSection = data["data"]["items"][0]["type"]["backendValue"]
    for item in data["data"]["items"]:
        if lastSection != item["type"]["backendValue"]:
            text = text + "```"
            embed.add_field(name=lastSection, value=text, inline=False)
            lastSection = item["type"]["backendValue"]
            newname = item["name"]
            text = f'``` {newid} - {newname}\n'
        else:
            newname = item["name"]
            text = text + " " + f'{newid} - {newname}\n'
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)


@slash.slash()
async def fltoken(ctx):
  r = requests.get('https://api.nitestats.com/v1/epic/builds/fltoken')
  rr = r.json()

  version = rr['version']
  fltoken = rr['fltoken']
  embed = discord.Embed(title=f"FLToken", description="")
  embed.add_field(name='Version', value=f'``{version}``', inline=False)
  embed.add_field(name='FLToken', value=f"``{fltoken}``", inline=False)
  embed.set_footer(text=f'Refreshes automatically in under 1sec when a new build releases - {ctx.guild.name}', icon_url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)


@slash.slash()
async def ping(ctx):
    await ctx.send(f'bots ping is {round(client.latency * 1000)}ms')


@slash.slash(name="brnews", description="Shows Current Br News")
async def brnews(ctx):
    response = requests.get('https://fortnite-api.com/v2/news/br')
    data = response.json()
    news = data["data"]["image"]
    embed = discord.Embed(title='Battle Royale News', color=0x64fffb)
    embed.set_image(url=news)
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="brmap", description="Shows Current Br Map")
async def brmap(ctx):
    response=requests.get('https://fortnite-api.com/v1/map').json()

    embed=discord.Embed(title='Battle Royale Map', color=0x64fffb)
    embed.set_image(url=response["data"]["images"]["pois"])
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="brshop", description="Shows Current Br Shop")
async def shop(ctx):
    embed=discord.Embed(title='Result', color=0x4173ff)
    embed.set_image(url=f"https://api.nitestats.com/v1/shop/image?header=Shop%20Today!&footer=FNBRInspect")
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="weapon", description="Search For A Weapon")
async def wid(ctx, *, weapon):
    await ctx.defer()

    embed=discord.Embed(title=f"All Weapons Matching: {weapon}", color=color)
    url = "https://fortniteapi.io/v1/loot/list?lang=en"
    headers = {
        "Authorization": fortnite_api_io_key
    }
    r = requests.post(url, headers=headers)
    data = r.json()
    wids = data['weapons']
    for item in wids:
      namee = item['name']
      if weapon.title() in namee:
        if item['rarity'] == "common":
          rarity = f"common {bs}"
        if item['rarity'] == "uncommon":
          rarity = f"uncommon {bs}{bs}"
        if item['rarity'] == "rare":
          rarity = f"rare {bs}{bs}{bs}"
        if item['rarity'] == "epic":
          rarity = f"epic {bs}{bs}{bs}{bs}"
        if item['rarity'] == "legendary":
          rarity = f"legendary {bs}{bs}{bs}{bs}{bs}"
        if item['rarity'] == "mythic":
          rarity = f"mythic | {bs}{bs}{bs}{bs}{bs}{bs}"
        if item['rarity'] == "exotic":
          rarity = f"exotic | {bs}{bs}{bs}{bs}{bs}"
        embed.add_field(name=f"{namee} | {item['id']}", value=f"Rarity - **{rarity}**\n\n", inline=False)
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)



@slash.slash(name="vehicles", description="Shows All Vehicles")
async def vehicles(ctx):
    headers = {'Authorization': "94aa02a1-deda7712-adc56662-69db0061"}
    r = requests.get("https://fortniteapi.io/v2/game/vehicles", headers=headers)
    data = r.json()
    embed = discord.Embed(title="All Vehicles In Fortnite!", color=discord.Color.random())
    #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/974905128375160892/975254914508935198/Vehicle.png")
    key = data["vehicles"]
    for key in data["vehicles"]:
        embed.add_field(name=key["name"], value=key["id"], inline=True) 
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="styles", description="Shows Skin Styles")
async def styles(ctx, *, skin):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={skin}')
  data = r.json()

  for sub_dict in data['data']:
    for troll in sub_dict['variants']:
      #print(troll['channel'])
      pp = troll['options']

      for style in pp:
        embed=discord.Embed(title=style['name'], color=color)
        embed.set_thumbnail(url=style['image'])
        embed.set_footer(text=footertext)
        await ctx.send(embed=embed)


@slash.slash(name="icon", description="Get info on a Cosmetic by entering name and get Icon Image")
async def icon(ctx, *, item):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={item}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(title=sub_dict['name'], description=sub_dict['description'], color=color)
      embed.add_field(name='ID', value=sub_dict['id'])
      embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
      embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
      #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")
      
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=sub_dict['introduction']['text'])
        embed.set_image(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=footertext)
        message = await ctx.send(embed=embed)

@slash.slash(name="featured", description="Get info on a Cosmetic by entering name and get Featured Image")
async def featured(ctx, *, item):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={item}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(title=sub_dict['name'], description=sub_dict['description'], color=color)
      embed.add_field(name='ID', value=sub_dict['id'])
      embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
      embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
      #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")
      
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=sub_dict['introduction']['text'])
        embed.set_image(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/featured.png")
        embed.set_footer(text=footertext)
        message = await ctx.send(embed=embed)


@slash.slash(name="newids", description="Get All Cosmetic Names And IDS From Latest Version")
async def newids(ctx):
    r = requests.get("https://fortnite-api.com/v2/cosmetics/br/new")
    data = r.json()
    embed = discord.Embed(title="New Cosmetic ID'S", color=discord.Color.blue())
    text = "```md\n"
    lastSection = data["data"]["items"][0]["type"]["backendValue"]
    for item in data["data"]["items"]:
        if lastSection != item["type"]["backendValue"]:
            text = text + "```"
            embed.add_field(name=lastSection, value=text, inline=False)
            lastSection = item["type"]["backendValue"]
            newid = item["id"]
            newname = item["name"]
            text = f'``` {newid} - {newname}\n'
        else:
            newid = item["id"]
            newname = item["name"]
            text = text + " " + f'{newid} - {newname}\n'
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="creator", description="Search Info About SAC")
async def creator(ctx, *, code):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/creatorcode?name={code}')
  if r.status_code == 200:
    data = r.json()
    embed=discord.Embed(title=f"Creator Code - {code}", color=color)
    embed.add_field(name="Epic Games Name", value=data['data']['account']['name'], inline=False)
    embed.add_field(name="Epic Games ID", value=data['data']['account']['id'], inline=False)
    embed.add_field(name="Status", value=data['data']['status'], inline=False)
    embed.add_field(name="Verified", value=data['data']['verified'], inline=False)
    await ctx.send(embed=embed)
    embed.set_footer(text=footertext)
  else:
    await ctx.send("Creator Not Found!")

@slash.slash(name="iland", description="Search Info For Creative Map")
async def island(ctx, code):
  await ctx.defer()
  url = f"https://fortniteapi.io/v1/creative/island?code={code}"
  headers = {
      "Authorization": fortnite_api_io_key
  }
  r = requests.post(url, headers=headers)
  data = r.json()
  embed=discord.Embed(title=data['island']['title'], description=f"Creator - {data['island']['creator']}", color=color)
  embed.add_field(name="Island Type", value=data['island']['islandPlotTemplate']['name'])
  embed.add_field(name="Published Date", value=data['island']['publishedDate'])
  embed.add_field(name="Description", value=data['island']['description'])
  embed.set_image(url=data['island']['image'])
  embed.set_footer(text=f"Tags - {data['island']['tags']}")
  embed.set_footer(text=footertext)
  await ctx.send(embed=embed)

@slash.slash(name="aes", description="Sends Fortnite Aes Keys")
async def aes(ctx):
    response = requests.get('https://fortnite-api.com/v2/aes')
    embed=discord.Embed(title='Fortnite Aes Keys', color=000000)
    data = response.json()
    for i in data["data"]["dynamicKeys"]:
      key = i["key"]
      name = i["pakFilename"]
      embed.add_field(name=name, value=key)
    await ctx.send(embed=embed)

#keep_alive()
client.run("from keep_alive import keep_alive
import discord
import discord.ext
import requests
from replit import db
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands

client = discord.Client()

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("Online!")
    r = requests.get("https://api.nitestats.com/v1/epic/staging/fortnite")
    data = r.json()
    FortniteGame_Build = data["FortniteLive"]["version"]
    await client.change_presence(activity=discord.Game(name=f'{FortniteGame_Build}'))
	
footertext = "FNBRInspect"
thumbmail = "https://cdn.discordapp.com/attachments/1037171117330284674/1037186283547656293/Fortnite_-_2022-11-01T201222.344.png"
color = 0x5865F2
fortnite_api_io_key = os.environ["fnio"]
bs = ""
#got dis shit from noteason :>

@slash.slash(name="newid", description="Get All Cosmetic Names And IDS From Latest Version")
async def newid(ctx):
    r = requests.get("https://fortnite-api.com/v2/cosmetics/br/new")
    data = r.json()
    embed = discord.Embed(title="New Cosmetic ID'S", color=discord.Color.blue())
    text = "```md\n"
    lastSection = data["data"]["items"][0]["type"]["backendValue"]
    for item in data["data"]["items"]:
        if lastSection != item["type"]["backendValue"]:
            text = text + "```"
            embed.add_field(name=lastSection, value=text, inline=False)
            lastSection = item["type"]["backendValue"]
            newname = item["name"]
            text = f'``` {newid} - {newname}\n'
        else:
            newname = item["name"]
            text = text + " " + f'{newid} - {newname}\n'
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)


@slash.slash()
async def fltoken(ctx):
  r = requests.get('https://api.nitestats.com/v1/epic/builds/fltoken')
  rr = r.json()

  version = rr['version']
  fltoken = rr['fltoken']
  embed = discord.Embed(title=f"FLToken", description="")
  embed.add_field(name='Version', value=f'``{version}``', inline=False)
  embed.add_field(name='FLToken', value=f"``{fltoken}``", inline=False)
  embed.set_footer(text=f'Refreshes automatically in under 1sec when a new build releases - {ctx.guild.name}', icon_url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)


@slash.slash()
async def ping(ctx):
    await ctx.send(f'bots ping is {round(client.latency * 1000)}ms')


@slash.slash(name="brnews", description="Shows Current Br News")
async def brnews(ctx):
    response = requests.get('https://fortnite-api.com/v2/news/br')
    data = response.json()
    news = data["data"]["image"]
    embed = discord.Embed(title='Battle Royale News', color=0x64fffb)
    embed.set_image(url=news)
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="brmap", description="Shows Current Br Map")
async def brmap(ctx):
    response=requests.get('https://fortnite-api.com/v1/map').json()

    embed=discord.Embed(title='Battle Royale Map', color=0x64fffb)
    embed.set_image(url=response["data"]["images"]["pois"])
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="brshop", description="Shows Current Br Shop")
async def shop(ctx):
    embed=discord.Embed(title='Result', color=0x4173ff)
    embed.set_image(url=f"https://api.nitestats.com/v1/shop/image?header=Shop%20Today!&footer=FNBRInspect")
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="weapon", description="Search For A Weapon")
async def wid(ctx, *, weapon):
    await ctx.defer()

    embed=discord.Embed(title=f"All Weapons Matching: {weapon}", color=color)
    url = "https://fortniteapi.io/v1/loot/list?lang=en"
    headers = {
        "Authorization": fortnite_api_io_key
    }
    r = requests.post(url, headers=headers)
    data = r.json()
    wids = data['weapons']
    for item in wids:
      namee = item['name']
      if weapon.title() in namee:
        if item['rarity'] == "common":
          rarity = f"common {bs}"
        if item['rarity'] == "uncommon":
          rarity = f"uncommon {bs}{bs}"
        if item['rarity'] == "rare":
          rarity = f"rare {bs}{bs}{bs}"
        if item['rarity'] == "epic":
          rarity = f"epic {bs}{bs}{bs}{bs}"
        if item['rarity'] == "legendary":
          rarity = f"legendary {bs}{bs}{bs}{bs}{bs}"
        if item['rarity'] == "mythic":
          rarity = f"mythic | {bs}{bs}{bs}{bs}{bs}{bs}"
        if item['rarity'] == "exotic":
          rarity = f"exotic | {bs}{bs}{bs}{bs}{bs}"
        embed.add_field(name=f"{namee} | {item['id']}", value=f"Rarity - **{rarity}**\n\n", inline=False)
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)



@slash.slash(name="vehicles", description="Shows All Vehicles")
async def vehicles(ctx):
    headers = {'Authorization': "94aa02a1-deda7712-adc56662-69db0061"}
    r = requests.get("https://fortniteapi.io/v2/game/vehicles", headers=headers)
    data = r.json()
    embed = discord.Embed(title="All Vehicles In Fortnite!", color=discord.Color.random())
    #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/974905128375160892/975254914508935198/Vehicle.png")
    key = data["vehicles"]
    for key in data["vehicles"]:
        embed.add_field(name=key["name"], value=key["id"], inline=True) 
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="styles", description="Shows Skin Styles")
async def styles(ctx, *, skin):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={skin}')
  data = r.json()

  for sub_dict in data['data']:
    for troll in sub_dict['variants']:
      #print(troll['channel'])
      pp = troll['options']

      for style in pp:
        embed=discord.Embed(title=style['name'], color=color)
        embed.set_thumbnail(url=style['image'])
        embed.set_footer(text=footertext)
        await ctx.send(embed=embed)


@slash.slash(name="icon", description="Get info on a Cosmetic by entering name and get Icon Image")
async def icon(ctx, *, item):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={item}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(title=sub_dict['name'], description=sub_dict['description'], color=color)
      embed.add_field(name='ID', value=sub_dict['id'])
      embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
      embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
      #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")
      
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=sub_dict['introduction']['text'])
        embed.set_image(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=footertext)
        message = await ctx.send(embed=embed)

@slash.slash(name="featured", description="Get info on a Cosmetic by entering name and get Featured Image")
async def featured(ctx, *, item):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={item}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(title=sub_dict['name'], description=sub_dict['description'], color=color)
      embed.add_field(name='ID', value=sub_dict['id'])
      embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
      embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
      #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")
      
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=sub_dict['introduction']['text'])
        embed.set_image(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/featured.png")
        embed.set_footer(text=footertext)
        message = await ctx.send(embed=embed)


@slash.slash(name="newids", description="Get All Cosmetic Names And IDS From Latest Version")
async def newids(ctx):
    r = requests.get("https://fortnite-api.com/v2/cosmetics/br/new")
    data = r.json()
    embed = discord.Embed(title="New Cosmetic ID'S", color=discord.Color.blue())
    text = "```md\n"
    lastSection = data["data"]["items"][0]["type"]["backendValue"]
    for item in data["data"]["items"]:
        if lastSection != item["type"]["backendValue"]:
            text = text + "```"
            embed.add_field(name=lastSection, value=text, inline=False)
            lastSection = item["type"]["backendValue"]
            newid = item["id"]
            newname = item["name"]
            text = f'``` {newid} - {newname}\n'
        else:
            newid = item["id"]
            newname = item["name"]
            text = text + " " + f'{newid} - {newname}\n'
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)

@slash.slash(name="creator", description="Search Info About SAC")
async def creator(ctx, *, code):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/creatorcode?name={code}')
  if r.status_code == 200:
    data = r.json()
    embed=discord.Embed(title=f"Creator Code - {code}", color=color)
    embed.add_field(name="Epic Games Name", value=data['data']['account']['name'], inline=False)
    embed.add_field(name="Epic Games ID", value=data['data']['account']['id'], inline=False)
    embed.add_field(name="Status", value=data['data']['status'], inline=False)
    embed.add_field(name="Verified", value=data['data']['verified'], inline=False)
    await ctx.send(embed=embed)
    embed.set_footer(text=footertext)
  else:
    await ctx.send("Creator Not Found!")

@slash.slash(name="iland", description="Search Info For Creative Map")
async def island(ctx, code):
  await ctx.defer()
  url = f"https://fortniteapi.io/v1/creative/island?code={code}"
  headers = {
      "Authorization": fortnite_api_io_key
  }
  r = requests.post(url, headers=headers)
  data = r.json()
  embed=discord.Embed(title=data['island']['title'], description=f"Creator - {data['island']['creator']}", color=color)
  embed.add_field(name="Island Type", value=data['island']['islandPlotTemplate']['name'])
  embed.add_field(name="Published Date", value=data['island']['publishedDate'])
  embed.add_field(name="Description", value=data['island']['description'])
  embed.set_image(url=data['island']['image'])
  embed.set_footer(text=f"Tags - {data['island']['tags']}")
  embed.set_footer(text=footertext)
  await ctx.send(embed=embed)

@slash.slash(name="aes", description="Sends Fortnite Aes Keys")
async def aes(ctx):
    response = requests.get('https://fortnite-api.com/v2/aes')
    embed=discord.Embed(title='Fortnite Aes Keys', color=000000)
    data = response.json()
    for i in data["data"]["dynamicKeys"]:
      key = i["key"]
      name = i["pakFilename"]
      embed.add_field(name=name, value=key)
    await ctx.send(embed=embed)

@slash.slash(name="login", description="login using your authcode")
async def _help(ctx, *, auth=None):
  if auth == None:
    embed = discord.Embed(title="📲 Log in to your Epic Games account",
                              url='https://www.epicgames.com/id/login?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Fapi%2Fredirect%3FclientId%3D34a02cf8f4414e29b15921876da36f9a%26responseType%3Dcode',
                              color=0x00aaff)
    embed.add_field(name="Please Login Using The Info Below",
                        value="1. Visit the link above to get your login code.\n2. Copy the 32 character code that looks like aabbccddeeff11223344556677889900, located after ?code=.\n3. Send /login <32 character code> to complete your Verifaction process.",
                        inline=True)
    await ctx.send(embed=embed)
  else:
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    payload = f'grant_type=authorization_code&code={auth}'
    headers = {
                'Authorization':
                    'Basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'EPIC_DEVICE=23b3996fb0b24d428e5404799c0f8b17'
            }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
                embed = discord.Embed(color=0xff0000)
                discord.Embed(color=0xff0000)
                embed.add_field(name="Failed",
                                value="The Authorization Code Is Invalid Or Expired",
                                inline=True)
                await ctx.send(embed=embed)
      
    else:
              await ctx.send(content="Successfully logged in!! ")
              db[ctx.author.display_name + 'DN'] = response.json()['displayName']
              db[ctx.author.display_name + 'id'] = response.json()['account_id']
              db[ctx.author.display_name + 'TOKEN'] = response.json()['access_token']

@slash.slash(name="who", description="shows who you are logged into!")
async def who(ctx):
  embed = discord.Embed(color=0xff0000)
  discord.Embed(color=0xff0000)
  embed.add_field(name="Who am i Logged into",
                                value="you are logged into " + db[ctx.author.display_name + 'DN'] + "!",
                                inline=True)
  await ctx.send(embed=embed)

keep_alive()
client.run("MTAzNDM0NTgzOTg1NTk0MzY4MA.G7F6tl.xECBCV9Id6Xx7W5Xw9UYOw-7N6GsnMLYUKwrJQ"))
