import os

# Load from .env file if it exists
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip("\"'"))

TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
GUILD_ID = int(os.getenv("GUILD_ID", 1540883913914978306))