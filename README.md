# Discord Bot

A Discord bot with auto-restart functionality that includes `/hello`, `/ping`, and `/echo` slash commands.

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

## Available Commands

- `/hello` - Responds with "discord world"
- `/ping` - Shows bot latency in milliseconds
- `/echo <message>` - Echoes back your message

## Usage

1. Invite the bot to your Discord server with the proper permissions
2. Use any of the slash commands listed above in any channel

## Development

The bot code is located in `bot/main.py`. The bot includes automatic restart functionality that monitors file changes.

### Auto-Restart Feature
- The bot automatically restarts when any `.py` file is modified
- Docker Compose will automatically restart the bot process if it crashes
- No manual intervention needed during development

### Manual Docker Operations

**Start the bot:**
```bash
docker-compose up --build
```

**Start in background:**
```bash
docker-compose up -d --build
```

**Restart the bot:**
```bash
docker-compose restart
```

**Stop the bot:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Rebuild and restart:**
```bash
docker-compose down && docker-compose up --build
```

## Testing

The project includes comprehensive automated testing with multiple options:

### Automatic Testing (Recommended for Development)

**Standalone Test Watcher**
```bash
python watch_and_test.py
```
- Runs tests automatically when any Python file changes
- Can be used independently of the bot
- Shows detailed test output

### Manual Testing

**Install test dependencies:**
```bash
pip install -r requirements.txt
```

**Run all tests:**
```bash
pytest
```

**Run tests with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest test_bot.py -v
```

**Quick test run:**
```bash
pytest -q
```

### Test Coverage
- Command functionality testing (`/hello`, `/ping`, `/echo`)
- User interaction mocking
- Bot configuration validation
- Latency testing for ping command (handles both connected/disconnected states)
- Message parameter testing for echo command
- Command registration verification
- Auto-restart functionality testing

## Project Structure

```
.
├── bot/
│   ├── main.py              # Main bot code with auto-restart
│   └── test_commands.py     # Command-specific tests
├── docker-compose.yml       # Docker development setup
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies (includes pytest)
├── test_bot.py            # Main test suite
├── watch_and_test.py      # Standalone test watcher script
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment variable template
└── README.md            # This file
```

app id
1418152335514927116

public key
8451abb71b33b4d1dc535398c3b403f467839ec7b7e420fe75455244522016be

vps pass
Kotatu@0047