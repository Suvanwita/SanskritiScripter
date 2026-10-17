"""
app.py — SanskritiScripter
AI-powered children's storybook generator celebrating Indian culture.
"""

import os
import streamlit as st
from story_generator import (
    generate_story,
    get_regions,
    get_festivals,
    get_languages,
    get_morals,
    check_ollama_available,
    check_model_available,
    OLLAMA_MODEL,
    OLLAMA_HOST,
)

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SanskritiScripter – Stories that bring your culture to life",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS – storybook aesthetic
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Imports ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&family=Noto+Sans+Bengali&family=Noto+Sans+Devanagari&display=swap');

/* ── Root palette ── */
:root {
    --saffron:   #FF8C42;
    --deep-red:  #8B1A1A;
    --gold:      #D4AF37;
    --turmeric:  #F5C842;
    --cream:     #FFF8EE;
    --warm-bg:   #FFF3E0;
    --card-bg:   #FFFDF7;
    --text-dark: #2C1810;
    --text-med:  #5C3A1E;
    --text-soft: #8B6A4F;
    --border:    #E8D5B7;
    --shadow:    rgba(139,26,26,0.12);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #FFF8EE 0%, #FFF0D6 40%, #FFF8EE 100%);
    background-attachment: fixed;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2C1810 0%, #4A2010 100%) !important;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #FFD699 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFE8B0 !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] textarea {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(212,175,55,0.40) !important;
    color: #FFE8B0 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stToggle"] {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* ── Hero banner ── */
.hero-section {
    background: linear-gradient(135deg, #8B1A1A 0%, #C0392B 35%, #E67E22 70%, #D4AF37 100%);
    border-radius: 24px;
    padding: 56px 48px 48px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(139,26,26,0.30);
}

.hero-section::before {
    content: "🪔 ✨ 🌸 ✨ 🪔 ✨ 🌸 ✨ 🪔 ✨ 🌸 ✨ 🪔 ✨ 🌸";
    position: absolute;
    top: 14px;
    left: 0; right: 0;
    text-align: center;
    font-size: 18px;
    letter-spacing: 4px;
    opacity: 0.45;
}

.hero-section::after {
    content: "🌺 ❁ 🌺 ❁ 🌺 ❁ 🌺 ❁ 🌺 ❁ 🌺 ❁ 🌺 ❁ 🌺";
    position: absolute;
    bottom: 14px;
    left: 0; right: 0;
    text-align: center;
    font-size: 16px;
    letter-spacing: 4px;
    opacity: 0.40;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.8rem;
    font-weight: 700;
    color: #FFFFFF;
    text-align: center;
    line-height: 1.15;
    text-shadow: 0 3px 12px rgba(0,0,0,0.35);
    letter-spacing: -0.5px;
    margin: 0 0 8px 0;
}

.hero-tagline {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.35rem;
    font-style: italic;
    color: #FFE8B0;
    text-align: center;
    margin-bottom: 20px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.25);
}

.hero-description {
    font-size: 1.05rem;
    color: #FFD699;
    text-align: center;
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Section headings ── */
.section-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--deep-red);
    margin: 8px 0 24px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid var(--gold);
    display: inline-block;
}

/* ── Form card ── */
.form-card {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 36px 40px;
    box-shadow: 0 6px 24px var(--shadow);
}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div > div {
    background: var(--cream) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-dark) !important;
    font-size: 1rem !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--saffron) !important;
    box-shadow: 0 0 0 3px rgba(255,140,66,0.20) !important;
}

label[data-testid="stWidgetLabel"] p,
div.stSelectbox label p {
    color: var(--text-med) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.3px;
}

/* ── Generate button ── */
div.stButton > button {
    background: linear-gradient(135deg, #8B1A1A, #C0392B, #E67E22) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 14px 42px !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 6px 20px rgba(139,26,26,0.35) !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(139,26,26,0.45) !important;
    filter: brightness(1.08) !important;
}

div.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Status pills ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 3px;
}

.status-ok {
    background: rgba(34,139,34,0.18);
    border: 1px solid rgba(34,139,34,0.40);
    color: #1a7a1a;
}

.status-warn {
    background: rgba(255,140,0,0.18);
    border: 1px solid rgba(255,140,0,0.40);
    color: #8B5500;
}

