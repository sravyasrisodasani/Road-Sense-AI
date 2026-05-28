"""
Crash Detection via Device Accelerometer — Auto Crash Detection
Uses browser's DeviceMotion API to detect sudden impact (crash).
When triggered, shows a 10-minute safety countdown with audible alarm.
If countdown expires without user cancellation, auto-fires the emergency flow.
Works on mobile browsers (Chrome/Safari on Android/iOS).
"""

import streamlit as st
import streamlit.components.v1 as components
from storage import load_user_data, save_user_data
from browser_storage import save_to_browser


def render_crash_detector(
    enabled: bool = True,
    crash_threshold: float = 25.0,
    countdown_seconds: int = 600,
    alarm_interval_seconds: int = 30,
) -> None:
    """
    Injects accelerometer crash detection with 10-minute safety countdown.

    Parameters
    ----------
    enabled : bool
        If False, injects a no-op stub. Controlled by session_state.auto_crash_enabled.
    crash_threshold : float
        Acceleration magnitude in m/s² that triggers detection. Default 25.
    countdown_seconds : int
        Duration of the safety countdown before auto-triggering emergency. Default 600 (10 min).
    alarm_interval_seconds : int
        How often (in seconds) the alarm beeps during the countdown. Default 30.
    """
    if not enabled:
        # No-op stub — no listeners attached
        components.html("""
        <script>
        // [RoadSoS] Auto crash detection is disabled.
        window.startCrashDetection = function(){};
        window.stopCrashDetection  = function(){};
        window.cancelCountdown     = function(){};
        </script>
        """, height=0)
        return

    components.html(f"""
<style>
@keyframes crashPulse {{
    0%, 100% {{ box-shadow: 0 0 30px rgba(255,59,59,0.4); }}
    50%       {{ box-shadow: 0 0 60px rgba(255,59,59,0.9); }}
}}
#crash-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    z-index: 99999;
    background: rgba(10,0,0,0.92);
    color: white;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: sans-serif;
    text-align: center;
    padding: 24px;
}}
#crash-countdown-display {{
    font-size: 72px;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
    color: #FF3B3B;
    letter-spacing: 4px;
    margin-bottom: 8px;
    animation: crashPulse 1.5s ease-in-out infinite;
}}
#crash-cancel-btn {{
    background: #22C55E;
    color: white;
    border: none;
    padding: 18px 40px;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 0 24px rgba(34,197,94,0.5);
    transition: transform 0.1s;
}}
#crash-cancel-btn:active {{ transform: scale(0.96); }}
</style>

<!-- Crash Overlay -->
<div id="crash-overlay"
     role="alertdialog"
     aria-live="assertive"
     aria-label="Crash detected. Emergency countdown in progress.">

    <div style="font-size:48px;margin-bottom:8px;">🚨</div>
    <div style="font-size:22px;font-weight:900;color:#FF3B3B;margin-bottom:4px;">
        CRASH DETECTED
    </div>
    <div style="font-size:14px;color:#aaa;margin-bottom:24px;">
        Emergency will be triggered automatically if you don't respond
    </div>

    <div id="crash-countdown-display">10:00</div>

    <div style="font-size:13px;color:#888;margin-bottom:32px;">
        remaining before auto-trigger
    </div>

    <button id="crash-cancel-btn"
            ontouchstart="AlarmAudio.unlock()"
            onclick="window.cancelCountdown()">
        ✅ Cancel — False Alarm
    </button>

    <div style="font-size:11px;color:#555;margin-top:20px;">
        If you are injured and cannot respond, help is on the way.
    </div>
</div>

<script>
(function(){{
    // ── Constants (injected from Python) ──────────────────────────────────
    var CRASH_THRESHOLD  = {crash_threshold};
    var COUNTDOWN_SECONDS = {countdown_seconds};
    var ALARM_INTERVAL_S  = {alarm_interval_seconds};
    var COOLDOWN_MS       = 15000;

    // ── Helpers ───────────────────────────────────────────────────────────
    function pad2(n) {{ return n < 10 ? '0' + n : '' + n; }}

    function formatMMSS(seconds) {{
        var m = Math.floor(seconds / 60);
        var s = seconds % 60;
        return pad2(m) + ':' + pad2(s);
    }}

    function showOverlay(remaining) {{
        var overlay = window.parent.document.getElementById('crash-overlay');
        if (!overlay) {{
            // Overlay lives in the iframe — try local document
            overlay = document.getElementById('crash-overlay');
        }}
        if (overlay) {{
            overlay.style.display = 'flex';
            var disp = overlay.querySelector('#crash-countdown-display');
            if (disp) disp.textContent = formatMMSS(remaining);
        }}
    }}

    function hideOverlay() {{
        var overlay = window.parent.document.getElementById('crash-overlay');
        if (!overlay) overlay = document.getElementById('crash-overlay');
        if (overlay) overlay.style.display = 'none';
    }}

    function updateOverlayDisplay(remaining) {{
        var disp = window.parent.document.getElementById('crash-countdown-display');
        if (!disp) disp = document.getElementById('crash-countdown-display');
        if (disp) disp.textContent = formatMMSS(remaining);
    }}

    function triggerEmergency() {{
        sessionStorage.removeItem('roadsos_countdown_start');
        sessionStorage.removeItem('roadsos_countdown_duration');
        var url = new URL(window.parent.location.href);
        url.searchParams.set('action', 'emergency');
        url.searchParams.set('crash_auto', '1');
        window.parent.location.href = url.toString();
    }}

    // ── AlarmAudio Module ─────────────────────────────────────────────────
    var AlarmAudio = (function() {{
        var audioCtx = null;

        function getCtx() {{
            if (!audioCtx) {{
                var AC = window.AudioContext || window.webkitAudioContext;
                if (AC) audioCtx = new AC();
            }}
            return audioCtx;
        }}

        function beep() {{
            var ctx = getCtx();
            if (!ctx) return;
            // iOS: if suspended, skip silently — unlock() will resume on user gesture
            if (ctx.state === 'suspended') return;

            try {{
                var oscillator = ctx.createOscillator();
                var gainNode   = ctx.createGain();

                oscillator.type      = 'sine';
                oscillator.frequency.setValueAtTime(880, ctx.currentTime);

                // Gain envelope: attack 0.01s, sustain, release 0.1s, total 0.6s
                var now = ctx.currentTime;
                gainNode.gain.setValueAtTime(0, now);
                gainNode.gain.linearRampToValueAtTime(1.0, now + 0.01);
                gainNode.gain.setValueAtTime(1.0, now + 0.5);
                gainNode.gain.linearRampToValueAtTime(0, now + 0.6);

                oscillator.connect(gainNode);
                gainNode.connect(ctx.destination);

                oscillator.start(now);
                oscillator.stop(now + 0.6);
            }} catch(e) {{
                console.warn('[RoadSoS] AlarmAudio.beep error:', e);
            }}
        }}

        function stop() {{
            // Tones are self-terminating (oscillator.stop scheduled); nothing to do
        }}

        function unlock() {{
            var ctx = getCtx();
            if (ctx && ctx.state === 'suspended') {{
                ctx.resume().catch(function(e) {{
                    console.warn('[RoadSoS] AudioContext resume failed:', e);
                }});
            }}
        }}

        return {{ beep: beep, stop: stop, unlock: unlock }};
    }})();

    // Expose AlarmAudio globally so the overlay button can call unlock()
    window.AlarmAudio = AlarmAudio;

    // ── CountdownTimer Module ─────────────────────────────────────────────
    var CountdownTimer = (function() {{
        var intervalId  = null;
        var startTime   = null;
        var durationSec = null;
        var running     = false;

        function isRunning() {{ return running; }}

        function start(durationSeconds) {{
            if (running) return;  // Idempotent guard
            running     = true;
            durationSec = durationSeconds;
            startTime   = Date.now();

            // Persist to sessionStorage for resume-on-refresh
            sessionStorage.setItem('roadsos_countdown_start',    String(startTime));
            sessionStorage.setItem('roadsos_countdown_duration', String(durationSec));

            // Play first beep immediately
            AlarmAudio.beep();

            intervalId = setInterval(function() {{
                var elapsed   = Math.floor((Date.now() - startTime) / 1000);
                var remaining = durationSec - elapsed;

                if (remaining < 0) remaining = 0;

                updateOverlayDisplay(remaining);

                // Beep at every ALARM_INTERVAL_S mark (but not at 0 — handled below)
                if (remaining > 0 && remaining % ALARM_INTERVAL_S === 0) {{
                    AlarmAudio.beep();
                }}

                if (remaining <= 0) {{
                    clearInterval(intervalId);
                    intervalId = null;
                    running    = false;
                    AlarmAudio.stop();
                    console.log('[RoadSoS] Countdown expired — triggering emergency.');
                    triggerEmergency();
                }}
            }}, 1000);

            console.log('[RoadSoS] Countdown started:', durationSeconds, 'seconds');
        }}

        function cancel() {{
            if (intervalId) {{
                clearInterval(intervalId);
                intervalId = null;
            }}
            running = false;
            AlarmAudio.stop();
            hideOverlay();
            sessionStorage.removeItem('roadsos_countdown_start');
            sessionStorage.removeItem('roadsos_countdown_duration');
            console.log('[RoadSoS] Countdown cancelled by user.');
        }}

        return {{ start: start, cancel: cancel, isRunning: isRunning }};
    }})();

    // ── CrashDetector Module ──────────────────────────────────────────────
    var lastTrigger = 0;
    var active      = false;

    function listenForCrash() {{
        active = true;
        window.addEventListener('devicemotion', function(e) {{
            if (!active) return;
            var acc = e.accelerationIncludingGravity;
            if (!acc) return;

            var magnitude = Math.sqrt(
                (acc.x || 0) * (acc.x || 0) +
                (acc.y || 0) * (acc.y || 0) +
                (acc.z || 0) * (acc.z || 0)
            );

            var now = Date.now();
            if (magnitude > CRASH_THRESHOLD && (now - lastTrigger) > COOLDOWN_MS) {{
                lastTrigger = now;
                console.log('[RoadSoS] Crash detected. Magnitude:', magnitude);

                if (!CountdownTimer.isRunning()) {{
                    CountdownTimer.start(COUNTDOWN_SECONDS);
                    showOverlay(COUNTDOWN_SECONDS);
                }}
            }}
        }});
        console.log('[RoadSoS] Crash detection active. Threshold:', CRASH_THRESHOLD, 'm/s²');
    }}

    function startDetection() {{
        if (!window.DeviceMotionEvent) {{
            console.log('[RoadSoS] Accelerometer not supported');
            return;
        }}
        // iOS 13+ requires explicit permission
        if (typeof DeviceMotionEvent.requestPermission === 'function') {{
            DeviceMotionEvent.requestPermission()
                .then(function(state) {{
                    if (state === 'granted') listenForCrash();
                    else console.warn('[RoadSoS] DeviceMotion permission denied.');
                }})
                .catch(console.error);
        }} else {{
            listenForCrash();
        }}
    }}

    function stopDetection() {{
        active = false;
        CountdownTimer.cancel();
        console.log('[RoadSoS] Crash detection stopped.');
    }}

    // Expose globally
    window.startCrashDetection = startDetection;
    window.stopCrashDetection  = stopDetection;
    window.cancelCountdown     = function() {{ CountdownTimer.cancel(); }};

    // ── Resume-on-refresh logic ───────────────────────────────────────────
    (function resumeIfNeeded() {{
        var start = sessionStorage.getItem('roadsos_countdown_start');
        var dur   = sessionStorage.getItem('roadsos_countdown_duration');
        if (!start || !dur) return;

        var elapsed   = Math.floor((Date.now() - parseInt(start)) / 1000);
        var remaining = parseInt(dur) - elapsed;

        if (remaining > 0) {{
            console.log('[RoadSoS] Resuming countdown:', remaining, 'seconds remaining');
            CountdownTimer.start(remaining);
            showOverlay(remaining);
        }} else {{
            // Countdown expired while page was reloading — trigger immediately
            sessionStorage.removeItem('roadsos_countdown_start');
            sessionStorage.removeItem('roadsos_countdown_duration');
            triggerEmergency();
        }}
    }})();

    // ── Auto-start on mobile ──────────────────────────────────────────────
    if (/Mobi|Android|iPhone|iPad/i.test(navigator.userAgent)) {{
        startDetection();
    }}

}})();
</script>
""", height=0)


