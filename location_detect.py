import streamlit as st
import streamlit.components.v1 as components
import requests


def get_location_from_ip() -> str:
    """Get approximate location from IP address. Works on PC without GPS."""
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5)
        data = res.json()
        city    = data.get("city", "")
        region  = data.get("region", "")
        country = data.get("country_name", "")
        lat     = data.get("latitude")
        lon     = data.get("longitude")
        if lat and lon:
            return f"{lat},{lon}"
        if city:
            return f"{city}, {region}, {country}".strip(", ")
    except Exception:
        pass
    return ""


def render_auto_location():
    """
    Tries GPS first (mobile/HTTPS), falls back silently.
    Saves coords to URL param on success.
    """
    components.html("""
    <script>
    (function(){
        var statusEl = document.getElementById('loc-status');
        if(!navigator.geolocation){
            if(statusEl) statusEl.innerText = '📍 Using IP location';
            return;
        }
        navigator.geolocation.getCurrentPosition(
            function(pos){
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                var coords = lat + ',' + lon;
                var url = new URL(window.parent.location.href);
                if(url.searchParams.get('geo_coords') !== coords){
                    url.searchParams.set('geo_coords', coords);
                    window.parent.location.href = url.toString();
                } else {
                    if(statusEl){
                        statusEl.innerText = '✅ GPS: ' + lat + ', ' + lon;
                        statusEl.style.color = '#22C55E';
                    }
                }
            },
            function(err){ /* silent fail — IP location used as fallback */ },
            { timeout: 6000, maximumAge: 60000, enableHighAccuracy: true }
        );
    })();
    </script>
    <div id="loc-status"
         style="font-family:sans-serif;font-size:12px;color:#64748B;padding:4px 0;">
        📡 Detecting GPS location...
    </div>
    """, height=28)


def get_coords_from_url() -> str | None:
    coords = st.query_params.get("geo_coords")
    return coords if coords else None