.status-err {
    background: rgba(180,0,0,0.14);
    border: 1px solid rgba(180,0,0,0.35);
    color: #8B0000;
}

.demo-banner {
    background: linear-gradient(135deg, #FFF0D6, #FFE4B0);
    border: 1.5px solid var(--gold);
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 0.92rem;
    color: var(--text-med);
    margin: 12px 0;
    text-align: center;
}

/* ── Storybook cover card ── */
.cover-card {
    background: linear-gradient(160deg, #8B1A1A 0%, #C0392B 50%, #D4AF37 100%);
    border-radius: 24px;
    padding: 40px 32px;
    text-align: center;
    box-shadow: 0 16px 48px rgba(139,26,26,0.35);
    color: white;
    position: relative;
    overflow: hidden;
}

.cover-card::before {
    content: "";
    position: absolute;
    top: -30px; right: -30px;
    width: 160px; height: 160px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}

.cover-card::after {
    content: "";
    position: absolute;
    bottom: -40px; left: -20px;
    width: 200px; height: 200px;
    background: rgba(212,175,55,0.08);
    border-radius: 50%;
}

.cover-story-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FFE8A0;
    line-height: 1.25;
    text-shadow: 0 2px 8px rgba(0,0,0,0.35);
    margin: 16px 0 8px 0;
}

.cover-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.30);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #FFD699;
    margin: 4px 4px;
    letter-spacing: 0.3px;
    backdrop-filter: blur(4px);
}

/* ── Chapter reader ── */
.chapter-card {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 40px 44px;
    box-shadow: 0 8px 28px var(--shadow);
    position: relative;
}

.chapter-number-badge {
    position: absolute;
    top: -18px;
    left: 36px;
    background: linear-gradient(135deg, #8B1A1A, #E67E22);
    color: white;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 18px;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(139,26,26,0.30);
}

.chapter-title-text {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--deep-red);
    margin: 16px 0 24px 0;
    line-height: 1.3;
}

.chapter-body {
    font-size: 1.18rem;
    color: var(--text-dark);
    line-height: 2.0;
    white-space: pre-wrap;
    font-family: 'Lato', sans-serif;
}

.chapter-body.regional {
    font-size: 1.22rem;
    line-height: 2.1;
}

/* ── Illustration placeholder ── */
.illustration-box {
    background: linear-gradient(135deg, #FFF0D6, #FFE0A8);
    border: 2.5px dashed var(--gold);
    border-radius: 16px;
    padding: 36px 24px;
    text-align: center;
    margin: 28px 0;
}

.illustration-icon {
    font-size: 3.5rem;
    margin-bottom: 10px;
}

.illustration-caption {
    font-style: italic;
    color: var(--text-soft);
    font-size: 0.95rem;
    line-height: 1.5;
    max-width: 360px;
    margin: 0 auto;
}

/* ── Moral banner ── */
.moral-banner {
    background: linear-gradient(135deg, #FFF8EE, #FFE8C0);
    border-left: 5px solid var(--gold);
    border-radius: 0 14px 14px 0;
    padding: 20px 28px;
    margin-top: 32px;
}

.moral-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--saffron);
    margin-bottom: 6px;
}

.moral-text {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.15rem;
    font-style: italic;
    color: var(--text-dark);
    line-height: 1.55;
}

/* ── Chapter progress dots ── */
.progress-dots {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--border);
    display: inline-block;
}

.dot-active {
    background: var(--deep-red);
    transform: scale(1.3);
}

/* ── Language toggle ── */
div[data-testid="stRadio"] > div {
    gap: 10px !important;
}

div[data-testid="stRadio"] label {
    background: var(--cream) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 7px 18px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--deep-red) !important;
    border-color: var(--deep-red) !important;
    color: white !important;
}

/* ── Ornamental divider ── */
.ornamental-divider {
    text-align: center;
    font-size: 1.4rem;
    letter-spacing: 12px;
    color: var(--gold);
    margin: 30px 0;
    opacity: 0.7;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 4px; }

/* ── Spinner override ── */
div[data-testid="stSpinner"] p {
    color: var(--deep-red) !important;
    font-weight: 600 !important;
}

