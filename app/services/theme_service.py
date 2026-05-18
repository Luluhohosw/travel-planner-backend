"""主题色板服务 — 四套季节主题"""
from datetime import datetime

SEASONS = {
    "spring": {
        "name": "樱花拿铁",
        "bg_main": "#fef9f4", "bg_card": "#fff8f0", "bg_sidebar": "#fef5f7",
        "text_primary": "#4a3728", "text_secondary": "#7a6b5c", "text_heading": "#c97b5d",
        "accent": "#e8a87c", "accent_soft": "#fbe8d8", "border": "#f0d5c0",
        "btn_primary_bg": "#e8a87c", "btn_primary_text": "#ffffff", "btn_hover_glow": "rgba(232,168,124,0.4)",
        "tab_active_bg": "#fbe8d8", "tab_active_text": "#c97b5d",
        "alert_info_bg": "#fef5e7", "alert_info_border": "#f9e4b7",
        "shadow_card": "0 2rpx 12rpx rgba(180,140,110,0.12)",
    },
    "summer": {
        "name": "海盐汽水",
        "bg_main": "#f4f9fb", "bg_card": "#f5fafc", "bg_sidebar": "#f2f8fb",
        "text_primary": "#2c3e50", "text_secondary": "#5d7b93", "text_heading": "#3e8ab3",
        "accent": "#7ab8d4", "accent_soft": "#d8eef7", "border": "#c5dce8",
        "btn_primary_bg": "#7ab8d4", "btn_primary_text": "#ffffff", "btn_hover_glow": "rgba(122,184,212,0.4)",
        "tab_active_bg": "#d8eef7", "tab_active_text": "#3e8ab3",
        "alert_info_bg": "#e8f4f8", "alert_info_border": "#b8d8e8",
        "shadow_card": "0 2rpx 12rpx rgba(100,160,190,0.12)",
    },
    "autumn": {
        "name": "焦糖玛奇朵",
        "bg_main": "#fdf8f2", "bg_card": "#fef9f3", "bg_sidebar": "#fdf6ef",
        "text_primary": "#3d2e1f", "text_secondary": "#6b5d4a", "text_heading": "#b87d4a",
        "accent": "#c8966a", "accent_soft": "#f2e0cc", "border": "#e0ccb0",
        "btn_primary_bg": "#c8966a", "btn_primary_text": "#ffffff", "btn_hover_glow": "rgba(200,150,106,0.4)",
        "tab_active_bg": "#f2e0cc", "tab_active_text": "#b87d4a",
        "alert_info_bg": "#fdf3e5", "alert_info_border": "#f0d5a8",
        "shadow_card": "0 2rpx 12rpx rgba(160,120,80,0.12)",
    },
    "winter": {
        "name": "芋泥波波",
        "bg_main": "#f7f5fa", "bg_card": "#faf7fc", "bg_sidebar": "#f6f3f9",
        "text_primary": "#3a3045", "text_secondary": "#6b5e78", "text_heading": "#8b7aaa",
        "accent": "#a894c4", "accent_soft": "#e8e0f2", "border": "#d5cce0",
        "btn_primary_bg": "#a894c4", "btn_primary_text": "#ffffff", "btn_hover_glow": "rgba(168,148,196,0.4)",
        "tab_active_bg": "#e8e0f2", "tab_active_text": "#8b7aaa",
        "alert_info_bg": "#f0eaf6", "alert_info_border": "#d0c0e4",
        "shadow_card": "0 2rpx 12rpx rgba(130,110,160,0.12)",
    },
}

SEASON_DECOR = {
    "spring": {"emoji": "🌸🌿🌺", "mascot_name": "樱花鹿宝"},
    "summer": {"emoji": "🌊🐚☀️", "mascot_name": "海盐鹿宝"},
    "autumn": {"emoji": "🍂🍁🌾", "mascot_name": "焦糖鹿宝"},
    "winter": {"emoji": "❄️⛄🌟", "mascot_name": "芋泥鹿宝"},
}


def get_season(month: int = None) -> str:
    if month is None:
        month = datetime.now().month
    if month in (3, 4):
        return "spring"
    elif month in (5, 6, 7, 8):
        return "summer"
    elif month in (9, 10, 11):
        return "autumn"
    else:
        return "winter"


def get_colors(season: str) -> dict:
    return SEASONS.get(season, SEASONS["spring"])
