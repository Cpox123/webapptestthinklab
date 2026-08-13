"""Shared UI helpers: theme, colors, and reusable display components."""

import os
import base64
import math

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# THEME
# =========================================================

def _dark_mode():
    try:
        return st.get_option("theme.base") == "dark"
    except Exception:
        return False


DARK = _dark_mode()

if DARK:
    NAVY, NAVY_2 = "#182235", "#24324A"
    ACCENT, ACCENT_LIGHT = "#7890E8", "#91A5F0"
    BG, CARD, CARD_ALT = "#121923", "#1B2533", "#222D3D"
    BORDER = "#344255"
    TEXT_DARK, TEXT_MUTED, TEXT_LIGHT = "#F2F4F8", "#AEB8C7", "#D5DCE6"
    INPUT_BG, SOFT_BG, BAR_BG = "#1B2533", "#263246", "#354256"
else:
    NAVY, NAVY_2 = "#24324A", "#30415E"
    ACCENT, ACCENT_LIGHT = "#5B73C7", "#7188D8"
    BG, CARD, CARD_ALT = "#FFFFFF", "#F8FAFC", "#F4F6F9"
    BORDER = "#D9E0E8"
    TEXT_DARK, TEXT_MUTED, TEXT_LIGHT = "#263449", "#68778A", "#475569"
    INPUT_BG, SOFT_BG, BAR_BG = "#FFFFFF", "#EEF2F7", "#DCE3EC"


SENTIMENT_COLORS = {
    "Negative": "#C95757",
    "Neutral": "#C58A32",
    "Positive": "#398565",
}

SENTIMENT_EMOJIS = {
    "Negative": "🔴",
    "Neutral": "🟡",
    "Positive": "🟢",
}

SENTIMENT_FACES = {
    "Negative": "😞",
    "Neutral": "😐",
    "Positive": "😊",
}

INVALID_COLOR = "#8994A5"
INVALID_EMOJI = "⚪"

METRIC_COLORS = {
    "blue": ACCENT,
    "cyan": "#4B91A7",
    "purple": "#7864A8",
    "orange": "#C77D43",
    "green": "#398565",
    "yellow": "#C58A32",
    "red": "#C95757",
}


# =========================================================
# BASIC HELPERS
# =========================================================

def sentiment_color(label):
    return SENTIMENT_COLORS.get(label, INVALID_COLOR)


def sentiment_emoji(label):
    return SENTIMENT_EMOJIS.get(label, INVALID_EMOJI)


def sentiment_face(label):
    return SENTIMENT_FACES.get(label, "🙂")


# =========================================================
# THEME CSS
# =========================================================

