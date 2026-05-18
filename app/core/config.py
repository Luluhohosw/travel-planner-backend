from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///travel_planner_miniapp.db")
SECRET_KEY = os.getenv("SECRET_KEY", "")
