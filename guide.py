"""
RoadSoS — Complete User Guide Page
A friendly, easy-to-understand guide for users of all ages.
"""
import streamlit as st


def render_guide():
    st.markdown("""
<style>
.guide-section{background:#11182B;border:1px solid #1E2A47;border-radius:16px;padding:24px;margin-bottom:20px;}
.guide-step{background:rgba(0,194,255,0.06);border-left:4px solid #00C2FF;border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;color:#E2E8F0;font-size:0.95rem;line-height:1.6;}
.guide-warning{background:rgba(255,59,59,0.08);border-left:4px solid #FF3B3B;border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;color:#E2E8F0;}
.guide-tip{background:rgba(34,197,94,0.08);border-left:4px solid #22C55E;border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;color:#E2E8F0;}
.guide-feature{background:rgba(139,92,246,0.08);border-left:4px solid #8B5CF6;border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;color:#E2E8F0;}
.big-number{font-size:2.5rem;font-weight:900;color:#FF3B3B;margin-right:12px;}
.section-title{font-size:1.2rem;font-weight:800;color:#E2E8F0;margin-bottom:4px;}
.section-sub{font-size:0.85rem;color:#64748B;margin-bottom:16px;}
</style>
""", unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
<div style="background:linear-gradient(135deg,#0D1B2E,#111827);border:1px solid #1E2A47;
     border-radius:20px;padding:32px;margin-bottom:24px;position:relative;overflow:hidden;">
<div style="position:absolute;top:0;left:0;right:0;height:3px;
     background:linear-gradient(90deg,#FF3B3B,#F97316,#00C2FF,#22C55E);"></div>
<div style="font-size:2.2rem;font-weight:900;color:#fff;margin-bottom:8px;">📖 How to Use RoadSoS</div>
<div style="font-size:1rem;color:#94A3B8;line-height:1.7;">
    This guide explains <strong style="color:#E2E8F0;">every single feature</strong> of RoadSoS in simple words.<br>
    Whether you are 15 or 75, this guide will help you use the app confidently.<br>
    <span style="color:#22C55E;">✅ No technical knowledge needed.</span>
</div>
</div>
""", unsafe_allow_html=True)

    # ── WHAT IS ROADSOS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🚨 What is RoadSoS?</div>
<div class="section-sub">Understanding the app in simple words</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
RoadSoS is a <strong>free emergency helper app</strong> for road accidents. Imagine you are driving and suddenly there is an accident.
You are scared, confused, and don't know what to do. RoadSoS is like having a <strong>calm, smart friend</strong> right in your phone
who tells you exactly what to do, finds the nearest hospital, calls for help, and alerts your family — all in seconds.
</p>
<div class="guide-tip">💡 <strong>Think of it like this:</strong> RoadSoS is your personal emergency assistant that works 24 hours a day, 7 days a week, even without internet.</div>
<p style="color:#94A3B8;font-size:0.9rem;margin-top:12px;">
<strong style="color:#E2E8F0;">Who can use it?</strong> Anyone — accident victims, bystanders who see an accident, family members, drivers, passengers, even children who want to help an injured adult.
</p>
</div>
""", unsafe_allow_html=True)

    # ── FIRST TIME SETUP ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">⚙️ First Time Setup — Do This Once!</div>
<div class="section-sub">Takes only 2 minutes. You never have to do it again.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you open RoadSoS for the first time, look at the <strong>left side panel</strong> (called the sidebar).
On mobile, tap the small arrow or menu icon to open it. You will see a form to fill in your details.
</p>
<div class="guide-step">📝 <strong>Step 1 — Your Name:</strong> Type your full name. Example: "Rahul Sharma". This will appear in emergency messages sent to your family.</div>
<div class="guide-step">📱 <strong>Step 2 — Your Phone:</strong> Type your mobile number. Example: "9876543210". The app adds +91 automatically for India.</div>
<div class="guide-step">📍 <strong>Step 3 — Location:</strong> Your location is detected automatically! You don't need to type anything. But if it doesn't detect, just type your city name like "Hyderabad" or "Mumbai".</div>
<div class="guide-step">👥 <strong>Step 4 — Emergency Contacts:</strong> Add 3 phone numbers of people you trust — your parents, spouse, or close friends. These people will get an automatic alert if you are in an accident.</div>
<div class="guide-step">🩸 <strong>Step 5 — Blood Group:</strong> Select your blood group from the list (A+, B-, O+, etc.). This is very important — doctors need this information immediately in an emergency.</div>
<div class="guide-step">💊 <strong>Step 6 — Allergies:</strong> If you are allergic to any medicine or food, type it here. Example: "Penicillin, Aspirin". Doctors will know not to give you these medicines.</div>
<div class="guide-step">🏥 <strong>Step 7 — Medical Conditions:</strong> If you have any health conditions, mention them. Example: "Diabetic, High Blood Pressure". This helps paramedics treat you correctly.</div>
<div class="guide-step">💾 <strong>Step 8 — Click Save Details:</strong> Press the green "Save Details" button. Done! Your information is saved forever.</div>
<div class="guide-tip">✅ <strong>Good news:</strong> Once saved, your details are remembered even if you close the app, restart your phone, or come back after months. You never need to fill this again.</div>
</div>
""", unsafe_allow_html=True)

    # ── 5 MAIN BUTTONS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">⚡ The 5 Main Buttons — Your Emergency Controls</div>
<div class="section-sub">These are the most important buttons. Each one does something different.</div>
</div>
""", unsafe_allow_html=True)

    # Button 1
    st.markdown("""
<div class="guide-section" style="border-left:4px solid #FF3B3B;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
<div style="background:linear-gradient(90deg,#FF3B3B,#CC1111);padding:10px 16px;border-radius:10px;font-size:1.1rem;font-weight:800;color:white;">🚨 Accident</div>
<div style="color:#FF6B6B;font-size:0.8rem;font-weight:700;">RED BUTTON</div>
</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>When to press:</strong> When you see or are in a road accident.</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>What happens when you press it:</strong></p>
<div class="guide-step">⏱️ A <strong>Golden Hour Timer</strong> starts counting down from 60 minutes. The "golden hour" is the most important time after an accident — getting medical help within this time can save a life.</div>
<div class="guide-step">📋 An <strong>Emergency Checklist</strong> appears with simple steps like "Call 112", "Check breathing", "Don't move injured person". You can tick each step as you complete it.</div>
<div class="guide-step">🗺️ A <strong>map appears</strong> showing all nearby hospitals, ambulances, police stations, and towing services. You can tap any of them to call or get directions.</div>
<div class="guide-tip">💡 <strong>Tip:</strong> Even if you are scared and shaking, just follow the checklist one step at a time. It will guide you through everything.</div>
</div>
""", unsafe_allow_html=True)

    # Button 2
    st.markdown("""
<div class="guide-section" style="border-left:4px solid #00C2FF;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
<div style="background:linear-gradient(90deg,#00C2FF,#0099FF);padding:10px 16px;border-radius:10px;font-size:1.1rem;font-weight:800;color:white;">🗺️ Find Nearby Services</div>
<div style="color:#00C2FF;font-size:0.8rem;font-weight:700;">BLUE BUTTON</div>
</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>When to use:</strong> When you need to find any emergency service near you.</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>What you get:</strong></p>
<div class="guide-step">🏥 <strong>Trauma Centres</strong> — Hospitals with emergency departments, sorted by distance from you.</div>
<div class="guide-step">🚑 <strong>Ambulance Services</strong> — Nearest ambulance stations.</div>
<div class="guide-step">🚔 <strong>Police Stations</strong> — Nearest police stations.</div>
<div class="guide-step">🚛 <strong>Vehicle Rescue</strong> — Towing services if your vehicle is damaged.</div>
<div class="guide-step">🔧 <strong>Puncture/Repair Shops</strong> — Nearest tyre shops and garages.</div>
<div class="guide-step">🏪 <strong>Showrooms</strong> — Nearest vehicle showrooms.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">For each result, you see the <strong>name, distance in km, and phone number</strong>. You can tap <strong>📞 Call</strong> to call them directly, or tap <strong>🗺 Go</strong> to open Google Maps navigation to reach them.</p>
<div class="guide-tip">💡 Up to 15 results per category. All sorted from nearest to farthest.</div>
</div>
""", unsafe_allow_html=True)

    # Button 3
    st.markdown("""
<div class="guide-section" style="border-left:4px solid #FF1E1E;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
<div style="background:linear-gradient(90deg,#FF1E1E,#AA0000);padding:10px 16px;border-radius:10px;font-size:1.1rem;font-weight:800;color:white;">📞 Send SOS</div>
<div style="color:#FF6B6B;font-size:0.8rem;font-weight:700;">DARK RED BUTTON</div>
</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>When to use:</strong> When you want to immediately alert your family and friends that you are in danger.</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>What happens:</strong></p>
<div class="guide-step">📨 An <strong>automatic SMS</strong> is sent to all 3 of your saved emergency contacts.</div>
<div class="guide-step">📍 The message includes your <strong>exact location</strong> with a Google Maps link they can tap to find you.</div>
<div class="guide-step">🩸 The message also includes your <strong>blood group, allergies, and medical conditions</strong> so your family can inform the doctors.</div>
<div class="guide-step">📱 If there is no internet, the app shows <strong>manual SMS links</strong> — tap them to open your phone's SMS app with the message already written.</div>
<div class="guide-warning">⚠️ <strong>Important:</strong> Make sure you have saved at least one emergency contact. Without contacts, SOS cannot be sent.</div>
</div>
""", unsafe_allow_html=True)

    # Button 4
    st.markdown("""
<div class="guide-section" style="border-left:4px solid #8B5CF6;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
<div style="background:linear-gradient(90deg,#8B5CF6,#6D28D9);padding:10px 16px;border-radius:10px;font-size:1.1rem;font-weight:800;color:white;">⚡ What Should I Do Now?</div>
<div style="color:#A78BFA;font-size:0.8rem;font-weight:700;">PURPLE BUTTON</div>
</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>When to use:</strong> When you are confused and don't know what to do first after an accident.</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>What you get:</strong> A clear, numbered list of the most important things to do RIGHT NOW. For example:</p>
<div class="guide-step">1. Call the emergency number for your country (112 in India, 911 in USA, 999 in UK)</div>
<div class="guide-step">2. Stay on the line — tell them your exact location</div>
<div class="guide-step">3. Don't move injured people unless there is fire</div>
<div class="guide-step">4. Apply pressure on bleeding wounds with a cloth</div>
<div class="guide-step">5. Turn on hazard lights if in a vehicle</div>
<div class="guide-tip">💡 <strong>Works completely offline</strong> — no internet needed. Perfect for remote areas or highways.</div>
</div>
""", unsafe_allow_html=True)

    # Button 5
    st.markdown("""
<div class="guide-section" style="border-left:4px solid #F97316;">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
<div style="background:linear-gradient(90deg,#F97316,#EA580C);padding:10px 16px;border-radius:10px;font-size:1.1rem;font-weight:800;color:white;">🆘 ONE-TAP EMERGENCY</div>
<div style="color:#FB923C;font-size:0.8rem;font-weight:700;">ORANGE BUTTON — MOST POWERFUL</div>
</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>When to use:</strong> In the most serious emergency when you need everything done at once.</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>This single button does ALL of these at the same time:</strong></p>
<div class="guide-step">📞 <strong>Auto-dials ambulance</strong> on your phone immediately (108 in India)</div>
<div class="guide-step">🔴 Shows <strong>4 big call buttons</strong> — Ambulance, Emergency, Police, Fire — one tap to call any of them</div>
<div class="guide-step">👥 Shows <strong>Call, SMS, and WhatsApp buttons</strong> for each of your saved contacts</div>
<div class="guide-step">📨 <strong>Automatically sends SMS</strong> to all your contacts with your location, blood group, and medical info</div>
<div class="guide-step">🩺 Shows <strong>immediate first aid steps</strong> for the current situation</div>
<div class="guide-warning">🆘 <strong>This is the button to press if someone is seriously injured and you need help immediately.</strong></div>
</div>
""", unsafe_allow_html=True)

    # ── VOICE INPUT ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🎤 Voice Input — Speak Your Emergency</div>
