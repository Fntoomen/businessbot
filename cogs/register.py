from nextcord.ext import commands
from random import randint,choice
from time import sleep
import nextcord 
import os
import mariadb
import sys

def check_user_exists(id : int):
    try:
        conn = mariadb.connect(
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
    
    cur.execute("SELECT COUNT(discord_id) FROM users WHERE discord_id = ? LIMIT 1", (id,)) 
    user_exists : int = cur.fetchone()
    
    conn.close()

    return user_exists


class Register(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog: Register is on')
   
    @commands.command()
    async def register(self,ctx, name):
        try:
            conn = mariadb.connect(
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

        if not check_user_exists():
            cur.execute("INSERT INTO users (discord_id) VALUES (?);", (ctx.author.id,))
            cur.execute("INSERT INTO companies (name, user_id) VALUES (?, ?)", (name, ctx.author.id))
            conn.commit()
            embed=nextcord.Embed(title="Witamy w świecie biznesu, ", description="Użyj komendy !tutorial", color=0x44ff00)
            await ctx.send(embed=embed)
        else:
            embed=nextcord.Embed(title="Posiadasz już konto", color=0xff0000)
            await ctx.send(embed=embed)
        
        conn.close()

def setup(bot):
    bot.add_cog(Register(bot))