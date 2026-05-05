from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_context(transactions):
    lines = []
    for t in transactions:
        sign = "+" if t.type == "income" else "-"
        lines.append(f"{t.date} {sign}{t.amount} {t.note} [{t.category}]")
    return "\n".join(lines)


def ask_ai(question, transactions):
    context = build_context(transactions)
    prompt = f"""You are a personal finance assistant. You only answer questions related to the user's finances and transactions. If the question is not related to finance or the user's data, politely refuse to answer.

Here are the user's transactions:
{context}

Question: {question}

Answer based only on the transaction data above. If there is no relevant data, say so."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content