<div class="section-sub">You don't have to type. Just speak!</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
Below the 5 buttons, you will see a microphone section. This is for when you are too scared or injured to type.
</p>
<div class="guide-step">🎤 <strong>Step 1:</strong> Tap the microphone/record button.</div>
<div class="guide-step">🗣️ <strong>Step 2:</strong> Speak clearly. Say things like: "Person unconscious heavy bleeding" or "Someone fell from bike broken leg" or "Car accident on highway".</div>
<div class="guide-step">✅ <strong>Step 3:</strong> The app listens, converts your speech to text, and automatically gives you first aid instructions.</div>
<div class="guide-step">🔊 <strong>Step 4:</strong> The app also <strong>reads the instructions aloud</strong> — like Siri or Google Assistant — so you can listen while helping the injured person.</div>
<div class="guide-tip">💡 You can also just <strong>type</strong> in the text box if you prefer. Both work the same way.</div>
<div class="guide-warning">⚠️ Voice input works best on Chrome browser. If it doesn't work, just type your situation in the text box.</div>
</div>
""", unsafe_allow_html=True)

    # ── AI FIRST AID ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🤖 AI First Aid Assistant</div>
<div class="section-sub">Smart guidance powered by artificial intelligence</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you describe your emergency (by voice or text), the app's AI brain analyses what you said and gives you the right first aid steps.
</p>
<div class="guide-feature">🔴 <strong>CRITICAL</strong> — Life-threatening situation. Example: "Person not breathing, heavy bleeding". App tells you to call 112 immediately and start CPR.</div>
<div class="guide-feature">🟠 <strong>SERIOUS</strong> — Urgent but not immediately life-threatening. Example: "Broken leg, moderate bleeding". App gives step-by-step treatment.</div>
<div class="guide-feature">🟡 <strong>MODERATE</strong> — Needs medical attention. Example: "Sprained ankle, small cut". App gives basic first aid.</div>
<div class="guide-feature">🟢 <strong>MINOR</strong> — Small injury. Example: "Bruise, minor scratch". App gives simple home care advice.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
The AI understands natural language — you don't need to use medical words. Just describe what you see in simple words.
</p>
<div class="guide-tip">💡 <strong>Works offline too!</strong> Even without internet, the app uses smart keyword detection to give you first aid guidance.</div>
</div>
""", unsafe_allow_html=True)

    # ── GOLDEN HOUR TIMER ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">⏱️ Golden Hour Timer</div>
