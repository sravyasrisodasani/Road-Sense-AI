import streamlit as st
import streamlit.components.v1 as components

def render_geolocation_widget():
    components.html("""
        <script>
        function detectLocation() {
            const statusEl = document.getElementById("geo-status");
            if (!navigator.geolocation) {
                statusEl.innerText = "Geolocation not supported by your browser.";
                statusEl.style.color = "orange"; return;
            }
            statusEl.innerText = "Detecting your location...";
            statusEl.style.color = "#888";
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude.toFixed(6);
                    const lon = position.coords.longitude.toFixed(6);
                    const coords = lat + "," + lon;
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("geo_coords", coords);
                    window.parent.history.replaceState({}, "", url);
                    statusEl.innerText = "✅ Location detected: " + lat + ", " + lon;
                    statusEl.style.color = "green";
                    document.getElementById("geo-coords").value = coords;
                },
                function(error) {
                    const msgs = {1:"Permission denied. Enter manually.",
                                  2:"Location unavailable. Enter manually.",
                                  3:"Request timed out. Enter manually."};
                    statusEl.innerText = "⚠️ " + (msgs[error.code] || "Unknown error.");
                    statusEl.style.color = "orange";
                },
                { timeout: 8000, maximumAge: 60000 }
            );
        }
        window.onload = detectLocation;
        </script>
        <div style="font-family:sans-serif;font-size:13px;padding:4px 0;">
            <span id="geo-status" style="color:#888;">Requesting location...</span><br/>
            <input id="geo-coords" type="text" readonly
                style="margin-top:6px;width:100%;padding:4px;font-size:12px;
                       border:1px solid #ccc;border-radius:4px;background:#f9f9f9;"
                placeholder="Coordinates will appear here"/>
            <div style="margin-top:4px;color:#aaa;font-size:11px;">
                Copy coordinates into the location box above if auto-fill doesn't work.
            </div>
        </div>
    """, height=90)


def get_coords_from_url() -> str | None:
    params = st.query_params
    coords = params.get("geo_coords")
    return coords if coords else None
