import os
import logging
import discord
import asyncio
import threading
import math
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()

# Production logging setup
if os.getenv('ENVIRONMENT') == 'production':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Configure logging for production
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )
else:
    # Development logging
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
    logging.info(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logging.error(f"Failed to sync commands: {e}")

@bot.event
async def on_error(event, *args, **kwargs):
    logging.error(f'An error occurred in event {event}', exc_info=True)

@bot.event
async def on_command_error(ctx, error):
    logging.error(f'Command error: {error}', exc_info=True)

@bot.tree.command(name="hello", description="Responds with 'world'")
async def hello(interaction: discord.Interaction):
    logging.info(f'{interaction.user.name} requested /hello')
    await interaction.response.send_message("discord worldX")

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency
    if math.isnan(latency):
        latency_str = "Unknown"
    else:
        latency_str = f"{round(latency * 1000)}ms"
    logging.info(f'{interaction.user.name} requested /ping')
    await interaction.response.send_message(f"Pong! Latency: {latency_str}")

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    logging.info(f'{interaction.user.name} requested /echo with: {message}')
    await interaction.response.send_message(f"Echo: {message}")

@bot.tree.command(name="maketxt", description="Export all channel messages to a text file")
async def maketxt(interaction: discord.Interaction):
    logging.info(f'{interaction.user.name} requested /maketxt in channel: {interaction.channel.name}')

    # Send initial response
    await interaction.response.send_message("📝 Starting to export channel messages to text file...")

    try:
        # Get channel and create filename
        channel = interaction.channel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_channel_name = "".join(c for c in channel.name if c.isalnum() or c in ('-', '_')).rstrip()

        # Create exports directory if it doesn't exist
        exports_dir = "exports"
        os.makedirs(exports_dir, exist_ok=True)

        filename = os.path.join(exports_dir, f"channel_logs_{safe_channel_name}_{timestamp}.txt")

        # Fetch all messages from the channel
        messages = []
        async for message in channel.history(limit=None, oldest_first=True):
            # Format message with timestamp, author, and content
            timestamp_str = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            author_name = message.author.display_name
            content = message.content or "[No text content]"

            # Handle attachments
            if message.attachments:
                attachment_info = ", ".join([f"[Attachment: {att.filename}]" for att in message.attachments])
                content += f" {attachment_info}"

            # Handle embeds
            if message.embeds:
                content += f" [Embeds: {len(message.embeds)}]"

            formatted_message = f"[{timestamp_str}] {author_name}: {content}"
            messages.append(formatted_message)

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Channel Log Export: #{channel.name}\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Messages: {len(messages)}\n")
            f.write("=" * 50 + "\n\n")

            for message in messages:
                f.write(message + "\n")

        # Upload file to Discord
        try:
            with open(filename, 'rb') as f:
                discord_file = discord.File(f, filename=os.path.basename(filename))
                follow_up_message = f"✅ Successfully exported {len(messages)} messages from #{channel.name}!"
                await interaction.followup.send(follow_up_message, file=discord_file)

            logging.info(f"File {filename} uploaded to Discord for user {interaction.user.name}")

        except Exception as upload_error:
            logging.error(f"Failed to upload file to Discord: {upload_error}", exc_info=True)
            # Fallback to just sending a message about local file
            follow_up_message = f"✅ Successfully exported {len(messages)} messages to `{filename}`, but failed to upload to Discord. File saved locally in exports folder."
            await interaction.followup.send(follow_up_message)

    except discord.Forbidden:
        await interaction.followup.send("❌ Error: I don't have permission to read message history in this channel.")
    except Exception as e:
        error_message = f"❌ Error occurred while exporting messages: {str(e)}"
        logging.error(f"Error in maketxt command: {e}", exc_info=True)
        await interaction.followup.send(error_message)

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