<div class="section-sub">The most critical 60 minutes after an accident</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
Medical experts say that the first 60 minutes after a serious accident is called the <strong>"Golden Hour"</strong>.
If an injured person gets proper medical treatment within this time, their chances of survival are much higher.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you press the Accident button, a <strong>live countdown timer</strong> starts from 60:00 and counts down every second.
</p>
<div class="guide-step">🟢 <strong>0-50 minutes remaining:</strong> Timer shows in green — good amount of time left.</div>
<div class="guide-step">🟡 <strong>10 minutes remaining:</strong> Timer turns orange — hurry up, time is running out.</div>
<div class="guide-step">🔴 <strong>5 minutes remaining:</strong> Timer turns red and pulses — critical, get help immediately.</div>
<div class="guide-tip">💡 This timer is a reminder to keep moving fast. Every second counts in a real emergency.</div>
</div>
""", unsafe_allow_html=True)

    # ── EMERGENCY CHECKLIST ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📋 Emergency Action Checklist</div>
<div class="section-sub">Step-by-step guide you can tick off as you go</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When an accident happens, it's easy to forget what to do because of panic. The Emergency Checklist solves this problem.
It shows you a list of steps with checkboxes. As you complete each step, tick it off.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>There are 4 different checklists:</strong></p>
<div class="guide-step">🚨 <strong>Road Accident Checklist</strong> — General accident response: move to safety, call 112, check breathing, etc.</div>
<div class="guide-step">🩸 <strong>Bleeding Control Checklist</strong> — How to stop bleeding: press on wound, don't lift cloth, raise limb, etc.</div>
<div class="guide-step">😶 <strong>Unconscious Person Checklist</strong> — What to do if someone is not responding: check breathing, CPR steps, recovery position.</div>
<div class="guide-step">🔥 <strong>Vehicle Fire Checklist</strong> — What to do if a vehicle catches fire: exit immediately, move away, call fire brigade.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
Steps marked <strong style="color:#FF3B3B;">CRITICAL</strong> are the most important ones — do these first.
A progress bar at the top shows how many steps you have completed.
</p>
<div class="guide-tip">💡 The app automatically shows the right checklist based on what you described. If you said "bleeding", it shows the bleeding checklist.</div>
</div>
""", unsafe_allow_html=True)

    # ── CRASH DETECTION ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🛡️ Auto Crash Detection</div>
