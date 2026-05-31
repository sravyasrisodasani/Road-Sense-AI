import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime
from chatbot import get_response, is_gemini_configured
from sos import send_sos, format_number
from services import fetch_services, SERVICE_CONFIG
from location_detect import render_auto_location, get_coords_from_url, get_location_from_ip
from map_view import render_map, render_combined_map
from network_check import is_online
from storage import load_user_data, save_user_data
from global_emergency import get_emergency_numbers
from pwa import inject_pwa
from translations import t, LANGUAGES
from crash_detect import render_crash_detector, render_crash_settings
from golden_hour import render_golden_hour_timer
from severity import classify_severity, render_severity_badge
from checklist import render_checklist
from browser_storage import inject_storage_loader, save_to_browser, load_from_url_params
from guide import render_guide
from ux_effects import inject_ux_effects

st.set_page_config(page_title="RoadSoS Emergency Assistant", page_icon="🚨", layout="wide")

# Inject PWA support (manifest + service worker + install banner)
inject_pwa()

# Inject crash detection (accelerometer-based, mobile only)
render_crash_detector(
    enabled=st.session_state.get("auto_crash_enabled", False),
    crash_threshold=st.session_state.get("crash_threshold", 25.0),
    countdown_seconds=600,
    alarm_interval_seconds=30,
)

# Inject browser storage loader (reads localStorage → URL params)
inject_storage_loader()

# Inject UX effects (cursor glow, 3D cards, button ripple, input glow, shimmer)
inject_ux_effects()

