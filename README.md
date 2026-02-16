# 🏊 Swim Booker – Automated Swim Session Scheduler

A simple desktop app that books swim sessions for you.  
You choose the times. The app handles the rest.

---

## ✨ Features

- **Clear GUI**  
  Browse sessions, filter by location or time, and select bookings quickly.

- **Automatic booking**  
  The scheduler reserves sessions exactly when registration opens.

- **Telegram bot integration**  
  Set reminders & receive booking alerts.

- **One-click register**  
  Click any available session to open or complete registration instantly.

---

## 📸 Screenshot

<img width="1020" height="897" alt="app screenshot" src="https://github.com/user-attachments/assets/27f7acf5-0703-42be-8a3b-4304a25c2410" />

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/swimtime-booker.git
cd swimtime-booker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create environment variables

Create a `.env` file in the project root:
```ini
LOGIN_USERNAME=your_username
LOGIN_PASSWORD=your_password
TELEGRAM_TOKEN=your_telegram_bot_token
```

### 4. Run the app

```bash
python main.py
```


## 📌 Notes

- The app must stay running for the automatic booking/telegram bot to work
- Don't be dumb and commit .env (as if anyone would ever commit)