_THEME_CSS = f"""
<style>
/* Main page */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {{
    background:{BG} !important;
}}

[data-testid="stHeader"] {{
    background:transparent !important;
}}

[data-testid="stMainBlockContainer"] {{
    padding-top:3.8rem;
}}

/* All normal text */
body,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stText"],
[data-testid="stCaptionContainer"],
label,
.stCaption {{
    color:{TEXT_DARK};
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    color:{TEXT_DARK} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background:{NAVY} !important;
}}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {{
    color:#DCE3EE;
}}

[data-testid="stSidebarNavLink"] {{
    border-radius:9px;
    margin:2px 6px;
}}

[data-testid="stSidebarNavLink"]:hover {{
    background:rgba(255,255,255,.07);
}}

[data-testid="stSidebarNavLink"][aria-current="page"] {{
    background:{ACCENT};
}}

[data-testid="stSidebarNavLink"][aria-current="page"] span {{
    color:#fff !important;
    font-weight:700;
}}

/* Buttons */
button,
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button {{
    color:{TEXT_DARK} !important;
    background:{CARD} !important;
    border:1px solid {BORDER} !important;
    border-radius:9px !important;
}}

[data-testid="stButton"] button[kind="primary"],
[data-testid="stDownloadButton"] button[kind="primary"] {{
    background:{ACCENT} !important;
    color:#fff !important;
    border:none !important;
    font-weight:600;
}}

[data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stDownloadButton"] button[kind="primary"]:hover {{
    background:{ACCENT_LIGHT} !important;
}}

/* Inputs */
input,
textarea,
[data-baseweb="select"],
[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {{
    background:{INPUT_BG} !important;
    color:{TEXT_DARK} !important;
    border-color:{BORDER} !important;
}}

input::placeholder,
textarea::placeholder {{
    color:{TEXT_MUTED} !important;
    opacity:1 !important;
}}

/* Select menus */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[role="listbox"],
[role="option"] {{
    background:{CARD} !important;
    color:{TEXT_DARK} !important;
}}

[role="option"]:hover {{
    background:{SOFT_BG} !important;
}}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {{
    background:{CARD} !important;
    border:1px dashed {BORDER} !important;
    border-radius:11px;
}}

[data-testid="stFileUploaderDropzone"] * {{
    color:{TEXT_DARK} !important;
}}

[data-testid="stFileUploaderDropzoneInstructions"] span {{
    color:{TEXT_MUTED} !important;
}}

/* Checkbox, radio and switches */
[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label,
[data-testid="stToggle"] label {{
    color:{TEXT_DARK} !important;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background:{CARD} !important;
    border:1px solid {BORDER} !important;
    border-radius:11px;
}}

[data-testid="stMetric"] *,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {{
    color:{TEXT_DARK} !important;
}}

/* Tables / dataframes */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] *,
[data-testid="stTable"],
[data-testid="stTable"] * {{
    color:{TEXT_DARK} !important;
}}

[data-testid="stDataFrame"] {{
    background:{CARD} !important;
}}

/* Expander */
[data-testid="stExpander"] {{
    background:{CARD} !important;
    border:1px solid {BORDER} !important;
    border-radius:10px !important;
}}

[data-testid="stExpander"] * {{
    color:{TEXT_DARK};
}}

/* Tabs */
[data-baseweb="tab-list"] {{
    background:transparent !important;
}}

[data-baseweb="tab"] {{
    color:{TEXT_MUTED} !important;
}}

[data-baseweb="tab"][aria-selected="true"] {{
    color:{ACCENT} !important;
}}

/* Page links */
[data-testid="stPageLink"] a {{
    background:{ACCENT} !important;
    border-radius:9px !important;
}}

[data-testid="stPageLink"] a *,
[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {{
    color:#fff !important;
    font-weight:600;
}}

/* Alerts */
[data-testid="stAlert"] {{
    border-radius:10px;
}}

/* Code */
code,
pre {{
    background:{CARD_ALT} !important;
    color:{TEXT_DARK} !important;
}}

/* Floating menu */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[data-testid="stExpandSidebarButton"] {{
    display:none !important;
}}

#tl-topbar {{
    position:fixed;
    top:10px;
    left:12px;
    z-index:999997;
    display:flex;
    align-items:center;
    gap:9px;
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:10px;
    padding:6px 13px 6px 8px;
    cursor:pointer;
    box-shadow:0 2px 10px rgba(0,0,0,.08);
}}

#tl-topbar:hover {{
    border-color:{ACCENT};
}}

body.tl-sidebar-open #tl-topbar {{
    display:none !important;
}}

body.tl-sidebar-open [data-testid="stMainBlockContainer"] {{
    padding-top:2.2rem;
}}
</style>
"""


# =========================================================
# FLOATING MENU
# =========================================================

_TOPBAR_HTML = f"""
<div id="tl-topbar" role="button" tabindex="0" title="Open menu">
<svg width="29" height="29" viewBox="0 0 48 48">
<rect x="2" y="2" width="44" height="44" rx="11" fill="{ACCENT}"/>
<circle cx="15" cy="19" r="4.2" fill="#fff"/>
<circle cx="29" cy="19" r="4.2" fill="#fff"/>
<path d="M12 29 Q22 36 32 29" stroke="#fff"
stroke-width="3.4" fill="none" stroke-linecap="round"/>
</svg>
<span style="font-weight:700;font-size:.9rem;color:{TEXT_DARK};
white-space:nowrap">NLP Sentiment Analyzer</span>
<span style="color:{ACCENT};font-size:1rem">&#9776;</span>
</div>
"""