<div class="section-sub">The app detects accidents automatically — even if you can't press any button</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
This is one of the most powerful features. Your phone has a sensor called an <strong>accelerometer</strong> that measures movement.
When there is a sudden violent impact (like a crash), the app detects it automatically.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>Here is exactly what happens:</strong></p>
<div class="guide-step">💥 <strong>Crash detected:</strong> Your phone senses a sudden impact above a certain force level.</div>
<div class="guide-step">🚨 <strong>Alert appears:</strong> A big red screen appears saying "CRASH DETECTED" with a countdown timer.</div>
<div class="guide-step">⏱️ <strong>10-minute countdown starts:</strong> The app waits for 10 full minutes before doing anything. This is the safety window.</div>
<div class="guide-step">🔔 <strong>Alarm beeps every 30 seconds:</strong> Your phone makes a loud beeping sound every 30 seconds to alert you or anyone nearby.</div>
<div class="guide-step">✅ <strong>If you are okay:</strong> Tap the green "Cancel — False Alarm" button to stop everything. Nothing happens.</div>
<div class="guide-step">🆘 <strong>If you don't cancel:</strong> After 10 minutes, the app automatically sends SOS to your contacts and triggers the emergency flow — even if you are unconscious.</div>
<div class="guide-warning">⚠️ <strong>How to turn it on:</strong> Go to the left sidebar → Settings → turn on "🛡️ Auto Crash Detection". It is OFF by default for safety.</div>
<div class="guide-tip">💡 <strong>Why 10 minutes?</strong> Because sometimes the phone detects a false alarm (like dropping the phone). 10 minutes gives you enough time to cancel if you are okay, but if you are unconscious, help will still come.</div>
</div>
""", unsafe_allow_html=True)

    # ── GLOBAL EMERGENCY NUMBERS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🌍 Global Emergency Numbers</div>
<div class="section-sub">Works in 60+ countries automatically</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
Different countries have different emergency numbers. In India it's 112, in USA it's 911, in UK it's 999.
RoadSoS automatically detects which country you are in and shows the correct numbers.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>Examples:</strong></p>
<div class="guide-step">🇮🇳 <strong>India:</strong> Emergency 112 | Ambulance 108 | Police 100 | Fire 101 | Highway 1033</div>
<div class="guide-step">🇺🇸 <strong>USA:</strong> All services — 911</div>
<div class="guide-step">🇬🇧 <strong>UK:</strong> All services — 999</div>
<div class="guide-step">🇦🇪 <strong>UAE:</strong> Emergency 999 | Ambulance 998 | Police 999 | Fire 997</div>
<div class="guide-step">🇦🇺 <strong>Australia:</strong> All services — 000</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
The app detects your country from your location automatically. All call buttons in the sidebar update to show the correct numbers for your country.
</p>
<div class="guide-tip">💡 <strong>Travelling abroad?</strong> Just update your location and all numbers change automatically. No manual setting needed.</div>
</div>
""", unsafe_allow_html=True)

    # ── ACCIDENT REPORT ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📄 Accident Report Generator</div>