st.markdown("""
<style>
/* ══════════════════════════════════════════
   ROADSOS DESIGN SYSTEM
   Base:      #070B1A  (deep navy)
   Cards:     #11182B  (dark navy)
   Border:    #1E2A47
   Red:       #FF3B3B  (emergency/danger)
   Cyan:      #00C2FF  (services/info)
   Purple:    #8B5CF6  (guidance/AI)
   Green:     #22C55E  (success/active)
   Orange:    #F97316  (one-tap emergency)
   Text:      #E2E8F0
   Muted:     #64748B
══════════════════════════════════════════ */

/* ── Base ── */
.stApp { background: #070B1A !important; color: #E2E8F0; }
section[data-testid="stSidebar"] {
    background: #080D1C !important;
    border-right: 1px solid #1E2A47;
}
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* ── Section Headers — bigger, more visible ── */
.section-header {
    font-size: 0.72rem; font-weight: 800; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 3px;
    margin: 24px 0 12px 0;
    display: flex; align-items: center; gap: 8px;
}

/* ── Hero — richer with glow ── */
.hero-box {
    background: linear-gradient(135deg, #0D1B2E 0%, #0F1929 50%, #111827 100%);
    border: 1px solid #1E2A47; border-radius: 20px;
    padding: 28px 32px; margin-bottom: 20px;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 60px rgba(255,59,59,0.05);
}
.hero-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #FF3B3B 0%, #F97316 25%, #00C2FF 60%, #22C55E 100%);
    background-size: 200% 100%;
    animation: gradientShift 4s ease infinite;
}
.hero-box::after {
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,59,59,0.06) 0%, transparent 70%);
    pointer-events: none;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-title { color: #fff; font-size: 1.8rem; font-weight: 900; margin: 0; letter-spacing: -0.5px; }
.hero-sub { color: #64748B; font-size: 0.88rem; margin: 6px 0 0 0; }
.status-dot {
    display: inline-block; width: 9px; height: 9px;
    background: #22C55E; border-radius: 50%; margin-right: 6px;
    box-shadow: 0 0 10px rgba(34,197,94,0.8);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 6px rgba(34,197,94,0.6); }
    50% { box-shadow: 0 0 16px rgba(34,197,94,1); }
}

/* ── Section card tints — more visible ── */
.section-emergency-input {
    background: linear-gradient(135deg, rgba(0,194,255,0.06), rgba(0,153,255,0.03));
    border: 1px solid rgba(0,194,255,0.18);
    border-left: 3px solid #00C2FF;
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,194,255,0.05);
}
.section-response {
    background: linear-gradient(135deg, rgba(139,92,246,0.07), rgba(109,40,217,0.03));
    border: 1px solid rgba(139,92,246,0.2);
    border-left: 3px solid #8B5CF6;
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(139,92,246,0.06);
}
.section-quick-actions {
    background: linear-gradient(135deg, rgba(255,59,59,0.05), rgba(249,115,22,0.02));
    border: 1px solid rgba(255,59,59,0.15);
    border-left: 3px solid #FF3B3B;
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(255,59,59,0.04);
}
.section-report {
    background: linear-gradient(135deg, rgba(30,42,71,0.8), rgba(15,25,41,0.6));
    border: 1px solid #1E2A47;
    border-left: 3px solid #64748B;
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
}

/* ── All Buttons base ── */
.stButton button {
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 0.85rem !important; padding: 12px 10px !important;
    transition: all 0.2s ease !important;
    border: 1px solid #1E2A47 !important;
    background: #11182B !important; color: #E2E8F0 !important;
    width: 100% !important; height: 72px !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
}

/* ── Col 1: Accident → Red ── */
div[data-testid="column"]:nth-child(1) .stButton button {
    background: linear-gradient(90deg, #FF3B3B, #CC1111) !important;
    border: none !important; color: white !important;
    box-shadow: 0 0 18px rgba(255,59,59,0.25) !important;
}
div[data-testid="column"]:nth-child(1) .stButton button:hover {
    box-shadow: 0 0 28px rgba(255,59,59,0.45) !important;
}

/* ── Col 2: Find Nearby Services → Cyan ── */
div[data-testid="column"]:nth-child(2) .stButton button {
    background: linear-gradient(90deg, #00C2FF, #0099FF) !important;
    border: none !important; color: white !important;
    box-shadow: 0 0 18px rgba(0,194,255,0.2) !important;
}
div[data-testid="column"]:nth-child(2) .stButton button:hover {
    box-shadow: 0 0 28px rgba(0,194,255,0.4) !important;
}

/* ── Col 3: Send SOS → Strong Red ── */
div[data-testid="column"]:nth-child(3) .stButton button {
    background: linear-gradient(90deg, #FF1E1E, #AA0000) !important;
    border: none !important; color: white !important;
    box-shadow: 0 0 18px rgba(255,30,30,0.3) !important;
}
div[data-testid="column"]:nth-child(3) .stButton button:hover {
    box-shadow: 0 0 28px rgba(255,30,30,0.5) !important;
}

/* ── Col 4: What Should I Do Now? → Purple ── */
div[data-testid="column"]:nth-child(4) .stButton button {
    background: linear-gradient(90deg, #8B5CF6, #6D28D9) !important;
    border: none !important; color: white !important;
    box-shadow: 0 0 18px rgba(139,92,246,0.25) !important;
}
div[data-testid="column"]:nth-child(4) .stButton button:hover {
    box-shadow: 0 0 28px rgba(139,92,246,0.45) !important;
}

/* ── Col 5 / Last: ONE-TAP EMERGENCY → Orange-Red ── */
div[data-testid="column"]:nth-child(5) .stButton button,
div[data-testid="column"]:last-child .stButton button {
    background: linear-gradient(90deg, #F97316, #EA580C) !important;
    border: none !important; color: white !important;
    font-size: 0.95rem !important; font-weight: 800 !important;
    height: 72px !important;
    box-shadow: 0 0 24px rgba(249,115,22,0.4) !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="column"]:nth-child(5) .stButton button:hover,
div[data-testid="column"]:last-child .stButton button:hover {
    box-shadow: 0 0 36px rgba(249,115,22,0.6) !important;
    transform: translateY(-2px) !important;
}

/* ── Get Help button — strong red glow ── */
div[data-testid="stVerticalBlock"] .stButton button[data-testid="baseButton-secondary"] {
    background: linear-gradient(90deg, #FF3B3B, #FF1E1E) !important;
    border: none !important; color: white !important;
    font-size: 1rem !important; font-weight: 700 !important;
    padding: 16px !important; height: auto !important;
    box-shadow: 0 0 20px rgba(255,59,59,0.35) !important;
}

/* ── Form Submit ── */
.stFormSubmitButton button {
    background: linear-gradient(90deg, #FF3B3B, #FF1E1E) !important;
    color: white !important; border-radius: 12px !important;
    font-weight: 700 !important; border: none !important;
    padding: 14px !important; font-size: 0.95rem !important;
    box-shadow: 0 0 16px rgba(255,59,59,0.3) !important;
}

/* ── Sidebar Save button → Green ── */
section[data-testid="stSidebar"] .stFormSubmitButton button {
    background: linear-gradient(90deg, #22C55E, #16A34A) !important;
    box-shadow: 0 0 14px rgba(34,197,94,0.35) !important;
}

/* ── Inputs ── */
label, .stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stDateInput label, .stTimeInput label {
    color: #64748B !important; font-size: 0.75rem !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
.stTextInput input, .stTextArea textarea {
    background: #0B1120 !important; border: 1px solid #1E2A47 !important;
    border-radius: 10px !important; color: #E2E8F0 !important;
    padding: 12px 14px !important; font-size: 0.9rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #00C2FF !important;
    box-shadow: 0 0 0 2px rgba(0,194,255,0.15) !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #11182B !important; border-radius: 12px !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #64748B !important; font-size: 0.82rem !important;
    border-radius: 8px !important; padding: 8px 14px !important;
}
.stTabs [aria-selected="true"] {
    color: #E2E8F0 !important; background: #1E2A47 !important;
    border-bottom: 2px solid #00C2FF !important;
}

/* ── Divider ── */
hr { border-color: #1E2A47 !important; margin: 20px 0 !important; }

/* ── Caption ── */
.stCaption { color: #64748B !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #11182B !important; border: 1px solid #1E2A47 !important;
    border-radius: 12px !important; color: #E2E8F0 !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: #11182B !important; border: 1px solid #1E2A47 !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Sidebar inputs ── */
section[data-testid="stSidebar"] .stTextInput input {
    background: #070B1A !important; font-size: 0.88rem !important;
}

/* ── Audio input ── */
.stAudioInput { background: #11182B !important; border-radius: 12px !important; }

/* ── Spinner ── */
.stSpinner { color: #00C2FF !important; }

/* ── Success/Warning/Error/Info ── */
div[data-testid="stNotification"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- Session State + Storage ---
if "storage_loaded" not in st.session_state:
    # Try browser localStorage first (survives server restarts)
    browser_data = load_from_url_params()
    # Fall back to file storage
    saved = load_user_data()
    # Browser data takes priority over file data
    merged = {**saved, **browser_data}

    st.session_state.location          = merged.get("location", "")
    st.session_state.user_name         = merged.get("user_name", "")
    st.session_state.user_phone        = merged.get("user_phone", "")
    st.session_state.contact1          = merged.get("contact1", "")
    st.session_state.contact2          = merged.get("contact2", "")
    st.session_state.contact3          = merged.get("contact3", "")
    st.session_state.blood_group       = merged.get("blood_group", "")
    st.session_state.allergies         = merged.get("allergies", "")
    st.session_state.medical_conditions= merged.get("medical_conditions", "")
    st.session_state.low_network       = False
    st.session_state.lang              = merged.get("lang", "en")
    st.session_state.storage_loaded    = True
    st.session_state.auto_crash_enabled = merged.get("auto_crash_enabled", False)
    st.session_state.crash_threshold    = float(merged.get("crash_threshold", 25.0))
    if not st.session_state.location:
        ip_loc = get_location_from_ip()
        if ip_loc:
            st.session_state.location = ip_loc

# Shorthand for current language
lang = st.session_state.get("lang", "en")

if "network_checked" not in st.session_state:
    st.session_state.online = is_online()
    st.session_state.network_checked = True

auto_coords = get_coords_from_url()
# GPS coords always override IP-based location (more accurate)
if auto_coords:
    st.session_state.location = auto_coords

# --- Auto-trigger emergency mode from URL param ---
# When app icon is tapped (shortcut URL has ?action=emergency)
# or user shares emergency link, auto-fire the emergency flow
_url_action = st.query_params.get("action", "")
_crash_auto = st.query_params.get("crash_auto", "0") == "1"
auto_emergency = (_url_action == "emergency")

# --- Voice input from URL param ---
_voice_raw = st.query_params.get("voice_input", "")
if _voice_raw:
    st.session_state["voice_transcript"] = urllib.parse.unquote(_voice_raw)
    params = dict(st.query_params)
    params.pop("voice_input", None)
    st.query_params.update(params)

offline_mode = st.session_state.low_network or not st.session_state.online

# --- Sidebar ---
with st.sidebar:
    # ── Fix 5: Network status at TOP ──
    _net_color = "#00e676" if st.session_state.online else "#e53935"
    _net_label = "Connected" if st.session_state.online else "Offline"
    _ai_color  = "#00e676" if is_gemini_configured() else "#fb8c00"
    _ai_label  = "Active" if is_gemini_configured() else "Not configured"
    st.markdown(f"""
<div style="background:linear-gradient(135deg,{_net_color}12,{_net_color}06);
     border:1px solid {_net_color}33;border-radius:10px;padding:10px;margin-bottom:10px;
     box-shadow:0 0 12px {_net_color}15;">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
        <span style="color:#64748B;font-size:0.78rem;">&#127760; Network</span>
        <span style="color:{_net_color};font-size:0.78rem;font-weight:700;">{_net_label}</span>
    </div>
    <div style="display:flex;justify-content:space-between;">
        <span style="color:#64748B;font-size:0.78rem;">&#129504; Gemini AI</span>
        <span style="color:{_ai_color};font-size:0.78rem;font-weight:700;">{_ai_label}</span>
    </div>
</div>""", unsafe_allow_html=True)
    if st.button("🔄 Recheck Network", use_container_width=True):
        st.session_state.online = is_online()
        st.rerun()

    st.divider()

    # ── Fix 1: Inline editable YOUR DETAILS (no expander, no read-only card) ──
    st.markdown('<div class="section-header">YOUR DETAILS</div>', unsafe_allow_html=True)
    _loc_for_sidebar = st.session_state.get("location","")
    _en = get_emergency_numbers(_loc_for_sidebar)

    with st.form("sidebar_details_form", clear_on_submit=False):
        _edit_name  = st.text_input("Your Name",
            value=st.session_state.get("user_name",""),
            placeholder="e.g. Rahul Sharma")
        _edit_phone = st.text_input("Your Phone",
            value=st.session_state.get("user_phone",""),
            placeholder="9876543210")
        # Fix 3: Location shown in field, auto-detected value pre-filled
        _edit_loc = st.text_input("📍 Location",
            value=_loc_for_sidebar,
            placeholder="Auto-detected or type city name")
        # Show GPS detection status right below the location field
        if not offline_mode:
            render_auto_location()
        st.caption("Emergency Contacts (+91 auto-added)")
        _edit_c1 = st.text_input("Contact 1 *", value=st.session_state.contact1, placeholder="9876543210")
        _edit_c2 = st.text_input("Contact 2",   value=st.session_state.contact2, placeholder="9123456789")
        _edit_c3 = st.text_input("Contact 3",   value=st.session_state.contact3, placeholder="9000000000")
        st.caption("🩺 Medical Info (sent in SOS for paramedics)")
        _blood_options = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]
        _edit_blood = st.selectbox("Blood Group",
            options=_blood_options,
            index=_blood_options.index(st.session_state.get("blood_group","")) if st.session_state.get("blood_group","") in _blood_options else 0)
        _edit_allergies = st.text_input("Allergies", value=st.session_state.get("allergies",""), placeholder="e.g. Penicillin, Peanuts")
        _edit_conditions = st.text_input("Medical Conditions", value=st.session_state.get("medical_conditions",""), placeholder="e.g. Diabetic, Heart patient")
        _save = st.form_submit_button("💾 Save Details", use_container_width=True)
        if _edit_name:  st.session_state.user_name  = _edit_name
        if _edit_phone: st.session_state.user_phone = _edit_phone
        if _edit_loc:   st.session_state.location   = _edit_loc
        if _edit_c1:    st.session_state.contact1   = _edit_c1
        if _edit_c2:    st.session_state.contact2   = _edit_c2
        if _edit_c3:    st.session_state.contact3   = _edit_c3
        st.session_state.blood_group        = _edit_blood
        st.session_state.allergies          = _edit_allergies
        st.session_state.medical_conditions = _edit_conditions
        if _save:
            _data_to_save = {
                "location":           st.session_state.location,
                "user_name":          st.session_state.get("user_name",""),
                "user_phone":         st.session_state.get("user_phone",""),
                "contact1":           st.session_state.contact1,
                "contact2":           st.session_state.contact2,
                "contact3":           st.session_state.contact3,
                "blood_group":        st.session_state.get("blood_group",""),
                "allergies":          st.session_state.get("allergies",""),
                "medical_conditions": st.session_state.get("medical_conditions",""),
                "lang":               st.session_state.get("lang","en"),
            }
            save_user_data(_data_to_save)
            save_to_browser(_data_to_save)
            st.success("✅ Saved!")
            st.rerun()

    st.divider()

    # ── QUICK CALL ──
    st.markdown('<div class="section-header">QUICK CALL</div>', unsafe_allow_html=True)
    _call_items = [
        (_en["emergency"], "Emergency", "#FF3B3B", "🚨"),
        (_en["ambulance"], "Ambulance", "#FF6B6B", "🚑"),
        (_en["police"],    "Police",    "#00C2FF", "🚔"),
        (_en["fire"],      "Fire",      "#F97316", "🚒"),
    ]
    if _en.get("extra"):
        for _lbl, _num in list(_en["extra"].items())[:1]:
            _call_items.append((_num, _lbl, "#22C55E", "🛣️"))
    for _num, _label, _color, _icon in _call_items:
        st.markdown(f'''<a href="tel:{_num}" style="display:flex;align-items:center;gap:10px;
background:linear-gradient(90deg,{_color}22,{_color}11);
border:1px solid {_color}44;color:#E2E8F0;
padding:10px 12px;border-radius:10px;text-decoration:none;
font-weight:600;font-size:0.85rem;margin-bottom:6px;
box-shadow:0 0 10px {_color}15;">
<span style="background:linear-gradient(90deg,{_color},{_color}cc);padding:5px 9px;border-radius:7px;font-size:0.82rem;font-weight:700;">{_icon} {_num}</span>
<span style="color:#E2E8F0;">{_label}</span></a>''', unsafe_allow_html=True)

    st.divider()

    # ── SETTINGS ──
    st.markdown('<div class="section-header">SETTINGS</div>', unsafe_allow_html=True)
    _lang_options = list(LANGUAGES.keys())
    _selected_lang = st.selectbox(
        "Language",
        options=_lang_options,
        format_func=lambda x: LANGUAGES[x],
        index=_lang_options.index(st.session_state.get("lang","en")),
    )
    if _selected_lang != st.session_state.get("lang","en"):
        st.session_state.lang = _selected_lang
        save_user_data({
            "location":   st.session_state.location,
            "user_name":  st.session_state.get("user_name",""),
            "user_phone": st.session_state.get("user_phone",""),
            "contact1":   st.session_state.contact1,
            "contact2":   st.session_state.contact2,
            "contact3":   st.session_state.contact3,
            "lang":       _selected_lang,
        })
        st.rerun()
    lang = st.session_state.get("lang","en")
    st.session_state.low_network = st.toggle("Low Network Mode", value=st.session_state.low_network)
    offline_mode = st.session_state.low_network or not st.session_state.online
    render_crash_settings()
    st.caption("Tap numbers to call on mobile.")

# Re-read lang after sidebar (in case user changed it)
lang = st.session_state.get("lang", "en")
offline_mode = st.session_state.low_network or not st.session_state.online

# --- Page Navigation ---
_page = st.radio("", ["🚨 Emergency Assistant", "📖 How to Use Guide"],
    horizontal=True, label_visibility="collapsed",
    key="page_nav")

if _page == "📖 How to Use Guide":
    render_guide()
    st.stop()

# --- Hero ---
st.markdown(f"""
<div class="hero-box">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="
                background:linear-gradient(135deg,#FF3B3B22,#FF3B3B11);
                border:1px solid #FF3B3B44;border-radius:16px;
                padding:14px;font-size:2rem;line-height:1;
                box-shadow:0 0 20px rgba(255,59,59,0.2);
            ">🚨</div>
            <div>
                <div class="hero-title">RoadSoS</div>
                <div style="color:#94A3B8;font-size:0.95rem;font-weight:500;margin:3px 0 6px 0;letter-spacing:0.3px;">Emergency Assistant</div>
                <div style="display:flex;gap:12px;flex-wrap:wrap;">
                    <span style="background:rgba(255,59,59,0.12);color:#FF6B6B;font-size:0.7rem;padding:3px 10px;border-radius:20px;border:1px solid rgba(255,59,59,0.2);">🏥 First Aid</span>
                    <span style="background:rgba(0,194,255,0.12);color:#00C2FF;font-size:0.7rem;padding:3px 10px;border-radius:20px;border:1px solid rgba(0,194,255,0.2);">🗺️ Nearby Services</span>
                    <span style="background:rgba(139,92,246,0.12);color:#A78BFA;font-size:0.7rem;padding:3px 10px;border-radius:20px;border:1px solid rgba(139,92,246,0.2);">🤖 AI Guided</span>
                    <span style="background:rgba(34,197,94,0.12);color:#22C55E;font-size:0.7rem;padding:3px 10px;border-radius:20px;border:1px solid rgba(34,197,94,0.2);">📴 Works Offline</span>
                </div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="
                background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);
                border-radius:20px;padding:6px 14px;display:inline-block;
            ">
                <span class="status-dot"></span>
                <span style="font-size:0.72rem;color:#22C55E;font-weight:700;letter-spacing:1.5px;">SYSTEM ACTIVE</span>
            </div>
            <div style="font-size:0.65rem;color:#64748B;margin-top:6px;">All systems operational</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Quick Actions ---
st.markdown("""
<div class="section-quick-actions">
<div class="section-header" style="margin-top:0;">
    <span style="display:inline-block;width:10px;height:10px;background:#FF3B3B;border-radius:50%;box-shadow:0 0 8px #FF3B3B;"></span>
    ⚡ QUICK ACTIONS
</div>
""", unsafe_allow_html=True)

# Colored quick action buttons using HTML — full color control
btn_style = """
display:flex;align-items:center;justify-content:center;gap:6px;
width:100%;padding:16px 8px;border-radius:12px;border:none;
font-weight:700;font-size:0.88rem;cursor:pointer;color:white;
text-align:center;text-decoration:none;
"""
qa_col1, qa_col2 = st.columns([3, 2])
with qa_col1:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        accident_btn = st.button(t("btn_accident", lang), use_container_width=True, key="acc_btn")
        st.markdown(f"""<style>div[data-testid="stButton"] button[kind="secondary"]{{background:transparent}}</style>""", unsafe_allow_html=True)
    with c2:
        services_btn = st.button(t("btn_services", lang), use_container_width=True, key="svc_btn")
    with c3:
        sos_btn = st.button(t("btn_sos", lang), use_container_width=True, key="sos_btn")
    with c4:
        now_btn = st.button(t("btn_now", lang), use_container_width=True, key="now_btn")
with qa_col2:
    emergency_btn = st.button(t("btn_emergency", lang), use_container_width=True, key="emergency_main")

# Inject button colors directly into parent document
components.html("""
<script>
(function(){
    function applyColors(){
        var doc = window.parent.document;
        var btns = doc.querySelectorAll('button');
        btns.forEach(function(btn){
            var txt = (btn.innerText || '').trim();
            if((txt.includes('Accident') || txt.includes('दुर्घटना') || txt.includes('ప్రమాదం') || txt.includes('விபத்து')) && !txt.includes('ONE') && !txt.includes('Report')){
                btn.style.cssText += 'background:linear-gradient(90deg,#FF3B3B,#CC1111)!important;color:white!important;border:none!important;box-shadow:0 0 18px rgba(255,59,59,0.4)!important;border-radius:12px!important;';
            } else if(txt.includes('Find Nearby') || txt.includes('Nearby Services') || txt.includes('नजदीकी') || txt.includes('సమీప') || txt.includes('அருகிலுள்ள')){
                btn.style.cssText += 'background:linear-gradient(90deg,#00C2FF,#0099FF)!important;color:white!important;border:none!important;box-shadow:0 0 18px rgba(0,194,255,0.35)!important;border-radius:12px!important;';
            } else if((txt.includes('Send SOS') || txt.includes('SOS भेजें') || txt.includes('SOS పంపండి') || txt.includes('SOS அனுப்பு')) && !txt.includes('ONE')){
                btn.style.cssText += 'background:linear-gradient(90deg,#FF1E1E,#AA0000)!important;color:white!important;border:none!important;box-shadow:0 0 18px rgba(255,30,30,0.4)!important;border-radius:12px!important;';
            } else if(txt.includes('Should') || txt.includes('Do Now') || txt.includes('क्या करना') || txt.includes('ఏమి చేయాలి') || txt.includes('என்ன செய்ய')){
                btn.style.cssText += 'background:linear-gradient(90deg,#8B5CF6,#6D28D9)!important;color:white!important;border:none!important;box-shadow:0 0 18px rgba(139,92,246,0.4)!important;border-radius:12px!important;';
            } else if(txt.includes('ONE-TAP') || txt.includes('EMERGENCY') || txt.includes('आपातकाल') || txt.includes('అత్యవసరం') || txt.includes('அவசரநிலை')){
                btn.style.cssText += 'background:linear-gradient(90deg,#F97316,#EA580C)!important;color:white!important;border:none!important;box-shadow:0 0 24px rgba(249,115,22,0.5)!important;border-radius:12px!important;font-size:1rem!important;font-weight:800!important;';
            } else if(txt.includes('Get Help') || txt.includes('सहायता') || txt.includes('సహాయం') || txt.includes('உதவி')){
                btn.style.cssText += 'background:linear-gradient(90deg,#FF3B3B,#FF1E1E)!important;color:white!important;border:none!important;box-shadow:0 0 20px rgba(255,59,59,0.45)!important;border-radius:12px!important;font-size:1rem!important;font-weight:700!important;';
            }
        });
    }
    applyColors();
    setTimeout(applyColors, 300);
    setTimeout(applyColors, 800);
    setTimeout(applyColors, 2000);
    var observer = new MutationObserver(function(){ applyColors(); });
    observer.observe(window.parent.document.body, {childList:true, subtree:true});
})();
</script>
""", height=0)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- Voice + Chat Input ---
st.markdown("""
<div class="section-emergency-input">
<div class="section-header" style="margin-top:0;">
    <span style="display:inline-block;width:10px;height:10px;background:#00C2FF;border-radius:50%;box-shadow:0 0 8px #00C2FF;"></span>
    💬 DESCRIBE YOUR EMERGENCY
</div>
""", unsafe_allow_html=True)

# Voice transcript stored in session state
if "voice_transcript" not in st.session_state:
    st.session_state.voice_transcript = ""

# Read voice from URL param (fallback for browsers that support it)
_voice_prefill = ""
_vp = st.query_params.get("voice_input", "")
if _vp:
    _voice_prefill = urllib.parse.unquote(_vp)
    _params = dict(st.query_params)
    _params.pop("voice_input", None)
    st.query_params.update(_params)

# ── Native Streamlit Audio Input (works 100% reliably) ──
st.markdown("**🎤 Speak Your Emergency**")
audio_input = st.audio_input("Record your emergency", label_visibility="collapsed")

if audio_input is not None:
    try:
        import speech_recognition as sr
        import io
        recognizer = sr.Recognizer()
        audio_bytes = audio_input.read()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data, language="en-IN")
        st.session_state["last_voice"] = transcript
        st.success(f'✅ Heard: "{transcript}"')
        _voice_prefill = transcript
    except Exception as e:
        st.warning(f"⚠️ Could not transcribe audio. Please type your emergency below.")