def render_crash_settings() -> None:
    """
    Renders the Auto Crash Detection settings UI in the sidebar.
    Reads/writes:
        st.session_state.auto_crash_enabled  (bool)
        st.session_state.crash_threshold     (float)
    Persists changes via save_user_data() and save_to_browser().
    """
    current_enabled = st.session_state.get("auto_crash_enabled", False)

    new_enabled = st.toggle(
        "🛡️ Auto Crash Detection",
        value=current_enabled,
        help=(
            "Detects crashes via accelerometer. "
            "If a crash is detected, a 10-minute countdown starts before alerting your contacts. "
            "You can cancel it if it's a false alarm."
        ),
    )

    if new_enabled:
        st.caption("Detects crashes automatically. 10-min countdown before alerting.")

    if new_enabled != current_enabled:
        st.session_state.auto_crash_enabled = new_enabled

        # Build full data dict for persistence
        data_to_save = {
            "location":           st.session_state.get("location", ""),
            "user_name":          st.session_state.get("user_name", ""),
            "user_phone":         st.session_state.get("user_phone", ""),
            "contact1":           st.session_state.get("contact1", ""),
            "contact2":           st.session_state.get("contact2", ""),
            "contact3":           st.session_state.get("contact3", ""),
            "blood_group":        st.session_state.get("blood_group", ""),
            "allergies":          st.session_state.get("allergies", ""),
            "medical_conditions": st.session_state.get("medical_conditions", ""),
            "lang":               st.session_state.get("lang", "en"),
            "auto_crash_enabled": new_enabled,
            "crash_threshold":    st.session_state.get("crash_threshold", 25.0),
        }
        save_user_data(data_to_save)
        save_to_browser(data_to_save)
        st.rerun()
