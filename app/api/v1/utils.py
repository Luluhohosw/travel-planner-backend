from __future__ import annotations

from fastapi import APIRouter, Query
from app.schemas.common import Response

router = APIRouter()

TRANSLATIONS = {
    "en": {"你好": "Hello", "谢谢": "Thank you", "多少钱": "How much?", "在哪里": "Where is...?",
           "卫生间在哪里": "Where is the restroom?", "请给我这个": "I'd like this one, please",
           "结账": "Check, please", "救命": "Help!", "我要去...": "I want to go to...",
           "有没有推荐的菜": "What do you recommend?", "可以便宜一点吗": "Can it be cheaper?",
           "我过敏": "I have allergies", "请帮我叫医生": "Please call a doctor",
           "有WiFi吗": "Do you have WiFi?"},
    "ja": {"你好": "こんにちは", "谢谢": "ありがとう", "多少钱": "いくらですか?", "在哪里": "どこですか?",
           "卫生间在哪里": "トイレはどこですか?", "请给我这个": "これをください",
           "结账": "お会計お願いします", "救命": "助けて!", "我要去...": "...に行きたいです",
           "有没有推荐的菜": "おすすめは何ですか?", "可以便宜一点吗": "もう少し安くなりますか?",
           "我过敏": "アレルギーがあります", "请帮我叫医生": "医者を呼んでください",
           "有WiFi吗": "WiFiはありますか?"},
    "ko": {"你好": "안녕하세요", "谢谢": "감사합니다", "多少钱": "얼마예요?", "在哪里": "어디예요?",
           "卫生间在哪里": "화장실이 어디예요?", "请给我这个": "이것 주세요",
           "结账": "계산해 주세요", "救命": "살려주세요!", "我要去...": "...에 가고 싶어요",
           "有没有推荐的菜": "추천 메뉴 있어요?", "可以便宜一点吗": "좀 깎아 주세요?",
           "我过敏": "알레르기가 있어요", "请帮我叫医生": "의사 불러 주세요",
           "有WiFi吗": "와이파이 있어요?"},
}

EXCHANGE_RATES = {
    "CNY": {"USD": 0.14, "JPY": 21.5, "KRW": 185, "EUR": 0.127, "GBP": 0.11,
            "THB": 4.9, "VND": 3400, "HKD": 1.08, "TWD": 4.4, "SGD": 0.187, "MYR": 0.65},
    "USD": {"CNY": 7.15, "JPY": 153, "EUR": 0.91, "GBP": 0.79, "KRW": 1320, "THB": 35},
}

PHRASES = [
    ("你好", "打招呼"), ("谢谢", "道谢"), ("多少钱", "问价"), ("在哪里", "问路"),
    ("卫生间在哪里", "找厕所"), ("请给我这个", "点餐"), ("结账", "买单"), ("救命", "紧急求助"),
    ("我要去...", "打车/问路"), ("有没有推荐的菜", "问美食"), ("可以便宜一点吗", "砍价"),
    ("我过敏", "过敏告知"), ("请帮我叫医生", "医疗求助"), ("有WiFi吗", "问网络"),
]


@router.get("/utils/translate")
async def translate(lang: str = Query(default="en")):
    lang_trans = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    result = [{"phrase": p, "context": c, "translation": lang_trans.get(p, "")} for p, c in PHRASES]
    return Response(data=result)


@router.get("/utils/exchange-rate")
async def exchange_rate(
    amount: float = Query(default=100.0, ge=0),
    from_currency: str = Query(default="CNY"),
    to_currency: str = Query(default="USD"),
):
    from_parts = from_currency.split() if from_currency else ["CNY"]
    to_parts = to_currency.split() if to_currency else ["USD"]
    from_code = from_parts[0].upper()
    to_code = to_parts[0].upper()

    if from_code == to_code:
        result = amount
    elif from_code in EXCHANGE_RATES and to_code in EXCHANGE_RATES[from_code]:
        result = amount * EXCHANGE_RATES[from_code][to_code]
    elif to_code in EXCHANGE_RATES and from_code in EXCHANGE_RATES[to_code]:
        result = amount / EXCHANGE_RATES[to_code][from_code]
    elif from_code == "CNY" or to_code == "CNY":
        result = amount * 7.15 if from_code == "USD" else amount / 7.15
    else:
        result = amount

    return Response(data={
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "result": round(result, 2),
        "disclaimer": "汇率为参考值，非实时数据，请以银行/换汇点当日挂牌价为准",
    })
