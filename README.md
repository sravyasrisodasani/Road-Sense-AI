# 🚨 RoadSoS — Emergency Assistant

> **National Road Safety Hackathon 2026 | IIT Madras (CoERS, RBG Labs)**
> Topic: RoadSoS | Theme: AI in Road Safety

---

## 📌 What is RoadSoS?

RoadSoS is an AI-powered emergency assistant for road accident victims and bystanders. It provides **instant, location-based access** to nearby trauma centres, ambulance services, vehicle rescue services, police stations, and emergency contacts — all in one place, with offline support.

Built with Python + Streamlit. Works on any device — PC, mobile, tablet.

---

## 🎯 Problem It Solves

When a road accident happens:
- Victims and bystanders **don't know who to call**
- Finding the **nearest hospital or ambulance** takes precious minutes
- The **"golden hour"** — the critical 60 minutes after an accident — is often wasted
- Emergency contacts **don't know where the victim is**
- Bystanders **don't know what first aid to give**

RoadSoS solves all of this in one tap.

---

## ✨ Features

### 🆘 Emergency Response
| Feature | Description |
|---------|-------------|
| **ONE-TAP EMERGENCY** | Single button that auto-dials ambulance, sends SOS to all contacts, shares live location |
| **Golden Hour Timer** | 60-minute countdown showing the critical intervention window |
| **Crash Detection** | Accelerometer-based auto-detection on mobile — triggers emergency automatically |
| **Emergency Checklist** | Interactive step-by-step checklist for accident, bleeding, unconscious, fire scenarios |
| **Severity Classifier** | AI classifies emergency as CRITICAL / SERIOUS / MODERATE / MINOR |

### 🗺️ Location-Based Services
| Feature | Description |
|---------|-------------|
| **Trauma Centres** | Nearest hospitals with emergency/trauma departments |
| **Ambulance Services** | Nearest ambulance stations |
| **Police Stations** | Nearest police stations |
| **Vehicle Rescue** | Towing and vehicle recovery services |
| **Puncture/Repair** | Nearest tyre shops and garages |
| **Showrooms** | Nearest vehicle showrooms |
| **Combined Map** | All services on one color-coded interactive map |
| **Up to 15 results** | Per category, sorted by distance |

### 🤖 AI Features
| Feature | Description |
|---------|-------------|
| **Gemini AI Chatbot** | Natural language emergency guidance powered by Google Gemini |
| **Voice Input** | Speak your emergency — auto-transcribed and processed |
| **Text-to-Speech** | App reads first aid instructions aloud (like Siri) |
| **Offline Fallback** | Keyword-based AI works without internet |

### 📞 SOS & Communication
| Feature | Description |
|---------|-------------|
| **Twilio SMS** | Automatic SMS to all saved contacts with location + medical info |
| **Live Location Link** | Google Maps link in SOS message |
| **WhatsApp SOS** | Pre-filled WhatsApp message to contacts |
| **Medical Info in SOS** | Blood group, allergies, conditions sent to contacts |

### 📋 Documentation
| Feature | Description |
|---------|-------------|
| **Accident Report PDF** | Professional PDF report for insurance/police |
| **Auto-filled Details** | Name, phone, location pre-filled from profile |

### 🌍 Global & Accessibility
| Feature | Description |
|---------|-------------|
| **60+ Countries** | Correct emergency numbers auto-detected from location |
| **4 Languages** | English, Hindi, Telugu, Tamil |
| **Offline Mode** | First aid, emergency numbers, report generator work without internet |
| **PWA** | Installable on phone home screen like a native app |

---

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/roadsos.git
cd roadsos

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file with:
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1xxxxxxxxxx
GEMINI_API_KEY=your_gemini_key

# 5. Run the app
streamlit run app.py
```

### API Keys (Optional)
| Key | Purpose | Get it free at |
|-----|---------|----------------|
| `GEMINI_API_KEY` | AI chatbot responses | [aistudio.google.com](https://aistudio.google.com) |
| `TWILIO_*` | SMS SOS alerts | [twilio.com](https://twilio.com) |

> **Note:** The app works without API keys. Gemini falls back to keyword AI, Twilio SMS falls back to manual SMS links.

---

## 📦 Packages Used

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | latest | Web framework |
| `twilio` | latest | SMS sending |
| `python-dotenv` | latest | Environment variables |
| `requests` | latest | API calls (Gemini, OpenStreetMap) |
| `reportlab` | latest | PDF generation |
| `SpeechRecognition` | latest | Voice input transcription |

### External APIs (Free)
| API | Purpose |
|-----|---------|
| OpenStreetMap / Overpass API | Nearby services lookup |
| Nominatim | Location geocoding |
| Google Gemini API | AI chatbot |
| ipapi.co | IP-based location detection |
| Google Maps | Navigation links |

---

## 📁 Project Structure

```
roadsos/
├── app.py                 # Main Streamlit application
├── chatbot.py             # AI chatbot (Gemini + keyword fallback)
├── services.py            # Nearby services fetcher (OpenStreetMap)
├── sos.py                 # SOS SMS sender (Twilio)
├── storage.py             # User data persistence
├── global_emergency.py    # Emergency numbers for 60+ countries
├── location_detect.py     # GPS + IP location detection
├── map_view.py            # Interactive maps (Leaflet.js)
├── network_check.py       # Internet connectivity check
├── pwa.py                 # PWA manifest + service worker
├── translations.py        # Multilingual support (EN/HI/TE/TA)
├── crash_detect.py        # Accelerometer crash detection
├── golden_hour.py         # Golden hour countdown timer
├── severity.py            # Accident severity classifier
├── checklist.py           # Emergency action checklists
├── report_generator.py    # PDF accident report generator
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed)
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

