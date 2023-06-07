from nextcord.ext import commands
from random import randint,choice
from time import sleep
import nextcord
import os
import mariadb
import sys

try:
	conn = mariadb.connect (
	user="mariadb",
	password="passwd",
	host="localhost",
	port=3306,
	database="BusinessBot"
	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

cur = conn.cursor()

def check_user_exists(id : int):
	cur.execute("SELECT COUNT(discord_id) FROM users WHERE discord_id = ? LIMIT 1", (id,))
	return int(cur.fetchone())


class Register(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('Cog: Register is on')

	@commands.command()
	async def register(self, ctx, name):
		if not check_user_exists():
            discordID = ctx.author.id
			cur.execute("INSERT INTO users (discord_id) VALUES (?);", (discordID,))
			cur.execute("SELECT (user_id) FROM users WHERE discord_id = ?", (discordID,))
            userID = cur.user_id
			cur.execute("INSERT INTO companies (name, user_id) VALUES (?, ?)", (name, userID))
			embed=nextcord.Embed(title="Witamy w świecie biznesu, ", description="Użyj komendy !tutorial", color=0x44ff00)
			await ctx.send(embed=embed)
		else:
			embed=nextcord.Embed(title="Posiadasz już konto", color=0xff0000)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Register(bot))

conn.close()
