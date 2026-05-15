"""
Accident Severity Classifier
Classifies emergency situations into severity levels:
- CRITICAL (Red)   — Life-threatening, immediate intervention needed
- SERIOUS  (Orange) — Urgent, needs hospital within 30 min
- MODERATE (Yellow) — Needs medical attention, not immediately life-threatening
- MINOR    (Green)  — Minor injuries, can wait for medical care
"""
import streamlit as st
import streamlit.components.v1 as components


# Keyword-based severity scoring (works offline)
CRITICAL_KEYWORDS = [
    "unconscious", "not breathing", "no pulse", "cardiac arrest", "heart attack",
    "stroke", "unresponsive", "heavy bleeding", "severe bleeding", "can't stop bleeding",
    "choking", "can't breathe", "not responding", "passed out", "major accident",
    "multiple injured", "fire", "trapped", "head injury", "spine", "neck injury",
    "fainted", "seizure", "convulsion", "overdose", "drowning"
]

SERIOUS_KEYWORDS = [
    "bleeding", "fracture", "broken bone", "unconscious", "head", "chest pain",
    "difficulty breathing", "deep cut", "wound", "burn", "shock", "dizzy",
    "vomiting blood", "severe pain", "can't move", "paralyzed", "accident",
    "crash", "collision", "hit", "vehicle", "motorcycle", "truck"
]

MODERATE_KEYWORDS = [
    "sprain", "twisted", "bruise", "minor cut", "small wound", "pain",
    "swelling", "limping", "hurt", "injured", "fell", "fall", "bump"
]


def classify_severity(text: str) -> dict:
    """
    Classify the severity of an emergency from text description.
    Returns dict with level, color, label, action, score.
    """
    text_lower = text.lower()

    critical_score = sum(1 for kw in CRITICAL_KEYWORDS if kw in text_lower)
    serious_score  = sum(1 for kw in SERIOUS_KEYWORDS  if kw in text_lower)
    moderate_score = sum(1 for kw in MODERATE_KEYWORDS if kw in text_lower)

    # Check for severity modifiers
    severe_modifier = any(w in text_lower for w in [
        "severe", "heavy", "major", "serious", "critical", "extreme",
        "lot of", "too much", "can't stop", "very bad", "worse"
    ])

    if critical_score > 0 or (serious_score >= 2 and severe_modifier):
        return {
            "level": "CRITICAL",
            "color": "#FF3B3B",
            "bg": "rgba(255,59,59,0.1)",
            "border": "#FF3B3B",
            "icon": "🔴",
            "label": "CRITICAL — Life-Threatening",
            "action": "Call 112 IMMEDIATELY. Do not wait.",
            "eta": "Needs help within 10 minutes",
            "score": critical_score + serious_score
        }
    elif serious_score > 0 or (moderate_score >= 2 and severe_modifier):
        return {
            "level": "SERIOUS",
            "color": "#F97316",
            "bg": "rgba(249,115,22,0.1)",
            "border": "#F97316",
            "icon": "🟠",
            "label": "SERIOUS — Urgent Medical Attention",
            "action": "Call ambulance now. Keep patient still and calm.",
            "eta": "Needs hospital within 30 minutes",
            "score": serious_score
        }
    elif moderate_score > 0:
        return {
            "level": "MODERATE",
            "color": "#EAB308",
            "bg": "rgba(234,179,8,0.1)",
            "border": "#EAB308",
            "icon": "🟡",
            "label": "MODERATE — Medical Attention Needed",
            "action": "Visit nearest clinic or hospital. Monitor condition.",
            "eta": "Needs attention within 1-2 hours",
            "score": moderate_score
        }
    else:
        return {
            "level": "MINOR",
            "color": "#22C55E",
            "bg": "rgba(34,197,94,0.1)",
            "border": "#22C55E",
            "icon": "🟢",
            "label": "MINOR — Basic First Aid",
            "action": "Apply basic first aid. Monitor for worsening.",
            "eta": "Can wait for medical care if stable",
            "score": 0
        }


def render_severity_badge(severity: dict):
    """Render a visual severity badge."""
    st.markdown(f"""
<div style="
    background:{severity['bg']};
    border:1px solid {severity['border']};
    border-left:4px solid {severity['border']};
    border-radius:12px;padding:14px 18px;
    margin:8px 0;
">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
        <span style="font-size:1.4rem;">{severity['icon']}</span>
        <div>
            <div style="
                font-weight:800;font-size:0.95rem;
                color:{severity['color']};letter-spacing:0.5px;
            ">{severity['label']}</div>
            <div style="font-size:0.78rem;color:#94a3b8;margin-top:2px;">
                ⏱️ {severity['eta']}
            </div>
        </div>
    </div>
    <div style="
        font-size:0.85rem;color:#E2E8F0;
        background:rgba(0,0,0,0.2);border-radius:8px;
        padding:8px 12px;margin-top:4px;
    ">
        ⚡ <strong>Action:</strong> {severity['action']}
    </div>
</div>
""", unsafe_allow_html=True)
