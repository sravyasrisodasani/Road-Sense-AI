# 🚨 RoadSoS Emergency Assistant

AI-powered road accident emergency assistant — First Aid · Nearby Services · SOS Alerts

## Setup

```bash
pip install streamlit twilio python-dotenv requests
```

Add your Twilio credentials to `.env`:
```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1XXXXXXXXXX
```

## Run

```bash
streamlit run app.py
```

## Features
- 🧠 AI chatbot — 8 emergency types with severity detection
- 🗺️ Find nearby hospitals, ambulance, police, towing, repair, showrooms
- 📞 SOS SMS to 3 contacts via Twilio
- 📴 Offline-first — first aid works without internet
- 🎤 Voice input
- 🆘 One-tap emergency mode
- 🔗 Auto-connect: injury → hospital, accident → all services

## Emergency Numbers (always work offline)
- 🆘 112 — Universal Emergency
- 🚑 108 — Ambulance
- 🚔 100 — Police
- 🚒 101 — Fire
- 🛣️ 1033 — Highway Help