_TOPBAR_COMPONENT = """
<script>
(function(){
const d=window.parent.document;

function sync(){
    try{
        const s=d.querySelector('section[data-testid="stSidebar"]');
        const open=s ? s.getAttribute("aria-expanded")!=="false" : false;
        d.body.classList.toggle("tl-sidebar-open",open);
        d.body.classList.toggle("tl-sidebar-closed",!open);
        d.querySelectorAll("#tl-topbar").forEach((x,i)=>{if(i)x.remove()});
    }catch(e){}
}

function toggle(){
    const s=d.querySelector('section[data-testid="stSidebar"]');
    const open=s ? s.getAttribute("aria-expanded")!=="false" : false;
    const b=open
      ? d.querySelector('[data-testid="stSidebarCollapseButton"]')
      : d.querySelector('button[data-testid="stExpandSidebarButton"]')
        || d.querySelector('[data-testid="collapsedControl"] button')
        || d.querySelector('button[aria-label="Open sidebar"]');
    if(b)b.click();
    setTimeout(sync,150);
    setTimeout(sync,500);
}

d.addEventListener("click",e=>{
    if(e.target.closest("#tl-topbar")){
        e.preventDefault();
        toggle();
    }
    if(e.target.closest('[data-testid="stSidebarCollapseButton"]')){
        setTimeout(sync,150);
        setTimeout(sync,500);
    }
},true);

new MutationObserver(sync).observe(d.documentElement,{
    attributes:true,
    attributeFilter:["aria-expanded"],
    subtree:true
});

sync();
})();
</script>
"""


def apply_theme():
    st.markdown(_THEME_CSS + _TOPBAR_HTML, unsafe_allow_html=True)
    components.html(_TOPBAR_COMPONENT, height=0)


def render_brand():
    st.logo("assets/logo.svg", size="large")


# =========================================================
# HEADER / FOOTER
# =========================================================

def render_page_header(title, subtitle=None):
    from config.project_data import GROUP_NAME

    chip = (
        f'<div style="text-align:right;margin-bottom:5px">'
        f'<span style="background:{NAVY};color:#fff;font-weight:600;'
        f'font-size:.8rem;padding:6px 12px;border-radius:999px">'
        f'🧠 {GROUP_NAME}</span></div>'
    )

    sub = (
        f'<div style="color:{TEXT_MUTED};font-size:.95rem;margin-top:3px">'
        f'{subtitle}</div>'
        if subtitle else ""
    )

    st.markdown(
        chip +
        f'<div style="font-size:1.85rem;font-weight:800;'
        f'color:{TEXT_DARK};margin-bottom:2px">{title}</div>' +
        sub,
        unsafe_allow_html=True,
    )
    st.write("")


