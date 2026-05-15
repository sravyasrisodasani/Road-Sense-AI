"""
Crash Detection via Device Accelerometer
Uses browser's DeviceMotion API to detect sudden impact (crash).
When triggered, auto-fires the emergency flow.
Works on mobile browsers (Chrome/Safari on Android/iOS).
"""

import streamlit.components.v1 as components


def render_crash_detector():
    """
    Injects accelerometer-based crash detection.
    If sudden acceleration > threshold detected, redirects to ?action=emergency
    """
    components.html("""
    <script>
    (function(){
        var CRASH_THRESHOLD = 25;  // m/s² — typical crash impact
        var COOLDOWN_MS = 10000;   // 10 seconds between triggers
        var lastTrigger = 0;
        var active = false;

        function startDetection(){
            if(!window.DeviceMotionEvent){
                console.log('[RoadSoS] Accelerometer not supported');
                return;
            }

            // iOS 13+ requires permission
            if(typeof DeviceMotionEvent.requestPermission === 'function'){
                DeviceMotionEvent.requestPermission()
                    .then(function(state){
                        if(state === 'granted') listenForCrash();
                    })
                    .catch(console.error);
            } else {
                listenForCrash();
            }
        }

        function listenForCrash(){
            active = true;
            window.addEventListener('devicemotion', function(e){
                if(!active) return;
                var acc = e.accelerationIncludingGravity;
                if(!acc) return;

                var magnitude = Math.sqrt(
                    (acc.x||0)*(acc.x||0) +
                    (acc.y||0)*(acc.y||0) +
                    (acc.z||0)*(acc.z||0)
                );

                var now = Date.now();
                if(magnitude > CRASH_THRESHOLD && (now - lastTrigger) > COOLDOWN_MS){
                    lastTrigger = now;
                    console.log('[RoadSoS] CRASH DETECTED! Magnitude:', magnitude);

                    // Show alert
                    var banner = document.getElementById('crash-banner');
                    if(banner){
                        banner.style.display = 'flex';
                        // Auto-dismiss after 5 seconds if not cancelled
                        setTimeout(function(){
                            if(banner.style.display !== 'none'){
                                triggerEmergency();
                            }
                        }, 5000);
                    } else {
                        triggerEmergency();
                    }
                }
            });
            console.log('[RoadSoS] Crash detection active. Threshold:', CRASH_THRESHOLD, 'm/s²');
        }

        function triggerEmergency(){
            var url = new URL(window.parent.location.href);
            url.searchParams.set('action', 'emergency');
            window.parent.location.href = url.toString();
        }

        function cancelAlert(){
            var banner = document.getElementById('crash-banner');
            if(banner) banner.style.display = 'none';
        }

        // Expose globally
        window.startCrashDetection = startDetection;
        window.cancelCrashAlert = cancelAlert;

        // Auto-start on mobile
        if(/Mobi|Android|iPhone|iPad/i.test(navigator.userAgent)){
            startDetection();
        }
    })();
    </script>

    <!-- Crash Alert Banner -->
    <div id="crash-banner" style="
        display:none;position:fixed;top:0;left:0;right:0;z-index:99999;
        background:linear-gradient(90deg,#FF3B3B,#CC1111);
        color:white;padding:16px 20px;
        align-items:center;justify-content:space-between;
        font-family:sans-serif;box-shadow:0 4px 20px rgba(255,59,59,0.6);
    ">
        <div>
            <div style="font-weight:800;font-size:16px;">🚨 CRASH DETECTED!</div>
            <div style="font-size:13px;opacity:0.9;">Triggering emergency in 5 seconds... Tap Cancel if false alarm</div>
        </div>
        <button onclick="cancelCrashAlert()" style="
            background:rgba(255,255,255,0.2);color:white;border:1px solid rgba(255,255,255,0.4);
            padding:8px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px;
        ">✕ Cancel</button>
    </div>
    """, height=0)