<div class="section-sub">Create an official report for insurance and police — in seconds</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
After an accident, you need to file a report with your insurance company and sometimes the police.
This usually takes hours of paperwork. RoadSoS generates a professional PDF report in seconds.
</p>
<div class="guide-step">📍 <strong>Auto-filled details:</strong> Your name, phone number, and location are already filled in from your saved profile. You don't need to type them again.</div>
<div class="guide-step">📅 <strong>Fill in accident details:</strong> Date, time, type of accident (collision, hit and run, etc.), road condition, weather.</div>
<div class="guide-step">🚗 <strong>Vehicle details:</strong> How many vehicles, vehicle numbers (like MH-01-AB-1234).</div>
<div class="guide-step">🏥 <strong>Injury details:</strong> How many people injured, what injuries, which hospital they went to.</div>
<div class="guide-step">📝 <strong>Description:</strong> Write what happened in your own words.</div>
<div class="guide-step">👁️ <strong>Witness details:</strong> If someone saw the accident, add their name and phone number.</div>
<div class="guide-step">⬇️ <strong>Download PDF:</strong> Click "Generate Report" and download a professional PDF document.</div>
<div class="guide-tip">💡 <strong>Submit this PDF</strong> to your insurance company or police station. It has all the information they need in a proper format.</div>
</div>
""", unsafe_allow_html=True)

    # ── OFFLINE MODE ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📴 Offline Mode — Works Without Internet</div>
<div class="section-sub">Many features work even in remote areas with no signal</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
Accidents often happen on highways or remote roads where there is no internet. RoadSoS is designed to work in these situations too.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>✅ Works WITHOUT internet:</strong></p>
<div class="guide-step">🩺 First aid instructions for all emergencies</div>
<div class="guide-step">📞 Emergency numbers for your country</div>
<div class="guide-step">📋 Emergency checklists (accident, bleeding, unconscious, fire)</div>
<div class="guide-step">⏱️ Golden hour timer</div>
<div class="guide-step">📄 Accident report PDF generation</div>
<div class="guide-step">💬 Manual SMS links (opens your phone's SMS app with message pre-written)</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;"><strong>❌ Needs internet:</strong></p>
<div class="guide-warning">🗺️ Finding nearby hospitals, police, ambulance on the map requires internet. But emergency numbers are always available offline.</div>
<div class="guide-tip">💡 <strong>Pro tip:</strong> Install the app on your phone's home screen (see "Install on Phone" section below). This makes it load faster even with slow internet.</div>
</div>
""", unsafe_allow_html=True)

    # ── INSTALL ON PHONE ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📱 Install on Your Phone — Like a Real App</div>
