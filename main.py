import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup
import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): 
    return "بۆتەکەی ئاڤا سپۆرت کاردەکات!"
def run(): 
    app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# ⚠️ لێرەدا ئایدی کەنالە وەرزشییەکەی خۆت دابنێ
CHANNEL_ID = 123456789012345678  
LAST_NEWS_URL = ""

@bot.event
async def on_ready():
    print(f'{bot.user} بە سەرکەوتووانە بەستراوەتەوە بە ئاڤا سپۆرت!')
    check_ava_sport.start()

@tasks.loop(minutes=10)
async def check_ava_sport():
    global LAST_NEWS_URL
    channel = bot.get_channel(CHANNEL_ID)
    if not channel: 
        return

    try:
        url = "ava.news"
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        news_box = soup.find('a', href=True) 
        
        if news_box and "/sport/" in news_box['href']:
            news_link = news_box['href']
            if not news_link.startswith("https"):
                news_link = "https://ava.news" + news_link
            
            if news_link != LAST_NEWS_URL:
                LAST_NEWS_URL = news_link
                
                embed = discord.Embed(
                    title="🚨 نوێترین هەواڵ لە ئاڤا سپۆرتەوە",
                    url=news_link,
                    color=discord.Color.red()
                )
                embed.description = f"بۆ خوێندنەوەی تەواوی هەواڵەکە کلیک لە بەستەری سەرەوە بکە.\n\n🔗 {news_link}"
                embed.set_footer(text="AVA Sport Bot • خۆکار")
                
                await channel.send(embed=embed)
    except Exception as e:
        print("هەڵەیەک ڕوویدا لە کاتی هێنانی هەواڵ:", e)

Thread(target=run).start()
bot.run(os.environ.get('DISCORD_TOKEN'))
