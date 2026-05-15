"""
Global Emergency Numbers Database
Covers 60+ countries with country detection from location string or coordinates.
Fully offline — no API needed.
"""

# Country emergency numbers database
# Format: "COUNTRY_CODE": {"name", "emergency", "ambulance", "police", "fire", "extra"}
EMERGENCY_DB = {
    # --- South Asia ---
    "IN": {"name": "India",        "emergency": "112", "ambulance": "108", "police": "100", "fire": "101", "extra": {"Highway Help": "1033", "Women Helpline": "1091", "Disaster": "108"}},
    "PK": {"name": "Pakistan",     "emergency": "115", "ambulance": "115", "police": "15",  "fire": "16",  "extra": {"Rescue": "1122"}},
    "BD": {"name": "Bangladesh",   "emergency": "999", "ambulance": "199", "police": "999", "fire": "199", "extra": {}},
    "LK": {"name": "Sri Lanka",    "emergency": "119", "ambulance": "110", "police": "119", "fire": "111", "extra": {}},
    "NP": {"name": "Nepal",        "emergency": "100", "ambulance": "102", "police": "100", "fire": "101", "extra": {}},
    "AF": {"name": "Afghanistan",  "emergency": "119", "ambulance": "112", "police": "119", "fire": "119", "extra": {}},

    # --- Southeast Asia ---
    "SG": {"name": "Singapore",    "emergency": "999", "ambulance": "995", "police": "999", "fire": "995", "extra": {"Non-Emergency": "1800-255-0000"}},
    "MY": {"name": "Malaysia",     "emergency": "999", "ambulance": "999", "police": "999", "fire": "994", "extra": {}},
    "TH": {"name": "Thailand",     "emergency": "191", "ambulance": "1669","police": "191", "fire": "199", "extra": {"Tourist Police": "1155"}},
    "PH": {"name": "Philippines",  "emergency": "911", "ambulance": "911", "police": "911", "fire": "911", "extra": {}},
    "ID": {"name": "Indonesia",    "emergency": "112", "ambulance": "118", "police": "110", "fire": "113", "extra": {}},
    "VN": {"name": "Vietnam",      "emergency": "113", "ambulance": "115", "police": "113", "fire": "114", "extra": {}},
    "MM": {"name": "Myanmar",      "emergency": "199", "ambulance": "192", "police": "199", "fire": "191", "extra": {}},
    "KH": {"name": "Cambodia",     "emergency": "117", "ambulance": "119", "police": "117", "fire": "118", "extra": {}},

    # --- East Asia ---
    "CN": {"name": "China",        "emergency": "110", "ambulance": "120", "police": "110", "fire": "119", "extra": {"Traffic": "122"}},
    "JP": {"name": "Japan",        "emergency": "110", "ambulance": "119", "police": "110", "fire": "119", "extra": {}},
    "KR": {"name": "South Korea",  "emergency": "112", "ambulance": "119", "police": "112", "fire": "119", "extra": {}},
    "TW": {"name": "Taiwan",       "emergency": "110", "ambulance": "119", "police": "110", "fire": "119", "extra": {}},
    "HK": {"name": "Hong Kong",    "emergency": "999", "ambulance": "999", "police": "999", "fire": "999", "extra": {}},

    # --- Middle East ---
    "AE": {"name": "UAE",          "emergency": "999", "ambulance": "998", "police": "999", "fire": "997", "extra": {"Coast Guard": "996"}},
    "SA": {"name": "Saudi Arabia", "emergency": "911", "ambulance": "911", "police": "911", "fire": "911", "extra": {"Traffic": "993"}},
    "QA": {"name": "Qatar",        "emergency": "999", "ambulance": "999", "police": "999", "fire": "999", "extra": {}},
    "KW": {"name": "Kuwait",       "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "BH": {"name": "Bahrain",      "emergency": "999", "ambulance": "999", "police": "999", "fire": "999", "extra": {}},
    "OM": {"name": "Oman",         "emergency": "9999","ambulance": "9999","police": "9999","fire": "9999","extra": {}},
    "IL": {"name": "Israel",       "emergency": "100", "ambulance": "101", "police": "100", "fire": "102", "extra": {}},
    "TR": {"name": "Turkey",       "emergency": "112", "ambulance": "112", "police": "155", "fire": "110", "extra": {}},
    "IR": {"name": "Iran",         "emergency": "115", "ambulance": "115", "police": "110", "fire": "125", "extra": {}},

    # --- Europe ---
    "GB": {"name": "UK",           "emergency": "999", "ambulance": "999", "police": "999", "fire": "999", "extra": {"Non-Emergency Police": "101"}},
    "DE": {"name": "Germany",      "emergency": "112", "ambulance": "112", "police": "110", "fire": "112", "extra": {}},
    "FR": {"name": "France",       "emergency": "112", "ambulance": "15",  "police": "17",  "fire": "18",  "extra": {}},
    "IT": {"name": "Italy",        "emergency": "112", "ambulance": "118", "police": "113", "fire": "115", "extra": {}},
    "ES": {"name": "Spain",        "emergency": "112", "ambulance": "112", "police": "091", "fire": "080", "extra": {}},
    "PT": {"name": "Portugal",     "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "NL": {"name": "Netherlands",  "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "BE": {"name": "Belgium",      "emergency": "112", "ambulance": "100", "police": "101", "fire": "100", "extra": {}},
    "CH": {"name": "Switzerland",  "emergency": "112", "ambulance": "144", "police": "117", "fire": "118", "extra": {}},
    "AT": {"name": "Austria",      "emergency": "112", "ambulance": "144", "police": "133", "fire": "122", "extra": {}},
    "SE": {"name": "Sweden",       "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "NO": {"name": "Norway",       "emergency": "112", "ambulance": "113", "police": "112", "fire": "110", "extra": {}},
    "DK": {"name": "Denmark",      "emergency": "112", "ambulance": "112", "police": "114", "fire": "112", "extra": {}},
    "FI": {"name": "Finland",      "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "PL": {"name": "Poland",       "emergency": "112", "ambulance": "999", "police": "997", "fire": "998", "extra": {}},
    "RU": {"name": "Russia",       "emergency": "112", "ambulance": "103", "police": "102", "fire": "101", "extra": {}},
    "UA": {"name": "Ukraine",      "emergency": "112", "ambulance": "103", "police": "102", "fire": "101", "extra": {}},
    "GR": {"name": "Greece",       "emergency": "112", "ambulance": "166", "police": "100", "fire": "199", "extra": {}},
    "RO": {"name": "Romania",      "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},

    # --- Americas ---
    "US": {"name": "USA",          "emergency": "911", "ambulance": "911", "police": "911", "fire": "911", "extra": {"Non-Emergency": "311"}},
    "CA": {"name": "Canada",       "emergency": "911", "ambulance": "911", "police": "911", "fire": "911", "extra": {}},
    "MX": {"name": "Mexico",       "emergency": "911", "ambulance": "911", "police": "911", "fire": "911", "extra": {}},
    "BR": {"name": "Brazil",       "emergency": "190", "ambulance": "192", "police": "190", "fire": "193", "extra": {"Civil Defense": "199"}},
    "AR": {"name": "Argentina",    "emergency": "911", "ambulance": "107", "police": "911", "fire": "100", "extra": {}},
    "CO": {"name": "Colombia",     "emergency": "123", "ambulance": "125", "police": "123", "fire": "119", "extra": {}},
    "CL": {"name": "Chile",        "emergency": "131", "ambulance": "131", "police": "133", "fire": "132", "extra": {}},
    "PE": {"name": "Peru",         "emergency": "105", "ambulance": "106", "police": "105", "fire": "116", "extra": {}},

    # --- Africa ---
    "ZA": {"name": "South Africa", "emergency": "10111","ambulance": "10177","police": "10111","fire": "10177","extra": {"National": "112"}},
    "NG": {"name": "Nigeria",      "emergency": "112", "ambulance": "112", "police": "112", "fire": "112", "extra": {}},
    "KE": {"name": "Kenya",        "emergency": "999", "ambulance": "999", "police": "999", "fire": "999", "extra": {"National": "112"}},
    "EG": {"name": "Egypt",        "emergency": "123", "ambulance": "123", "police": "122", "fire": "180", "extra": {}},
    "GH": {"name": "Ghana",        "emergency": "112", "ambulance": "193", "police": "191", "fire": "192", "extra": {}},
    "ET": {"name": "Ethiopia",     "emergency": "911", "ambulance": "907", "police": "911", "fire": "939", "extra": {}},

    # --- Oceania ---
    "AU": {"name": "Australia",    "emergency": "000", "ambulance": "000", "police": "000", "fire": "000", "extra": {"Non-Emergency": "131 444"}},
    "NZ": {"name": "New Zealand",  "emergency": "111", "ambulance": "111", "police": "111", "fire": "111", "extra": {}},
}

# Country name keywords → country code mapping (for text-based detection)
COUNTRY_KEYWORDS = {
    # India
    "india": "IN", "hyderabad": "IN", "mumbai": "IN", "delhi": "IN", "bangalore": "IN",
    "bengaluru": "IN", "chennai": "IN", "kolkata": "IN", "pune": "IN", "ahmedabad": "IN",
    "jaipur": "IN", "lucknow": "IN", "surat": "IN", "nagpur": "IN", "visakhapatnam": "IN",
    "bhopal": "IN", "patna": "IN", "vadodara": "IN", "ghaziabad": "IN", "ludhiana": "IN",
    "agra": "IN", "nashik": "IN", "faridabad": "IN", "meerut": "IN", "rajkot": "IN",
    "varanasi": "IN", "srinagar": "IN", "aurangabad": "IN", "dhanbad": "IN", "amritsar": "IN",
    "navi mumbai": "IN", "allahabad": "IN", "ranchi": "IN", "howrah": "IN", "coimbatore": "IN",
    "vijayawada": "IN", "jodhpur": "IN", "madurai": "IN", "raipur": "IN", "kota": "IN",
    "guwahati": "IN", "chandigarh": "IN", "solapur": "IN", "hubli": "IN", "mysore": "IN",
    "tiruchirappalli": "IN", "bareilly": "IN", "aligarh": "IN", "moradabad": "IN",
    "gurgaon": "IN", "gurugram": "IN", "noida": "IN", "thane": "IN", "kerala": "IN",
    "telangana": "IN", "andhra": "IN", "karnataka": "IN", "maharashtra": "IN",
    "tamil nadu": "IN", "tamilnadu": "IN", "gujarat": "IN", "rajasthan": "IN",
    "uttar pradesh": "IN", "madhya pradesh": "IN", "west bengal": "IN", "bihar": "IN",
    "odisha": "IN", "punjab": "IN", "haryana": "IN", "assam": "IN", "jharkhand": "IN",
    # USA
    "usa": "US", "united states": "US", "new york": "US", "los angeles": "US",
    "chicago": "US", "houston": "US", "phoenix": "US", "philadelphia": "US",
    "san antonio": "US", "san diego": "US", "dallas": "US", "san jose": "US",
    "california": "US", "texas": "US", "florida": "US", "new york state": "US",
    # UK
    "uk": "GB", "united kingdom": "GB", "england": "GB", "london": "GB",
    "manchester": "GB", "birmingham": "GB", "scotland": "GB", "wales": "GB",
    # Australia
    "australia": "AU", "sydney": "AU", "melbourne": "AU", "brisbane": "AU",
    "perth": "AU", "adelaide": "AU", "canberra": "AU",
    # Canada
    "canada": "CA", "toronto": "CA", "vancouver": "CA", "montreal": "CA",
    "calgary": "CA", "ottawa": "CA", "edmonton": "CA",
    # Germany
    "germany": "DE", "berlin": "DE", "munich": "DE", "hamburg": "DE",
    "frankfurt": "DE", "cologne": "DE", "stuttgart": "DE",
    # France
    "france": "FR", "paris": "FR", "marseille": "FR", "lyon": "FR", "toulouse": "FR",
    # UAE
    "uae": "AE", "dubai": "AE", "abu dhabi": "AE", "sharjah": "AE",
    "united arab emirates": "AE",
    # Singapore
    "singapore": "SG",
    # Japan
    "japan": "JP", "tokyo": "JP", "osaka": "JP", "kyoto": "JP", "yokohama": "JP",
    # China
    "china": "CN", "beijing": "CN", "shanghai": "CN", "guangzhou": "CN", "shenzhen": "CN",
    # Brazil
    "brazil": "BR", "sao paulo": "BR", "rio de janeiro": "BR", "brasilia": "BR",
    # South Africa
    "south africa": "ZA", "johannesburg": "ZA", "cape town": "ZA", "durban": "ZA",
    # Pakistan
    "pakistan": "PK", "karachi": "PK", "lahore": "PK", "islamabad": "PK",
    # Bangladesh
    "bangladesh": "BD", "dhaka": "BD", "chittagong": "BD",
    # Sri Lanka
    "sri lanka": "LK", "colombo": "LK",
    # Malaysia
    "malaysia": "MY", "kuala lumpur": "MY", "kl": "MY",
    # Thailand
    "thailand": "TH", "bangkok": "TH", "phuket": "TH", "chiang mai": "TH",
    # Philippines
    "philippines": "PH", "manila": "PH", "cebu": "PH",
    # Indonesia
    "indonesia": "ID", "jakarta": "ID", "bali": "ID", "surabaya": "ID",
    # Saudi Arabia
    "saudi arabia": "SA", "riyadh": "SA", "jeddah": "SA", "mecca": "SA",
    # Turkey
    "turkey": "TR", "istanbul": "TR", "ankara": "TR",
    # Russia
    "russia": "RU", "moscow": "RU", "saint petersburg": "RU",
    # Italy
    "italy": "IT", "rome": "IT", "milan": "IT", "naples": "IT",
    # Spain
    "spain": "ES", "madrid": "ES", "barcelona": "ES", "seville": "ES",
    # Netherlands
    "netherlands": "NL", "amsterdam": "NL", "rotterdam": "NL",
    # South Korea
    "south korea": "KR", "korea": "KR", "seoul": "KR", "busan": "KR",
    # New Zealand
    "new zealand": "NZ", "auckland": "NZ", "wellington": "NZ",
    # Nigeria
    "nigeria": "NG", "lagos": "NG", "abuja": "NG",
    # Kenya
    "kenya": "KE", "nairobi": "KE",
    # Egypt
    "egypt": "EG", "cairo": "EG", "alexandria": "EG",
    # Mexico
    "mexico": "MX", "mexico city": "MX", "guadalajara": "MX",
    # Argentina
    "argentina": "AR", "buenos aires": "AR",
    # Vietnam
    "vietnam": "VN", "hanoi": "VN", "ho chi minh": "VN",
    # Nepal
    "nepal": "NP", "kathmandu": "NP",
}

# Coordinate-based country bounding boxes (lat_min, lat_max, lon_min, lon_max)
# Used when user provides GPS coordinates
COUNTRY_BOUNDS = [
    ("IN", 6.0,  37.5, 68.0,  97.5),
    ("US", 24.0, 49.5, -125.0, -66.0),
    ("CA", 41.0, 83.0, -141.0, -52.0),
    ("MX", 14.0, 32.5, -118.0, -86.0),
    ("GB", 49.0, 61.0, -8.5,   2.0),
    ("AU", -44.0, -10.0, 113.0, 154.0),
    ("NZ", -47.0, -34.0, 166.0, 178.0),
    ("CN", 18.0, 53.5, 73.0,  135.0),
    ("JP", 24.0, 46.0, 122.0, 146.0),
    ("KR", 33.0, 38.5, 125.0, 130.0),
    ("IN", 6.0,  37.5, 68.0,  97.5),
    ("DE", 47.0, 55.0, 6.0,   15.0),
    ("FR", 41.0, 51.5, -5.0,  10.0),
    ("IT", 36.0, 47.5, 6.5,   18.5),
    ("ES", 36.0, 44.0, -9.5,  4.5),
    ("RU", 41.0, 82.0, 19.0,  190.0),
    ("BR", -33.5, 5.5, -74.0, -28.0),
    ("AR", -55.0, -21.0, -73.0, -53.0),
    ("ZA", -35.0, -22.0, 16.0, 33.0),
    ("NG", 4.0,  14.0, 2.5,   15.0),
    ("EG", 22.0, 31.5, 25.0,  37.0),
    ("SA", 16.0, 32.0, 36.0,  56.0),
    ("AE", 22.5, 26.5, 51.0,  56.5),
    ("TR", 36.0, 42.5, 26.0,  45.0),
    ("PK", 23.5, 37.5, 60.5,  77.5),
    ("BD", 20.5, 26.5, 88.0,  92.5),
    ("SG", 1.1,  1.5,  103.5, 104.1),
    ("MY", 0.8,  7.5,  99.5,  119.5),
    ("TH", 5.5,  20.5, 97.5,  105.5),
    ("ID", -11.0, 6.0, 95.0,  141.0),
    ("PH", 4.5,  21.0, 116.0, 127.0),
    ("VN", 8.5,  23.5, 102.0, 110.0),
]

DEFAULT_COUNTRY = {
    "name": "International",
    "emergency": "112",
    "ambulance": "112",
    "police": "112",
    "fire": "112",
    "extra": {"Note": "112 works in most countries"}
}


def detect_country_from_text(location: str) -> str:
    """Detect country code from location text. Returns 2-letter code or 'XX'."""
    loc = location.lower().strip()
    # Try longest match first to avoid partial matches
    sorted_keywords = sorted(COUNTRY_KEYWORDS.keys(), key=len, reverse=True)
    for keyword in sorted_keywords:
        if keyword in loc:
            return COUNTRY_KEYWORDS[keyword]
    return "XX"


def detect_country_from_coords(lat: float, lon: float) -> str:
    """Detect country code from GPS coordinates using bounding boxes."""
    for code, lat_min, lat_max, lon_min, lon_max in COUNTRY_BOUNDS:
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return code
    return "XX"


def get_emergency_numbers(location: str, lat: float = None, lon: float = None) -> dict:
    """
    Get emergency numbers for a location.
    Tries coordinates first (more accurate), then text matching, then defaults to 112.
    Returns the full country emergency info dict.
    """
    country_code = "XX"

    # Try coordinate-based detection first
    if lat is not None and lon is not None:
        country_code = detect_country_from_coords(lat, lon)

    # Fall back to text-based detection
    if country_code == "XX" and location:
        country_code = detect_country_from_text(location)

    if country_code in EMERGENCY_DB:
        result = EMERGENCY_DB[country_code].copy()
        result["country_code"] = country_code
        result["detected"] = True
        return result

    # Default fallback
    result = DEFAULT_COUNTRY.copy()
    result["country_code"] = "XX"
    result["detected"] = False
    return result


def get_all_countries() -> list:
    """Returns list of all supported countries for display."""
    return [{"code": k, "name": v["name"]} for k, v in EMERGENCY_DB.items()]