/* ── Alert boxes ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ── Characters tag list ── */
.char-tag {
    display: inline-block;
    background: linear-gradient(135deg, #FFF0D6, #FFE4B0);
    border: 1px solid var(--gold);
    color: var(--text-med);
    font-size: 0.82rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 3px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "story": None,
        "chapter_idx": 0,
        "lang_mode": "English",
        "generating": False,
        "last_error": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─────────────────────────────────────────────
# Helper: ornamental divider
# ─────────────────────────────────────────────
def ornamental_divider():
    st.markdown('<div class="ornamental-divider">❁ ✦ ❁ ✦ ❁</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR — Configuration
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    demo_mode = st.toggle(
        "🎭 Demo Mode",
        value=False,
        key="demo_mode",
        help="Use the built-in sample story without needing Ollama",
    )

    st.markdown("---")
    st.markdown("### 🤖 Ollama Configuration")

    model_name = st.text_input(
        "Model",
        value=OLLAMA_MODEL,
        key="model_input",
        help="e.g. qwen2.5:7b, llama3.2:3b, gemma2:9b",
    )

    st.markdown(
        f"<div style='font-size:0.78rem;opacity:0.7;margin-top:4px'>Host: {OLLAMA_HOST}</div>",
        unsafe_allow_html=True,
    )

    # Ollama status check
    st.markdown("---")
    st.markdown("### 🔌 Connection Status")

    if demo_mode:
        st.markdown(
            '<div class="status-pill status-ok">🎭 Demo Mode Active</div>',
            unsafe_allow_html=True,
        )
    else:
        ollama_ok, ollama_msg = check_ollama_available()
        if ollama_ok:
            st.markdown(
                '<div class="status-pill status-ok">✅ Ollama running</div>',
                unsafe_allow_html=True,
            )
            model_ok, model_msg = check_model_available(model_name)
            if model_ok:
                st.markdown(
                    f'<div class="status-pill status-ok">✅ {model_name}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="status-pill status-warn">⚠️ Model not found</div>',
                    unsafe_allow_html=True,
                )
                st.warning(model_msg)
        else:
            st.markdown(
                '<div class="status-pill status-err">❌ Ollama offline</div>',
                unsafe_allow_html=True,
            )
            st.error(
                "Ollama is not running.\n\n"
                "**To fix:**\n"
                "1. Install Ollama from ollama.com\n"
                "2. Run `ollama serve` in a terminal\n"
                "3. Run `ollama pull qwen2.5:7b`\n\n"
                "Or enable **Demo Mode** above."
            )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;opacity:0.5;line-height:1.6'>"
        "📖 SanskritiScripter<br>"
        "Celebrating India's stories,<br>one child at a time."
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="hero-section">
    <div class="hero-title">📖 SanskritiScripter</div>
    <div class="hero-tagline">"Stories that bring your culture to life."</div>
    <div class="hero-description">
        Generate personalised children's stories inspired by India's rich tapestry of festivals,
        folklore, regional traditions and languages. Every story celebrates the unique spirit of
        your culture — crafted just for your child.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Demo mode banner
if st.session_state.get("demo_mode"):
    st.markdown(
        '<div class="demo-banner">🎭 <strong>Demo Mode</strong> — Showing built-in sample story. '
        'Toggle Demo Mode off in the sidebar to use real AI generation with Ollama.</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# STORY CREATION FORM
# ─────────────────────────────────────────────
st.markdown('<div class="section-heading">✍️ Create Your Story</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        child_name = st.text_input(
            "👦 Child's Name",
            placeholder="e.g. Ananya, Arjun, Kavya …",
            key="input_name",
        )
        child_age = st.number_input(
            "🎂 Child's Age",
            min_value=3,
            max_value=14,
            value=8,
            step=1,
            key="input_age",
        )
        region = st.selectbox(
            "📍 Region / State",
            options=get_regions(),
            key="input_region",
        )

    with col2:
        festival = st.selectbox(
            "🎉 Festival / Cultural Theme",
            options=get_festivals(),
            key="input_festival",
        )
        language = st.selectbox(
            "🗣️ Story Language",
            options=get_languages(),
            key="input_language",
        )
        moral = st.selectbox(
            "💡 Moral / Value",
            options=get_morals(),
            key="input_moral",
        )

    with col3:
        story_idea = st.text_area(
            "💭 Your Story Idea",
            placeholder=(
                "Describe the adventure you'd like!\n\n"
                "e.g. A child discovers a magical flame during Durga Puja "
                "and helps a lost boy find his way home…\n\n"
                "(Leave blank for the AI to create freely)"
            ),
            height=210,
            key="input_idea",
        )

    st.markdown("</div>", unsafe_allow_html=True)

ornamental_divider()

# ── Generate button ────────────────────────
gen_col1, gen_col2, gen_col3 = st.columns([2, 1.5, 2])
with gen_col2:
    is_demo = st.session_state.get("demo_mode", False)
    btn_label = "🎭 Load Demo Story" if is_demo else "🪔 Generate Story"
    generate_clicked = st.button(
        btn_label,
        key="btn_generate",
        use_container_width=True,
    )

# ── Last error display ─────────────────────
if st.session_state.get("last_error"):
    st.error(st.session_state["last_error"])

if generate_clicked:
    if not child_name.strip():
        st.warning("Please enter the child's name before generating a story.")
    else:
        st.session_state["last_error"] = None
        is_demo = st.session_state.get("demo_mode", False)
        spinner_msg = (
            "📖 Loading demo story…"
            if is_demo
            else f"✨ Generating your story with {model_name}… (this may take a minute)"
        )
        with st.spinner(spinner_msg):
            story, error = generate_story(
                child_name=child_name.strip(),
                child_age=int(child_age),
                region=region,
                festival=festival,
                language=language,
                story_idea=story_idea.strip(),
                moral=moral,
                demo_mode=is_demo,
                model=model_name,
            )

        if error:
            st.session_state["last_error"] = error
            st.rerun()
        else:
            st.session_state["story"] = story
            st.session_state["chapter_idx"] = 0
            st.session_state["lang_mode"] = "English"
            st.rerun()


# ─────────────────────────────────────────────
# STORYBOOK READER
# ─────────────────────────────────────────────
if st.session_state["story"] is not None:
    story = st.session_state["story"]
    chapters = story.get("chapters", [])
    total_chapters = len(chapters)
    idx = st.session_state["chapter_idx"]

    if total_chapters == 0:
        st.error("The story has no chapters. Try regenerating.")
    else:
        idx = min(idx, total_chapters - 1)
        chapter = chapters[idx]

        ornamental_divider()
        is_demo_story = story.get("_demo", False)
        reader_label = "📚 Your Storybook" + (" (Demo)" if is_demo_story else "")
        st.markdown(f'<div class="section-heading">{reader_label}</div>', unsafe_allow_html=True)

        # ── Two-column layout: Cover | Reader ──
        left_col, right_col = st.columns([1, 2], gap="large")

        # ─── LEFT: COVER ───────────────────────
        with left_col:
            # Cover image
            cover_path = os.path.join(os.path.dirname(__file__), "story_cover.png")
            if os.path.exists(cover_path):
                st.image(cover_path, use_column_width=True, caption="")
            else:
                st.markdown(
                    '<div style="font-size:5rem;text-align:center;padding:30px">🪔</div>',
                    unsafe_allow_html=True,
                )

            # Cover card
            display_region = story.get("region", story.get("requested_region", "India"))
            display_festival = story.get("festival", story.get("requested_festival", ""))
            display_language = story.get("language", story.get("requested_language", ""))
            display_name = story.get("requested_child_name", child_name)
            display_age = story.get("requested_age", child_age)

            badges_html = "".join(
                f'<span class="cover-badge">{b}</span>'
                for b in [
                    f"📍 {display_region}",
                    f"🎉 {display_festival}",
                    f"🗣️ {display_language}",
                ]
            )

            st.markdown(
                f"""
<div class="cover-card">
    <div style="font-size:2.5rem">📖</div>
    <div class="cover-story-title">{story['title']}</div>
    <div style="margin: 14px 0">{badges_html}</div>
    <div style="font-size:0.82rem;color:#FFD699;margin-top:10px;opacity:0.9">
        A story for <strong style="color:#FFE8B0">{display_name}</strong>
        · Age {display_age}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            # Characters
            characters = story.get("characters", [])
            if characters:
                chars_html = "".join(f'<span class="char-tag">👤 {c}</span>' for c in characters)
                st.markdown(
                    f'<div style="margin-top:16px;text-align:center">{chars_html}</div>',
                    unsafe_allow_html=True,
                )

            # Progress dots
            dots_html = '<div class="progress-dots">' + "".join(
                f'<span class="dot{"" if i != idx else " dot-active"}"></span>'
                for i in range(total_chapters)
            ) + "</div>"
            st.markdown(dots_html, unsafe_allow_html=True)

            # Moral banner
            moral_text = story.get("moral", story.get("requested_moral", ""))
            st.markdown(
                f"""
<div class="moral-banner">
    <div class="moral-label">✨ Moral of the Story</div>
    <div class="moral-text">"{moral_text}"</div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ─── RIGHT: CHAPTER READER ─────────────
        with right_col:

            # Language toggle
            lang_col, _ = st.columns([1, 2])
            with lang_col:
                regional_label = f"Regional ({display_language})"
                lang_choice = st.radio(
                    "🌐 Language",
                    options=["English", regional_label],
                    index=0 if st.session_state["lang_mode"] == "English" else 1,
                    horizontal=True,
                    key="lang_toggle",
                    label_visibility="collapsed",
                )
                st.session_state["lang_mode"] = (
                    "English" if lang_choice == "English" else "Regional"
                )

            is_regional = st.session_state["lang_mode"] == "Regional"

            # Resolve chapter fields — handle both old and new schema keys
            ch_title = chapter.get("title", chapter.get("title_en", f"Chapter {idx + 1}"))
            ch_body = (
                chapter.get("regional_text", chapter.get("text_regional", ""))
                if is_regional
                else chapter.get("english_text", chapter.get("text_en", ""))
            )
            scene_desc = chapter.get("scene_description", chapter.get("illustration_desc", ""))
            body_class = "chapter-body regional" if is_regional else "chapter-body"
            ch_num = chapter.get("chapter_number", chapter.get("number", idx + 1))

            # Escape HTML in chapter text for safe rendering
            import html as html_lib
            safe_body = html_lib.escape(ch_body).replace("\n", "<br>")
            safe_title = html_lib.escape(ch_title)

            # Chapter card
            st.markdown(
                f"""
<div class="chapter-card">
    <div class="chapter-number-badge">Chapter {ch_num} of {total_chapters}</div>
    <div class="chapter-title-text">{safe_title}</div>
    <div class="{body_class}">{safe_body}</div>
</div>
""",
                unsafe_allow_html=True,
            )

            # Illustration placeholder
            if scene_desc:
                safe_scene = html_lib.escape(scene_desc)
                st.markdown(
                    f"""
<div class="illustration-box">
    <div class="illustration-icon">🎨</div>
    <div class="illustration-caption">
        <strong>Scene:</strong> {safe_scene}
    </div>
</div>
""",
                    unsafe_allow_html=True,
                )

            # ── Prev / Next navigation ──────────
            nav_left, nav_mid, nav_right = st.columns([1, 2, 1])

            with nav_left:
                if idx > 0:
                    if st.button("← Previous", key="btn_prev", use_container_width=True):
                        st.session_state["chapter_idx"] = idx - 1
                        st.rerun()

            with nav_mid:
                st.markdown(
                    f"<div style='text-align:center;color:var(--text-soft);font-size:0.9rem;padding-top:10px'>"
                    f"📄 {idx + 1} / {total_chapters}</div>",
                    unsafe_allow_html=True,
                )

            with nav_right:
                if idx < total_chapters - 1:
                    if st.button("Next →", key="btn_next", use_container_width=True):
                        st.session_state["chapter_idx"] = idx + 1
                        st.rerun()

        ornamental_divider()

        # ── Reset ───────────────────────────────
        reset_col1, reset_col2, reset_col3 = st.columns([3, 1, 3])
        with reset_col2:
            if st.button("🔄 New Story", key="btn_reset", use_container_width=True):
                st.session_state["story"] = None
                st.session_state["chapter_idx"] = 0
                st.session_state["last_error"] = None
                st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
ornamental_divider()
ai_status = "Demo Mode" if st.session_state.get("demo_mode") else f"AI: {model_name}"
st.markdown(
    f"""
<div style="text-align:center;color:#B08050;font-size:0.85rem;padding:8px 0 32px 0;line-height:1.8">
    📖 <strong>SanskritiScripter</strong> — Celebrating the stories of India, one child at a time.<br>
    <span style="opacity:0.65">{ai_status} · Powered by Ollama</span>
</div>
""",
    unsafe_allow_html=True,
)
