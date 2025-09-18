# Discord Bot VPS Deployment Guide

This guide will help you deploy your Discord bot to a VPS (Virtual Private Server).

## Prerequisites

1. **VPS with Ubuntu 20.04+ or similar**
2. **SSH access to your VPS**
3. **Discord Bot Token** (from Discord Developer Portal)
4. **Basic command line knowledge**

## Step 1: Prepare Your VPS

### Connect to your VPS
```bash
ssh username@your-vps-ip
```

### Update system packages
```bash
sudo apt update && sudo apt upgrade -y
```

### Install basic dependencies
```bash
sudo apt install -y curl git
```

## Step 2: Upload Your Bot Code

### Option A: Using Git (Recommended)
```bash
# Clone your repository
git clone https://github.com/yourusername/your-bot-repo.git
cd your-bot-repo
```

### Option B: Using SCP
```bash
# From your local machine
scp -r /path/to/bot-folder username@your-vps-ip:/home/username/
```

## Step 3: Configure Environment

### Set up your Discord token
```bash
# Copy the example environment file
cp .env.example .env

# Edit the environment file
nano .env
```

Add your Discord bot token:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

## Step 4: Deploy the Bot

### Run the deployment script
```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Install Docker and Docker Compose if needed
- Create necessary directories
- Build and start your bot container
- Set up logging and monitoring

## Step 5: Verify Deployment

### Check if the bot is running
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Test the bot
Go to your Discord server and try the commands:
- `/hello` - Should respond with "discord worldX"
- `/ping` - Should show bot latency
- `/maketxt` - Should export channel messages to a text file

## Managing Your Bot

### Start the bot
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Stop the bot
```bash
docker-compose -f docker-compose.prod.yml down
```

### Restart the bot
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update the bot
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### View exported files
```bash
ls -la exports/
```

## Troubleshooting

### Bot not starting
1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify Discord token in `.env` file
3. Ensure bot has proper permissions in Discord server

### Permission errors
```bash
# Fix permissions for exports directory
chmod 755 exports/
```

### Memory issues
```bash
# Check system resources
free -h
df -h
```

### Container issues
```bash
# Remove all containers and rebuild
docker-compose -f docker-compose.prod.yml down
docker system prune -af
docker-compose -f docker-compose.prod.yml up -d --build
```

## Security Considerations

1. **Firewall**: Only open necessary ports
```bash
sudo ufw enable
sudo ufw allow ssh
```

2. **Regular updates**: Keep your VPS updated
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Backup**: Regularly backup your `.env` file and exported data

4. **Monitoring**: Check logs regularly for any issues

## File Locations

- **Bot logs**: `./logs/`
- **Exported channel logs**: `./exports/`
- **Configuration**: `.env`
- **Docker logs**: Use `docker-compose logs`

## Support

If you encounter issues:
1. Check the logs first
2. Verify your Discord token and bot permissions
3. Ensure your VPS has enough resources (RAM, disk space)
4. Check Discord API status

## Commands Reference

| Command | Description |
|---------|-------------|
| `./deploy.sh` | Deploy/redeploy the bot |
| `docker-compose -f docker-compose.prod.yml logs -f` | View live logs |
| `docker-compose -f docker-compose.prod.yml ps` | Check container status |
| `docker-compose -f docker-compose.prod.yml down` | Stop the bot |
| `docker-compose -f docker-compose.prod.yml up -d` | Start the bot |