import matplotlib.pyplot as plt
import io
from datetime import date


def generate_graph(transactions):
    now = date.today()
    monthly = [t for t in transactions if t.date.month == now.month and t.date.year == now.year and t.type == "expense"]

    if not monthly:
        return None

    categories = {}
    for t in monthly:
        categories[t.category] = categories.get(t.category, 0) + t.amount

    labels = list(categories.keys())
    values = list(categories.values())

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title(f"Spending Breakdown — {now.strftime('%B %Y')}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return buf