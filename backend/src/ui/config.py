"""
ui/config.py — UI configuration constants and style definitions.
"""

# ──────────────────────────────────────────────────────────────
#  Page configuration
# ──────────────────────────────────────────────────────────────

PAGE_TITLE = "🍽️ Zomato AI — Smart Restaurant Recommendations"
PAGE_ICON = "🍽️"
PAGE_LAYOUT = "wide"

# ──────────────────────────────────────────────────────────────
#  Theming & CSS
# ──────────────────────────────────────────────────────────────

CUSTOM_CSS = """
<style>
/* ── Global ───────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hero Section ─────────────────────────────────────────── */
.hero-container {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,107,107,0.1) 0%, transparent 60%);
    animation: pulse-glow 6s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #ff9ff3, #54a0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    position: relative;
}
.hero-subtitle {
    color: rgba(255, 255, 255, 0.7);
    font-size: 1.1rem;
    font-weight: 300;
    position: relative;
}

/* ── Recommendation Cards ─────────────────────────────────── */
.rec-card {
    background: linear-gradient(145deg, rgba(30, 30, 60, 0.95), rgba(20, 20, 40, 0.98));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #54a0ff);
    opacity: 0;
    transition: opacity 0.3s;
}
.rec-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 107, 107, 0.3);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}
.rec-card:hover::before {
    opacity: 1;
}
.rec-rank {
    display: inline-block;
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}
.rec-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.8rem;
}
.rec-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1rem;
}
.rec-badge {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.35rem 0.8rem;
    border-radius: 10px;
    font-size: 0.88rem;
    color: rgba(255, 255, 255, 0.85);
}
.rec-explanation {
    background: rgba(84, 160, 255, 0.08);
    border-left: 3px solid #54a0ff;
    padding: 0.9rem 1.1rem;
    border-radius: 0 10px 10px 0;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.92rem;
    line-height: 1.6;
    font-style: italic;
}

/* ── Sidebar Styling ──────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29, #1a1a3e);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stTextArea label {
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 500;
}

/* ── Stats Row ────────────────────────────────────────────── */
.stat-card {
    background: linear-gradient(145deg, rgba(30, 30, 60, 0.9), rgba(20, 20, 40, 0.95));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

/* ── Loading Animation ────────────────────────────────────── */
.loading-pulse {
    animation: loading 1.5s ease-in-out infinite;
}
@keyframes loading {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* ── Misc ─────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(238, 90, 36, 0.4) !important;
}
</style>
"""

# ──────────────────────────────────────────────────────────────
#  Default values
# ──────────────────────────────────────────────────────────────

DEFAULT_MIN_RATING = 3.0
RATING_STEP = 0.5
MAX_RECOMMENDATIONS = 5
