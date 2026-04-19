def get_response(user_input):
    text = user_input.lower().strip()

    severe = any(w in text for w in [
        "heavy", "severe", "lot of", "too much", "can't stop",
        "serious", "major", "extreme", "bad", "worse", "critical"
    ])

    has_bleeding    = any(w in text for w in ["bleeding", "blood", "cut", "wound"])
    has_unconscious = any(w in text for w in ["unconscious", "fainted", "not responding", "passed out", "unresponsive"])
    has_fracture    = any(w in text for w in ["fracture", "broken", "bone", "sprain", "twisted"])
    has_accident    = any(w in text for w in ["accident", "crash", "collision", "hit", "vehicle"])
    has_burn        = any(w in text for w in ["burn", "fire", "scalded", "burning", "flame"])
    has_choking     = any(w in text for w in ["chok", "choking", "can't breathe", "cannot breathe", "airway", "swallowed"])
    has_head        = any(w in text for w in ["head", "skull", "concussion", "head injury", "hit head", "brain"])
    has_shock       = any(w in text for w in ["shock", "pale", "shaking", "trembling", "cold sweat", "dizzy", "faint"])
    has_services    = any(w in text for w in ["hospital", "ambulance", "doctor", "medical", "help"])

    if has_unconscious:
        if severe or has_bleeding:
            return {"type": "critical", "title": "😶 CRITICAL: Unconscious + Possible Bleeding",
                "steps": ["Call 112 NOW — stay on the line.",
                    "Check breathing — look, listen, feel for 10 seconds.",
                    "If NOT breathing: start CPR (30 compressions, 2 breaths).",
                    "If bleeding: press firmly on wound without moving the person.",
                    "Do NOT give water or food. Keep them still."],
                "tip": "Keep doing CPR until paramedics arrive — do not stop."}
        return {"type": "first_aid", "title": "😶 First Aid: Unconscious Person",
            "steps": ["Tap shoulder and shout — check for response.", "Call 112 immediately.",
                "If breathing: place on their side (recovery position).",
                "If NOT breathing: start CPR — 30 compressions, 2 breaths.",
                "Stay with them until help arrives."],
            "tip": "If unsure whether they're breathing, start CPR — it's better to act."}

    elif has_choking:
        if severe:
            return {"type": "critical", "title": "🫁 CRITICAL: Severe Choking",
                "steps": ["Call 112 immediately.",
                    "Stand behind the person, wrap arms around their waist.",
                    "Give 5 firm back blows between shoulder blades.",
                    "Then give 5 abdominal thrusts (Heimlich maneuver).",
                    "Repeat until object comes out or person loses consciousness.",
                    "If unconscious: start CPR immediately."],
                "tip": "Do NOT leave the person alone — keep alternating back blows and thrusts."}
        return {"type": "first_aid", "title": "🫁 First Aid: Choking",
            "steps": ["Ask: 'Are you choking?' — if they can speak, encourage coughing.",
                "If they cannot speak or breathe: give 5 firm back blows.",
                "Then give 5 abdominal thrusts (push inward and upward).",
                "Repeat until object is dislodged.",
                "Call 112 if it doesn't clear quickly."],
            "tip": "Never do blind finger sweeps in the mouth — it can push the object deeper."}

    elif has_head:
        if severe:
            return {"type": "critical", "title": "🧠 CRITICAL: Severe Head Injury",
                "steps": ["Call 112 immediately — do NOT move the person.",
                    "Keep head and neck completely still — suspect spine injury.",
                    "If bleeding from head: apply gentle pressure without pressing on skull.",
                    "Watch for: vomiting, seizures, unequal pupils — report to 112.",
                    "Do NOT give food, water, or any medication."],
                "tip": "Any head injury with unconsciousness is a medical emergency — do not delay."}
        return {"type": "first_aid", "title": "🧠 First Aid: Head Injury",
            "steps": ["Keep the person still and calm.",
                "Apply gentle pressure on any bleeding wound.",
                "Do NOT remove any object stuck in the head.",
                "Watch for confusion, vomiting, or unequal pupils.",
                "Call 112 or take to hospital immediately."],
            "tip": "Even a 'minor' head injury can worsen — always get medical evaluation."}

    elif has_bleeding:
        if severe:
            return {"type": "critical", "title": "🩸 SEVERE BLEEDING — Act Now",
                "steps": ["Call 112 immediately.",
                    "Press HARD with both hands using any cloth available.",
                    "Do NOT lift the cloth — keep pressing non-stop.",
                    "If a limb: tie a tight band above the wound.",
                    "Keep person lying down and still."],
                "tip": "If bleeding doesn't slow in 5 minutes, call 112 again and keep pressing."}
        return {"type": "first_aid", "title": "🩸 First Aid: Bleeding",
            "steps": ["Press firmly on wound with a clean cloth.",
                "Do NOT lift cloth — add more on top if soaked.",
                "Raise injured part above heart level if possible.",
                "Never pull out any stuck object.",
                "Call 112 if bleeding is heavy or won't stop."],
            "tip": "If unsure how serious it is, call 112 — better safe than sorry."}

    elif has_burn:
        if severe:
            return {"type": "critical", "title": "🔥 SEVERE BURN — Emergency",
                "steps": ["Call 112 immediately.",
                    "Cool the burn with cool (not cold/ice) running water for 20 minutes.",
                    "Do NOT use ice, butter, toothpaste, or any cream.",
                    "Remove clothing/jewelry near burn — unless stuck to skin.",
                    "Cover loosely with a clean non-fluffy cloth.",
                    "Keep person warm to prevent shock."],
                "tip": "Never burst blisters — it increases infection risk."}
        return {"type": "first_aid", "title": "🔥 First Aid: Burns",
            "steps": ["Cool the burn under cool running water for at least 10 minutes.",
                "Do NOT use ice, butter, or toothpaste.",
                "Remove rings/watches near the burn area.",
                "Cover with a clean, loose bandage or cloth.",
                "Seek medical help if burn is larger than palm size."],
            "tip": "Cool water is the only correct first treatment for burns."}

    elif has_shock:
        if severe:
            return {"type": "critical", "title": "⚡ CRITICAL: Shock",
                "steps": ["Call 112 immediately.",
                    "Lay person flat — raise legs 30cm unless head/spine injury.",
                    "Keep them warm with a blanket.", "Do NOT give food or water.",
                    "Loosen tight clothing around neck and chest.",
                    "Monitor breathing — start CPR if they stop breathing."],
                "tip": "Shock is life-threatening — do not leave the person alone."}
        return {"type": "first_aid", "title": "⚡ First Aid: Shock",
            "steps": ["Lay the person down and raise their legs slightly.",
                "Keep them warm and calm.", "Do NOT give food, water, or medication.",
                "Loosen any tight clothing.", "Call 112 and monitor their condition."],
            "tip": "Reassure the person — anxiety makes shock worse."}

    elif has_fracture:
        if severe:
            return {"type": "critical", "title": "🦴 SEVERE FRACTURE — Do Not Move",
                "steps": ["Call 112 — do not attempt to move the person.",
                    "If neck/spine suspected: keep completely still.",
                    "Support limb gently without straightening.",
                    "Cover with cloth/blanket to prevent shock.", "Wait for medical help."],
                "tip": "When in doubt, don't move them — wait for paramedics."}
        return {"type": "first_aid", "title": "🦴 First Aid: Fracture",
            "steps": ["Do NOT move or straighten the injured limb.",
                "Support it gently as found.",
                "Apply ice wrapped in cloth to reduce swelling.",
                "Keep person still and calm.", "Go to hospital or call 112."],
            "tip": "If unsure if it's broken, treat it as a fracture — don't risk it."}

    elif has_accident:
        if severe:
            return {"type": "critical", "title": "🚨 MAJOR ACCIDENT — Emergency Response",
                "steps": ["Call 112 NOW — report exact location.",
                    "Do NOT move anyone with possible spine injuries.",
                    "If fire: move people away immediately.",
                    "Block traffic and switch on hazard lights.",
                    "Stay on the line with emergency services."],
                "tip": "If unsure about injuries, don't move anyone — wait for paramedics."}
        return {"type": "emergency", "title": "🚨 Road Accident Response",
            "steps": ["Move yourself to safety away from traffic.",
                "Call 112 — give your location.",
                "Don't move injured people unless there's fire.",
                "Switch on hazard lights.",
                "Stay with the injured until help arrives."],
            "tip": "If unsure what to do, call 112 and follow their instructions."}

    elif has_services:
        return {"type": "services", "title": "🏥 Emergency Numbers (Works Offline)",
            "steps": ["🚑 Ambulance: 108", "🚔 Police: 100", "🚒 Fire: 101",
                "🆘 Universal Emergency: 112",
                "🏥 Use 'Find Nearby Services' button for live results."],
            "tip": "112 works even without a SIM card or network balance."}

    else:
        return {"type": "unknown", "title": "🤔 Could Not Identify Emergency",
            "steps": ["Try describing with keywords like:",
                "→ 'bleeding' or 'heavy bleeding'",
                "→ 'unconscious' or 'not responding'",
                "→ 'fracture' or 'broken bone'",
                "→ 'burn' or 'fire'",
                "→ 'choking' or 'can't breathe'",
                "→ 'head injury' or 'concussion'",
                "→ 'shock' or 'pale and shaking'",
                "→ 'accident' or 'crash'",
                "Or use the quick action buttons above."],
            "tip": "For any emergency, call 112 immediately — don't wait."}
