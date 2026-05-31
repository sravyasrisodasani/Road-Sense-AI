"""
RoadSoS UX Effects Module
Injects premium UI/UX enhancements:
- Cursor glow (mouse-following radial glow)
- Glow pulse on CTA buttons
- 3D card hover effects
- Input focus glow
- Floating icon animations
- Animated gradient background
- Button click ripple effect
"""
import streamlit.components.v1 as components


def inject_ux_effects():
    """Inject all UX effects into the Streamlit page."""
    components.html("""
<script>
(function() {
    var doc = window.parent.document;

    // ── 1. CURSOR GLOW ────────────────────────────────────────────────────
    var cursorGlow = doc.createElement('div');
    cursorGlow.id = 'roadsos-cursor-glow';
    cursorGlow.style.cssText = [
        'position:fixed',
        'pointer-events:none',
        'z-index:99998',
        'width:320px',
        'height:320px',
        'border-radius:50%',
        'background:radial-gradient(circle, rgba(255,59,59,0.10) 0%, rgba(255,59,59,0.04) 40%, transparent 70%)',
        'transform:translate(-50%,-50%)',
        'transition:background 0.4s ease',
        'top:-200px',
        'left:-200px',
        'mix-blend-mode:screen'
    ].join(';');
    doc.body.appendChild(cursorGlow);

    var mouseX = -500, mouseY = -500;
    var glowX  = -500, glowY  = -500;

    doc.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateGlow() {
        // Lerp for smooth follow
        glowX += (mouseX - glowX) * 0.08;
        glowY += (mouseY - glowY) * 0.08;
        cursorGlow.style.left = glowX + 'px';
        cursorGlow.style.top  = glowY + 'px';
        requestAnimationFrame(animateGlow);
    }
    animateGlow();

    // ── 2. BUTTON EFFECTS ─────────────────────────────────────────────────
    function enhanceButtons() {
        var btns = doc.querySelectorAll('button');
        btns.forEach(function(btn) {
            if (btn.dataset.uxDone) return;
            btn.dataset.uxDone = '1';

            var txt = (btn.innerText || '').trim();

            // Glow pulse on emergency/SOS/Get Help buttons
            var isEmergency = txt.includes('EMERGENCY') || txt.includes('SOS') ||
                              txt.includes('Get Help') || txt.includes('सहायता') ||
                              txt.includes('సహాయం') || txt.includes('உதவி');

            if (isEmergency) {
                btn.style.animation = 'roadsos-glow-pulse 2s ease-in-out infinite';
            }

            // Ripple effect on click
            btn.addEventListener('click', function(e) {
                var ripple = doc.createElement('span');
                var rect   = btn.getBoundingClientRect();
                var size   = Math.max(rect.width, rect.height);
                ripple.style.cssText = [
                    'position:absolute',
                    'border-radius:50%',
                    'background:rgba(255,255,255,0.25)',
                    'width:' + size + 'px',
                    'height:' + size + 'px',
                    'left:' + (e.clientX - rect.left - size/2) + 'px',
                    'top:' + (e.clientY - rect.top - size/2) + 'px',
                    'transform:scale(0)',
                    'animation:roadsos-ripple 0.5s ease-out forwards',
                    'pointer-events:none'
                ].join(';');
                btn.style.position = 'relative';
                btn.style.overflow = 'hidden';
                btn.appendChild(ripple);
                setTimeout(function() { ripple.remove(); }, 600);
            });
        });
    }

    // ── 3. 3D CARD HOVER ──────────────────────────────────────────────────
    function enhance3DCards() {
        var cards = doc.querySelectorAll(
            '.guide-section, .rs-card, [class*="section-quick"], [class*="section-emergency"], [class*="section-response"]'
        );
        cards.forEach(function(card) {
            if (card.dataset.ux3d) return;
            card.dataset.ux3d = '1';
            card.style.transition = 'transform 0.25s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s ease';

            card.addEventListener('mouseenter', function() {
                card.style.transform = 'translateY(-5px) scale(1.005)';
                card.style.boxShadow = '0 16px 40px rgba(0,0,0,0.5), 0 0 30px rgba(255,59,59,0.08)';
            });
            card.addEventListener('mouseleave', function() {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = '';
            });
        });
    }

    // ── 4. INPUT FOCUS GLOW ───────────────────────────────────────────────
    function enhanceInputs() {
        var inputs = doc.querySelectorAll('input[type="text"], textarea');
        inputs.forEach(function(inp) {
            if (inp.dataset.uxGlow) return;
            inp.dataset.uxGlow = '1';
            inp.addEventListener('focus', function() {
                inp.style.boxShadow = '0 0 0 3px rgba(0,194,255,0.25), 0 0 16px rgba(0,194,255,0.15)';
                inp.style.borderColor = '#00C2FF';
                inp.style.transition = 'box-shadow 0.2s ease, border-color 0.2s ease';
            });
            inp.addEventListener('blur', function() {
                inp.style.boxShadow = '';
                inp.style.borderColor = '';
            });
        });
    }

    // ── 5. INJECT KEYFRAMES ───────────────────────────────────────────────
    if (!doc.getElementById('roadsos-ux-keyframes')) {
        var style = doc.createElement('style');
        style.id = 'roadsos-ux-keyframes';
        style.textContent = `
            @keyframes roadsos-glow-pulse {
                0%, 100% { box-shadow: 0 0 16px rgba(255,59,59,0.3); }
                50%       { box-shadow: 0 0 32px rgba(255,59,59,0.7), 0 0 48px rgba(255,59,59,0.3); }
            }
            @keyframes roadsos-ripple {
                to { transform: scale(2.5); opacity: 0; }
            }
            @keyframes roadsos-float {
                0%, 100% { transform: translateY(0px); }
                50%       { transform: translateY(-8px); }
            }
            @keyframes roadsos-shimmer {
                0%   { background-position: -200% center; }
                100% { background-position:  200% center; }
            }
        `;
        doc.head.appendChild(style);
    }

    // ── 6. FLOATING HERO BADGES ───────────────────────────────────────────
    function floatBadges() {
        var badges = doc.querySelectorAll('.hero-box span[style*="border-radius:20px"]');
        badges.forEach(function(badge, i) {
            badge.style.animation = 'roadsos-float ' + (2.5 + i * 0.4) + 's ease-in-out infinite';
            badge.style.display = 'inline-block';
        });
    }

    // ── 7. SHIMMER ON SECTION HEADERS ────────────────────────────────────
    function shimmerHeaders() {
        var headers = doc.querySelectorAll('.section-header');
        headers.forEach(function(h) {
            if (h.dataset.uxShimmer) return;
            h.dataset.uxShimmer = '1';
            h.style.background = 'linear-gradient(90deg, #64748B 0%, #94A3B8 40%, #64748B 80%)';
            h.style.backgroundSize = '200% auto';
            h.style.webkitBackgroundClip = 'text';
            h.style.webkitTextFillColor = 'transparent';
            h.style.backgroundClip = 'text';
            h.style.animation = 'roadsos-shimmer 3s linear infinite';
        });
    }

    // ── 8. RUN ALL + OBSERVE DOM CHANGES ─────────────────────────────────
    function runAll() {
        enhanceButtons();
        enhance3DCards();
        enhanceInputs();
        floatBadges();
        shimmerHeaders();
    }

    runAll();
    setTimeout(runAll, 500);
    setTimeout(runAll, 1500);

    var observer = new MutationObserver(function() { runAll(); });
    observer.observe(doc.body, { childList: true, subtree: true });

})();
</script>
""", height=0)