user_input = st.text_input(
    t("type_situation", lang),
    value=_voice_prefill,
    placeholder=t("placeholder_emergency", lang),
    key="emergency_input"
)
if _voice_prefill:
    st.session_state["last_voice"] = _voice_prefill

send_btn = st.button(t("get_help", lang), use_container_width=True)

# Auto-fire response if voice came in
if _voice_prefill:
    send_btn = True

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- Helper Functions ---
def check_location():
    if not st.session_state.location:
        st.warning(t("no_location", lang))
        st.info("💡 Type your city name in the location box above and click **Save Details**.")
        return None
    return st.session_state.location

def show_response(response, loc):
    rtype = response["type"]
    if rtype in ("critical", "emergency"): st.error(f"**{response['title']}**")
    elif rtype == "first_aid":             st.warning(f"**{response['title']}**")
    elif rtype == "services":              st.success(f"**{response['title']}**")
    else:                                  st.info(f"**{response['title']}**")
    st.caption(f"📍 Location: {loc}")
    if response.get("ai_powered"):
        st.caption("🤖 Powered by Gemini AI")
    for i, step in enumerate(response["steps"], 1):
        st.markdown(f"{i}. {step}")
    tip = response.get("tip", "If unsure, call 112 immediately.")
    st.info(f"💡 {tip}")

    # ── Text-to-Speech: speak the response like Siri ──
    speak_text = response["title"] + ". " + ". ".join(response["steps"]) + ". Tip: " + tip
    speak_text = speak_text.replace('"', '').replace("'", "")
    components.html(f"""
    <script>
    (function(){{
        if(!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance({repr(speak_text)});
        msg.lang = 'en-IN';
        msg.rate = 0.95;
        msg.pitch = 1.0;
        msg.volume = 1.0;
        window.speechSynthesis.speak(msg);
    }})();
    </script>
    """, height=0)

