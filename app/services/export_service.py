"""行程导出为 Markdown"""
import json


def safe_json_loads(text: str, default=None):
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def itinerary_to_markdown(trip: dict) -> str:
    itinerary = safe_json_loads(trip.get("itinerary_json"), {})
    budget = safe_json_loads(trip.get("budget_json"), {})
    checklist = safe_json_loads(trip.get("checklist_json"), [])

    lines = []
    lines.append(f"# 🗺️ {trip['destination']}旅行计划")
    lines.append("")
    lines.append(f"- **出发地**: {trip['departure']}")
    lines.append(f"- **目的地**: {trip['destination']}")
    lines.append(f"- **出行日期**: {trip['travel_date']}")
    lines.append(f"- **天数**: {trip['days']}天")
    people = f"- **人数**: 成人{trip['adults']}人"
    if trip.get('children'):
        people += f" 儿童{trip['children']}人"
    if trip.get('elders'):
        people += f" 老人{trip['elders']}人"
    lines.append(people)
    lines.append(f"- **预算级别**: {trip['budget']}")
    if trip.get("requirements"):
        lines.append(f"- **特别需求**: {trip['requirements']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    if itinerary.get("date_advice"):
        da = itinerary["date_advice"]
        lines.append("## 📅 出行日期建议")
        lines.append(f"- **最佳季节**: {da.get('best_season', '')}")
        if da.get("recommended_windows"):
            lines.append("- **推荐时间段**:")
            for w in da["recommended_windows"]:
                lines.append(f"  - {w}")
        if da.get("avoid_periods"):
            lines.append("- **建议避开**:")
            for a in da["avoid_periods"]:
                lines.append(f"  - {a}")
        lines.append("")

    if itinerary.get("overview"):
        lines.append("## 📖 行程概览")
        lines.append(itinerary["overview"])
        lines.append("")

    daily = itinerary.get("daily_plans", [])
    if daily:
        for day in daily:
            lines.append(f"## Day {day.get('day', '?')}: {day.get('title', '')}")
            lines.append("")
            for slot in ["morning", "lunch", "afternoon", "dinner", "evening"]:
                d = day.get(slot)
                if not d:
                    continue
                labels = {
                    "morning": "🌅 上午", "lunch": "🍜 午餐",
                    "afternoon": "☀️ 下午", "dinner": "🍽️ 晚餐", "evening": "🌙 晚上"
                }
                lines.append(f"**{labels.get(slot, slot)}** {d.get('activity', d.get('restaurant', ''))}")
                if d.get("time"):
                    lines.append(f"  ⏰ {d['time']} | 时长: {d.get('duration', '')}")
                if d.get("price_per_person"):
                    lines.append(f"  💰 人均: {d['price_per_person']}")
                if d.get("tips"):
                    lines.append(f"  💡 {d['tips']}")
                lines.append("")
            lines.append(f"🚗 **交通**: {day.get('transportation', '')}")
            if day.get("weather_plan_b"):
                lines.append(f"🌧️ **雨天备选**: {day['weather_plan_b']}")
            lines.append("")

    attractions = itinerary.get("attraction_details", [])
    if attractions:
        lines.append("---")
        lines.append("## 🏛️ 景点详情")
        lines.append("")
        for attr in attractions:
            lines.append(f"### {attr.get('name', '')}")
            for key, label in [("open_time", "开放时间"), ("ticket", "门票"), ("discount_info", "优惠"),
                               ("duration", "建议时长"), ("indoor_outdoor", "类型"), ("photo_spot", "拍照点"),
                               ("avoid_trap", "⚠️ 避坑"), ("nearby_food", "周边美食")]:
                if attr.get(key):
                    lines.append(f"- **{label}**: {attr[key]}")
            lines.append("")

    food = itinerary.get("food_recommendations", {})
    if food:
        lines.append("---")
        lines.append("## 🍜 美食推荐")
        lines.append("")
        if food.get("must_eat"):
            lines.append("### 必吃美食")
            for item in food["must_eat"]:
                lines.append(f"- **{item.get('name', '')}**: {item.get('description', '')} | 📍{item.get('where', '')} | 💰{item.get('price', '')}")
            lines.append("")
        if food.get("night_market"):
            lines.append("### 夜市/美食街")
            for nm in food["night_market"]:
                lines.append(f"- **{nm.get('name', '')}**: {nm.get('location', '')} - {nm.get('highlight', '')}")
            lines.append("")
        if food.get("food_tips"):
            lines.append(f"💡 {food['food_tips']}")
            lines.append("")

    if budget:
        lines.append("---")
        lines.append("## 💰 预算明细")
        lines.append("")
        for item in budget.get("items", []):
            per = "人均" if item.get("per_person") else "总计"
            lines.append(f"- **{item.get('category', '')}**: ¥{item.get('amount', 0):,.0f} ({per}) {item.get('note', '')}")
        lines.append(f"- **人均总计**: ¥{budget.get('total_per_person', 0):,.0f}")
        lines.append(f"- **全员总计**: ¥{budget.get('total_all', 0):,.0f}")
        if budget.get("save_tips"):
            lines.append("")
            lines.append("### 💡 省钱建议")
            for tip in budget["save_tips"]:
                lines.append(f"- {tip}")
        lines.append("")

    tips = itinerary.get("tips_and_warnings", {})
    if tips:
        lines.append("---")
        lines.append("## ⚠️ 旅行须知")
        lines.append("")
        for section, key in [("风俗禁忌", "culture"), ("安全提示", "safety"), ("健康提醒", "health"), ("常见骗局", "scam")]:
            content = tips.get(key, [])
            if content:
                lines.append(f"### {section}")
                for c in content:
                    lines.append(f"- {c}")
                lines.append("")
        emergency = tips.get("emergency", {})
        if emergency:
            lines.append("### 紧急联系")
            for k, v in emergency.items():
                lines.append(f"- {k}: {v}")
            lines.append("")

    if checklist:
        lines.append("---")
        lines.append("## 🎒 打包清单")
        lines.append("")
        if isinstance(checklist, list):
            for cat in checklist:
                if isinstance(cat, dict):
                    lines.append(f"**{cat.get('category', '')}**: {'、'.join(cat.get('items', []))}")
                else:
                    lines.append(f"- {cat}")

    lines.append("")
    lines.append("---")
    lines.append("*由 AI 旅游规划助手生成*")

    return "\n".join(lines)
