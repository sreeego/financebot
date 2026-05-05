# 💰 FinanceBot

A **privacy-first Telegram bot** for personal finance management. Log transactions using natural messages, analyze spending with AI, and export detailed reports — all inside Telegram.

---

## 🚀 Overview

FinanceBot is built for simplicity, control, and privacy. Each user operates on an **isolated local database**, ensuring zero data overlap. It combines structured finance tracking with **AI-powered insights** to turn raw transactions into meaningful understanding.

---

## ✨ Features

### 🧾 Smart Transaction Logging

- Log income/expenses using natural inputs  
  `-300 tea` · `+40000 salary`

### 🔐 Privacy-First Architecture

- Per-user isolated SQLite databases
- No shared data across users
- Full control over export and deletion

### 🤖 AI-Powered Insights

- `/ask` queries using natural language
- Understand spending patterns instantly

### 📊 Visual Analytics

- Monthly spending breakdown (pie chart)
- Category-based expense distribution

### 📁 Reports & Export

- Export reports as:
  - PDF (via ReportLab)
  - Excel (via openpyxl)

### 💸 Budget Tracking

- Set limits per category
- Monitor usage and overspending

---

## ⚙️ Commands

| Command | Description |
|--------|-------------|
| `-300 tea` / `+40000 salary` | Log a transaction |
| `/summary` | Monthly income, expense, balance |
| `/history` | Last 10 transactions |
| `/budget food 3000` | Set category budget |
| `/budget` | View all budgets |
| `/graph` | Spending pie chart |
| `/report` | Export PDF report |
| `/report excel` | Export Excel report |
| `/ask <question>` | AI-based financial query |
| `/undo` | Remove last transaction |
| `/deletedata` | Delete all user data |

---

## 🏗️ Tech Stack

- **Language:** Python
- **Bot Framework:** python-telegram-bot
- **Database:** SQLAlchemy + SQLite
- **AI Engine:** Groq API (LLaMA 3.3)
- **Visualization:** Matplotlib
- **Reporting:** ReportLab, openpyxl

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/sreeego/financebot.git
cd financebot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Bot

```bash
python main.py
```

---

## 📂 Project Structure

```
financebot/
├── main.py
├── bot/
│   ├── handlers.py
│   └── commands.py
├── core/
│   ├── parser.py
│   └── database.py
├── ai/
│   └── ask.py
├── reports/
│   ├── graph.py
│   └── export.py
├── data/
├── requirements.txt
└── .env
```

---

## 🔐 Privacy Model

- Each user gets a **dedicated SQLite database**
- No centralized storage or shared user tables
- Data remains fully under user control
- `/deletedata` ensures complete removal

---

## 🛣️ Roadmap

- [x] Transaction logging
- [x] Per-user isolated databases
- [x] AI-powered `/ask`
- [x] Charts and reporting
- [x] Budget tracking
- [ ] End-to-End encryption (SQLCipher)
- [ ] Recurring transactions
- [ ] Multi-currency support

---

## 📜 License

MIT License © 2026 SREE GOVIND S A

---

## 👤 Author

- GitHub: https://github.com/sreeego

---

## 🧠 Design Philosophy

- Minimal friction input
- Maximum user control
- Strong privacy guarantees
- AI as an assistant, not a dependency

---

