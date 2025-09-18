# Discord Bot

A simple Discord bot that responds to the `/hello` slash command with "world".

## Setup

1. **Create a Discord Application and Bot**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a bot
   - Copy the bot token

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```

3. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

## Usage

1. Invite the bot to your Discord server with the proper permissions
2. Use the `/hello` slash command in any channel
3. The bot will respond with "world"

## Development

The bot code is located in `bot/main.py`. To make changes:

1. Edit the code
2. Restart the container: `docker-compose restart`

## Project Structure

```
.
├── bot/
│   └── main.py          # Main bot code
├── docker-compose.yml   # Docker development setup
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variable template
└── README.md         # This file
```

app id
1418152335514927116

public key
8451abb71b33b4d1dc535398c3b403f467839ec7b7e420fe75455244522016be