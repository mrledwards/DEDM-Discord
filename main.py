import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from replit import db
from pathlib import Path
import sqlite3
from sqlite3 import Error
import os
from db import *


intents = discord.Intents.default()
intents.members = True

secret_key = ""

bot = commands.Bot(command_prefix='!', description="DEDM Discord bot", intents=intents)

DBPATH = "bot.db"
if os.path.isfile(str(DBPATH)):
  print("db exists")
else:
	blank_db = sqlite3.connect(str(DBPATH))
	init_db()
	print("db created")
  


@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')
  await bot.change_presence(activity=discord.Game(name="StarTrek Fleet Command"))

@bot.command(name='?', aliases=['info'])
async def _bot(ctx):
  embed = discord.Embed(title="Help Commands", description="The following commands are available")
  embed.set_author(name="DEDM Bot Help", icon_url="https://i.imgur.com/8C2kiJ9.png")
  embed.add_field(name="!epic have x", value="add/update how many epic BP's you have (x)", inline="False")
  embed.add_field(name="!epic list all", value="lists members and how many BP's they in in a DM to you", inline="False")
  embed.add_field(name="!epic obtained all", value="use this when you have all the BP's to be taken off the list", inline="False")
  embed.add_field(name="!roe", value="sends a DM with current ROE", inline="False")
  embed.add_field(name="!?", value="This help message", inline="False")
  embed.add_field(name="!event", value="sends a link to the event xls to you via DM")
  embed.set_footer(text="if you have any questions, or need help, please feel free to contact Wakdem")
  await ctx.message.delete()
  await ctx.author.send(embed=embed)



@bot.command(name="event")
async def _bot(ctx):
  await ctx.message.delete()
  embed=discord.Embed(title="Event Information Link", url="https://docs.google.com/spreadsheets/d/e/2PACX-1vT_KZ7U4STiA18gvAFs0jCwpIKobcUGGcteoLo4hDcE3Pkn9W2bqix6m2IeQ818EY_qgGlqk4Bisnly/pubhtml", description="List to event spreadsheet")
  embed.set_author(name="DEDM Bot", icon_url="https://i.imgur.com/XCL9PUZ.jpg")
  embed.add_field(name="Link:", value="https://docs.google.com/spreadsheets/d/e/2PACX-1vT_KZ7U4STiA18gvAFs0jCwpIKobcUGGcteoLo4hDcE3Pkn9W2bqix6m2IeQ818EY_qgGlqk4Bisnly/pubhtml", inline=False)
  await ctx.author.send(embed=embed)


@bot.command(name='roe', aliases=['ROE']) #sends user a DM with current roe
async def _bot(ctx):
  await ctx.message.delete()
  await ctx.author.send("__**Current ROE:**__ \n **SUB W40:** \n 1 Zero node hits are allowed with a 10 min warning \(hit zeroed whether under or over protected cargo\) for w40 to w48 nodes. \n 2 Northstar with full cargo is considered a zero node and can be hit in line with point 1 above. i.e. with a 10 min warning. \n 3 Over Protected hits are not allowed \n 4 All Warships are KOS with no limitations on Nodes , at your own risk.\n 5 Botany Bay and Frengi DVor (except for Suliban and other w40 - w48 Lat systems) ships Are Banned. \n 6 Over Protected (OP) Lat node hits are fair game during Latinum \n Rush events on w40 - w48 nodes.\n 7 Share your Nodes\n \n \n **W40-W48** \n 1 Zero node hits are allowed with a 10 min warning for w40 to w48 nodes. \n 2 Northstar with full cargo is considered a zero node and can be hit in line with point 1 above. i.e. with a 10 min warning.\n 3 Over Protected hits are not allowed\n 4 All Warships are KOS with no limitations on Nodes , at your own risk.\n 5 Botany Bay and Frengi D'Vor (except for Suliban and other w40 - w48 Lat systems) ships Are Banned. \n 6 Over Protected (OP) Lat node hits are fair game during Latinum Rush events on w40 - w48 nodes.\n7 Share your Nodes")
 

@bot.event
async def on_member_join(member):
  print("member has joined")
