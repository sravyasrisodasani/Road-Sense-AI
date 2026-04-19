import streamlit.components.v1 as components
import json

def render_map(user_lat: float, user_lon: float, places: list = None, color: str = "#e53935"):
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
