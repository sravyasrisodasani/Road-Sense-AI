import streamlit.components.v1 as components
import json

# Color per service category
CATEGORY_COLORS = {
    "Hospitals":       "#e53935",
    "Ambulance":       "#e53935",
    "Police":          "#1e88e5",
    "Towing":          "#fb8c00",
    "Puncture/Repair": "#fb8c00",
    "Showrooms":       "#00897b",
}

CATEGORY_ICONS = {
    "Hospitals":       "🏥",
    "Ambulance":       "🚑",
    "Police":          "🚔",
    "Towing":          "🚛",
    "Puncture/Repair": "🔧",
    "Showrooms":       "🏪",
}


def render_map(user_lat: float, user_lon: float, places: list = None, color: str = "#e53935"):
    """Single-category map — used in per-tab service views."""
    places = places or []
    places_json = json.dumps(places)

    html = f"""
    <!DOCTYPE html><html>
    <head>
        <meta charset="utf-8"/>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body{{margin:0;padding:0;}}
            #map{{height:420px;width:100%;border-radius:10px;}}
            .share-btn{{position:absolute;bottom:16px;right:16px;z-index:1000;
                background:#e53935;color:white;border:none;padding:10px 16px;
                border-radius:8px;font-size:14px;cursor:pointer;font-weight:bold;
                box-shadow:0 2px 6px rgba(0,0,0,0.3);}}
            #share-output{{position:absolute;bottom:60px;right:16px;z-index:1000;
                background:white;padding:8px 12px;border-radius:8px;font-size:12px;
                max-width:260px;display:none;box-shadow:0 2px 6px rgba(0,0,0,0.2);
                word-break:break-all;}}
        </style>
    </head>
    <body>
    <div style="position:relative;">
        <div id="map"></div>
        <button class="share-btn" onclick="shareLocation()">📍 Share My Location</button>
        <div id="share-output"></div>
    </div>
    <script>
        const userLat={user_lat}, userLon={user_lon};
        const places={places_json}, dotColor="{color}";
        const map=L.map('map').setView([userLat,userLon],14);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{
            attribution:'© OpenStreetMap',maxZoom:19}}).addTo(map);
        const userIcon=L.divIcon({{className:'',
            html:`<div style="width:16px;height:16px;background:#1565C0;border-radius:50%;
                  border:3px solid white;box-shadow:0 0 0 4px rgba(21,101,192,0.3);"></div>`,
            iconSize:[16,16],iconAnchor:[8,8]}});
        L.marker([userLat,userLon],{{icon:userIcon}}).addTo(map)
         .bindPopup("<b>📍 You are here</b>").openPopup();
        const placeIcon=L.divIcon({{className:'',
            html:`<div style="width:14px;height:14px;background:${{dotColor}};border-radius:50%;
                  border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.4);"></div>`,
            iconSize:[14,14],iconAnchor:[7,7]}});
        places.forEach(function(p){{
            if(!p.lat||!p.lon)return;
            L.marker([p.lat,p.lon],{{icon:placeIcon}}).addTo(map)
             .bindPopup(`<b>${{p.name}}</b><br/>📏 ${{p.distance_km}} km<br/>
                📞 ${{p.phone}}<br/><a href="${{p.maps_link}}" target="_blank">🗺 OSM</a>`);
            L.polyline([[userLat,userLon],[p.lat,p.lon]],
                {{color:dotColor,weight:1.5,dashArray:'5,8',opacity:0.5}}).addTo(map);
        }});
        function shareLocation(){{
            const link=`https://www.openstreetmap.org/?mlat=${{userLat}}&mlon=${{userLon}}&zoom=16`;
            const out=document.getElementById('share-output');
            out.style.display='block';
            out.innerHTML=`<b>🔗 Share:</b><br/><a href="${{link}}" target="_blank">${{link}}</a>`;
            navigator.clipboard.writeText(link).catch(()=>{{}});
        }}
    </script></body></html>"""
    components.html(html, height=440)


