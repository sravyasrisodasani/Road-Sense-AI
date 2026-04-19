import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
from chatbot import get_response
from sos import send_sos, format_number
from services import fetch_services, SERVICE_CONFIG
from location_detect import render_geolocation_widget, get_coords_from_url
from map_view import render_map
from network_check import is_online
from storage import load_user_data, save_user_data

st.set_page_config(page_title="RoadSoS Emergency Assistant", page_icon="🚨", layout="centered")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#f0f0f0;}
.title-box{background:linear-gradient(90deg,#e53935,#b71c1c);border-radius:16px;
    padding:24px 32px;text-align:center;margin-bottom:8px;
    box-shadow:0 4px 20px rgba(229,57,53,0.4);}
.title-box h1{color:white;font-size:2.2rem;margin:0;letter-spacing:1px;}
.title-box p{color:#ffcdd2;margin:6px 0 0 0;font-size:1rem;}
.stat-row{display:flex;gap:12px;margin:16px 0;}
.stat-card{flex:1;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
    border-radius:12px;padding:14px;text-align:center;}
.stat-card .icon{font-size:1.6rem;}
.stat-card .label{font-size:0.75rem;color:#aaa;margin-top:4px;}
.stat-card .value{font-size:1rem;font-weight:bold;color:#fff;}
.section-header{font-size:1rem;font-weight:700;color:#ff8a80;
    text-transform:uppercase;letter-spacing:1.5px;margin:20px 0 8px 0;}
label,.stTextInput label{color:#ffcdd2 !important;font-weight:600 !important;}
.stTextInput input{background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.2) !important;
    border-radius:10px !important;color:white !important;padding:10px 14px !important;}
.stTextInput input:focus{border-color:#e53935 !important;
    box-shadow:0 0 0 2px rgba(229,57,53,0.3) !important;}
.stButton button{border-radius:10px !important;font-weight:700 !important;
    font-size:0.9rem !important;padding:10px !important;
    transition:all 0.2s ease !important;border:none !important;}
.stButton button:hover{transform:translateY(-2px) !important;
    box-shadow:0 6px 16px rgba(0,0,0,0.3) !important;}
div[data-testid="column"]:nth-child(1) .stButton button{
    background:linear-gradient(135deg,#e53935,#b71c1c) !important;color:white !important;}
div[data-testid="column"]:nth-child(2) .stButton button{
    background:linear-gradient(135deg,#43a047,#1b5e20) !important;color:white !important;}
div[data-testid="column"]:nth-child(3) .stButton button{
    background:linear-gradient(135deg,#1e88e5,#0d47a1) !important;color:white !important;}
div[data-testid="column"]:nth-child(4) .stButton button{
    background:linear-gradient(135deg,#fb8c00,#e65100) !important;color:white !important;}
div[data-testid="column"]:nth-child(5) .stButton button{
    background:linear-gradient(135deg,#8e24aa,#4a148c) !important;color:white !important;}
hr{border-color:rgba(255,255,255,0.1) !important;margin:16px 0 !important;}
.stAlert{border-radius:12px !important;}
.stFormSubmitButton button{background:linear-gradient(135deg,#e53935,#b71c1c) !important;
    color:white !important;border-radius:10px !important;font-weight:700 !important;}
.stCaption{color:#aaa !important;}
.stTabs [data-baseweb="tab"]{color:#ffcdd2 !important;}
.stTabs [aria-selected="true"]{border-bottom:2px solid #e53935 !important;}
</style>
""", unsafe_allow_html=True)

# --- Session State + Storage ---
if "storage_loaded" not in st.session_state:
    saved = load_user_data()
    st.session_state.location    = saved.get("location", "")
    st.session_state.contact1    = saved.get("contact1", "")
    st.session_state.contact2    = saved.get("contact2", "")
    st.session_state.contact3    = saved.get("contact3", "")
    st.session_state.low_network = False
    st.session_state.storage_loaded = True

if "network_checked" not in st.session_state:
    st.session_state.online = is_online()
    st.session_state.network_checked = True

auto_coords = get_coords_from_url()
if auto_coords and not st.session_state.location:
    st.session_state.location = auto_coords

offline_mode = st.session_state.low_network or not st.session_state.online

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.session_state.online:
        st.success("🟢 Internet: Connected")
    else:
        st.error("🔴 Internet: Not detected")
        st.caption("Running in offline-first mode.")
    st.session_state.low_network = st.toggle("📶 Force Low Network Mode",
        value=st.session_state.low_network,
        help="Force offline mode even if internet is available")
    offline_mode = st.session_state.low_network or not st.session_state.online
    if st.button("🔄 Recheck Network", use_container_width=True):
        st.session_state.online = is_online()
        st.rerun()
    st.divider()
    st.markdown("### 🆘 Quick Call")
    st.markdown("""
<a href="tel:112" style="display:block;background:#e53935;color:white;text-align:center;
   padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:6px;">
   📞 112 — Emergency</a>
<a href="tel:108" style="display:block;background:#e53935;color:white;text-align:center;
   padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:6px;">
   🚑 108 — Ambulance</a>
<a href="tel:100" style="display:block;background:#1e88e5;color:white;text-align:center;
   padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:6px;">
   🚔 100 — Police</a>
<a href="tel:101" style="display:block;background:#fb8c00;color:white;text-align:center;
   padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:6px;">
   🚒 101 — Fire</a>
<a href="tel:1033" style="display:block;background:#fb8c00;color:white;text-align:center;
   padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;">
   🛣️ 1033 — Highway</a>
    """, unsafe_allow_html=True)
    st.caption("Tap to call on mobile. On PC, dial manually.")

# --- Hero ---
st.markdown("""
<div class="title-box">
    <h1>🚨 RoadSoS Emergency Assistant</h1>
    <p>Instant help during road accidents · First Aid · Nearby Services · SOS Alerts</p>
</div>
<div class="stat-row">
    <div class="stat-card"><div class="icon">🏥</div><div class="value">Real-time</div><div class="label">Service Finder</div></div>
    <div class="stat-card"><div class="icon">📞</div><div class="value">Instant</div><div class="label">SOS Alerts</div></div>
    <div class="stat-card"><div class="icon">🩺</div><div class="value">AI-Guided</div><div class="label">First Aid</div></div>
    <div class="stat-card"><div class="icon">📴</div><div class="value">Offline</div><div class="label">First Aid Works</div></div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Details Form ---
st.markdown('<div class="section-header">📍 Your Details</div>', unsafe_allow_html=True)
with st.form("details_form", clear_on_submit=False):
    loc_col, _ = st.columns([2, 1])
    with loc_col:
        location_input = st.text_input("📍 Your Location",
            value=st.session_state.location, placeholder="e.g. Hyderabad, Mumbai")
    st.markdown("**📞 Emergency Contacts** *(+91 added automatically · saved for next time)*")
    c1, c2, c3 = st.columns(3)
    with c1: contact1 = st.text_input("Contact 1 *", value=st.session_state.contact1, placeholder="9876543210")
    with c2: contact2 = st.text_input("Contact 2",   value=st.session_state.contact2, placeholder="9123456789")
    with c3: contact3 = st.text_input("Contact 3",   value=st.session_state.contact3, placeholder="9000000000")
    save_btn = st.form_submit_button("💾 Save Details", use_container_width=True)
    if location_input: st.session_state.location = location_input
    if contact1:       st.session_state.contact1 = contact1
    if contact2:       st.session_state.contact2 = contact2
    if contact3:       st.session_state.contact3 = contact3
    if save_btn:
        save_user_data({"location": st.session_state.location,
                        "contact1": st.session_state.contact1,
                        "contact2": st.session_state.contact2,
                        "contact3": st.session_state.contact3})
        st.success("✅ Details saved! Will be remembered next time.")

if not offline_mode:
    render_geolocation_widget()

st.divider()

# --- Quick Actions ---
st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: accident_btn  = st.button("🚨 Accident",              use_container_width=True)
with col2: services_btn  = st.button("🗺️ Find Nearby Services",  use_container_width=True)
with col3: sos_btn       = st.button("📞 Send SOS",              use_container_width=True)
with col4: now_btn       = st.button("⚡ What Should I Do Now?", use_container_width=True)
with col5: emergency_btn = st.button("🆘 ONE-TAP EMERGENCY",     use_container_width=True)

st.divider()

# --- Voice + Chat Input ---
st.markdown('<div class="section-header">💬 Describe Your Emergency</div>', unsafe_allow_html=True)
components.html("""
<div style="margin-bottom:8px;">
    <button onclick="startVoice()" id="mic-btn"
        style="background:linear-gradient(135deg,#e53935,#b71c1c);color:white;border:none;
               border-radius:10px;padding:10px 20px;font-size:14px;font-weight:bold;
               cursor:pointer;box-shadow:0 2px 8px rgba(229,57,53,0.4);">
        🎤 Speak Your Emergency
    </button>
    <span id="mic-status" style="margin-left:12px;color:#aaa;font-size:13px;"></span>
</div>
<script>
function startVoice(){
    const btn=document.getElementById('mic-btn');
    const status=document.getElementById('mic-status');
    if(!('webkitSpeechRecognition' in window)&&!('SpeechRecognition' in window)){
        status.innerText='⚠️ Voice not supported. Use Chrome.';status.style.color='orange';return;}
    const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
    const r=new SR();r.lang='en-IN';r.interimResults=false;r.maxAlternatives=1;
    btn.innerText='🔴 Listening...';btn.style.background='#b71c1c';
    status.innerText='Speak now...';status.style.color='#ff8a80';
    r.start();
    r.onresult=function(e){
        const t=e.results[0][0].transcript;
        const inputs=window.parent.document.querySelectorAll('input[type="text"]');
        if(inputs.length>0){
            const target=inputs[inputs.length-1];
            const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
            setter.call(target,t);target.dispatchEvent(new Event('input',{bubbles:true}));}
        btn.innerText='🎤 Speak Your Emergency';
        btn.style.background='linear-gradient(135deg,#e53935,#b71c1c)';
        status.innerText='✅ Heard: "'+t+'"';status.style.color='#69f0ae';};
    r.onerror=function(){
        btn.innerText='🎤 Speak Your Emergency';
        btn.style.background='linear-gradient(135deg,#e53935,#b71c1c)';
        status.innerText='⚠️ Could not hear. Try again or type below.';status.style.color='orange';};}
</script>
""", height=60)

user_input = st.text_input("Or type your situation",
    placeholder="e.g. heavy bleeding, unconscious, fracture, burn, choking, head injury, shock")
send_btn = st.button("🔍 Get Help", use_container_width=True)

st.divider()

# --- Helper Functions ---
def check_location():
    if not st.session_state.location:
        st.warning("⚠️ Please enter your location above and click **Save Details**.")
        return None
    return st.session_state.location

def show_response(response, loc):
    t = response["type"]
    if t in ("critical", "emergency"): st.error(f"**{response['title']}**")
    elif t == "first_aid":             st.warning(f"**{response['title']}**")
    elif t == "services":              st.success(f"**{response['title']}**")
    else:                              st.info(f"**{response['title']}**")
    st.caption(f"📍 Location: {loc}")
    for i, step in enumerate(response["steps"], 1):
        st.markdown(f"{i}. {step}")
    st.info(f"💡 {response.get('tip', 'If unsure, call 112 immediately.')}")

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
    if offline_mode:
        st.warning("📶 No internet — showing emergency numbers only.")
        st.markdown("""
| Service | Number |
|---------|--------|
| 🆘 Emergency | **112** |
| 🚑 Ambulance | **108** |
| 🚔 Police | **100** |
| 🚒 Fire | **101** |
| 🛣️ Highway | **1033** |
        """)
        return
    st.markdown("### 🗺️ All Nearby Emergency Services")
    st.caption(f"📍 Fetching services near: {loc}")
    categories = ["Hospitals", "Ambulance", "Police", "Towing", "Puncture/Repair", "Showrooms"]
    tabs = st.tabs(["🏥 Hospitals","🚑 Ambulance","🚔 Police","🚛 Towing","🔧 Puncture/Repair","🏪 Showrooms"])
    for tab, sname in zip(tabs, categories):
        with tab:
            config = SERVICE_CONFIG[sname]
            with st.spinner(f"Finding {sname.lower()}..."):
                result = fetch_services(loc, sname)
            if not result["success"]:
                st.error(f"❌ {result['error']}")
                st.markdown(f"**{config['icon']} Call: {config['emergency_number']}**")
            else:
                show_places(result["places"], config, loc)
                render_map(result["lat"], result["lon"], result["places"], color=config["color"])

def do_sos(loc):
    contacts = [st.session_state.contact1, st.session_state.contact2, st.session_state.contact3]
    valid = [c for c in contacts if c.strip()]
    if not valid:
        st.warning("⚠️ No emergency contacts saved. Please add contacts above.")
        return
    if offline_mode:
        st.warning("📶 No internet — Twilio SMS unavailable.")
        msg = f"🚨 EMERGENCY! I need help. My location: {loc}. Please call me or send help immediately. - Sent via RoadSoS"
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
        result = send_sos(valid, loc)
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
st.markdown('<div class="section-header">📋 Response</div>', unsafe_allow_html=True)

if accident_btn:
    loc = check_location()
    if loc:
        st.error("🚨 **Accident Detected!**")
        st.caption(f"📍 Location: {loc}")
        st.markdown("""
1. Stay calm. Move yourself to safety away from traffic.
2. Call **112** immediately — give your location.
3. Do NOT move injured people unless there is fire or danger.
4. Switch on hazard lights and warn other drivers.
5. Stay with the injured and keep them calm until help arrives.
        """)
        st.info("💡 If unsure what to do, call 112 and follow their instructions.")
        st.divider()
        show_all_services(loc)

elif services_btn:
    loc = check_location()
    if loc:
        service_tabs = st.tabs(["🏥 Hospitals","🚑 Ambulance","🚔 Police","🚛 Towing","🔧 Puncture/Repair","🏪 Showrooms"])
        service_names = ["Hospitals","Ambulance","Police","Towing","Puncture/Repair","Showrooms"]
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

elif sos_btn:
    loc = check_location()
    if loc:
        do_sos(loc)

elif now_btn:
    loc = check_location()
    if loc:
        st.error("⚡ **IMMEDIATE ACTION GUIDE**")
        st.caption(f"📍 Location: {loc}")
        st.markdown("""
**Do these RIGHT NOW:**
1. **Call 112** — India's universal emergency number
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
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
**🩺 Immediate First Aid:**
1. Call **112** NOW
2. Check breathing
3. Press on bleeding wounds
4. Don't move injured people
5. Keep them warm and calm
            """)
        with col_b:
            st.markdown("""
**📞 Emergency Numbers:**
- 🆘 Emergency: **112**
- 🚑 Ambulance: **108**
- 🚔 Police: **100**
- 🚒 Fire: **101**
- 🛣️ Highway: **1033**
            """)
        st.divider()
        st.markdown("**📨 Sending SOS to all saved contacts...**")
        do_sos(loc)

elif send_btn:
    if not user_input:
        st.warning("⚠️ Please type or speak your emergency first.")
    else:
        loc = check_location()
        if loc:
            response = get_response(user_input)
            show_response(response, loc)
            if response["type"] in ("critical", "first_aid", "emergency") and not offline_mode:
                st.divider()
                if response["type"] == "emergency":
                    show_all_services(loc)
                else:
                    st.markdown("### 🏥 Nearest Hospital to You")
                    with st.spinner(f"Finding nearest hospital near {loc}..."):
                        hosp_result = fetch_services(loc, "Hospitals")
                    if hosp_result["success"]:
                        places = hosp_result["places"][:3]
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
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                border-radius:12px;padding:20px;text-align:center;color:#aaa;">
        👆 Enter your location, then click a button or describe your emergency to get help.
    </div>""", unsafe_allow_html=True)

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