#  await member.create_dm() #Create a DM chat with the new user
  await member.send("Welcome to DEDM Discord server. I am the freindly helper. \n if you are here to report an ROE violation, please reply with \"roe\" and you will have access to the appropriate channel")
  print("dm sent")
  response = await bot.wait_for('message', timeout=30.0)
  if response == "roe" or "ROE":
    await member.send('you will be assigned the role for roe complaints')
    u = member.name
    r = discord.utils.get(member.guild.roles, name="EXTERNAL-roe-violations")
    await member.add_roles(r)
    await member.send("role has been updated")
    print("roe selected")
  else:
    await member.send("no role will currently be set, please wait for an admin to assign a role")
    print("nothing selected")


@bot.command(name='greetings', aliases=['greeting', 'hi', 'hello']) #a simple greeting
async def _bot(ctx):
    """Is the bot cool?"""
    text_to_send = ("welcome " + ctx.message.author.mention + ", stay a while and listen")
    await ctx.message.delete()
    await ctx.send(text_to_send)

@bot.command(name="author", aliases=['who', 'version'])
async def _bot(ctx):
  await ctx.send("DEDM Discord Bot, Written by Wakdem for the DEDM alliance of STFC Server 193")


@bot.command(name="epic")
async def _bot(ctx, arg1, arg2):
	await ctx.message.delete()
	memberName = str(ctx.author.display_name)
	if arg1 == "have":
	
		m = ctx.message.content
		x = m.rsplit(" ")
		bp = x[-1]
		print(memberName, arg2, bp)
		conn = db_connect()
		c = conn.cursor()
		sql = f"""INSERT OR REPLACE INTO epic_bp_needed (discord_name, ship_name, bp_have) VALUES ('{memberName}', '{arg2}', {bp});"""
		#print(sql)
		conn.execute(sql)
		conn.commit()
		conn.close()
		await ctx.author.send("updated list")
	elif arg1 == "obtained":

		await ctx.author.send("Congratulations!!!!! May you fight with honour. \n Your information is now removed from the list \n https://i.imgur.com/C3Oiobz.gif")
		conn = db_connect()
		c= conn.cursor()
		sql = f"""DELETE FROM epic_bp_needed WHERE discord_name = '{memberName}' AND ship_name = '{arg2}';"""
		conn.execute(sql)
		conn.commit()
		conn.close()
	elif arg1 == "list":
		conn = db_connect()
		c = conn.cursor()
		sql = """SELECT discord_name, ship_name, bp_have FROM epic_bp_needed;"""
		c.execute(sql)
		conn.commit()
		fetched = c.fetchall()
		conn.close
		results = "\n".join(map(str, fetched)) 
		await ctx.author.send("Member | Ship | BP \n" + results)
	else:
		await ctx.author.send("Something went wrong, please try again") 


@bot.command(name="admin")
#@commands.has_role("Leadership")
async def _bot(ctx, arg1):
  await ctx.message.delete()
  role = discord.utils.get(ctx.guild.roles, id=772697868225740820) #change id to the target id for the server (539467965276356620) (772697868225740820) is testing only

  if role in ctx.author.roles:
  #if member.has_role("Leadership"):
    m = ctx.message.content
    if arg1 == "delete":
    #  m = ctx.message.content
      to_delete = m.replace("!admin ", "").replace("delete ", "")
      await ctx.author.send(to_delete + " will be removed")
      del db[to_delete]
    elif arg1 == "update":
      to_update = m.replace("!admin ", "").replace("update ", "")
      m = to_update.rsplit(" ")
      #s = m.rsplit(" ")
      x = m[-1]
      m.remove(x)
      u = " ".join(m)
      db[u] = x
      await ctx.author.send("member " + u + " updated with " + x + " BP total")

    else:
      await ctx.author.send("something went wrong")
  else:
    await ctx.author.send("you don't have permission to do that")


#del db["wakdem#4244"]


keep_alive()
init_db()
token = os.environ.get("TOKEN")
bot.run(token)

#to do, see if can add what ship people are going for in the epic section. maybe acc too.