def show_places(places, config, loc):
    st.success(f"{config['icon']} **{len(places)} results near: {loc}**")
    st.caption("Sorted by relevance + distance · Distances are approximate")
    for i, p in enumerate(places, 1):
        with st.container():
            col_info, col_call, col_nav = st.columns([3, 1, 1])
            with col_info:
                st.markdown(f"**{i}. {p['name']}**")
                st.markdown(f"📏 {p['distance_km']} km &nbsp;|&nbsp; 📞 {p['phone'] or 'No phone'}")
            with col_call:
                if p.get("call_link"):
                    st.markdown(f"<a href='{p['call_link']}' style='display:block;background:#43a047;"
                        f"color:white;text-align:center;padding:8px;border-radius:8px;"
                        f"text-decoration:none;font-weight:bold;font-size:12px;'>📞 Call</a>",
                        unsafe_allow_html=True)
            with col_nav:
                st.markdown(f"<a href='{p['gmaps_link']}' target='_blank' style='display:block;"
                    f"background:#1e88e5;color:white;text-align:center;padding:8px;border-radius:8px;"
                    f"text-decoration:none;font-weight:bold;font-size:12px;'>🗺 Go</a>",
                    unsafe_allow_html=True)
            st.divider()
    st.info(f"📞 Emergency number: **{config['emergency_number']}**")