<div class="section-sub">Add RoadSoS to your home screen for instant access</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
RoadSoS can be installed on your phone's home screen so it opens like a regular app — no browser needed.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>On Android (Chrome browser):</strong></p>
<div class="guide-step">1. Open RoadSoS in Chrome browser</div>
<div class="guide-step">2. You will see a banner at the bottom saying "Install RoadSoS" — tap Install</div>
<div class="guide-step">3. OR tap the 3 dots menu (⋮) at the top right → "Add to Home Screen"</div>
<div class="guide-step">4. The RoadSoS icon appears on your home screen. Tap it to open instantly.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;"><strong>On iPhone (Safari browser):</strong></p>
<div class="guide-step">1. Open RoadSoS in Safari browser</div>
<div class="guide-step">2. Tap the Share button (the box with an arrow pointing up)</div>
<div class="guide-step">3. Scroll down and tap "Add to Home Screen"</div>
<div class="guide-step">4. Tap "Add" — the icon appears on your home screen</div>
<div class="guide-tip">💡 <strong>Why install it?</strong> In an emergency, you don't have time to open a browser and type a URL. With the icon on your home screen, you can open RoadSoS in ONE tap.</div>
<div class="guide-tip">💡 <strong>Long press the icon</strong> on Android to see quick shortcuts: "ONE-TAP EMERGENCY" and "Find Nearby Services" — even faster access.</div>
</div>
""", unsafe_allow_html=True)

    # ── LANGUAGE ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🌐 Language Settings</div>
<div class="section-sub">Use RoadSoS in your preferred language</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
RoadSoS supports 4 languages. You can switch languages at any time from the sidebar.
</p>
<div class="guide-step">🇬🇧 <strong>English</strong> — Default language</div>
<div class="guide-step">🇮🇳 <strong>हिंदी (Hindi)</strong> — All buttons and text in Hindi</div>
<div class="guide-step">🇮🇳 <strong>తెలుగు (Telugu)</strong> — All buttons and text in Telugu</div>
<div class="guide-step">🇮🇳 <strong>தமிழ் (Tamil)</strong> — All buttons and text in Tamil</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
<strong>How to change:</strong> Open the left sidebar → scroll to Settings → select your language from the dropdown. The entire app changes instantly.
</p>
<div class="guide-tip">💡 Your language preference is saved. Next time you open the app, it will be in your chosen language.</div>
</div>
""", unsafe_allow_html=True)

    # ── SIDEBAR QUICK CALL ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📞 Quick Call Buttons (Left Sidebar)</div>
<div class="section-sub">One-tap calling for all emergency services</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
In the left sidebar, you will always see colored call buttons for emergency services. These update automatically based on your country.
</p>
<div class="guide-step">🚨 <strong>Emergency button (Red)</strong> — Calls the universal emergency number (112 in India). Use this first in any emergency.</div>
<div class="guide-step">🚑 <strong>Ambulance button (Pink-Red)</strong> — Calls the ambulance directly (108 in India).</div>
<div class="guide-step">🚔 <strong>Police button (Blue)</strong> — Calls the police (100 in India).</div>
<div class="guide-step">🚒 <strong>Fire button (Orange)</strong> — Calls the fire brigade (101 in India).</div>
<div class="guide-step">🛣️ <strong>Highway Help (Green)</strong> — Calls highway emergency services (1033 in India).</div>
<div class="guide-tip">💡 On mobile — tap any button to call directly. On computer — note the number and dial manually.</div>
</div>
""", unsafe_allow_html=True)

    # ── LOCATION DETECTION ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📍 Automatic Location Detection</div>
<div class="section-sub">The app finds where you are automatically</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
You don't need to type your location. RoadSoS detects it automatically in two ways:
</p>
<div class="guide-step">🛰️ <strong>GPS (on mobile):</strong> Your phone's GPS gives the most accurate location — exact street-level coordinates. The browser will ask "Allow location?" — tap Allow.</div>
<div class="guide-step">🌐 <strong>IP Address (on computer):</strong> If GPS is not available, the app uses your internet connection to detect your city. Less precise but still useful.</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
Your location is used to:
</p>
<div class="guide-step">🗺️ Find nearby hospitals, ambulances, police stations</div>
<div class="guide-step">📞 Show correct emergency numbers for your country</div>
<div class="guide-step">📨 Include your location in SOS messages to your contacts</div>
<div class="guide-tip">💡 You can also manually type your location in the sidebar if auto-detection doesn't work. Just type your city name like "Hyderabad" or "Chennai".</div>
</div>
""", unsafe_allow_html=True)

    # ── MEDICAL INFO IN SOS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🩺 Medical Information in SOS Messages</div>
<div class="section-sub">Why saving your medical details can save your life</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When an SOS is sent, it doesn't just say "help me". It sends a complete medical profile so doctors and family know exactly how to help you.
</p>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;"><strong>A typical SOS message looks like this:</strong></p>
<div style="background:#0B1120;border:1px solid #1E2A47;border-radius:10px;padding:16px;margin:12px 0;font-family:monospace;font-size:0.85rem;color:#94A3B8;line-height:1.8;">
🚨 EMERGENCY ALERT 🚨<br>
Rahul Sharma needs immediate help!<br>
📍 Location: 17.385044, 78.486671<br>
🗺️ Live Map: https://maps.google.com/?q=17.38,78.48<br>
🩸 Medical: Blood: B+. Allergies: Penicillin. Conditions: Diabetic.<br>
Please call immediately or send help!<br>
- Sent via RoadSoS
</div>
<div class="guide-tip">💡 <strong>The Google Maps link</strong> in the message lets your family tap it and navigate directly to where you are.</div>
<div class="guide-warning">⚠️ <strong>Important:</strong> Fill in your blood group and medical conditions in the sidebar. This information can be life-saving for doctors treating you.</div>
</div>
""", unsafe_allow_html=True)

    # ── WHATSAPP SOS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📲 WhatsApp SOS</div>
<div class="section-sub">Alert your contacts on WhatsApp too</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you press ONE-TAP EMERGENCY, you get three options for each saved contact:
</p>
<div class="guide-step">📞 <strong>Call Now</strong> — Directly calls that person's phone number.</div>
<div class="guide-step">💬 <strong>SMS SOS</strong> — Opens your phone's SMS app with the emergency message already written. Just tap Send.</div>
<div class="guide-step">📲 <strong>WhatsApp</strong> — Opens WhatsApp with the emergency message pre-written to that contact. Just tap Send.</div>
<div class="guide-tip">💡 Use WhatsApp if the person doesn't pick up calls — they will see the message notification immediately.</div>
</div>
""", unsafe_allow_html=True)

    # ── SEVERITY CLASSIFIER ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🎯 Severity Classifier</div>
