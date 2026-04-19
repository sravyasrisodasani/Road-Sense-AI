import requests
import math

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def geocode_location(location: str):
    if "," in location:
        parts = location.split(",")
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return {"lat": lat, "lon": lon}
        except ValueError:
            pass
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json", "limit": 1}
    headers = {"User-Agent": "RoadSoS-Emergency-App/1.0"}
    try:
        res = requests.get(url, params=params, headers=headers, timeout=6)
        data = res.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    except Exception:
        pass
    return None


SERVICE_CONFIG = {
    "Hospitals": {
        "icon": "🏥",
        "query_tags": ['["amenity"="hospital"]', '["amenity"="clinic"]',
                       '["amenity"="doctors"]', '["amenity"="trauma_centre"]'],
        "emergency_number": "108 (Ambulance)", "color": "#e53935",
        "keywords": ["hospital", "medical", "clinic", "health", "care", "emergency", "trauma"]
    },
    "Ambulance": {
        "icon": "🚑",
        "query_tags": ['["emergency"="ambulance_station"]',
                       '["amenity"="ambulance_station"]', '["amenity"="hospital"]'],
        "emergency_number": "108", "color": "#e53935",
        "keywords": ["ambulance", "hospital", "emergency", "rescue"]
    },
    "Police": {
        "icon": "🚔",
        "query_tags": ['["amenity"="police"]'],
        "emergency_number": "100", "color": "#1e88e5",
        "keywords": ["police", "station", "thana", "cop"]
    },
    "Towing": {
        "icon": "🚛",
        "query_tags": ['["shop"="car_repair"]', '["amenity"="vehicle_inspection"]',
                       '["shop"="vehicle"]', '["highway"="services"]'],
        "emergency_number": "1033 (Highway Help)", "color": "#fb8c00",
        "keywords": ["tow", "recovery", "rescue", "vehicle", "car", "auto"]
    },
    "Puncture/Repair": {
        "icon": "🔧",
        "query_tags": ['["shop"="tyres"]', '["shop"="car_repair"]',
                       '["shop"="motorcycle_repair"]', '["shop"="bicycle"]'],
        "emergency_number": "1033 (Highway Help)", "color": "#fb8c00",
        "keywords": ["tyre", "tire", "puncture", "repair", "garage", "workshop"]
    },
    "Showrooms": {
        "icon": "🏪",
        "query_tags": ['["shop"="car"]', '["shop"="motorcycle"]',
                       '["amenity"="car_rental"]', '["shop"="vehicle"]'],
        "emergency_number": "1033 (Highway Help)", "color": "#00897b",
        "keywords": ["showroom", "car", "vehicle", "dealer", "motors", "auto"]
    }
}


def _run_overpass_query(query: str) -> tuple:
    mirrors = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]
    last_err = ""
    for mirror in mirrors:
        try:
            res = requests.post(mirror, data={"data": query}, timeout=15)
            if res.status_code == 200 and res.text.strip():
                return res.json().get("elements", []), None
            last_err = f"Status {res.status_code}"
        except Exception as e:
            last_err = str(e)
    return [], last_err


def _build_query(tags, lat, lon, radius):
    node_ways = ""
    for tag in tags:
        node_ways += f'node{tag}(around:{radius},{lat},{lon});\n'
        node_ways += f'way{tag}(around:{radius},{lat},{lon});\n'
    return f"[out:json][timeout:15];\n(\n{node_ways});\nout center 20;"


def fetch_services(location: str, service_type: str, radius_m: int = 8000) -> dict:
    if service_type in ("Ambulance", "Towing", "Puncture/Repair"):
        radius_m = 12000

    coords = geocode_location(location)
    if not coords:
        return {"success": False, "error": f"Could not find location: '{location}'."}

    lat, lon = coords["lat"], coords["lon"]
    config = SERVICE_CONFIG.get(service_type, SERVICE_CONFIG["Hospitals"])
    tags = config["query_tags"]
    keywords = config.get("keywords", [])

    elements, err = _run_overpass_query(_build_query(tags, lat, lon, radius_m))
    if not elements:
        elements, err = _run_overpass_query(_build_query(tags, lat, lon, radius_m * 2))

    if err and not elements:
        return {"success": False, "error": f"Map service unavailable: {err}"}

    places = []
    seen_names = set()
    seen_coords = set()

    for el in elements:
        tags_data = el.get("tags", {})
        name = (tags_data.get("name") or tags_data.get("name:en") or tags_data.get("operator"))
        if not name:
            continue
        name_key = name.strip().lower()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)

        p_lat = el.get("lat") or el.get("center", {}).get("lat")
        p_lon = el.get("lon") or el.get("center", {}).get("lon")
        if not p_lat or not p_lon:
            continue

        coord_key = (round(p_lat, 3), round(p_lon, 3))
        if coord_key in seen_coords:
            continue
        seen_coords.add(coord_key)

        distance = haversine(lat, lon, p_lat, p_lon)
        phone = (tags_data.get("phone") or tags_data.get("contact:phone") or
                 tags_data.get("contact:mobile") or "")
        score = sum(1 for kw in keywords if kw in name_key)

        places.append({
            "name": name, "distance_km": distance, "phone": phone,
            "lat": p_lat, "lon": p_lon, "score": score,
            "maps_link": f"https://www.openstreetmap.org/?mlat={p_lat}&mlon={p_lon}&zoom=17",
            "gmaps_link": f"https://www.google.com/maps/dir/?api=1&destination={p_lat},{p_lon}",
            "call_link": f"tel:{phone.replace(' ', '').replace('-', '')}" if phone else ""
        })

    places = sorted(places, key=lambda x: (-x["score"], x["distance_km"]))[:6]

    if not places:
        return {"success": False,
                "error": f"No {service_type.lower()} found near '{location}'. "
                         f"Call {config.get('emergency_number', '112')} directly."}

    return {"success": True, "places": places, "location": location,
            "lat": lat, "lon": lon, "service_type": service_type, "config": config}