def show_all_services(loc):
    en = get_emergency_numbers(loc)
    if offline_mode:
        st.warning("📶 No internet — showing emergency numbers only.")
        st.markdown(f"""
| Service | Number |
|---------|--------|
| 🆘 Emergency | **{en['emergency']}** |
| 🚑 Ambulance | **{en['ambulance']}** |
| 🚔 Police | **{en['police']}** |
| 🚒 Fire | **{en['fire']}** |
        """)
        if en.get("extra"):
            for label, num in en["extra"].items():
                st.markdown(f"| 📲 {label} | **{num}** |")
        return
    st.markdown("### 🗺️ All Nearby Emergency Services")
    st.caption(f"📍 Fetching services near: {loc}")
    categories = ["Trauma Centres", "Ambulance", "Police", "Vehicle Rescue", "Puncture/Repair", "Showrooms"]

    # Fetch all categories first for combined map
    all_results = {}
    ref_lat, ref_lon = None, None
    with st.spinner("Loading all nearby services..."):
        for sname in categories:
            result = fetch_services(loc, sname)
            if result["success"]:
                all_results[sname] = result["places"]
                if ref_lat is None:
                    ref_lat, ref_lon = result["lat"], result["lon"]

    # Combined map at the top
    if all_results and ref_lat:
        st.markdown("#### 🗺️ All Services — Combined Map")
        render_combined_map(ref_lat, ref_lon, all_results)
        st.divider()

    # Per-category tabs below
    tabs = st.tabs(["🏥 Trauma Centres","🚑 Ambulance","🚔 Police","🚛 Vehicle Rescue","🔧 Puncture/Repair","🏪 Showrooms"])
    for tab, sname in zip(tabs, categories):
        with tab:
            config = SERVICE_CONFIG[sname]
            if sname in all_results:
                show_places(all_results[sname], config, loc)
                if ref_lat:
                    render_map(ref_lat, ref_lon, all_results[sname], color=config["color"])
            else:
                st.error(f"❌ No {sname.lower()} found near '{loc}'.")
                st.markdown(f"**{config['icon']} Call: {config['emergency_number']}**")

