"""
Golden Hour Timer
The "golden hour" is the critical 60-minute window after a road accident
when timely medical intervention can save lives.
Displays a live countdown timer when activated.
"""
import streamlit.components.v1 as components


def render_golden_hour_timer():
    """Renders a live golden hour countdown timer."""
    components.html("""
    <div id="golden-hour-container" style="
        background: linear-gradient(135deg, #1a0a0a, #2d0f0f);
        border: 1px solid #FF3B3B;
        border-radius: 14px;
        padding: 16px 20px;
        margin: 12px 0;
        position: relative;
        overflow: hidden;
    ">
        <!-- Animated border glow -->
        <div style="
            position:absolute;top:0;left:0;right:0;height:3px;
            background:linear-gradient(90deg,#FF3B3B,#F97316,#FF3B3B);
            background-size:200% 100%;
            animation:shimmer 2s infinite linear;
        "></div>

        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="
                    font-family:sans-serif;font-size:0.7rem;font-weight:700;
                    color:#FF3B3B;text-transform:uppercase;letter-spacing:2px;
                    margin-bottom:4px;
                ">⏱️ GOLDEN HOUR</div>
                <div style="
                    font-family:sans-serif;font-size:0.8rem;color:#94a3b8;
                ">Critical window for life-saving intervention</div>
            </div>
            <div style="text-align:center;">
                <div id="timer-display" style="
                    font-family:monospace;font-size:2.2rem;font-weight:800;
                    color:#FF3B3B;letter-spacing:3px;
                    text-shadow:0 0 20px rgba(255,59,59,0.6);
                ">60:00</div>
                <div id="timer-status" style="
                    font-family:sans-serif;font-size:0.72rem;
                    color:#22C55E;font-weight:600;
                ">● ACTIVE</div>
            </div>
        </div>

        <!-- Progress bar -->
        <div style="
            margin-top:12px;background:rgba(255,59,59,0.15);
            border-radius:6px;height:6px;overflow:hidden;
        ">
            <div id="timer-bar" style="
                height:100%;width:100%;
                background:linear-gradient(90deg,#FF3B3B,#F97316);
                border-radius:6px;
                transition:width 1s linear;
            "></div>
        </div>

        <div style="
            margin-top:8px;font-family:sans-serif;font-size:0.72rem;
            color:#64748B;text-align:center;
        ">
            Every second counts — emergency services have been alerted
        </div>
    </div>

    <style>
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    </style>

    <script>
    (function(){
        var totalSeconds = 3600; // 60 minutes
        var remaining = totalSeconds;
        var display = document.getElementById('timer-display');
        var bar = document.getElementById('timer-bar');
        var status = document.getElementById('timer-status');

        function update(){
            if(remaining <= 0){
                display.innerText = '00:00';
                display.style.color = '#64748B';
                status.innerText = '● EXPIRED';
                status.style.color = '#64748B';
                bar.style.width = '0%';
                return;
            }

            var mins = Math.floor(remaining / 60);
            var secs = remaining % 60;
            display.innerText =
                String(mins).padStart(2,'0') + ':' +
                String(secs).padStart(2,'0');

            var pct = (remaining / totalSeconds) * 100;
            bar.style.width = pct + '%';

            // Color changes as time runs out
            if(remaining <= 600){ // last 10 min
                display.style.color = '#F97316';
                display.style.textShadow = '0 0 20px rgba(249,115,22,0.6)';
                bar.style.background = 'linear-gradient(90deg,#F97316,#EF4444)';
            }
            if(remaining <= 300){ // last 5 min
                display.style.color = '#EF4444';
                display.style.animation = 'pulse-red 0.5s infinite alternate';
            }

            remaining--;
            setTimeout(update, 1000);
        }

        update();
    })();
    </script>
    """, height=160)