def render_footer():
    from config.project_data import COURSE, COPYRIGHT_YEAR, GROUP_NAME

    st.markdown(
        f'<div style="text-align:center;color:{TEXT_MUTED};font-size:.78rem;'
        f'padding:16px 0 5px;border-top:1px solid {BORDER}">'
        f'© {COPYRIGHT_YEAR} {GROUP_NAME} | {COURSE}</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# PANELS / CARDS
# =========================================================

def panel_html(body, title=None, icon=None):
    heading = (
        f'<div style="font-size:1rem;font-weight:700;color:{TEXT_DARK};'
        f'margin-bottom:11px">{icon + " " if icon else ""}{title}</div>'
        if title else ""
    )

    return (
        f'<div style="background:{CARD};border:1px solid {BORDER};'
        f'border-radius:12px;padding:18px 20px;'
        f'box-shadow:0 1px 2px rgba(0,0,0,.04);margin-bottom:13px">'
        f'{heading}{body}</div>'
    )


def stat_card_html(icon, label, value, sublabel, color):
    body = (
        f'<div style="display:flex;align-items:center;gap:13px">'
        f'<div style="width:44px;height:44px;min-width:44px;border-radius:10px;'
        f'background:{color}1A;color:{color};font-size:1.3rem;'
        f'display:flex;align-items:center;justify-content:center">{icon}</div>'
        f'<div>'
        f'<div style="font-size:.78rem;color:{TEXT_MUTED};font-weight:600">{label}</div>'
        f'<div style="font-size:1.2rem;font-weight:800;color:{TEXT_DARK};'
        f'line-height:1.25">{value}</div>'
        f'<div style="font-size:.74rem;color:{TEXT_MUTED}">{sublabel}</div>'
        f'</div></div>'
    )
    return panel_html(body)


def render_stat_cards(cards):
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            st.markdown(stat_card_html(*card), unsafe_allow_html=True)


# =========================================================
# SENTIMENT CHARTS
# =========================================================

def _donut_segments(parts):
    radius = 52
    circumference = 2 * math.pi * radius
    gap = 1.5
    segments = []
    offset = 0

    for label, percent in parts:
        length = max(
            0,
            percent / 100 * circumference - (gap if percent > 0 else 0)
        )

        segments.append(
            f'<circle cx="70" cy="70" r="{radius}" fill="none" '
            f'stroke="{sentiment_color(label)}" stroke-width="16" '
            f'stroke-dasharray="{length:.2f} {circumference:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}"/>'
        )

        offset += percent / 100 * circumference

    return "".join(segments)


def donut_chart_html(parts, center_value, center_label):
    body = (
        '<div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap">'
        '<div style="position:relative;width:150px;height:150px">'
        '<svg width="150" height="150" viewBox="0 0 140 140" '
        'style="transform:rotate(-90deg)">'
        f'<circle cx="70" cy="70" r="52" fill="none" '
        f'stroke="{BAR_BG}" stroke-width="16"/>'
        f'{_donut_segments(parts)}</svg>'
        '<div style="position:absolute;inset:0;display:flex;'
        'flex-direction:column;align-items:center;justify-content:center">'
        f'<div style="font-size:1.2rem;font-weight:800;color:{TEXT_DARK}">'
        f'{center_value}</div>'
        f'<div style="font-size:.74rem;color:{TEXT_MUTED}">{center_label}</div>'
        '</div></div><div>'
    )

    for label, percent in parts:
        color = sentiment_color(label)
        body += (
            '<div style="display:flex;align-items:center;gap:8px;margin:7px 0">'
            f'<span style="width:10px;height:10px;border-radius:50%;'
            f'background:{color};display:inline-block"></span>'
            f'<span style="font-size:.88rem;color:{TEXT_DARK};font-weight:600">'
            f'{label}</span>'
            f'<span style="font-size:.82rem;color:{TEXT_MUTED}">'
            f'({percent:.1f}%)</span></div>'
        )

    return body + '</div></div>'


def vbar_chart_html(counts):
    values = [int(counts.get(x, 0)) for x in SENTIMENT_COLORS]
    total = sum(values)
    max_value = max(values) if values else 1
    bars = ""

    for label, value in zip(SENTIMENT_COLORS, values):
        color = sentiment_color(label)
        height = max(3, 100 * value / max_value) if value else 0
        share = 100 * value / total if total else 0

        bars += (
            '<div style="flex:1;display:flex;flex-direction:column;'
            'align-items:center;justify-content:flex-end;height:190px">'
            f'<div style="font-size:.84rem;font-weight:700;color:{color}">'
            f'{value:,}</div>'
            f'<div style="width:42px;height:{190*height/100:.0f}px;'
            f'background:{color};border-radius:7px 7px 4px 4px;margin:6px 0"></div>'
            f'<div style="font-size:.78rem;color:{TEXT_MUTED};font-weight:600">'
            f'{label}</div>'
            f'<div style="font-size:.7rem;color:{TEXT_MUTED}">({share:.1f}%)</div>'
            '</div>'
        )

    return (
        f'<div style="display:flex;align-items:flex-end;gap:18px;'
        f'padding:6px 10px 0;border-bottom:2px solid {BAR_BG}">{bars}</div>'
    )


def sentiment_distribution_html(counts):
    total = sum(int(counts.get(x, 0)) for x in SENTIMENT_COLORS)
    safe_total = total or 1
    bars = []

    for label, color in SENTIMENT_COLORS.items():
        count = int(counts.get(label, 0))
        percent = 100 * count / safe_total
        width = max(percent, 2) if count else 0

        bars.append(
            '<div style="margin-bottom:13px">'
            '<div style="display:flex;justify-content:space-between;margin-bottom:5px">'
            f'<span style="font-weight:600;color:{TEXT_DARK}">'
            f'{SENTIMENT_EMOJIS[label]} {label}</span>'
            f'<span style="font-weight:600;color:{color}">'
            f'{count} &middot; {percent:.0f}%</span></div>'
            f'<div style="background:{BAR_BG};border-radius:999px;height:12px;'
            f'overflow:hidden"><div style="width:{width:.1f}%;height:100%;'
            f'background:{color};border-radius:999px"></div></div></div>'
        )

    return '<div style="margin:6px 0 10px">' + "".join(bars) + "</div>"


def render_sentiment_distribution(counts):
    st.markdown(sentiment_distribution_html(counts), unsafe_allow_html=True)


# =========================================================
# PREDICTION
# =========================================================

def _placeholder_result_html():
    return (
        '<div style="text-align:center;padding:10px 0 16px">'
        f'<div style="width:84px;height:84px;margin:auto;border-radius:50%;'
        f'border:2px dashed {BORDER};display:flex;align-items:center;'
        f'justify-content:center;font-size:2rem;color:{TEXT_MUTED}">?</div>'
        f'<div style="margin-top:12px;color:{TEXT_MUTED};font-size:.92rem">'
        'Run a prediction to see the result</div></div>'
    )


def result_card_html(result):
    if not result:
        return panel_html(
            _placeholder_result_html(),
            "Prediction Result",
            "🎯"
        )

    label = result["label"]
    confidence = result.get("confidence", 0)
    color = sentiment_color(label)
    pct = confidence * 100

    body = (
        '<div style="text-align:center">'
        f'<div style="width:84px;height:84px;margin:auto;border-radius:50%;'
        f'background:{color}1A;border:3px solid {color};display:flex;'
        f'align-items:center;justify-content:center;font-size:2.1rem">'
        f'{sentiment_face(label)}</div>'
        f'<div style="font-size:1.45rem;font-weight:800;color:{color};margin-top:10px">'
        f'{label}</div>'
        f'<div style="color:{TEXT_MUTED};font-size:.84rem;margin-top:13px">'
        'Confidence Score</div>'
        f'<div style="font-size:1.35rem;font-weight:800;color:{color}">'
        f'{pct:.2f}%</div>'
        f'<div style="background:{BAR_BG};border-radius:999px;height:9px;'
        f'margin:8px 6px 2px;overflow:hidden">'
        f'<div style="width:{pct:.1f}%;height:100%;background:{color};'
        f'border-radius:999px"></div></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:.72rem;'
        f'color:{TEXT_MUTED};margin:0 6px"><span>0%</span><span>50%</span>'
        '<span>100%</span></div></div>'
    )

    return panel_html(body, "Prediction Result", "🎯")


def prob_panel_html(result):
    probs = (
        result["probabilities"] if result else
        {"Negative": 0, "Neutral": 0, "Positive": 0}
    )

    rows = ""

    for label in ["Positive", "Neutral", "Negative"]:
        color = sentiment_color(label)
        pct = probs.get(label, 0) * 100

        rows += (
            '<div style="display:flex;align-items:center;gap:12px;margin:11px 0">'
            f'<div style="width:74px;color:{TEXT_DARK};font-size:.88rem;font-weight:600">'
            f'{label}</div>'
            f'<div style="flex:1;background:{BAR_BG};border-radius:999px;height:9px;'
            f'overflow:hidden"><div style="width:{max(pct,1.2) if pct else 0:.1f}%;'
            f'height:100%;background:{color};border-radius:999px"></div></div>'
            f'<div style="width:58px;text-align:right;color:{TEXT_MUTED};'
            f'font-size:.82rem;font-weight:600">{pct:.2f}%</div></div>'
        )

    return panel_html(rows, "Prediction Probabilities", "📈")


def model_info_html(model_info):
    rows = ""

    for key, value in model_info.items():
        rows += (
            '<div style="display:flex;justify-content:space-between;'
            f'padding:8px 2px;border-bottom:1px dashed {BORDER}">'
            f'<span style="color:{TEXT_MUTED};font-size:.86rem">{key}</span>'
            f'<span style="color:{TEXT_DARK};font-size:.86rem;font-weight:600;'
            f'text-align:right">{value}</span></div>'
        )

    return panel_html(rows, "Model Information", "🤖")


def render_sentiment_result(label, heading="Predicted Sentiment"):
    color = sentiment_color(label)

    st.markdown(
        '<div style="display:flex;align-items:center;gap:15px;'
        f'background:{color}1A;border:2px solid {color};border-radius:12px;'
        f'padding:15px 20px;margin:4px 0 8px">'
        f'<div style="font-size:2.3rem">{sentiment_emoji(label)}</div>'
        '<div>'
        f'<div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;'
        f'text-transform:uppercase;color:{TEXT_MUTED}">{heading}</div>'
        f'<div style="font-size:1.75rem;font-weight:800;color:{color}">'
        f'{label}</div></div></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# BULK PAGE
# =========================================================

def bulk_requirements_html(row_limit, candidates):
    checks = "".join(
        f'<div style="display:flex;gap:9px;margin:8px 0">'
        f'<span style="color:{METRIC_COLORS["green"]};font-weight:800">✓</span>'
        f'<span style="font-size:.86rem;color:{TEXT_DARK}">{line}</span></div>'
        for line in [
            "CSV must contain a column with the review text",
            "Supported column names: " + ", ".join(candidates),
            "File should use UTF-8 or Latin-1 encoding",
            f"Maximum {row_limit:,} reviews are processed per file",
        ]
    )

    return panel_html(checks, "CSV Requirements", "📋")


def example_csv_html():
    cell = (
        f'<td style="border:1px solid {BORDER};padding:6px 10px;'
        f'font-size:.82rem;color:{TEXT_DARK}">'
    )

    table = (
        '<table style="border-collapse:collapse;width:100%">'
        f'<tr><th style="text-align:left;border:1px solid {BORDER};'
        f'background:{CARD_ALT};padding:6px 10px;font-size:.78rem;'
        f'color:{TEXT_MUTED}">Review Text</th>'
        f'<th style="text-align:left;border:1px solid {BORDER};'
        f'background:{CARD_ALT};padding:6px 10px;font-size:.78rem;'
        f'color:{TEXT_MUTED}">other columns...</th></tr>'
        f'<tr>{cell}This is a great product!</td>{cell}123</td></tr>'
        f'<tr>{cell}Very bad quality...</td>{cell}466</td></tr>'
        f'<tr>{cell}Average product, it\'s ok</td>{cell}789</td></tr>'
        '</table>'
    )

    return panel_html(table, "Example CSV Format", "📄")


# =========================================================
# MODEL COMPARISON
# =========================================================

def model_comparison_html(model_results, final_model):
    acc_color = ACCENT
    f1_color = METRIC_COLORS["cyan"]

    legend = (
        f'<div style="display:flex;gap:18px;margin-bottom:13px">'
        f'<span style="font-size:.82rem;color:{TEXT_MUTED}">'
        f'<span style="display:inline-block;width:10px;height:10px;'
        f'background:{acc_color};border-radius:3px;margin-right:6px"></span>'
        'Accuracy</span>'
        f'<span style="font-size:.82rem;color:{TEXT_MUTED}">'
        f'<span style="display:inline-block;width:10px;height:10px;'
        f'background:{f1_color};border-radius:3px;margin-right:6px"></span>'
        'Macro F1</span></div>'
    )

    rows = ""

    for model, results in model_results.items():
        star = (
            ' <span style="color:#C58A32;font-weight:700">★</span>'
            if model == final_model else ""
        )

        acc = results["accuracy"] * 100
        f1 = results["macro_f1"] * 100

        rows += (
            '<div style="display:flex;align-items:center;gap:13px;margin:10px 0">'
            f'<div style="width:150px;min-width:150px;font-size:.86rem;'
            f'color:{TEXT_DARK};font-weight:600">{model}{star}</div>'
            '<div style="flex:1">'
            f'<div style="height:8px;background:{BAR_BG};border-radius:999px;'
            f'margin:3px 0;overflow:hidden"><div style="width:{acc:.1f}%;'
            f'height:100%;background:{acc_color};border-radius:999px"></div></div>'
            f'<div style="height:8px;background:{BAR_BG};border-radius:999px;'
            f'overflow:hidden"><div style="width:{f1:.1f}%;height:100%;'
            f'background:{f1_color};border-radius:999px"></div></div></div>'
            f'<div style="width:115px;min-width:115px;text-align:right;'
            f'font-size:.76rem;color:{TEXT_MUTED}">'
            f'<b style="color:{acc_color}">{acc:.2f}%</b> '
            f'&middot; {f1:.2f}% F1</div></div>'
        )

    return legend + rows


# =========================================================
# ABOUT PAGE
# =========================================================

def pipeline_html(steps):
    items = ""

    for index, (icon, name) in enumerate(steps):
        connector = (
            f'<div style="flex:1;height:2px;background:{BORDER};'
            f'margin-top:29px"></div>'
            if index < len(steps) - 1 else ""
        )

        items += (
            '<div style="display:flex;flex-direction:column;align-items:center;'
            'min-width:86px">'
            f'<div style="width:56px;height:56px;border-radius:50%;'
            f'background:{SOFT_BG};border:2px solid {ACCENT};display:flex;'
            f'align-items:center;justify-content:center;font-size:1.35rem;'
            f'position:relative">{icon}'
            f'<span style="position:absolute;top:-7px;right:-7px;'
            f'background:{ACCENT};color:#fff;font-size:.65rem;font-weight:700;'
            f'width:19px;height:19px;border-radius:50%;display:flex;'
            f'align-items:center;justify-content:center">{index+1}</span></div>'
            f'<div style="margin-top:8px;font-size:.76rem;font-weight:600;'
            f'color:{TEXT_DARK};text-align:center;max-width:96px">{name}</div>'
            '</div>' + connector
        )

    return (
        '<div style="display:flex;align-items:flex-start;overflow-x:auto;'
        'padding:5px 2px;gap:4px">' + items + '</div>'
    )


def team_card_html(member):
    photo_path = member.get("photo", "")

    if photo_path and os.path.exists(photo_path):
        with open(photo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        ext = os.path.splitext(photo_path)[1].lower()
        mime = {
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }.get(ext, "image/jpeg")

        photo = (
            f'<img src="data:{mime};base64,{data}" '
            'style="width:54px;height:54px;border-radius:50%;'
            'object-fit:cover;display:block" alt="Team member photo">'
        )
    else:
        initials = "".join(
            x[0] for x in member["name"].replace("(Leader)", "").split()
        )[:2].upper()

        photo = (
            f'<div style="width:54px;height:54px;border-radius:50%;'
            f'background:{ACCENT};color:#fff;font-weight:700;font-size:1rem;'
            f'display:flex;align-items:center;justify-content:center">'
            f'{initials}</div>'
        )

    body = (
        '<div style="display:flex;align-items:center;gap:13px">'
        f'<div style="width:54px;height:54px;min-width:54px;'
        f'border-radius:50%;overflow:hidden">{photo}</div>'
        '<div>'
        f'<div style="font-weight:700;color:{TEXT_DARK}">{member["name"]}</div>'
        f'<div style="font-size:.76rem;color:{TEXT_MUTED}">ID: {member["sid"]}</div>'
        f'<div style="font-size:.78rem;color:{ACCENT};margin-top:2px">'
        f'{member["role"]}</div>'
        '</div></div>'
    )

    return panel_html(body)


def model_badge_html(model_name, model_type, is_final):
    final_chip = (
        ' <span style="background:#E9E3D0;color:#80672C;font-size:.68rem;'
        'font-weight:700;padding:3px 7px;border-radius:999px;margin-left:7px">'
        '🏆 FINAL</span>'
        if is_final else ""
    )

    type_color = (
        METRIC_COLORS["purple"]
        if model_type == "DL" else ACCENT
    )

    return (
        '<div style="display:flex;justify-content:space-between;'
        f'align-items:center;padding:8px 2px;border-bottom:1px dashed {BORDER}">'
        f'<span style="font-size:.87rem;color:{TEXT_DARK};font-weight:600">'
        f'{model_name}{final_chip}</span>'
        f'<span style="font-size:.7rem;font-weight:700;color:{type_color};'
        f'background:{type_color}18;padding:3px 8px;border-radius:999px">'
        f'{model_type}</span></div>'
    )


# =========================================================
# RESULTS TABLE
# =========================================================

def style_results_table(result_df):

    def _cell_style(value):
        color = SENTIMENT_COLORS.get(value, INVALID_COLOR)
        return f"color:{color};font-weight:600;"

    return (
        result_df.style
        .map(_cell_style, subset=["Predicted Sentiment"])
        .format(
            lambda value: f"{sentiment_emoji(value)} {value}",
            subset=["Predicted Sentiment"],
        )
    )
