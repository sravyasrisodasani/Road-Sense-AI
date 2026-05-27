
"""
PWA (Progressive Web App) support for RoadSoS.
Injects web app manifest and service worker registration into the Streamlit page.
This makes the app installable on Android/iOS from the browser.
"""

import streamlit.components.v1 as components


def inject_pwa():
    """
    Injects PWA manifest and service worker into the Streamlit page.
    Call this once at the top of app.py after st.set_page_config().
    """
    components.html("""
    <script>
    (function() {
        // ── 1. Inject Web App Manifest ──────────────────────────────────
        const manifest = {
            "name": "RoadSoS Emergency Assistant",
            "short_name": "RoadSoS",
            "description": "Instant emergency help during road accidents — First Aid, Nearby Services, SOS Alerts",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0f0c29",
            "theme_color": "#e53935",
            "orientation": "portrait-primary",
            "categories": ["medical", "utilities", "navigation"],
            "icons": [
                {
                    "src": "https://img.icons8.com/emoji/192/ambulance.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "https://img.icons8.com/emoji/512/ambulance.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "shortcuts": [
                {
                    "name": "ONE-TAP EMERGENCY",
                    "short_name": "🆘 Emergency",
                    "description": "Instantly call ambulance and send SOS to all contacts",
                    "url": "/?action=emergency",
                    "icons": [{"src": "https://img.icons8.com/emoji/96/sos-button.png", "sizes": "96x96"}]
                },
                {
                    "name": "Find Nearby Services",
                    "short_name": "🗺️ Services",
                    "description": "Find hospitals, police, ambulance nearby",
                    "url": "/?action=services",
                    "icons": [{"src": "https://img.icons8.com/emoji/96/hospital.png", "sizes": "96x96"}]
                }
            ]
        };

        // Inject manifest as blob URL
        const manifestBlob = new Blob(
            [JSON.stringify(manifest)],
            { type: "application/json" }
        );
        const manifestURL = URL.createObjectURL(manifestBlob);

        // Remove existing manifest if any
        const existing = window.parent.document.querySelector('link[rel="manifest"]');
        if (existing) existing.remove();

        const link = window.parent.document.createElement("link");
        link.rel = "manifest";
        link.href = manifestURL;
        window.parent.document.head.appendChild(link);

        // ── 2. Meta tags for iOS PWA support ────────────────────────────
        const metas = [
            { name: "apple-mobile-web-app-capable",          content: "yes" },
            { name: "apple-mobile-web-app-status-bar-style", content: "black-translucent" },
            { name: "apple-mobile-web-app-title",            content: "RoadSoS" },
            { name: "mobile-web-app-capable",                content: "yes" },
            { name: "theme-color",                           content: "#e53935" },
            { name: "application-name",                      content: "RoadSoS" },
        ];

        metas.forEach(function(m) {
            const existing = window.parent.document.querySelector(`meta[name="${m.name}"]`);
            if (existing) existing.remove();
            const meta = window.parent.document.createElement("meta");
            meta.name = m.name;
            meta.content = m.content;
            window.parent.document.head.appendChild(meta);
        });

        // ── 3. Service Worker Registration ──────────────────────────────
        const swCode = `
            const CACHE_NAME = 'roadsos-v1';
            const OFFLINE_URLS = ['/'];

            self.addEventListener('install', function(event) {
                event.waitUntil(
                    caches.open(CACHE_NAME).then(function(cache) {
                        return cache.addAll(OFFLINE_URLS);
                    })
                );
                self.skipWaiting();
            });

            self.addEventListener('activate', function(event) {
                event.waitUntil(
                    caches.keys().then(function(keys) {
                        return Promise.all(
                            keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
                        );
                    })
                );
                self.clients.claim();
            });

            self.addEventListener('fetch', function(event) {
                // Network first, fall back to cache
                event.respondWith(
                    fetch(event.request).catch(function() {
                        return caches.match(event.request);
                    })
                );
            });
        `;

        if ('serviceWorker' in navigator) {
            const swBlob = new Blob([swCode], { type: 'application/javascript' });
            const swURL  = URL.createObjectURL(swBlob);
            navigator.serviceWorker.register(swURL, { scope: '/' })
                .then(function(reg) {
                    console.log('[RoadSoS PWA] Service Worker registered:', reg.scope);
                })
                .catch(function(err) {
                    console.warn('[RoadSoS PWA] SW registration failed:', err);
                });
        }

        // ── 4. Install prompt banner ─────────────────────────────────────
        let deferredPrompt = null;

        window.addEventListener('beforeinstallprompt', function(e) {
            e.preventDefault();
            deferredPrompt = e;

            // Show install banner
            const banner = document.getElementById('pwa-install-banner');
            if (banner) banner.style.display = 'flex';
        });

        window.addEventListener('appinstalled', function() {
            const banner = document.getElementById('pwa-install-banner');
            if (banner) banner.style.display = 'none';
            deferredPrompt = null;
            console.log('[RoadSoS PWA] App installed!');
        });

        // Expose install function globally
        window.installPWA = function() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(result) {
                    deferredPrompt = null;
                });
            }
        };

        console.log('[RoadSoS PWA] Manifest and meta tags injected.');
    })();
    </script>

    <!-- Install Banner -->
    <div id="pwa-install-banner" style="
        display: none;
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background: linear-gradient(135deg, #b71c1c, #e53935);
        color: white;
        padding: 12px 16px;
        align-items: center;
        justify-content: space-between;
        z-index: 9999;
        font-family: sans-serif;
        box-shadow: 0 -4px 16px rgba(0,0,0,0.4);
    ">
        <div>
            <div style="font-weight: bold; font-size: 14px;">📱 Install RoadSoS</div>
            <div style="font-size: 12px; opacity: 0.9;">Add to home screen for instant emergency access</div>
        </div>
        <div style="display: flex; gap: 8px;">
            <button onclick="installPWA()" style="
                background: white; color: #b71c1c;
                border: none; padding: 8px 16px;
                border-radius: 8px; font-weight: bold;
                font-size: 13px; cursor: pointer;
            ">Install</button>
            <button onclick="document.getElementById('pwa-install-banner').style.display='none'" style="
                background: rgba(255,255,255,0.2); color: white;
                border: none; padding: 8px 12px;
                border-radius: 8px; font-size: 13px; cursor: pointer;
            ">✕</button>
        </div>
    </div>
    """, height=0)
