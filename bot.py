import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command('synccommands')
async def synccommands(ctx):
    await bot.tree.sync()
    await ctx.send("同步完成")


@bot.command('yo')
async def yo(ctx):
    """測試機器人是否在線"""
    await ctx.send("hey bro")


@bot.command('add')
async def add(ctx, a: int, b: int):
    """把兩個數字作加法"""
    await ctx.send(a + b)


@bot.hybrid_command('play')
async def play(ctx):
    await ctx.send("選擇你要出什麼吧", view=PlayView())


import random  

class PlayView(discord.ui.View):
    def get_content(self, player_choice):
        options = ["剪刀", "石頭", "布"]
        bot_choice = random.choice(options) 
        
        win_map = {
            "剪刀": "布",
            "石頭": "剪刀",
            "布": "石頭"
        }

        if player_choice == bot_choice:
            result = "雙方平手！"
        elif win_map[player_choice] == bot_choice:
            result = "恭喜你贏了！"
        else:
            result = "可惜你輸了..."

        return f"你出了 **{player_choice}**, 機器人出了 **{bot_choice}**\n結果：{result}"

    @discord.ui.button(label="剪刀", style=discord.ButtonStyle.green, emoji="✂️")
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="石頭", style=discord.ButtonStyle.green, emoji="🪨")
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="布", style=discord.ButtonStyle.green, emoji="📄")
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="不玩了", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="遊戲已結束", view=None)



bot.run(token)