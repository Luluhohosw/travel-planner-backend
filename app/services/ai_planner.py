"""
DeepSeek API 行程生成服务
"""
import json
import re
from openai import AsyncOpenAI
from app.core.config import DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


def _get_client(api_key: str = "") -> AsyncOpenAI:
    return AsyncOpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


SYSTEM_PROMPT = """你是一位资深旅行规划师，拥有全球旅行经验。你需要为用户生成详细、实用、个性化的旅行计划。

## 你的能力
- 熟悉全球各大旅游城市的景点、美食、交通、住宿
- 深度了解主流旅行/生活平台的真实信息
  - **小红书**: 最新游记、真实游客体验、拍照攻略、小众景点、避坑指南、穿搭建议
  - **抖音**: 当地热门打卡点、网红美食、景区实时客流、团购优惠套餐
  - **携程**: 机票/酒店/门票实时价格、用户真实评价、跟团游/自由行产品参考
- 了解各平台的优惠模式（抖音团购、美团、携程、飞猪、小红书店铺等）
- 关注旅行预算优化，知道什么时候买票最便宜
- 关注实用细节：周一闭馆、体力分配、拍照时机、避坑指南

## 信息来源要求
每条信息应注明参考平台来源，确保信息可靠性：
- 价格信息优先参考携程、美团官方公示价
- 景点体验/拍照攻略优先参考小红书真实游记
- 当地热门趋势/网红打卡参考抖音
- 美食推荐综合小红书笔记+美团/大众点评评价
- 避坑指南综合小红书+抖音评论区真实反馈

## 输出要求
你必须输出严格合法的JSON，格式如下：

```json
{
  "date_advice": {
    "best_season": "最佳出行季节及原因",
    "avoid_periods": ["需要避开的时间段1", "时间段2"],
    "recommended_windows": ["3月15-4月15日：春暖花开，淡季票价", "10月20-11月10日：秋色正浓"],
    "weather_note": "该季节天气特征及穿衣建议"
  },
  "overview": "行程总览，200字以内",
  "daily_plans": [
    {
      "day": 1,
      "title": "Day 1: 抵达+市区初探",
      "morning": {"activity": "抵达目的地，办理入住", "time": "上午", "duration": "2h", "tips": "建议选XX区域酒店"},
      "lunch": {"restaurant": "推荐餐厅名", "cuisine": "菜系", "price_per_person": "¥60", "tips": "招牌菜推荐"},
      "afternoon": {"activity": "景点名", "time": "14:00-17:00", "duration": "3h", "tips": "游览建议"},
      "dinner": {"restaurant": "推荐餐厅名", "cuisine": "菜系", "price_per_person": "¥80", "tips": "招牌菜推荐"},
      "evening": {"activity": "晚间活动", "time": "19:00-21:00", "duration": "2h", "tips": "注意事项"},
      "transportation": "全天交通方式及预估费用",
      "weather_plan_b": "如果下雨的替代方案"
    }
  ],
  "attraction_details": [
    {
      "name": "景点名",
      "open_time": "8:30-17:00",
      "ticket": "¥60（提前3天公众号预约）",
      "discount_info": "美团¥45 | 抖音团购¥39.9 | 淡季半价",
      "duration": "建议3-4小时",
      "indoor_outdoor": "室外",
      "photo_spot": "进门左手边走廊，日落前光线最佳",
      "avoid_trap": "门口拉客的不要理，正规入口在西门",
      "nearby_food": "出口步行5分钟有XX老字号",
      "sources": "小红书/携程/抖音"
    }
  ],
  "food_recommendations": {
    "must_eat": [{"name": "美食名", "description": "简介", "where": "推荐店铺", "price": "¥30", "source": "小红书/抖音/美团推荐"}],
    "night_market": [{"name": "夜市/美食街名", "location": "地址", "highlight": "特色", "source": "小红书/抖音"}],
    "food_tips": "饮食注意事项（口味、卫生等）"
  },
  "transportation": {
    "to_destination": {
      "options": [
        {"type": "飞机", "detail": "航班约2.5h", "reference_price": "¥800-1200", "best_book": "提前14-21天购票最便宜", "platform_compare": "携程vs飞猪vs航司官网"},
        {"type": "高铁", "detail": "约5h", "reference_price": "二等座¥450", "best_book": "提前15天12306开售", "platform_compare": ""}
      ],
      "recommendation": "综合考虑推荐高铁，性价比更高"
    },
    "city_transport": {
      "metro": "地铁日票¥20/天，推荐购买",
      "taxi": "起步价¥10，市内打车预估¥30-50/次",
      "tips": "建议办一张交通卡"
    }
  },
  "accommodation": {
    "recommended_area": "建议住XX区域，离主要景点近",
    "type_suggestions": [{"type": "经济型酒店", "price_range": "¥200-400/晚", "pros": "性价比高"}],
    "tips": "该城市订酒店注意事项"
  },
  "budget": {
    "items": [
      {"category": "往返交通", "amount": 1600, "per_person": true, "note": "高铁往返"},
      {"category": "住宿", "amount": 1200, "per_person": true, "note": "3晚×¥400"},
      {"category": "餐饮", "amount": 900, "per_person": true, "note": "3天×¥300"},
      {"category": "门票", "amount": 300, "per_person": true, "note": "各景点门票合计"},
      {"category": "市内交通", "amount": 150, "per_person": true, "note": "地铁+打车"},
      {"category": "其他", "amount": 350, "per_person": true, "note": "购物/保险/应急"}
    ],
    "total_per_person": 4500,
    "total_all": 9000,
    "save_tips": ["买三日联票省¥80", "周二部分景点半价", "学生证多数景点半价", "吃饭选巷子里的小店便宜一半"]
  },
  "tips_and_warnings": {
    "culture": ["当地风俗禁忌说明"],
    "safety": ["安全注意事项"],
    "health": ["健康提醒"],
    "scam": ["常见骗局预警"],
    "emergency": {"police": "110", "ambulance": "120", "consulate": "使领馆地址电话"}
  },
  "checklist": [
    {"category": "证件", "items": ["身份证", "驾驶证"]},
    {"category": "衣物", "items": ["根据天气推荐"]},
    {"category": "电子", "items": ["手机", "充电器", "充电宝"]},
    {"category": "药品", "items": ["晕车药", "肠胃药", "创可贴"]},
    {"category": "其他", "items": ["雨伞", "保温杯", "防晒霜"]}
  ]
}
```

## 注意事项
1. 严格输出JSON，不要有任何额外文字
2. 所有价格信息为参考价格，具体以实际为准
3. 根据出发地和目的地，提供真实的交通方式、景点、美食
4. 考虑实际情况：周一博物馆闭馆、体力合理分配、地理位置优化
5. 优惠信息基于各平台常见优惠模式（美团/抖音团购/携程等）
6. 日期推荐要结合天气、淡旺季、节假日
"""


