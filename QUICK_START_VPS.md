# Quick Start: Deploy Discord Bot to VPS

## 🚀 One-Command Deployment

1. **Upload your bot code to VPS** (via git clone or scp)
2. **Set your Discord token**:
   ```bash
   cp .env.example .env
   nano .env  # Add your DISCORD_TOKEN
   ```
3. **Deploy**:
   ```bash
   ./deploy.sh
   ```

That's it! Your bot is now running on your VPS.

## 📁 Files Created

Your VPS deployment includes:

### Core Files
- `docker-compose.prod.yml` - Production Docker configuration
- `deploy.sh` - One-command deployment script
- `.env` - Your Discord token and config

### Directories
- `exports/` - Channel exports accessible from host
- `logs/` - Bot logs and monitoring
- `backups/` - Automated backups
- `scripts/` - Maintenance utilities

### Management Scripts
- `scripts/backup.sh` - Create backups
- `scripts/maintenance.sh` - Routine maintenance
- `scripts/update.sh` - Update bot code

## 🔧 Quick Commands

```bash
# View bot status
docker-compose -f docker-compose.prod.yml ps

# View live logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop bot
docker-compose -f docker-compose.prod.yml down

# Start bot
docker-compose -f docker-compose.prod.yml up -d

# Update bot (if using git)
./scripts/update.sh

# Run maintenance
./scripts/maintenance.sh

# Create backup
./scripts/backup.sh
```

## 📝 Bot Commands

Once deployed, these commands work in Discord:

- `/hello` - Test command
- `/ping` - Check bot latency
- `/echo <message>` - Echo a message
- `/maketxt` - Export channel messages to text file

## 📂 File Access

- **Exported files**: `./exports/channel_logs_*.txt`
- **Logs**: `./logs/bot.log`
- **Backups**: `./backups/discord_bot_backup_*.tar.gz`

## 🔍 Troubleshooting

**Bot won't start?**
```bash
docker-compose -f docker-compose.prod.yml logs
```

**Can't find exported files?**
```bash
ls -la exports/
```

**Need to restart?**
```bash
docker-compose -f docker-compose.prod.yml restart
```

## 📚 Full Documentation

See `VPS_DEPLOYMENT.md` for detailed instructions.

---

**Ready to deploy?** Just run `./deploy.sh` and your Discord bot will be live! 🎉