<div class="section-sub">The app tells you how serious the situation is</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you describe an emergency, the app immediately shows a coloured badge telling you how serious it is.
This helps you understand how urgently you need to act.
</p>
<div style="background:rgba(255,59,59,0.1);border:1px solid #FF3B3B;border-radius:10px;padding:14px;margin:8px 0;">
🔴 <strong style="color:#FF3B3B;">CRITICAL</strong> — Life is in immediate danger. Call 112 RIGHT NOW. Do not wait even one second.<br>
<span style="color:#94A3B8;font-size:0.85rem;">Examples: Person not breathing, severe bleeding that won't stop, unconscious person.</span>
</div>
<div style="background:rgba(249,115,22,0.1);border:1px solid #F97316;border-radius:10px;padding:14px;margin:8px 0;">
🟠 <strong style="color:#F97316;">SERIOUS</strong> — Urgent medical attention needed within 30 minutes.<br>
<span style="color:#94A3B8;font-size:0.85rem;">Examples: Broken bone, moderate bleeding, head injury.</span>
</div>
<div style="background:rgba(234,179,8,0.1);border:1px solid #EAB308;border-radius:10px;padding:14px;margin:8px 0;">
🟡 <strong style="color:#EAB308;">MODERATE</strong> — Needs medical attention but not immediately life-threatening.<br>
<span style="color:#94A3B8;font-size:0.85rem;">Examples: Sprained ankle, small wound, bruise.</span>
</div>
<div style="background:rgba(34,197,94,0.1);border:1px solid #22C55E;border-radius:10px;padding:14px;margin:8px 0;">
🟢 <strong style="color:#22C55E;">MINOR</strong> — Small injury, basic first aid is enough.<br>
<span style="color:#94A3B8;font-size:0.85rem;">Examples: Small cut, minor scratch, mild pain.</span>
</div>
</div>
""", unsafe_allow_html=True)

    # ── INTERACTIVE MAP ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🗺️ Interactive Map</div>
<div class="section-sub">See all emergency services on a visual map</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
When you search for nearby services, a map appears showing all results as coloured dots.
</p>
<div class="guide-step">🔵 <strong>Blue dot</strong> — Your current location (you are here)</div>
<div class="guide-step">🔴 <strong>Red dots</strong> — Hospitals and ambulance services</div>
<div class="guide-step">🔵 <strong>Cyan dots</strong> — Police stations</div>
<div class="guide-step">🟠 <strong>Orange dots</strong> — Towing and repair services</div>
<div class="guide-step">🟢 <strong>Green dots</strong> — Showrooms</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;margin-top:12px;">
<strong>Tap any dot</strong> on the map to see the name, distance, phone number, and a "Get Directions" link.
</p>
<div class="guide-step">📍 <strong>Share My Location button</strong> — Tap this on the map to copy a link to your exact location. Share it with anyone so they can find you.</div>
<div class="guide-tip">💡 The combined map shows ALL service types together so you can see everything at once.</div>
</div>
""", unsafe_allow_html=True)

    # ── TTS ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">🔊 Text-to-Speech — The App Speaks to You</div>
