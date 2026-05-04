import re
from datetime import date, timedelta

CATEGORIES = {
    "food": ["food", "tea", "coffee", "lunch", "dinner", "breakfast", "restaurant", "swiggy", "zomato", "snack"],
    "transport": ["uber", "ola", "bus", "train", "fuel", "petrol", "auto", "cab", "metro"],
    "health": ["medicine", "doctor", "hospital", "pharmacy", "medic"],
    "shopping": ["shopping", "amazon", "flipkart", "clothes", "dress"],
    "bills": ["rent", "electricity", "wifi", "internet", "bill", "recharge"],
    "income": ["salary", "freelance", "bonus", "income", "payment", "stipend"],
}

def detect_category(note):
    note_lower = note.lower()
    for category, keywords in CATEGORIES.items():
        if any(k in note_lower for k in keywords):
            return category
    return "general"

def detect_date(note):
    if "yesterday" in note:
        return date.today() - timedelta(days=1)
    return date.today()

def parse_message(text):
    pattern = r'^([+-])(\d+\.?\d*k?)\s+(.+)$'
    match = re.match(pattern, text.strip().lower())
    if not match:
        return None

    sign, amount_str, note = match.groups()

    amount = float(amount_str.replace('k', ''))
    if 'k' in amount_str:
        amount *= 1000

    type_ = "income" if sign == "+" else "expense"
    date_ = detect_date(note)
    note = re.sub(r'\b(yesterday|today)\b', '', note).strip()
    category = detect_category(note)

    return {
        "amount": amount,
        "type": type_,
        "category": category,
        "note": note,
        "date": date_
    }