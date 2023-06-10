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

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog: Moderation is on')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member):
        await bot.kick(member)
        cur.execute("SELECT user_id FROM users WHERE discord_id = ?", (member.id,))
        userID = cur.fetchone()
        if userID is not None:
            userID = userID[0]
        cur.execute("DELETE FROM users WHERE user_id = ?", (userID,))
        cur.execute("DELETE FROM companies WHERE user_id = ?", (userID,))
        conn.commit()
        embed=nextcord.Embed(title="Wyrzucono użytkownika", description=member.mention, color=0x44ff00)
        await ctx.send(embed=embed)
    @kick.error
    async def kick_error(error, ctx):
        if isinstance(error, MissingPermissions):
            embed=nextcord.Embed(title="Nie masz uprawnień do wyrzucania!", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: nextcord.Member):
        await bot.ban(member)
        cur.execute("SELECT user_id FROM users WHERE discord_id = ?", (member.id,))
        userID = cur.fetchone()
        if userID is not None:
            userID = userID[0]
        cur.execute("DELETE FROM users WHERE user_id = ?", (userID,))
        cur.execute("DELETE FROM companies WHERE user_id = ?", (userID,))
        conn.commit()
        embed=nextcord.Embed(title="Zbanowano użytkownika", description=member.mention, color=0x44ff00)
        await ctx.send(embed=embed)
    @ban.error
    async def ban_error(error, ctx):
        if isinstance(error, MissingPermissions):
            embed=nextcord.Embed(title="Nie masz uprawnień do wyrzucania!", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_money(self, ctx, member: nextcord.Member):
        cur.execute("SELECT user_id FROM users WHERE discord_id = ?", (member.id,))
        userID = cur.fetchone()
        if userID is not None:
            userID = userID[0]
        cur.execute("UPDATE users SET money = 0 WHERE user_id = ?", (userID,))
        conn.commit()
        embed=nextcord.Embed(title="Wyczyszczono konto użytkownika", description=member.mention, color=0x44ff00)
        await ctx.send(embed=embed)
    @clear_money.error
    async def clear_money_error(error, ctx):
        if isinstance(error, MissingPermissions):
            embed=nextcord.Embed(title="Nie masz uprawnień do wyczyszczenia konta!", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))

conn.close()