<div class="section-sub">Like Siri or Google Assistant, but for emergencies</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
After the app gives you first aid instructions, it also <strong>reads them out loud</strong> automatically.
This means you can listen to the steps while keeping your eyes on the injured person — no need to keep looking at the screen.
</p>
<div class="guide-tip">💡 Works on Chrome, Edge, and Safari. The voice speaks clearly in Indian English accent.</div>
<div class="guide-tip">💡 If you want to stop the voice, just refresh the page or start a new search.</div>
</div>
""", unsafe_allow_html=True)

    # ── NETWORK MODE ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📶 Network Mode Settings</div>
<div class="section-sub">Control how the app behaves with slow or no internet</div>
<p style="color:#E2E8F0;font-size:0.95rem;line-height:1.8;">
In the sidebar under Settings, you will see a toggle called <strong>"Low Network Mode"</strong>.
</p>
<div class="guide-step">📶 <strong>Low Network Mode OFF (default):</strong> App tries to fetch live data — nearby services, maps, etc. Best when you have good internet.</div>
<div class="guide-step">📴 <strong>Low Network Mode ON:</strong> App skips live data and only shows offline features — emergency numbers, first aid, checklists. Best on highways or remote areas with weak signal.</div>
<div class="guide-step">🔄 <strong>Recheck Network button:</strong> If your internet comes back, tap this to reconnect and enable live features again.</div>
</div>
""", unsafe_allow_html=True)

    # ── FAQ ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">❓ Frequently Asked Questions</div>
<div class="section-sub">Common questions answered simply</div>
""", unsafe_allow_html=True)

    faqs = [
        ("Is RoadSoS free?", "Yes, completely free. No subscription, no hidden charges."),
        ("Do I need to create an account?", "No account needed. Just fill your details in the sidebar once and you are ready."),
        ("Does it work without internet?", "Yes! First aid, emergency numbers, checklists, and the accident report all work offline. Only the live map needs internet."),
        ("What if my location is wrong?", "You can manually type your city name in the location field in the sidebar. Tap Save Details after changing it."),
        ("Will my details be shared with anyone?", "No. Your details are stored only on your device. They are only sent when YOU press the SOS button."),
        ("What if I accidentally press SOS?", "If you pressed SOS by mistake, immediately call your contacts and tell them it was a false alarm."),
        ("What if the auto crash detection fires by mistake?", "You have 10 full minutes to tap the green Cancel button. If you tap it, nothing happens. The alarm is just to alert you."),
        ("Can I use this outside India?", "Yes! The app works in 60+ countries and automatically shows the correct emergency numbers for your location."),
        ("What languages does it support?", "English, Hindi, Telugu, and Tamil. More languages can be added in future."),
        ("Can I share this app with my family?", "Yes! Share the link with everyone. The more people who have it, the safer everyone is."),
    ]

    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f"<p style='color:#E2E8F0;font-size:0.95rem;line-height:1.7;'>{a}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── EMERGENCY NUMBERS REFERENCE ──
    st.markdown("---")
    st.markdown("""
<div class="guide-section">
<div class="section-title">📞 Emergency Numbers Quick Reference</div>
<div class="section-sub">Save these numbers in your memory</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div style="background:#0B1120;border-radius:12px;padding:16px;">
<div style="font-weight:700;color:#E2E8F0;margin-bottom:12px;">🇮🇳 India</div>
<div style="color:#FF3B3B;font-size:1.1rem;font-weight:700;">112 — Universal Emergency</div>
<div style="color:#94A3B8;font-size:0.85rem;margin-bottom:8px;">Works even without SIM balance</div>
<div style="color:#FF6B6B;font-weight:600;">108 — Ambulance</div>
<div style="color:#00C2FF;font-weight:600;">100 — Police</div>
<div style="color:#F97316;font-weight:600;">101 — Fire Brigade</div>
<div style="color:#22C55E;font-weight:600;">1033 — Highway Help</div>
<div style="color:#A78BFA;font-weight:600;">1091 — Women Helpline</div>
</div>
""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
<div style="background:#0B1120;border-radius:12px;padding:16px;">
<div style="font-weight:700;color:#E2E8F0;margin-bottom:12px;">🌍 International</div>
<div style="color:#FF3B3B;font-size:1.1rem;font-weight:700;">112 — Works in most countries</div>
<div style="color:#94A3B8;font-size:0.85rem;margin-bottom:8px;">Even without a SIM card</div>
<div style="color:#FF6B6B;font-weight:600;">911 — USA, Canada, Mexico</div>
<div style="color:#00C2FF;font-weight:600;">999 — UK, Bangladesh</div>
<div style="color:#F97316;font-weight:600;">000 — Australia</div>
<div style="color:#22C55E;font-weight:600;">111 — New Zealand</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("---")
    st.markdown("""
<div style="text-align:center;padding:24px;background:#11182B;border-radius:16px;border:1px solid #1E2A47;">
<div style="font-size:1.5rem;margin-bottom:8px;">🚨</div>
<div style="font-size:1rem;font-weight:700;color:#E2E8F0;margin-bottom:6px;">RoadSoS — Your Safety, Our Priority</div>
<div style="font-size:0.85rem;color:#64748B;line-height:1.7;">
Built for the National Road Safety Hackathon 2026 · IIT Madras<br>
Always call <strong style="color:#FF3B3B;">112</strong> first in any emergency.<br>
This app is a support tool — it does not replace professional emergency services.
</div>
</div>
""", unsafe_allow_html=True)