def render_combined_map(user_lat: float, user_lon: float, all_places: dict):
    """
    Multi-category map — shows all service types together with color-coded pins.
    all_places: {"Hospitals": [...], "Police": [...], ...}
    """
    # Build a flat list with category info for JS
    combined = []
    for category, places in all_places.items():
        color = CATEGORY_COLORS.get(category, "#e53935")
        icon  = CATEGORY_ICONS.get(category, "📍")
        for p in places:
            if p.get("lat") and p.get("lon"):
                combined.append({
                    "name":        p["name"],
                    "lat":         p["lat"],
                    "lon":         p["lon"],
                    "distance_km": p["distance_km"],
                    "phone":       p.get("phone", ""),
                    "maps_link":   p.get("maps_link", ""),
                    "gmaps_link":  p.get("gmaps_link", ""),
                    "color":       color,
                    "icon":        icon,
                    "category":    category,
                })

    combined_json = json.dumps(combined)

    # Build legend HTML
    legend_items = ""
    for cat, color in CATEGORY_COLORS.items():
        icon = CATEGORY_ICONS.get(cat, "📍")
        legend_items += (
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
            f'<div style="width:12px;height:12px;background:{color};border-radius:50%;'
            f'border:2px solid white;flex-shrink:0;"></div>'
            f'<span style="font-size:12px;">{icon} {cat}</span></div>'
        )

    html = f"""
    <!DOCTYPE html><html>
    <head>
        <meta charset="utf-8"/>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body{{margin:0;padding:0;}}
            #map{{height:500px;width:100%;border-radius:12px;}}
            .legend{{position:absolute;top:12px;right:12px;z-index:1000;
                background:rgba(255,255,255,0.95);padding:10px 14px;
                border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.2);
                font-family:sans-serif;}}
            .legend-title{{font-weight:bold;font-size:13px;margin-bottom:6px;color:#333;}}
            .share-btn{{position:absolute;bottom:16px;right:16px;z-index:1000;
                background:#e53935;color:white;border:none;padding:10px 16px;
                border-radius:8px;font-size:13px;cursor:pointer;font-weight:bold;
                box-shadow:0 2px 6px rgba(0,0,0,0.3);}}
            #share-output{{position:absolute;bottom:60px;right:16px;z-index:1000;
                background:white;padding:8px 12px;border-radius:8px;font-size:12px;
                max-width:260px;display:none;box-shadow:0 2px 6px rgba(0,0,0,0.2);
                word-break:break-all;}}
        </style>
    </head>
    <body>
    <div style="position:relative;">
        <div id="map"></div>
        <div class="legend">
            <div class="legend-title">🗺️ Map Legend</div>
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                <div style="width:14px;height:14px;background:#1565C0;border-radius:50%;
                     border:3px solid white;flex-shrink:0;"></div>
                <span style="font-size:12px;font-weight:bold;">📍 You</span>
            </div>
            {legend_items}
        </div>
        <button class="share-btn" onclick="shareLocation()">📍 Share My Location</button>
        <div id="share-output"></div>
    </div>
    <script>
        const userLat={user_lat}, userLon={user_lon};
        const places={combined_json};
        const map=L.map('map').setView([userLat,userLon],14);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{
            attribution:'© OpenStreetMap',maxZoom:19}}).addTo(map);

        // User location marker
        const userIcon=L.divIcon({{className:'',
            html:`<div style="width:18px;height:18px;background:#1565C0;border-radius:50%;
                  border:3px solid white;box-shadow:0 0 0 5px rgba(21,101,192,0.3);"></div>`,
            iconSize:[18,18],iconAnchor:[9,9]}});
        L.marker([userLat,userLon],{{icon:userIcon}}).addTo(map)
         .bindPopup("<b>📍 You are here</b>").openPopup();

        // Service markers
        places.forEach(function(p){{
            const icon=L.divIcon({{className:'',
                html:`<div style="width:13px;height:13px;background:${{p.color}};border-radius:50%;
                      border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.5);"></div>`,
                iconSize:[13,13],iconAnchor:[6,6]}});
            L.marker([p.lat,p.lon],{{icon:icon}}).addTo(map)
             .bindPopup(
                `<b>${{p.icon}} ${{p.name}}</b><br/>
                 <span style="color:#666;font-size:12px;">${{p.category}}</span><br/>
                 📏 ${{p.distance_km}} km &nbsp;|&nbsp; 📞 ${{p.phone||'N/A'}}<br/>
                 <a href="${{p.gmaps_link}}" target="_blank"
                    style="color:#1e88e5;font-weight:bold;">🗺 Get Directions</a>`
             );
        }});

        function shareLocation(){{
            const link=`https://www.openstreetmap.org/?mlat=${{userLat}}&mlon=${{userLon}}&zoom=16`;
            const out=document.getElementById('share-output');
            out.style.display='block';
            out.innerHTML=`<b>🔗 Share:</b><br/><a href="${{link}}" target="_blank">${{link}}</a>`;
            navigator.clipboard.writeText(link).catch(()=>{{}});
        }}
    </script></body></html>"""
    components.html(html, height=520)