def do_sos(loc):
    contacts = [st.session_state.contact1, st.session_state.contact2, st.session_state.contact3]
    valid = [c for c in contacts if c.strip()]
    if not valid:
        st.warning("⚠️ No emergency contacts saved. Please add contacts above.")
        return

    # Build rich SOS message with medical info + live location link
    name = st.session_state.get("user_name", "Someone")
    blood = st.session_state.get("blood_group", "")
    allergies = st.session_state.get("allergies", "")
    conditions = st.session_state.get("medical_conditions", "")

    # Live location link (Google Maps)
    if "," in loc:
        parts = loc.split(",")
        try:
            lat, lon = float(parts[0].strip()), float(parts[1].strip())
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        except:
            maps_link = f"https://www.google.com/maps/search/{urllib.parse.quote(loc)}"
    else:
        maps_link = f"https://www.google.com/maps/search/{urllib.parse.quote(loc)}"

    medical_info = ""
    if blood:       medical_info += f" Blood: {blood}."
    if allergies:   medical_info += f" Allergies: {allergies}."
    if conditions:  medical_info += f" Conditions: {conditions}."

    msg = (
        f"🚨 EMERGENCY ALERT 🚨\n"
        f"{name} needs immediate help!\n"
        f"📍 Location: {loc}\n"
        f"🗺️ Live Map: {maps_link}\n"
        f"🩺 Medical:{medical_info if medical_info else ' Not specified'}\n"
        f"Please call immediately or send help!\n"
        f"- Sent via RoadSoS"
    )
    if offline_mode:
        st.warning("📶 No internet — Twilio SMS unavailable.")
        st.markdown("**Copy and send this message manually:**")
        st.code(msg, language=None)
        st.markdown("**Or tap to open SMS app directly:**")
        for c in valid:
            num = format_number(c)
            sms_link = f"sms:{num}?body={urllib.parse.quote(msg)}"
            st.markdown(f"<a href='{sms_link}' style='display:inline-block;background:#1e88e5;"
                f"color:white;padding:8px 16px;border-radius:8px;text-decoration:none;"
                f"font-weight:bold;margin:4px;'>📱 SMS to {num}</a>", unsafe_allow_html=True)
        st.info("💡 These links open your phone's SMS app with the message pre-filled.")
        return
    with st.spinner(f"Sending SOS to {len(valid)} contact(s)..."):
        result = send_sos(valid, loc, custom_message=msg)
    if result["success"]:
        st.success(f"✅ SOS sent to {len(result['sent'])} contact(s)!")
        for num in result["sent"]:
            st.markdown(f"- 📨 **Sent** to {num}")
        st.info(f"📍 Location shared: **{loc}**")
        st.markdown(f"> *'EMERGENCY! I need help. My location: {loc}. Please call me immediately.'*")
    if result.get("failed"):
        for f in result["failed"]:
            st.error(f"❌ Failed for {f['number']}: {f['error']}")
        st.warning("Call 112 directly for immediate help.")

# --- Response Area ---
st.markdown("""
<div class="section-response">
<div class="section-header" style="margin-top:0;">
    <span style="display:inline-block;width:10px;height:10px;background:#8B5CF6;border-radius:50%;box-shadow:0 0 8px #8B5CF6;"></span>
    📋 RESPONSE
</div>
""", unsafe_allow_html=True)

# --- Auto Emergency Mode (triggered by URL ?action=emergency) ---
if auto_emergency and not st.session_state.get("auto_emergency_fired"):
    st.session_state.auto_emergency_fired = True
    loc = st.session_state.location
    if loc:
        st.error("🆘 **AUTO EMERGENCY MODE ACTIVATED**")
        st.caption("Triggered automatically from your emergency shortcut.")
        # Clear the action param so it doesn't re-fire on rerun
        st.query_params.clear()
        # Force the emergency button flow
        emergency_btn = True
    else:
        st.warning("⚠️ No location saved. Please set your location first, then use the emergency shortcut.")
        st.query_params.clear()

# Track which button was last pressed using session state
# This ensures content stays visible when checkboxes/widgets are interacted with
if accident_btn:
    st.session_state["active_action"] = "accident"
elif services_btn:
    st.session_state["active_action"] = "services"
elif sos_btn:
    st.session_state["active_action"] = "sos"
elif now_btn:
    st.session_state["active_action"] = "now"
elif emergency_btn:
    st.session_state["active_action"] = "emergency"
elif send_btn:
    st.session_state["active_action"] = "chat"
    st.session_state["last_chat_input"] = (
        st.session_state.get("emergency_input", "").strip() or
        _voice_prefill.strip() or
        st.session_state.get("last_voice", "").strip()
    )

_action = st.session_state.get("active_action", "")

if _action == "accident" or accident_btn:
    loc = check_location()
    if loc:
        st.error("🚨 **Accident Detected!**")
        st.caption(f"📍 Location: {loc}")

        # Golden Hour Timer
        render_golden_hour_timer()

        # Two columns: checklist + services
        acc_col1, acc_col2 = st.columns([1, 1])
        with acc_col1:
            st.markdown("#### 📋 Emergency Checklist")
            render_checklist("accident")
        with acc_col2:
            st.markdown("#### 🗺️ Nearby Emergency Services")
            show_all_services(loc)

elif _action == "services" or services_btn:
    loc = check_location()
    if loc:
        service_tabs = st.tabs(["🏥 Trauma Centres","🚑 Ambulance","🚔 Police","🚛 Vehicle Rescue","🔧 Puncture/Repair","🏪 Showrooms"])
        service_names = ["Trauma Centres","Ambulance","Police","Vehicle Rescue","Puncture/Repair","Showrooms"]
        for tab, sname in zip(service_tabs, service_names):
            with tab:
                config = SERVICE_CONFIG[sname]
                if offline_mode:
                    st.warning("📶 No internet — showing emergency number only.")
                    st.markdown(f"**{config['icon']} Call: {config['emergency_number']}**")
                    st.info("💡 Internet required to fetch live nearby services.")
                else:
                    with st.spinner(f"Finding {sname.lower()} near {loc}..."):
                        result = fetch_services(loc, sname)
                    if not result["success"]:
                        st.error(f"❌ {result['error']}")
                        st.markdown(f"**{config['icon']} Emergency: {config['emergency_number']}**")
                    else:
                        show_places(result["places"], config, loc)
                        render_map(result["lat"], result["lon"], result["places"], color=config["color"])

elif _action == "sos" or sos_btn:
    loc = check_location()
    if loc:
        do_sos(loc)

elif _action == "now" or now_btn:
    loc = check_location()
    if loc:
        en = get_emergency_numbers(loc)
        st.error("⚡ **IMMEDIATE ACTION GUIDE**")
        st.caption(f"📍 Location: {loc}")
        st.markdown(f"""
**Do these RIGHT NOW:**
1. **Call {en['emergency']}** — universal emergency number for {en['name']}
2. **Stay on the line** — tell them your exact location
3. **Don't move injured people** unless there's fire or immediate danger
4. **Apply pressure** on any bleeding wounds with a clean cloth
5. **Turn on hazard lights** if in a vehicle
6. **Send SOS** to your emergency contacts using the button above

> 💡 Then type or speak your specific situation below for detailed first aid guidance.
        """)