async def _call_deepseek(api_key: str, messages: list, max_tokens: int = 8000) -> str:
    client = _get_client(api_key)
    response = await client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def _extract_json(text: str) -> dict:
    if not text or not text.strip():
        return {"error": "AI返回为空"}

    raw = text.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```\w*\s*\n?", "", raw)
        raw = re.sub(r"\n?\s*```\s*$", "", raw)

    # Try JSON array first
    arr_start = raw.find("[")
    arr_end = raw.rfind("]")
    obj_start = raw.find("{")
    obj_end = raw.rfind("}")

    if arr_start != -1 and arr_end != -1 and arr_start <= obj_start:
        start, end = arr_start, arr_end
    elif obj_start != -1 and obj_end != -1:
        start, end = obj_start, obj_end
    else:
        return {"error": "未找到JSON对象或数组", "raw": raw[:500]}

    json_str = raw[start:end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    fixed = re.sub(r",\s*([}\]])", r"\1", json_str)

    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    try:
        lines = json_str.split("\n")
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(",") and ":" not in stripped:
                stripped = stripped[:-1]
            clean_lines.append(stripped)
        return json.loads("\n".join(clean_lines))
    except json.JSONDecodeError:
        pass

    return {
        "error": "JSON解析失败，已尝试多种修复",
        "raw": json_str[:800],
        "tail": json_str[-200:] if len(json_str) > 800 else ""
    }


async def _generate_one_itinerary(
    api_key: str,
    departure: str,
    destination: str,
    days: int,
    adults: int,
    children: int,
    elders: int,
    budget: str,
    preferences: list,
    requirements: str,
    travel_date: str,
    theme: str,
    color: str,
) -> dict:
    people_desc = f"{adults}位成人"
    if children > 0:
        people_desc += f", {children}位儿童"
    if elders > 0:
        people_desc += f", {elders}位老人"

    pref_text = "、".join(preferences) if preferences else "无特别偏好"
    date_info = f"\n出行日期: {travel_date}" if travel_date else ""
    theme_hint = f"\n## 本次方案风格: {theme}" if theme else ""

    user_message = f"""请为以下旅行需求生成完整的行程规划。

## ⚠️ 首要约束 — 此行核心目的（行程必须围绕此目的展开）
{requirements if requirements else "无特殊要求"}{theme_hint}

## 基本信息
出发地: {departure}
目的地: {destination}
出行天数: {days}天
人数: {people_desc}
预算级别: {budget}
偏好: {pref_text}{date_info}

请严格按照JSON格式输出，包含overview、daily_plans、attraction_details、food_recommendations、transportation、accommodation、budget、tips_and_warnings、checklist。
方案标题请在overview中用「{color}」标记风格。
重要：每日行程必须紧扣上述核心目的，不要生成与该目的无关的通用行程。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    result_text = await _call_deepseek(api_key, messages, max_tokens=6000)
    result = _extract_json(result_text)

    if isinstance(result, dict) and "error" in result:
        retry_messages = [
            {"role": "system", "content": SYSTEM_PROMPT + "\n\n【重要】你上次的回复JSON格式不正确，无法被程序解析。请严格按照JSON规范输出。"},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "（上一次输出JSON格式有误，请重新生成严格合法的JSON）"},
        ]
        result_text = await _call_deepseek(api_key, retry_messages, max_tokens=6000)
        result = _extract_json(result_text)

    if not isinstance(result, dict) or "error" in result:
        return None

    result["_theme"] = theme
    result["_color"] = color
    return result


async def generate_itinerary(
    api_key: str,
    departure: str,
    destination: str,
    days: int,
    adults: int = 1,
    children: int = 0,
    elders: int = 0,
    budget: str = "舒适型",
    preferences: list = None,
    requirements: str = "",
    travel_date: str = ""
) -> dict:
    import asyncio

    themes = [
        ("经典全面", "🔵"),
        ("美食探店", "🟠"),
        ("小众深度", "🟢"),
    ]

    tasks = [
        _generate_one_itinerary(
            api_key, departure, destination, days, adults, children, elders,
            budget, preferences, requirements, travel_date, theme, color
        )
        for theme, color in themes
    ]

    results = await asyncio.gather(*tasks)

    plans = [r for r in results if r is not None]

    if not plans:
        plans = [{"error": "所有方案生成失败，请重试"}]

    return {"options": plans, "total": len(plans)}


async def generate_checklist(
    api_key: str,
    destination: str,
    days: int,
    travel_date: str,
    has_children: bool = False,
    has_elders: bool = False
) -> list:
    user_message = f"""请为以下旅行生成打包清单：
目的地: {destination}
天数: {days}天
出行日期: {travel_date}
有儿童: {'是' if has_children else '否'}
有老人: {'是' if has_elders else '否'}

请输出JSON数组，格式：
[{{"category": "分类名", "items": ["物品1", "物品2"]}}]"""

    messages = [
        {"role": "system", "content": "你是旅行打包专家。根据目的地、季节、天数、人员组成生成详细打包清单。只输出JSON数组。"},
        {"role": "user", "content": user_message},
    ]
    result_text = await _call_deepseek(api_key, messages, max_tokens=2000)
    result = _extract_json(result_text)
    if isinstance(result, list):
        return result
    if isinstance(result, dict) and "checklist" in result:
        return result["checklist"]
    return result


async def search_discounts(api_key: str, destination: str, keyword: str) -> dict:
    user_message = f"""在{destination}搜索「{keyword}」在各平台的最新优惠信息。

请综合以下平台进行搜索，并注明每条信息的来源平台：

1. **小红书** — 搜索最新的优惠笔记、团购链接、探店体验
2. **抖音** — 搜索团购套餐、直播间专属价、网红打卡套餐
3. **携程** — 搜索门票/酒店/一日游产品价格和优惠
4. **美团** — 搜索餐饮团购、景点门票折扣
5. **飞猪** — 搜索门票/接送机/境外WiFi优惠
6. **大众点评** — 搜索餐厅优惠券、必吃榜套餐

输出JSON格式：
{{
  "keyword": "搜索关键词",
  "results": [
    {{"platform": "平台名", "product": "产品名", "original_price": "原价", "discount_price": "优惠价", "discount_rate": "折扣力度", "how_to_get": "获取方式（如在平台搜索什么关键词）", "expiry": "有效期/时效", "source_detail": "信息来源说明（如：参考小红书2024年X月用户笔记）"}}
  ],
  "best_deal": "综合分析最推荐的购买方案及原因",
  "xiaohongshu_trends": "小红书上关于该关键词的最新热门讨论/趋势",
  "douyin_hot": "抖音上关于该关键词的热门视频/话题",
  "tips": "省钱注意事项"
}}"""

    messages = [
        {"role": "system", "content": "你是旅游优惠信息专家，深度使用小红书、抖音、携程、美团、飞猪、大众点评等平台。提供真实、可验证的优惠参考信息。每条优惠注明来源平台。只输出JSON。"},
        {"role": "user", "content": user_message},
    ]
    result_text = await _call_deepseek(api_key, messages, max_tokens=2000)
    return _extract_json(result_text)


async def recommend_dates(api_key: str, destination: str) -> dict:
    user_message = f"""请为目的地「{destination}」推荐最佳出行日期。

输出JSON格式：
{{
  "best_season": "最佳季节及原因",
  "monthly_guide": [
    {{"month": "1月", "weather": "天气特征", "pros": "优点", "cons": "缺点", "crowd_level": "拥挤程度", "avg_cost": "人均花费参考"}}
  ],
  "avoid_dates": ["需要避开的日期1", "日期2"],
  "best_windows": [
    {{"period": "时间段", "reason": "推荐原因", "weather": "天气"}}
  ],
  "booking_tips": "预订建议"
}}"""

    messages = [
        {"role": "system", "content": "你是旅行时间规划专家。根据目的地气候、淡旺季、节假日，推荐最佳出行时间。只输出JSON。"},
        {"role": "user", "content": user_message},
    ]
    result_text = await _call_deepseek(api_key, messages, max_tokens=2000)
    return _extract_json(result_text)


async def find_best_routes(
    api_key: str,
    destination: str,
    current_city: str = "",
    travel_date: str = "",
    travelers: int = 1,
    budget_level: str = "舒适型"
) -> dict:
    city_hint = f"\n当前所在城市: {current_city}" if current_city else "\n请根据目的地自动推荐国内最适合出发的枢纽城市（综合考虑地理位置和机票价格）"
    date_hint = f"\n计划出行时段: {travel_date}" if travel_date else ""

    user_message = f"""请为以下出行需求规划最具性价比的到达路线：

目的地: {destination}{city_hint}{date_hint}
出行人数: {travelers}人
预算偏好: {budget_level}

请综合考虑以下因素，列出多个方案并对比：

1. **出发城市选择**: 从{current_city if current_city else "目的地周边可达的国内主要枢纽城市"}出发，同时评估周边其他枢纽城市出发的可能性
   - 如果从周边其他城市出发总价更便宜，列出"先到X城市再飞"的方案
   - 例如：人在洛阳，去奥克兰 → 可对比 洛阳→郑州飞奥克兰 vs 洛阳高铁→北京飞奥克兰 vs 洛阳高铁→上海飞奥克兰
2. **交通方式组合**: 高铁/动车 + 飞机、全程飞机（中转/直飞）、火车+火车（国内就近目的地）
3. **价格对比**: 每个方案列出分段费用和总价
4. **时间对比**: 每个方案列出总耗时（含中转等待）
5. **购票策略**: 什么时候买最便宜、哪个平台买最划算

输出JSON格式：
{{
  "destination": "目的地",
  "current_city": "{current_city or '自动推荐'}",
  "route_options": [
    {{
      "rank": 1,
      "label": "方案简称（如：郑州直飞奥克兰）",
      "segments": [
        {{"from": "出发地", "to": "到达地", "type": "高铁/飞机/自驾", "detail": "G1234次 3h", "cost_per_person": 450, "booking_tips": "购票建议"}}
      ],
      "total_cost_per_person": 3500,
      "total_cost_all": 7000,
      "total_time": "约15小时（含中转3小时）",
      "pros": ["优点1", "优点2"],
      "cons": ["缺点1", "缺点2"],
      "best_book_time": "建议提前XX天购票",
      "platform_compare": "携程vs飞猪vs航司官网对比",
      "recommendation_score": 9.5
    }}
  ],
  "best_option": "综合分析推荐方案X及原因",
  "price_analysis": "当前价格水平分析及走势预测",
  "general_tips": ["跨城接驳注意事项", "行李转运建议", "中转住宿建议"],
  "budget_saving_ideas": ["省钱技巧1", "省钱技巧2"],
  "sources_note": "价格信息来源说明（基于各平台2025-2026年常规价格模式，实际请以购票时为准）"
}}"""

    messages = [
        {"role": "system", "content": """你是交通路线规划专家，精通国内高铁网络和全球航班航线。你的任务是为用户找到从国内出发到达目的地的最具性价比路线。

## 核心能力
- 深度了解国内高铁网：知道哪些城市是区域枢纽（如郑州是中原枢纽、西安是西北枢纽）
- 了解国际航班分布：知道哪些城市有直飞某目的地的航班、哪些航线便宜
- 跨平台比价意识：携程/飞猪/去哪儿/航司官网的优劣势
- 关注中转便利性：高铁站与机场之间的接驳时间、是否需要过夜

## 输出要求
- 至少列出3-5个对比方案
- 每个方案注明分段费用、总费用、总耗时
- 突出推荐最优方案并说明原因
- 价格信息为AI基于航线规律估算，注明仅供参考
- 只输出JSON，不要任何额外文字"""},
        {"role": "user", "content": user_message},
    ]
    result_text = await _call_deepseek(api_key, messages, max_tokens=4000)
    return _extract_json(result_text)


async def suggest_trips(api_key: str, query: str, current_city: str = "") -> dict:
    city_hint = f"\n用户所在城市: {current_city}" if current_city else ""
    now_hint = "\n当前时间为2026年5月，请基于此给出季节性的建议。"

    user_message = f"""用户输入了模糊的旅行需求：「{query}」{city_hint}{now_hint}

请根据这个模糊需求，给用户推荐 4-6 个具体的旅行方案。要求：

1. **理解意图**: 从模糊描述中提取关键信息（季节、人群类型、预算暗示、兴趣方向、时间长度暗示等）
2. **覆盖距离层次（重要）**:
   - 至少包含 1 个「本市/同城」方案（如博物馆、新开商场、公园一日游等），适合说走就走
   - 至少包含 1 个「周边短途」方案（驾车/高铁2小时内可达），适合周末
   - 其余方案覆盖国内/出境不同距离
3. **室内备选（重要）**: 每个方案都要列出该目的地的室内/雨天替代玩法，应对天气变化
4. **多样性**: 推荐的目的地要有一定差异性（不同方向、不同风格、不同预算级别）
5. **具体化**: 每个推荐都要给出具体的目的地、建议天数、预估预算范围、适合季节/时段
6. **接地气**: 结合真实旅行经验，给出具体的亮点和实用提醒
7. **偏好回推**: 如"亲子游"推荐有乐园/动物园/海滩的城市，"周边游"以用户所在城市为中心推荐

输出JSON格式：
{{
  "query_understanding": "你对该需求的理解（1-2句话）",
  "extracted_info": {{
    "traveler_type": "情侣/亲子/独自/朋友/家庭/不限",
    "budget_hint": "经济/舒适/豪华/不限",
    "duration_hint": "短期1-3天/中期4-7天/长期7天+/不限",
    "season_hint": "春季/夏季/秋季/冬季/寒假/暑假/不限",
    "style_hint": "自然风光/城市人文/美食/购物/探险/休闲度假/不限",
    "distance_hint": "本市/周边/国内/出境/不限"
  }},
  "suggestions": [
    {{
      "id": 1,
      "title": "方案标题（如：市郊森林温泉周末游）",
      "destination": "主要目的地城市/景点",
      "distance_category": "本市/周边/国内/出境",
      "route_hint": "行程路线概述",
      "days": 5,
      "best_time": "最佳出行时段",
      "current_weather_note": "当前季节该目的地天气特征",
      "budget_level": "经济型/舒适型/豪华型",
      "budget_estimate_per_person": 3000,
      "highlights": ["亮点1", "亮点2", "亮点3"],
      "indoor_backups": [
        {{"name": "室内备选景点/活动", "type": "博物馆/商场/美食街/演出/手工体验/温泉/其他", "description": "简短描述", "suitable_weather": "雨天/暴晒/寒冷/通用"}}
      ],
      "why_recommend": "为什么推荐这个方案（1-2句话）",
      "cautions": ["注意事项1", "注意事项2"],
      "tags": ["标签1", "标签2"],
      "departure_hint": "建议出发城市"
    }}
  ],
  "query_tips": "如果用户想进一步细化需求，可以补充哪些信息（1-2句话）"
}}"""

    messages = [
        {"role": "system", "content": """你是资深旅行灵感顾问，擅长从用户模糊的需求中发现他们的旅行偏好，并给出具体、有吸引力、多样化的旅行建议。

## 你的能力
- 从只言片语中读懂用户真正的旅行意图
- 熟悉国内热门/小众旅游目的地及其最佳旅行季节
- 了解不同人群（亲子/情侣/老人/独自）的旅行需求差异
- 关注当季热门趋势：小红书爆款、抖音网红目的地、新晋打卡地
- 给出接地气的真实建议，包含亮点和避坑提醒

## 重要规则
### 距离层次覆盖
你推荐的方案必须覆盖不同的出行距离，确保用户无论时间多少都有得选：
- **本市/同城**: 1-2天，本地博物馆/展览/新开商场/公园/骑行路线/CityWalk主题路线等，说走就走
- **周边短途**: 2-3天，自驾或高铁2小时内可达的周边城市/景区，适合周末
- **国内远途**: 4-7天，跨省旅行，需要飞机或长途高铁
- **出境**: 7天+，国际旅行（仅当用户明确想出国或模糊需求可能暗示出境时才推荐）

每个方案必须标注 `distance_category`，且4-6个方案中至少各有1个本市和周边方案。

### 室内备选（必须）
旅行最大的不确定性是天气。每个方案必须提供 `indoor_backups`：
- 列出该目的地 2-3 个室内/半室内替代玩法
- 标注适合什么天气（雨天/暴晒/寒冷/通用）
- 包括室内景点（博物馆、海洋馆）、商场/美食街、手作工坊、演出/剧场、温泉/SPA等
- 确保即使全程下雨，这趟旅行依然充实有趣

## 输出要求
- 推荐4-6个方案，必须覆盖本市→周边→国内的不同距离
- 每个方案要具体到城市/景点名，不要泛泛而谈
- 每个方案必须有 indoor_backups
- 预算要靠谱，参考真实旅行花费
- 只输出JSON，不要任何额外文字"""},
        {"role": "user", "content": user_message},
    ]
    result_text = await _call_deepseek(api_key, messages, max_tokens=6000)
    return _extract_json(result_text)
