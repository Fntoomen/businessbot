import nextcord
from nextcord.ext import commands
import os
import mariadb
import sys

conn = mariadb.connect (
    user="root",
    password="passwd",
    host="localhost",
    port=3306,
    database="bot"
)
cur = conn.cursor()

def check_user_exists(discordID: int):
    cur.execute("SELECT COUNT(discord_id) FROM users WHERE discord_id = ? LIMIT 1", (discordID,))
    res = cur.fetchone()
    if res is not None:
        res = res[0]
    return res

def check_company_exists(name):
    cur.execute("SELECT COUNT(name) FROM companies WHERE LOWER(name) = ? LIMIT 1", (name.lower(),))
    res = cur.fetchone()
    if res is not None:
        res = res[0]
    return res

class Register(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog: Register is on')

    @commands.command()
    async def register(self, ctx):
        discordID = ctx.author.id
        if not check_user_exists(discordID):
            cur.execute("INSERT INTO users (discord_id) VALUES (?);", (discordID,))
            conn.commit()
            embed=nextcord.Embed(title="Witamy w świecie biznesu, ", description="Użyj komendy !tutorial", color=0x44ff00)
            await ctx.send(embed=embed)
        else:
            embed=nextcord.Embed(title="Posiadasz już konto", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def company(self, ctx, name):
        discordID = ctx.author.id
        if not check_company_exists(name):
            cur.execute("SELECT (user_id) FROM users WHERE discord_id = ?", (discordID,))
            userID = cur.fetchone()
            if userID is not None:
                userID = userID[0]
            cur.execute("INSERT INTO companies (name, user_id) VALUES (?, ?)", (name, userID))
            conn.commit()
            embed=nextcord.Embed(title="Założono firmę, ", description=f"Nazwa firmy: {name}", color=0x44ff00)
            await ctx.send(embed=embed)
        else:
            embed=nextcord.Embed(title="Firma z tą nazwą już istnieje", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Register(bot))