---

## 👤 User Guide

### First Time Setup (2 minutes)
1. Open the app
2. In the **left sidebar**, fill in:
   - Your Name
   - Your Phone Number
   - Blood Group (important for paramedics)
   - Allergies (e.g. Penicillin)
   - Medical Conditions (e.g. Diabetic)
   - Emergency Contact 1, 2, 3 (family/friends)
3. Click **💾 Save Details**
4. Your location is auto-detected — verify it's correct

### When You Witness an Accident

**Option 1 — Quick Response:**
1. Press **🚨 Accident** button
2. Golden Hour Timer starts automatically
3. Follow the Emergency Checklist step by step
4. Nearby trauma centres and ambulances appear on map
5. Tap any service to call or get directions

**Option 2 — Describe the Situation:**
1. Tap 🎤 or type what you see (e.g. "person unconscious, heavy bleeding")
2. App classifies severity (CRITICAL/SERIOUS/MODERATE/MINOR)
3. AI gives step-by-step first aid instructions
4. App reads instructions aloud
5. Relevant checklist appears automatically

**Option 3 — ONE-TAP EMERGENCY:**
1. Press **🆘 ONE-TAP EMERGENCY**
2. App auto-dials ambulance
3. Shows call buttons for all emergency services
4. Sends SMS + WhatsApp to all saved contacts with:
   - Your live location (Google Maps link)
   - Blood group and medical info
   - Emergency message

### Finding Nearby Services
1. Press **🗺️ Find Nearby Services**
2. Choose tab: Trauma Centres / Ambulance / Police / Vehicle Rescue / Puncture / Showrooms
3. See up to 15 results sorted by distance
4. Tap **📞 Call** to dial directly
5. Tap **🗺 Go** to open Google Maps navigation

### After the Accident — Filing a Report
1. Scroll to **Accident Report Generator**
2. Your name, phone, location are pre-filled
3. Fill in: accident type, vehicles, injuries, description
4. Click **📄 Generate Report**
5. Download PDF → submit to insurance or police

### Crash Detection (Mobile Only)
- Runs automatically in the background on mobile
- If sudden impact detected → 5-second countdown appears
- Tap **Cancel** if it's a false alarm
- Otherwise → ONE-TAP EMERGENCY fires automatically

### Language
- Change language from sidebar: English / हिंदी / తెలుగు / தமிழ்
- All buttons, labels, and messages change instantly

### Offline Mode
These features work **without internet**:
- First aid chatbot (keyword-based)
- Emergency numbers for your country
- Accident report PDF generation
- Emergency checklists
- Golden hour timer

---

## 🌍 Supported Countries (Emergency Numbers)

60+ countries including India, USA, UK, UAE, Australia, Germany, France, Japan, China, Brazil, South Africa, and more.

Auto-detected from your location. Falls back to **112** (works in most countries).

---

## 🔒 Assumptions

1. User has a smartphone with a browser (Chrome recommended)
2. Location permission granted for GPS accuracy
3. Internet connection for live services map (offline fallback available)
4. Twilio account for SMS (optional — manual SMS fallback provided)
5. Gemini API key for AI responses (optional — keyword AI fallback provided)
6. App is pre-configured before emergency (details saved in advance)

---

## 🏆 Hackathon Compliance

| Requirement | Status |
|-------------|--------|
| Nearest Police Station, hospitals, ambulance | ✅ |
| Towing services, puncture shops, showrooms | ✅ |
| Global applicability across countries | ✅ 60+ countries |
| Offline functionality | ✅ |
| Reliability and data accuracy | ✅ OpenStreetMap + dual mirror |
| Number of contacts fetched | ✅ Up to 15 per category |
| Innovation & additional features | ✅ AI, voice, TTS, crash detection, golden hour |
| Information integration across countries | ✅ |

---

## 📧 Contact

Built for **National Road Safety Hackathon 2026**
Organised by CoERS, RBG Labs, IIT Madras
Topic: RoadSoS

---

*Your safety, our priority. RoadSoS is here to help in critical moments.*