elif emergency_btn:
    loc = check_location()
    if loc:
        st.error("🆘 **ONE-TAP EMERGENCY ACTIVATED**")
        st.caption(f"📍 Location: {loc}")

        # Detect country-specific emergency numbers
        en = get_emergency_numbers(loc)
        flag = {"IN":"🇮🇳","US":"🇺🇸","GB":"🇬🇧","AU":"🇦🇺","CA":"🇨🇦","AE":"🇦🇪",
                "SG":"🇸🇬","DE":"🇩🇪","FR":"🇫🇷","JP":"🇯🇵","CN":"🇨🇳","XX":"🌍"}.get(en.get("country_code","XX"),"🌍")

        # Auto-dial ambulance on mobile via JS
        components.html(f"""
        <script>
        (function(){{
            try {{ window.location.href = 'tel:{en["ambulance"]}'; }} catch(e) {{}}
        }})();
        </script>
        """, height=0)

        # Call Buttons: country-specific numbers
        st.markdown(f"### {t('call_now', lang)}")
        st.caption(f"{flag} Emergency numbers for: **{en['name']}**")
        call_cols = st.columns(4)
        call_data = [
            (f"🚑 {en['ambulance']}\nAmbulance", f"tel:{en['ambulance']}", "#e53935"),
            (f"🆘 {en['emergency']}\nEmergency", f"tel:{en['emergency']}", "#b71c1c"),
            (f"🚔 {en['police']}\nPolice",        f"tel:{en['police']}",   "#1e88e5"),
            (f"🚒 {en['fire']}\nFire",             f"tel:{en['fire']}",     "#fb8c00"),
        ]
        for col, (label, href, color) in zip(call_cols, call_data):
            with col:
                st.markdown(
                    f"<a href='{href}' style='display:block;background:{color};"
                    f"color:white;text-align:center;padding:14px 6px;border-radius:12px;"
                    f"text-decoration:none;font-weight:bold;font-size:0.85rem;"
                    f"line-height:1.4;box-shadow:0 4px 12px rgba(0,0,0,0.4);'>"
                    f"{label}</a>",
                    unsafe_allow_html=True
                )

        st.divider()

        # Call Saved Contacts
        contacts = [st.session_state.contact1, st.session_state.contact2, st.session_state.contact3]
        valid_contacts = [c.strip() for c in contacts if c.strip()]

        if valid_contacts:
            st.markdown("### 👥 CALL YOUR EMERGENCY CONTACTS")
            sos_msg = urllib.parse.quote(
                f"🚨 EMERGENCY! I need help. My location: {loc}. "
                f"Please call me or send help immediately. - Sent via RoadSoS"
            )
            contact_cols = st.columns(len(valid_contacts))
            for col, contact in zip(contact_cols, valid_contacts):
                num = format_number(contact)
                wa_num = num.replace("+", "")
                with col:
                    st.markdown(
                        f"<div style='background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);"
                        f"border-radius:12px;padding:12px;text-align:center;'>"
                        f"<div style='color:#ffcdd2;font-size:0.8rem;margin-bottom:8px;'>📱 {num}</div>"
                        f"<a href='tel:{num}' style='display:block;background:#e53935;color:white;"
                        f"padding:10px;border-radius:8px;text-decoration:none;font-weight:bold;"
                        f"font-size:0.85rem;margin-bottom:6px;'>📞 Call Now</a>"
                        f"<a href='sms:{num}?body={sos_msg}' style='display:block;background:#1e88e5;"
                        f"color:white;padding:8px;border-radius:8px;text-decoration:none;"
                        f"font-weight:bold;font-size:0.8rem;margin-bottom:6px;'>💬 SMS SOS</a>"
                        f"<a href='https://wa.me/{wa_num}?text={sos_msg}' target='_blank' "
                        f"style='display:block;background:#25D366;color:white;padding:8px;"
                        f"border-radius:8px;text-decoration:none;font-weight:bold;font-size:0.8rem;'>"
                        f"📲 WhatsApp</a>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
        else:
            st.warning("⚠️ No emergency contacts saved — add them above to enable contact calling.")

        st.divider()

        # Send SMS SOS via Twilio
        st.markdown(t("sending_sos", lang))
        do_sos(loc)

        st.divider()

        # First Aid Quick Guide
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
**🩺 Immediate First Aid:**
1. Call **{en['ambulance']}** NOW
2. Check breathing
3. Press on bleeding wounds
4. Don't move injured people
5. Keep them warm and calm
            """)
        with col_b:
            st.markdown(f"""
**📞 {flag} Emergency Numbers ({en['name']}):**
- 🆘 Emergency: **{en['emergency']}**
- 🚑 Ambulance: **{en['ambulance']}**
- 🚔 Police: **{en['police']}**
- 🚒 Fire: **{en['fire']}**
            """)

elif send_btn:
    # Priority: typed input > voice prefill > last voice > session state
    final_input = (
        st.session_state.get("emergency_input", "").strip() or
        _voice_prefill.strip() or
        st.session_state.get("last_voice", "").strip()
    )
    if not final_input:
        st.warning("⚠️ Please type or speak your emergency first.")
    else:
        # Use location if available, else use a generic fallback
        loc = st.session_state.location or "Unknown Location"
        response = get_response(final_input)

        # Show severity classifier
        severity = classify_severity(final_input)
        render_severity_badge(severity)

        show_response(response, loc)

        # Show relevant checklist for critical/serious cases
        if severity["level"] in ("CRITICAL", "SERIOUS"):
            with st.expander("📋 Emergency Action Checklist", expanded=True):
                # Pick checklist type based on keywords
                if any(w in final_input.lower() for w in ["bleed", "blood", "cut", "wound"]):
                    render_checklist("bleeding")
                elif any(w in final_input.lower() for w in ["unconscious", "fainted", "not responding"]):
                    render_checklist("unconscious")
                elif any(w in final_input.lower() for w in ["fire", "burn", "flame"]):
                    render_checklist("fire")
                else:
                    render_checklist("accident")
        if response["type"] in ("critical", "first_aid", "emergency") and not offline_mode and st.session_state.location:
            st.divider()
            if response["type"] == "emergency":
                show_all_services(loc)
            else:
                st.markdown("### 🏥 Nearest Hospital to You")
                with st.spinner(f"Finding nearest hospital near {loc}..."):
                    hosp_result = fetch_services(loc, "Trauma Centres")
                if hosp_result["success"]:
                    places = hosp_result["places"][:5]
                    st.caption("📍 Closest hospitals — call before going")
                    for i, p in enumerate(places, 1):
                        ci, cc, cn = st.columns([3, 1, 1])
                        with ci:
                            st.markdown(f"**{i}. {p['name']}**")
                            st.markdown(f"📏 {p['distance_km']} km &nbsp;|&nbsp; 📞 {p['phone'] or 'No phone'}")
                        with cc:
                            if p.get("call_link"):
                                st.markdown(f"<a href='{p['call_link']}' style='display:block;"
                                    f"background:#43a047;color:white;text-align:center;padding:8px;"
                                    f"border-radius:8px;text-decoration:none;font-weight:bold;"
                                    f"font-size:12px;'>📞 Call</a>", unsafe_allow_html=True)
                        with cn:
                            st.markdown(f"<a href='{p['gmaps_link']}' target='_blank' style='display:block;"
                                f"background:#1e88e5;color:white;text-align:center;padding:8px;"
                                f"border-radius:8px;text-decoration:none;font-weight:bold;"
                                f"font-size:12px;'>🗺 Go</a>", unsafe_allow_html=True)
                    render_map(hosp_result["lat"], hosp_result["lon"], places, color="#e53935")
                else:
                    st.info("🏥 Could not fetch hospitals. Call **108** for ambulance.")
else:
    st.markdown("""
    <div style="background:#0B1120;border:1px solid #1E2A47;
                border-radius:12px;padding:24px;text-align:center;color:#64748B;">
        <div style="font-size:2rem;margin-bottom:8px;">🚨</div>
        <div style="font-size:0.95rem;font-weight:600;color:#E2E8F0;margin-bottom:4px;">Ready to help</div>
        <div style="font-size:0.85rem;">Use the Quick Actions above or describe your emergency below</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Accident Report Generator ---
st.divider()
st.markdown(f'<div class="section-header">{t("accident_report", lang)}</div>', unsafe_allow_html=True)
with st.expander("📄 Generate Accident Report (for Insurance / Police)", expanded=False):
    st.caption("Fill in the details below and download a PDF report for insurance or police filing.")

    from report_generator import generate_report_pdf, generate_report_text

    with st.form("accident_report_form"):
        st.markdown("**📍 Incident Details**")
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            r_date = st.date_input("Date of Accident", value=datetime.now().date())
            r_location = st.text_input("Location of Accident",
                value=st.session_state.get("location", ""),
                placeholder="e.g. NH-44, near Hyderabad")
            r_accident_type = st.selectbox("Type of Accident", [
                "Vehicle Collision", "Single Vehicle Crash", "Pedestrian Hit",
                "Hit and Run", "Multi-vehicle Pile-up", "Animal on Road", "Other"
            ])
        with r_col2:
            r_time = st.time_input("Time of Accident", value=datetime.now().time())
            r_road = st.selectbox("Road Condition", [
                "Dry", "Wet / Rainy", "Foggy", "Under Construction",
                "Pothole / Damaged", "Slippery", "Good"
            ])
            r_weather = st.selectbox("Weather", [
                "Clear", "Rainy", "Foggy", "Night / Dark", "Sunny", "Stormy"
            ])

        st.markdown("**👤 Your Details**")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            r_name = st.text_input("Your Full Name",
                value=st.session_state.get("user_name", ""),
                placeholder="e.g. Rahul Sharma")
        with p_col2:
            r_phone = st.text_input("Your Phone",
                value=st.session_state.get("user_phone", "") or st.session_state.get("contact1", ""),
                placeholder="9876543210")
        with p_col3:
            r_role = st.selectbox("Your Role", [
                "Driver (Vehicle 1)", "Driver (Vehicle 2)", "Passenger",
                "Bystander / Witness", "First Responder"
            ])

        st.markdown("**🚗 Vehicles Involved**")
        v_col1, v_col2, v_col3 = st.columns(3)
        with v_col1:
            r_num_vehicles = st.number_input("Number of Vehicles", min_value=1, max_value=10, value=2)
        with v_col2:
            r_vehicle1 = st.text_input("Vehicle 1", placeholder="e.g. Honda City MH-01-AB-1234")
        with v_col3:
            r_vehicle2 = st.text_input("Vehicle 2", placeholder="e.g. Truck TN-09-XY-5678")

        st.markdown("**🏥 Casualties & Emergency**")
        c_col1, c_col2, c_col3, c_col4 = st.columns(4)
        with c_col1:
            r_injured = st.number_input("Persons Injured", min_value=0, max_value=50, value=0)
        with c_col2:
            r_fatalities = st.number_input("Fatalities", min_value=0, max_value=50, value=0)
        with c_col3:
            r_ambulance = st.selectbox("Ambulance Called?", ["Yes", "No", "Not Required"])
        with c_col4:
            r_police = st.selectbox("Police Called?", ["Yes", "No", "Not Required"])

        r_injury_details = st.text_input("Injury Details", placeholder="e.g. Head injury, fracture in left leg")
        r_hospital = st.text_input("Hospital Name (if admitted)", placeholder="e.g. Apollo Hospital, Hyderabad")

        st.markdown("**📝 Incident Description**")
        r_description = st.text_area("Describe what happened",
            placeholder="e.g. A truck overtook from the wrong side and collided with my car near the highway junction...",
            height=100)

        st.markdown("**👁️ Witness / Emergency Contact Details**")
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            r_witness_name = st.text_input("Witness / Parent Name",
                value=st.session_state.get("user_name","") and "" or "",
                placeholder="e.g. Priya Reddy")
        with w_col2:
            r_witness_phone = st.text_input("Witness / Parent Phone",
                value=st.session_state.get("contact1",""),
                placeholder="9000000000")

        generate_btn = st.form_submit_button("📄 Generate Report", use_container_width=True)

    if generate_btn:
        report_data = {
            "incident_date":   str(r_date),
            "incident_time":   str(r_time),
            "location":        r_location,
            "accident_type":   r_accident_type,
            "road_condition":  r_road,
            "weather":         r_weather,
            "reporter_name":   r_name,
            "reporter_phone":  r_phone,
            "reporter_role":   r_role,
            "num_vehicles":    str(r_num_vehicles),
            "vehicle1":        r_vehicle1,
            "vehicle2":        r_vehicle2,
            "num_injured":     str(r_injured),
            "num_fatalities":  str(r_fatalities),
            "injury_details":  r_injury_details,
            "ambulance_called": r_ambulance,
            "police_called":   r_police,
            "hospital_name":   r_hospital,
            "description":     r_description,
            "witness_name":    r_witness_name,
            "witness_phone":   r_witness_phone,
        }

        pdf_bytes = generate_report_pdf(report_data)
        filename = f"accident_report_{str(r_date).replace('-','')}.pdf"

        if pdf_bytes:
            st.success("✅ Report generated successfully!")
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )
        else:
            # Fallback to text
            st.warning("⚠️ PDF library not installed — downloading as text file instead.")
            st.info("Run `pip install reportlab` to enable PDF generation.")
            text_report = generate_report_text(report_data)
            st.download_button(
                label="⬇️ Download Text Report",
                data=text_report,
                file_name=filename.replace(".pdf", ".txt"),
                mime="text/plain",
                use_container_width=True
            )
            with st.expander("👁️ Preview Report"):
                st.code(text_report, language=None)

# --- Future Scope ---
st.divider()
with st.expander("🔭 Future Scope & Scalability"):
    st.markdown("""
- 📱 **Crash Detection** — Auto-trigger SOS using phone accelerometer on sudden impact
- ⌚ **Wearable Integration** — Smartwatch heart rate / fall detection triggers alert
- 🛰️ **Live Location Sharing** — Real-time GPS link updates every 30 seconds
- 🌐 **Multilingual Support** — Hindi, Telugu, Tamil
- 🤖 **LLM Upgrade** — Replace keyword logic with GPT/Gemini
- 📊 **Accident Heatmaps** — Show high-risk zones on map
- 🏥 **Hospital Bed Availability** — Real-time ICU/emergency bed status
    """)

st.divider()
st.markdown("""
<div style="text-align:center;color:#555;font-size:0.8rem;padding:8px 0;">
    🚨 RoadSoS · Built for emergencies · Always call
    <b style="color:#e53935">112</b> for immediate help · First aid works offline
</div>""", unsafe_allow_html=True)
