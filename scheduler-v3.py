import datetime
import schedule
import time
import discord
from dotenv import load_dotenv
import os
import asyncio

# .envファイルを読み込みます
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DEFAULT_CHANNEL_ID = int(os.getenv('DEFAULT_CHANNEL_ID'))

intents = discord.Intents.default()
intents.messages = True  # メッセージ関連のイベントを有効にする
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')  # ログインしたユーザーの名前を出力
    await send_message("起動しました", DEFAULT_CHANNEL_ID)

async def send_message(msg, channel_id):
    try:
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(msg)
            print(f'Message sent to channel {channel.name}')
        else:
            print(f'Channel with ID {channel_id} not found.')
    except Exception as e:
        print(f'Error sending message: {e}')

async def job(msg, channel_id):
    now = datetime.datetime.now()
    print(str(now) + " 通知したよ")
    await send_message(str(now) + " : " + msg, channel_id)

def schedule_job(msg, weekdays, channel_id):
    now = datetime.datetime.now()
    if now.weekday() in weekdays:
        client.loop.call_soon_threadsafe(asyncio.create_task, job(msg, channel_id))

# スケジュール設定
schedule.every().day.at("16:13").do(lambda: schedule_job("毎日", range(7), DEFAULT_CHANNEL_ID))  # 0-6: Monday to Sunday
schedule.every().day.at("16:13").do(lambda: schedule_job("火曜日", [1], DEFAULT_CHANNEL_ID))  # 1: Tuesday
schedule.every().day.at("16:13").do(lambda: schedule_job("スケジュール", range(5), DEFAULT_CHANNEL_ID))  # 0-4: Monday to Friday

# スケジュールを実行する関数
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# スケジュール実行を別スレッドで行う
import threading
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

# ボットの起動
client.run(TOKEN)

