"""
Emergency Action Checklist
Interactive step-by-step checklist for road accident response.
Uses Streamlit session state to track completed steps.
"""
import streamlit as st


CHECKLISTS = {
    "accident": {
        "title": "🚨 Road Accident Response Checklist",
        "color": "#FF3B3B",
        "steps": [
            {"id": "safe",     "text": "Move yourself to safety away from traffic",          "critical": True},
            {"id": "call112",  "text": "Call 112 — give your exact location",                "critical": True},
            {"id": "hazard",   "text": "Switch on hazard lights / warn other drivers",       "critical": False},
            {"id": "nomove",   "text": "Do NOT move injured people (unless fire danger)",    "critical": True},
            {"id": "breathe",  "text": "Check if injured person is breathing",               "critical": True},
            {"id": "bleed",    "text": "Apply pressure on any bleeding wounds",              "critical": False},
            {"id": "warm",     "text": "Keep injured person warm and calm",                  "critical": False},
            {"id": "sos",      "text": "Send SOS to emergency contacts",                     "critical": False},
            {"id": "wait",     "text": "Stay with injured until help arrives",               "critical": False},
        ]
    },
    "bleeding": {
        "title": "🩸 Bleeding Control Checklist",
        "color": "#FF3B3B",
        "steps": [
            {"id": "call",     "text": "Call 112 if bleeding is severe",                    "critical": True},
            {"id": "gloves",   "text": "Use gloves or plastic bag if available",            "critical": False},
            {"id": "press",    "text": "Press HARD on wound with clean cloth",              "critical": True},
            {"id": "nolift",   "text": "Do NOT lift cloth — add more on top if soaked",    "critical": True},
            {"id": "raise",    "text": "Raise injured limb above heart level if possible", "critical": False},
            {"id": "tourni",   "text": "Tie tight band above wound if limb is bleeding",   "critical": False},
            {"id": "still",    "text": "Keep person lying down and still",                  "critical": False},
        ]
    },
    "unconscious": {
        "title": "😶 Unconscious Person Checklist",
        "color": "#8B5CF6",
        "steps": [
            {"id": "call",     "text": "Call 112 immediately",                              "critical": True},
            {"id": "tap",      "text": "Tap shoulder and shout — check for response",      "critical": True},
            {"id": "airway",   "text": "Tilt head back, lift chin — open airway",          "critical": True},
            {"id": "breathe",  "text": "Check breathing for 10 seconds",                   "critical": True},
            {"id": "cpr",      "text": "If not breathing: start CPR (30 compressions)",    "critical": True},
            {"id": "recovery", "text": "If breathing: place in recovery position",         "critical": False},
            {"id": "monitor",  "text": "Monitor breathing until help arrives",              "critical": False},
        ]
    },
    "fire": {
        "title": "🔥 Vehicle Fire Checklist",
        "color": "#F97316",
        "steps": [
            {"id": "stop",     "text": "Stop vehicle immediately, turn off engine",        "critical": True},
            {"id": "exit",     "text": "Exit vehicle quickly — leave belongings",          "critical": True},
            {"id": "distance", "text": "Move 100+ meters away from vehicle",               "critical": True},
            {"id": "call",     "text": "Call 101 (Fire) and 112 (Emergency)",              "critical": True},
            {"id": "warn",     "text": "Warn other drivers to stay back",                  "critical": False},
            {"id": "nowater",  "text": "Do NOT use water on fuel/electrical fire",         "critical": True},
        ]
    }
}


def render_checklist(checklist_type: str = "accident"):
    """Render an interactive emergency checklist."""
    checklist = CHECKLISTS.get(checklist_type, CHECKLISTS["accident"])
    key_prefix = f"checklist_{checklist_type}"

    # Initialize session state for this checklist
    for step in checklist["steps"]:
        key = f"{key_prefix}_{step['id']}"
        if key not in st.session_state:
            st.session_state[key] = False

    # Count completed steps
    completed = sum(
        1 for step in checklist["steps"]
        if st.session_state.get(f"{key_prefix}_{step['id']}", False)
    )
    total = len(checklist["steps"])
    pct = int((completed / total) * 100) if total > 0 else 0

    color = checklist["color"]

    st.markdown(f"""
<div style="
    background:rgba(0,0,0,0.2);border:1px solid {color}44;
    border-radius:14px;padding:16px;margin:8px 0;
">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <div style="font-weight:700;font-size:0.95rem;color:#E2E8F0;">
            {checklist['title']}
        </div>
        <div style="
            font-size:0.8rem;font-weight:700;
            color:{color};background:{color}22;
            padding:4px 10px;border-radius:20px;
        ">{completed}/{total} done</div>
    </div>
    <div style="
        background:rgba(255,255,255,0.08);border-radius:6px;
        height:6px;margin-bottom:14px;overflow:hidden;
    ">
        <div style="
            height:100%;width:{pct}%;
            background:linear-gradient(90deg,{color},{color}aa);
            border-radius:6px;transition:width 0.3s ease;
        "></div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Render each step as a checkbox
    for step in checklist["steps"]:
        key = f"{key_prefix}_{step['id']}"
        done = st.session_state.get(key, False)

        col1, col2 = st.columns([0.08, 0.92])
        with col1:
            checked = st.checkbox("", value=done, key=key, label_visibility="collapsed")
        with col2:
            style = "text-decoration:line-through;color:#64748B;" if checked else "color:#E2E8F0;"
            critical_badge = " <span style='background:#FF3B3B22;color:#FF3B3B;font-size:0.65rem;padding:1px 6px;border-radius:4px;font-weight:700;'>CRITICAL</span>" if step["critical"] and not checked else ""
            st.markdown(
                f"<div style='{style}font-size:0.88rem;padding:4px 0;'>"
                f"{step['text']}{critical_badge}</div>",
                unsafe_allow_html=True
            )

    # Reset button
    if st.button("🔄 Reset Checklist", key=f"{key_prefix}_reset", use_container_width=False):
        for step in checklist["steps"]:
            st.session_state[f"{key_prefix}_{step['id']}"] = False
        st.rerun()

    if completed == total:
        st.success("✅ All steps completed! Help is on the way.")
