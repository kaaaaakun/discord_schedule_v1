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
TEST_SERVER_ID=1252162158574305373
THREAD_ID=1253246372791062540

intents = discord.Intents.default()
intents.messages = True  # メッセージ関連のイベントを有効にする
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as スケジューラー')  # ログインしたユーザーの名前を出力
    await send_message("起動しましたよ", DEFAULT_CHANNEL_ID)

# プログラム終了時にメッセージを送信する関数
async def to_close(msg):
    await send_message(msg, DEFAULT_CHANNEL_ID)

async def send_message(msg, channel_id):
    try:
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(msg)
            print(f'{channel.guild.name} : {channel.name} : (ID: {channel.guild.id}): (msg:' + msg + ')')
        else:
            print(f'Channel with ID {channel_id} not found.')
    except Exception as e:
        print(f'Error sending message: {e}')

async def job(msg, channel_id):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M")  # フォーマットを指定して時間を短くする
    await send_message(str(formatted_time) + " : " + msg, channel_id)

def schedule_job(msg, weekdays, channel_id):
    now = datetime.datetime.now()
    if now.weekday() in weekdays:
        client.loop.call_soon_threadsafe(asyncio.create_task, job(msg, channel_id))

# スケジュール設定
schedule.every().day.at("19:55").do(lambda: schedule_job("<@952322426769920010>@kaaaaakun_tokazaki yaruyo", range(7), DEFAULT_CHANNEL_ID))  # 0-6: Monday to Sunday
schedule.every().day.at("19:55").do(lambda: schedule_job("aa毎日", range(7), TEST_SERVER_ID))  # 0-6: Monday to Sunday
schedule.every().day.at("20:57").do(lambda: schedule_job("どう？日", range(7), THREAD_ID))  # 0-6: Monday to Sunday
schedule.every().day.at("16:13").do(lambda: schedule_job("火曜日", [1], DEFAULT_CHANNEL_ID))  # 1: Tuesday
schedule.every().day.at("16:13").do(lambda: schedule_job("スケジュール", range(5), DEFAULT_CHANNEL_ID))  # 0-4: Monday to Friday
schedule.every().day.at("16:13").do(lambda: schedule_job("確定日程", [], DEFAULT_CHANNEL_ID))  # 1: Tuesday

# スケジュールを実行する関数
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# スケジュール実行を別スレッドで行う
import threading
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

# メイン関数
async def main():
    await client.start(TOKEN)

# 実行部分
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, shutting down...")
        loop.run_until_complete(to_close("正常終了します。"))
        task.cancel()
        loop.run_until_complete(client.close())
    except Exception as e:
        print(f"Exception detected: {e}", flush=True)
        loop.run_until_complete(to_close("botが死にました"))
        task.cancel()
        loop.run_until_complete(client.close())
    finally:
        loop.close()
