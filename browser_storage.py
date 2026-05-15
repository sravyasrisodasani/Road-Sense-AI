"""
Browser-based persistent storage using localStorage.
Data is stored in the user's browser — survives server restarts,
redeployments, and works on Streamlit Cloud.

How it works:
1. On page load: JS reads localStorage and puts data in URL params
2. Python reads URL params and loads into session state
3. On save: Python updates session state, JS writes to localStorage
"""
import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.parse


def inject_storage_loader():
    """
    Inject JS that reads localStorage and passes data to Streamlit via URL params.
    Call this ONCE at the top of app.py before reading session state.
    """
    components.html("""
    <script>
    (function(){
        // Keys to sync between localStorage and Streamlit
        var KEYS = [
            'user_name','user_phone','contact1','contact2','contact3',
            'blood_group','allergies','medical_conditions','lang','location'
        ];

        var url = new URL(window.parent.location.href);
        var needsReload = false;

        KEYS.forEach(function(key){
            var stored = localStorage.getItem('roadsos_' + key);
            if(stored && !url.searchParams.has('ls_' + key)){
                url.searchParams.set('ls_' + key, encodeURIComponent(stored));
                needsReload = true;
            }
        });

        if(needsReload){
            window.parent.location.href = url.toString();
        }
    })();
    </script>
    """, height=0)


def save_to_browser(data: dict):
    """
    Inject JS to save data to localStorage.
    Call after saving to session state.
    """
    js_lines = []
    for key, value in data.items():
        safe_value = str(value).replace("'", "\\'").replace('"', '\\"')
        js_lines.append(f"localStorage.setItem('roadsos_{key}', '{safe_value}');")

    js_code = "\n".join(js_lines)
    components.html(f"""
    <script>
    (function(){{
        {js_code}
        console.log('[RoadSoS] Data saved to browser storage');
    }})();
    </script>
    """, height=0)


def load_from_url_params() -> dict:
    """
    Read data that was passed via URL params from localStorage.
    Returns dict of saved values.
    """
    data = {}
    keys = [
        'user_name', 'user_phone', 'contact1', 'contact2', 'contact3',
        'blood_group', 'allergies', 'medical_conditions', 'lang', 'location'
    ]
    params = st.query_params
    for key in keys:
        param_key = f'ls_{key}'
        val = params.get(param_key, '')
        if val:
            data[key] = urllib.parse.unquote(val)

    # Clean up ls_ params from URL after reading
    if data:
        clean_params = {k: v for k, v in dict(params).items()
                       if not k.startswith('ls_')}
        st.query_params.update(clean_params)

    return data
