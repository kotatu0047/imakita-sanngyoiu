import os
import logging
import discord
import asyncio
import threading
import math
from discord.ext import commands
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            print(f"File {event.src_path} modified, restarting bot...")
            self.restart_callback()

def setup_file_watcher(restart_callback):
    event_handler = RestartHandler(restart_callback)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    return observer

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="hello", description="Responds with 'world'")
async def hello(interaction: discord.Interaction):
    print(f'{interaction.user.name} requested /hello')
    await interaction.response.send_message("discord worldX")

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency
    if math.isnan(latency):
        latency_str = "Unknown"
    else:
        latency_str = f"{round(latency * 1000)}ms"
    print(f'{interaction.user.name} requested /ping')
    await interaction.response.send_message(f"Pong! Latency: {latency_str}")

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    print(f'{interaction.user.name} requested /echo with: {message}')
    await interaction.response.send_message(f"Echo: {message}")

def restart_bot():
    print("Restarting bot...")
    os._exit(1)

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set")
        return

    # Setup file watcher
    observer = setup_file_watcher(restart_bot)

    try:
        print("Starting bot with auto-restart on file changes...")
        bot.run(token)
    except KeyboardInterrupt:
        print("Bot stopped by user")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()