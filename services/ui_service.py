"""Shared UI helpers: theme, colors, and reusable display components."""

import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------
# Color system
# --------------------------------------------------

# Softer, more balanced sentiment colors
SENTIMENT_COLORS = {
    "Negative": "#B85C5C",   # muted red
    "Neutral": "#C58A3A",    # muted amber
    "Positive": "#3F8F6B",   # muted green
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

INVALID_COLOR = "#7A8494"
INVALID_EMOJI = "⚪"


# --------------------------------------------------
# Balanced brand palette
# --------------------------------------------------

NAVY = "#243B53"
NAVY_2 = "#334E68"

ACCENT = "#52739A"
ACCENT_LIGHT = "#7895B2"

BG = "#F4F6F8"
CARD = "#FFFFFF"
BORDER = "#D9E1E8"

TEXT_DARK = "#243B53"
TEXT_MUTED = "#64748B"

METRIC_COLORS = {
    "blue": "#52739A",
    "cyan": "#4F8C9E",
    "purple": "#756C9A",
    "orange": "#B87945",
    "green": "#3F8F6B",
    "yellow": "#C58A3A",
    "red": "#B85C5C",
}


def sentiment_color(label):
    """Hex color for a sentiment label (grey for anything unknown)."""
    return SENTIMENT_COLORS.get(label, INVALID_COLOR)


def sentiment_emoji(label):
    """Color-coded circle emoji for a sentiment label."""
    return SENTIMENT_EMOJIS.get(label, INVALID_EMOJI)


def sentiment_face(label):
    """Face emoji for a sentiment label."""
    return SENTIMENT_FACES.get(label, "🙂")


# --------------------------------------------------
# Theme (injected once per page)
# --------------------------------------------------

_THEME_CSS = """
<style>

/* ---------- App background ---------- */

[data-testid="stAppViewContainer"] {
    background: #F4F6F8;
}

[data-testid="stHeader"] {
    background: rgba(244,246,248,0.0);
}

[data-testid="stMainBlockContainer"] {
    padding-top: 4.3rem;
}

body.tl-sidebar-open [data-testid="stMainBlockContainer"] {
    padding-top: 2.2rem;
}


/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #243B53 0%,
        #334E68 100%
    );
    border-right: none;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #D7E0E8;
}


/* ---------- Navigation links ---------- */

[data-testid="stSidebarNavLink"] {
    border-radius: 10px;
    margin: 2px 6px;
    padding: 0.55rem 0.9rem;
    transition: background 0.15s ease;
}

[data-testid="stSidebarNavLink"] span {
    color: #D7E0E8;
    font-weight: 500;
}

[data-testid="stSidebarNavLink"]:hover {
    background: rgba(255,255,255,0.08);
}

[data-testid="stSidebarNavLink"][aria-current="page"],
[data-testid="stSidebarNavLink"].active {
    background: #52739A;
    box-shadow: 0 6px 16px rgba(36,59,83,0.25);
}

[data-testid="stSidebarNavLink"][aria-current="page"] span,
[data-testid="stSidebarNavLink"].active span {
    color: #FFFFFF !important;
    font-weight: 700;
}


/* ---------- Sidebar collapse buttons ---------- */

section[data-testid="stSidebar"] button svg {
    fill: #D7E0E8;
}


/* ---------- Buttons ---------- */

div[data-testid="stButton"] > button[kind="primary"] {
    background: #52739A;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.2rem;
    box-shadow: 0 5px 12px rgba(36,59,83,0.18);
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #456784;
    box-shadow: 0 7px 16px rgba(36,59,83,0.24);
}

div[data-testid="stButton"] > button[kind="secondary"],
div[data-testid="stDownloadButton"] > button {
    background: #FFFFFF;
    border: 1px solid #D9E1E8;
    border-radius: 10px;
    color: #243B53;
    font-weight: 500;
}

div[data-testid="stDownloadButton"] > button[kind="primary"] {
    background: #52739A;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    box-shadow: 0 5px 12px rgba(36,59,83,0.18);
}


/* ---------- File uploader ---------- */

[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF;
    border: 2px dashed #AEBBC7;
    border-radius: 16px;
    min-height: 160px;
    align-items: center;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
    padding: 16px 12px;
}

[data-testid="stFileUploaderDropzone"] > section {
    width: 100%;
}

[data-testid="stFileUploaderDropzone"] > div {
    width: 100%;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] > div,
[data-testid="stFileUploaderDropzoneInstructions"] span {
    width: 100%;
    text-align: center !important;
    justify-content: center !important;
    display: flex !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #52739A;
}


/* Mockup-style uploader instructions */

[data-testid="stFileUploaderDropzone"]::before {
    content: "☁️\\A Drag and drop your CSV file here\\A or click to browse";
    white-space: pre-line;
    display: block;
    width: 100%;
    text-align: center;
    color: #52739A;
    font-weight: 600;
    font-size: 1rem;
    line-height: 2.0;
}

[data-testid="stFileUploaderDropzone"]::after {
    content: "Supports: .csv files";
    display: block;
    width: 100%;
    text-align: center;
    color: #7A8794;
    font-size: 0.78rem;
    line-height: 2.2;
}


/* ---------- Page link CTA ---------- */

[data-testid="stPageLink"] a {
    background: #52739A;
    border-radius: 10px !important;
    box-shadow: 0 5px 12px rgba(36,59,83,0.18);
    padding: 0.6rem 1.1rem;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #FFFFFF !important;
    font-weight: 600;
}


/* ---------- Metrics ---------- */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #D9E1E8;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 1px 3px rgba(36,59,83,0.05);
}


/* ---------- Dataframes ---------- */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* ---------- Collapsible sidebar + top-left brand bar ---------- */

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"] {
    display: none !important;
}


/* ---------- Floating brand bar ---------- */

#tl-topbar {
    position: fixed;
    top: 10px;
    left: 12px;
    z-index: 999997;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #FFFFFF;
    border: 1px solid #D9E1E8;
    border-radius: 12px;
    padding: 6px 14px 6px 8px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(36,59,83,0.12);
    user-select: none;
    -webkit-user-select: none;
    transition: box-shadow 0.15s ease, transform 0.15s ease;
}

#tl-topbar:hover {
    box-shadow: 0 7px 18px rgba(36,59,83,0.20);
    transform: translateY(-1px);
}

body.tl-sidebar-open #tl-topbar {
    display: none !important;
}

</style>
"""


# --------------------------------------------------
# Top-left brand bar
# --------------------------------------------------

_TOPBAR_HTML = """
<div id="tl-topbar" role="button" tabindex="0" title="Open menu"
     aria-label="Open navigation menu">

  <svg width="30" height="30" viewBox="0 0 48 48"
       xmlns="http://www.w3.org/2000/svg" style="flex:none;">

    <rect x="2" y="2" width="44" height="44" rx="12" fill="#52739A"/>

    <circle cx="15" cy="19" r="4.2" fill="#FFFFFF"/>
    <circle cx="29" cy="19" r="4.2" fill="#FFFFFF"/>

    <path d="M12 29 Q22 36 32 29"
          stroke="#FFFFFF"
          stroke-width="3.4"
          fill="none"
          stroke-linecap="round"/>
  </svg>

  <span style="font-weight:700; font-size:0.92rem; color:#243B53;
        white-space:nowrap;">
        NLP Sentiment Analyzer
  </span>

  <span style="color:#52739A; font-size:1.1rem; margin-left:6px;
        line-height:1;">
        &#9776;
  </span>

</div>
"""


# st.markdown does NOT execute <script> tags, so the interaction logic is
# delivered through a (height-0) component iframe.

_TOPBAR_COMPONENT = """
<script>
(function () {

  var parentCode = function () {

    var D = document;

    var SIDEBAR_SEL = 'section[data-testid="stSidebar"]';


    window.__tlSync = function () {

      try {

        var sb = D.querySelector(SIDEBAR_SEL);

        var open = sb
          ? sb.getAttribute('aria-expanded') !== 'false'
          : false;

        if (D.body) {

          D.body.classList.toggle(
            'tl-sidebar-open',
            open
          );

          D.body.classList.toggle(
            'tl-sidebar-closed',
            !open
          );
        }


        var bars = D.querySelectorAll('#tl-topbar');

        for (var i = 1; i < bars.length; i++) {
          bars[i].remove();
        }

      } catch (e) {}

    };


    function nativeToggle() {

      var sb = D.querySelector(SIDEBAR_SEL);

      var open = sb
        ? sb.getAttribute('aria-expanded') !== 'false'
        : false;

      if (open) {
        return D.querySelector(
          '[data-testid="stSidebarCollapseButton"]'
        );
      }

      return (

        D.querySelector(
          'button[data-testid="stExpandSidebarButton"]'
        )

        ||

        D.querySelector(
          '[data-testid="stSidebarCollapsedControl"] button'
        )

        ||

        D.querySelector(
          '[data-testid="collapsedControl"] button'
        )

        ||

        D.querySelector(
          'button[aria-label="Open sidebar"]'
        )

      );
    }


    D.addEventListener(
      'click',
      function (ev) {

        var t = ev.target;

        if (!t || !t.closest) return;


        if (t.closest('#tl-topbar')) {

          ev.preventDefault();

          var btn = nativeToggle();

          if (btn) btn.click();

          setTimeout(
            window.__tlSync,
            150
          );

          setTimeout(
            window.__tlSync,
            500
          );

          return;
        }


        if (
          t.closest(
            '[data-testid="stSidebarCollapseButton"]'
          )
        ) {

          setTimeout(
            window.__tlSync,
            150
          );

          setTimeout(
            window.__tlSync,
            500
          );
        }

      },
      true
    );


    var mo = new MutationObserver(
      function () {
        window.__tlSync();
      }
    );


    mo.observe(
      D.documentElement,
      {
        attributes: true,
        attributeFilter: ['aria-expanded'],
        subtree: true
      }
    );


    window.__tlSync();

  };


  var W;

  try {
    W = window.parent;
  } catch (e) {
    return;
  }

  if (!W) return;

  try {
    if (!W.document) return;
  } catch (e) {
    return;
  }


  try {

    var bars =
      W.document.querySelectorAll('#tl-topbar');

    for (var i = 1; i < bars.length; i++) {
      bars[i].remove();
    }

  } catch (e) {}


  if (!W.__tlTopbarInit) {

    W.__tlTopbarInit = true;

    W.eval(
      '(' + parentCode.toString() + ')();'
    );

  } else if (
    typeof W.__tlSync === 'function'
  ) {

    W.__tlSync();

  }

})();
</script>
"""


# --------------------------------------------------
# Theme functions
# --------------------------------------------------

def apply_theme():
    """Inject the app-wide CSS theme + sidebar-opening brand bar."""
    st.markdown(
        _THEME_CSS + _TOPBAR_HTML,
        unsafe_allow_html=True,
    )

    components.html(
        _TOPBAR_COMPONENT,
        height=0,
    )


def render_brand():
    """Render the app logo at the top of the sidebar."""
    st.logo(
        "assets/logo.svg",
        size="large",
    )


def render_page_header(title, subtitle=None):
    """Big page title + optional subtitle + top-right group chip."""

    from config.project_data import GROUP_NAME

    chip = (
        '<div style="display:flex; justify-content:flex-end; '
        'margin-top:-1.4rem; margin-bottom:0.4rem;">'

        f'<span style="background:{NAVY}; color:#FFFFFF; '
        'font-weight:600; font-size:0.85rem; padding:7px 14px; '
        'border-radius:999px; '
        'box-shadow:0 4px 10px rgba(36,59,83,0.20);">'

        f'🧠 {GROUP_NAME}'

        '</span></div>'
    )


    sub = (

        f'<div style="color:{TEXT_MUTED}; '
        'font-size:1.0rem; margin-top:2px;">'
        f"{subtitle}</div>"

        if subtitle

        else ""

    )


    st.markdown(
        chip
        + f'<div style="font-size:1.9rem; font-weight:800; '
          f'color:{TEXT_DARK}; margin-bottom:2px;">'
          f'{title}</div>'
        + sub,
        unsafe_allow_html=True,
    )

    st.write("")


def render_footer():
    """Shared footer line."""

    from config.project_data import (
        COURSE,
        COPYRIGHT_YEAR,
        GROUP_NAME,
    )

    st.write("")

    st.markdown(
        f'<div style="text-align:center; '
        f'color:{TEXT_MUTED}; font-size:0.8rem; '
        f'padding:18px 0 6px 0; '
        f'border-top:1px solid {BORDER};">'
        f"© {COPYRIGHT_YEAR} {GROUP_NAME} | {COURSE}"
        '</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# White panel building blocks
# --------------------------------------------------

def panel_html(body, title=None, icon=None):
    """Wrap content in the app's white rounded card."""

    heading = ""

    if title:

        heading = (
            f'<div style="font-size:1.05rem; '
            f'font-weight:700; color:{TEXT_DARK}; '
            'margin-bottom:12px;">'

            + (f"{icon} " if icon else "")

            + title

            + "</div>"
        )


    return (
        f'<div style="background:{CARD}; '
        f'border:1px solid {BORDER}; '
        'border-radius:16px; padding:20px 22px; '
        'box-shadow:0 1px 3px rgba(36,59,83,0.05); '
        'margin-bottom:14px;">'

        f"{heading}{body}"

        '</div>'
    )


def stat_card_html(
    icon,
    label,
    value,
    sublabel,
    color,
):
    """Metric stat card."""

    return panel_html(

        '<div style="display:flex; '
        'align-items:center; gap:14px;">'

        f'<div style="width:46px; height:46px; '
        f'min-width:46px; border-radius:12px; '
        f'background:{color}1A; color:{color}; '
        'font-size:1.35rem; display:flex; '
        'align-items:center; justify-content:center;">'
        f'{icon}</div>'

        '<div>'

        f'<div style="font-size:0.8rem; '
        f'color:{TEXT_MUTED}; font-weight:600;">'
        f'{label}</div>'

        f'<div style="font-size:1.25rem; '
        f'font-weight:800; color:{TEXT_DARK}; '
        'line-height:1.25;">'
        f'{value}</div>'

        f'<div style="font-size:0.75rem; '
        f'color:{TEXT_MUTED};">'
        f'{sublabel}</div>'

        '</div></div>'
    )


def render_stat_cards(cards):
    """Render a row of stat cards."""

    cols = st.columns(len(cards))

    for col, card in zip(cols, cards):

        with col:

            st.markdown(
                stat_card_html(*card),
                unsafe_allow_html=True,
            )


# --------------------------------------------------
# Sentiment charts
# --------------------------------------------------

def _donut_segments(parts):
    """Build SVG circle segments for a donut chart."""

    import math

    radius = 52

    circumference = (
        2 * math.pi * radius
    )

    gap = 1.5

    segments = []

    offset = 0.0


    for label, percent in parts:

        length = max(
            0.0,
            (
                percent / 100.0
            ) * circumference
            - (
                gap if percent > 0 else 0
            ),
        )

        color = sentiment_color(label)


        segments.append(

            f'<circle cx="70" cy="70" '
            f'r="{radius}" fill="none" '
            f'stroke="{color}" '
            'stroke-width="16" '
            f'stroke-dasharray="{length:.2f} '
            f'{circumference:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" '
            'stroke-linecap="butt"/>'

        )


        offset += (
            percent / 100.0
        ) * circumference


    return "".join(segments)


def donut_chart_html(
    parts,
    center_value,
    center_label,
):
    """Donut chart with legend."""

    body = (

        '<div style="display:flex; '
        'align-items:center; gap:26px; '
        'flex-wrap:wrap;">'

        '<div style="position:relative; '
        'width:150px; height:150px; '
        'min-width:150px;">'

        '<svg width="150" height="150" '
        'viewBox="0 0 140 140" '
        'style="transform:rotate(-90deg);">'

        '<circle cx="70" cy="70" r="52" '
        'fill="none" stroke="#E8EDF2" '
        'stroke-width="16"/>'

        + _donut_segments(parts)

        + "</svg>"

        '<div style="position:absolute; inset:0; '
        'display:flex; flex-direction:column; '
        'align-items:center; justify-content:center;">'

        f'<div style="font-size:1.25rem; '
        f'font-weight:800; color:{TEXT_DARK};">'
        f'{center_value}</div>'

        f'<div style="font-size:0.75rem; '
        f'color:{TEXT_MUTED};">'
        f'{center_label}</div>'

        '</div></div>'

        '<div>'
    )


    for label, percent in parts:

        color = sentiment_color(label)

        body += (

            '<div style="display:flex; '
            'align-items:center; gap:8px; '
            'margin:7px 0;">'

            f'<span style="width:11px; '
            'height:11px; border-radius:50%; '
            f'background:{color}; '
            'display:inline-block;"></span>'

            f'<span style="font-size:0.9rem; '
            f'color:{TEXT_DARK}; font-weight:600;">'
            f'{label}</span>'

            f'<span style="font-size:0.85rem; '
            f'color:{TEXT_MUTED};">'
            f'({percent:.1f}%)</span>'

            '</div>'
        )


    body += "</div></div>"

    return body


def vbar_chart_html(counts):
    """Vertical sentiment bar chart."""

    values = [
        int(counts.get(label, 0))
        for label in SENTIMENT_COLORS
    ]

    total = sum(values)

    max_value = (
        max(values)
        if values
        else 1
    )

    max_value = max(
        max_value,
        1,
    )


    bars = ""


    for label, value in zip(
        SENTIMENT_COLORS,
        values,
    ):

        color = sentiment_color(label)

        height_pct = (
            max(
                3.0,
                100.0 * value / max_value,
            )
            if value
            else 0.0
        )

        share = (
            100.0 * value / total
            if total
            else 0.0
        )


        bars += (

            '<div style="flex:1; '
            'display:flex; flex-direction:column; '
            'align-items:center; '
            'justify-content:flex-end; '
            'height:190px;">'

            f'<div style="font-size:0.85rem; '
            f'font-weight:700; color:{color};">'
            f'{value:,}</div>'

            f'<div style="width:44px; '
            f'height:{190 * height_pct / 100.0:.0f}px; '
            f'background:{color}; '
            'border-radius:8px 8px 4px 4px; '
            'margin:6px 0;">'
            '</div>'

            f'<div style="font-size:0.8rem; '
            f'color:{TEXT_MUTED}; '
            'font-weight:600;">'
            f'{label}</div>'

            f'<div style="font-size:0.72rem; '
            f'color:{TEXT_MUTED};">'
            f'({share:.1f}%)</div>'

            '</div>'
        )


    return (

        '<div style="display:flex; '
        'align-items:flex-end; gap:18px; '
        'padding:6px 10px 0 10px; '
        'border-bottom:2px solid #E8EDF2;">'

        + bars

        + "</div>"
    )


def sentiment_distribution_html(counts):
    """Color-coded horizontal bars for bulk distribution."""

    total = sum(
        int(counts.get(label, 0))
        for label in SENTIMENT_COLORS
    )

    safe_total = (
        total
        if total > 0
        else 1
    )

    bars = []


    for label, color in SENTIMENT_COLORS.items():

        count = int(
            counts.get(label, 0)
        )

        percent = (
            100.0 * count / safe_total
        )

        bar_width = (
            max(percent, 2.0)
            if count
            else 0.0
        )


        bars.append(

            f'<div style="margin-bottom:14px;">'

            '<div style="display:flex; '
            'justify-content:space-between; '
            'margin-bottom:5px;">'

            '<span style="font-weight:600;">'
            f'{SENTIMENT_EMOJIS[label]} {label}'
            '</span>'

            f'<span style="font-weight:600; '
            f'color:{color};">'
            f'{count} &middot; {percent:.0f}%'
            '</span>'

            '</div>'

            '<div style="background:#E8EDF2; '
            'border-radius:999px; height:14px; '
            'overflow:hidden;">'

            f'<div style="width:{bar_width:.1f}%; '
            f'height:100%; background:{color}; '
            'border-radius:999px;"></div>'

            '</div></div>'
        )


    return (

        '<div style="margin-top:6px; '
        'margin-bottom:10px;">'

        + "".join(bars)

        + "</div>"
    )


def render_sentiment_distribution(counts):

    st.markdown(
        sentiment_distribution_html(counts),
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Single prediction panels
# --------------------------------------------------

def _placeholder_result_html():

    return (

        '<div style="text-align:center; '
        'padding:10px 0 16px 0;">'

        '<div style="width:84px; height:84px; '
        'margin:0 auto; border-radius:50%; '
        'border:2px dashed #B8C2CC; '
        'display:flex; align-items:center; '
        'justify-content:center; '
        'font-size:2rem; color:#B8C2CC;">'
        '?'
        '</div>'

        f'<div style="margin-top:12px; '
        f'color:{TEXT_MUTED}; '
        'font-size:0.95rem;">'
        'Run a prediction to see the result'
        '</div>'

        '</div>'
    )


def result_card_html(result):
    """Prediction result panel."""

    if not result:

        return panel_html(
            _placeholder_result_html(),
            "Prediction Result",
            "🎯",
        )


    label = result["label"]

    confidence = result.get(
        "confidence",
        0.0,
    )

    color = sentiment_color(label)

    face = sentiment_face(label)

    pct = confidence * 100.0


    body = (

        '<div style="text-align:center;">'

        '<div style="width:84px; height:84px; '
        'margin:0 auto; border-radius:50%; '

        f'background:{color}1A; '
        f'border:3px solid {color}; '

        'display:flex; '
        'align-items:center; '
        'justify-content:center; '
        'font-size:2.1rem;">'

        f'{face}'

        '</div>'

        f'<div style="font-size:1.5rem; '
        f'font-weight:800; color:{color}; '
        'margin-top:10px;">'

        f'{label}'

        '</div>'

        f'<div style="color:{TEXT_MUTED}; '
        'font-size:0.85rem; '
        'margin-top:14px;">'

        'Confidence Score'

        '</div>'

        f'<div style="font-size:1.4rem; '
        f'font-weight:800; color:{color};">'

        f'{pct:.2f}%'

        '</div>'

        '<div style="background:#E8EDF2; '
        'border-radius:999px; height:9px; '
        'margin:8px 6px 2px 6px; '
        'overflow:hidden;">'

        f'<div style="width:{pct:.1f}%; '
        f'height:100%; background:{color}; '
        'border-radius:999px;"></div>'

        '</div>'

        f'<div style="display:flex; '
        'justify-content:space-between; '
        f'font-size:0.72rem; '
        f'color:{TEXT_MUTED}; '
        'margin:0 6px;">'

        '<span>0%</span>'
        '<span>50%</span>'
        '<span>100%</span>'

        '</div>'

        '</div>'
    )


    return panel_html(
        body,
        "Prediction Result",
        "🎯",
    )


def prob_panel_html(result):
    """Prediction probabilities panel."""

    if result:

        probs = result["probabilities"]

    else:

        probs = {
            "Negative": 0.0,
            "Neutral": 0.0,
            "Positive": 0.0,
        }


    order = [
        "Positive",
        "Neutral",
        "Negative",
    ]

    rows = ""


    for label in order:

        color = sentiment_color(label)

        pct = (
            probs.get(label, 0.0)
            * 100.0
        )


        rows += (

            '<div style="display:flex; '
            'align-items:center; gap:12px; '
            'margin:12px 0;">'

            f'<div style="width:74px; '
            f'color:{TEXT_DARK}; '
            'font-size:0.9rem; '
            'font-weight:600;">'
            f'{label}</div>'

            '<div style="flex:1; '
            'background:#E8EDF2; '
            'border-radius:999px; '
            'height:9px; '
            'overflow:hidden;">'

            f'<div style="width:'
            f'{max(pct, 1.2) if pct else 0:.1f}%; '
            f'height:100%; background:{color}; '
            'border-radius:999px;"></div>'

            '</div>'

            f'<div style="width:58px; '
            'text-align:right; '
            f'color:{TEXT_MUTED}; '
            'font-size:0.85rem; '
            'font-weight:600;">'
            f'{pct:.2f}%</div>'

            '</div>'
        )


    return panel_html(
        rows,
        "Prediction Probabilities",
        "📈",
    )


def model_info_html(model_info):
    """Model information panel."""

    rows = ""


    for key, value in model_info.items():

        rows += (

            '<div style="display:flex; '
            'justify-content:space-between; '
            'padding:8px 2px; '
            'border-bottom:1px dashed #D9E1E8;">'

            f'<span style="color:{TEXT_MUTED}; '
            'font-size:0.88rem;">'
            f'{key}</span>'

            f'<span style="color:{TEXT_DARK}; '
            'font-size:0.88rem; '
            'font-weight:600; '
            'text-align:right;">'
            f'{value}</span>'

            '</div>'
        )


    return panel_html(
        rows,
        "Model Information",
        "🤖",
    )


def render_sentiment_result(
    label,
    heading="Predicted Sentiment",
):
    """Compact color-coded banner."""

    color = sentiment_color(label)

    emoji = sentiment_emoji(label)


    html = (

        '<div style="display:flex; '
        'align-items:center; gap:16px; '

        f'background:{color}1A; '
        f'border:2px solid {color}; '

        'border-radius:14px; '
        'padding:16px 22px; '
        'margin:4px 0 8px 0;">'

        f'<div style="font-size:2.4rem; '
        'line-height:1;">'
        f'{emoji}</div>'

        '<div style="line-height:1.2;">'

        '<div style="font-size:0.78rem; '
        'font-weight:700; '
        'letter-spacing:0.12em; '
        'text-transform:uppercase; '
        'opacity:0.65;">'

        f'{heading}'

        '</div>'

        f'<div style="font-size:1.8rem; '
        f'font-weight:800; color:{color};">'

        f'{label}'

        '</div>'

        '</div></div>'
    )


    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Bulk page static blocks
# --------------------------------------------------

def bulk_requirements_html(
    row_limit,
    candidates,
):

    checks = "".join(

        f'<div style="display:flex; '
        'gap:9px; margin:9px 0; '
        'align-items:flex-start;">'

        f'<span style="color:{METRIC_COLORS["green"]}; '
        'font-weight:800;">✓</span>'

        f'<span style="font-size:0.88rem; '
        f'color:{TEXT_DARK};">'
        f'{line}</span>'

        '</div>'

        for line in [

            "CSV must contain a column with the review text",

            "Supported column names: "
            + ", ".join(candidates),

            "File should use UTF-8 or Latin-1 encoding",

            f"Maximum {row_limit:,} reviews are processed per file",

        ]
    )


    return panel_html(
        f'<div style="color:{TEXT_DARK};">'
        f'{checks}</div>',
        "CSV Requirements",
        "📋",
    )


def example_csv_html():

    row = (

        '<td style="border:1px solid #D9E1E8; '
        'padding:6px 10px; '
        'font-size:0.84rem;'

        f' color:{TEXT_DARK};">'
    )


    table = (

        '<table style="border-collapse:collapse; '
        'width:100%; margin-top:2px;">'

        '<tr>'

        f'<th style="text-align:left; '
        'border:1px solid #D9E1E8; '
        'background:#F4F6F8; '
        'padding:6px 10px; '
        'font-size:0.8rem; '
        f'color:{TEXT_MUTED};">'
        'Review Text</th>'

        f'<th style="text-align:left; '
        'border:1px solid #D9E1E8; '
        'background:#F4F6F8; '
        'padding:6px 10px; '
        'font-size:0.8rem; '
        f'color:{TEXT_MUTED};">'
        'other columns...</th>'

        '</tr>'

        f'<tr>{row}'
        'This is a great product!</td>'
        f'{row}123</td></tr>'

        f'<tr>{row}'
        'Very bad quality...</td>'
        f'{row}466</td></tr>'

        f'<tr>{row}'
        "Average product, it's ok</td>"
        f'{row}789</td></tr>'

        '</table>'
    )


    return panel_html(
        table,
        "Example CSV Format",
        "📄",
    )


# --------------------------------------------------
# Dashboard components
# --------------------------------------------------

def model_comparison_html(
    model_results,
    final_model,
):
    """Grouped horizontal bars: accuracy vs macro F1."""

    acc_color = ACCENT

    f1_color = METRIC_COLORS["cyan"]


    legend = (

        '<div style="display:flex; '
        'gap:20px; margin-bottom:14px;">'

        f'<span style="font-size:0.85rem; '
        f'color:{TEXT_MUTED};">'

        '<span style="display:inline-block; '
        'width:11px; height:11px; '

        f'background:{acc_color}; '
        'border-radius:3px; '
        'margin-right:6px;">'
        '</span>'

        'Accuracy</span>'

        f'<span style="font-size:0.85rem; '
        f'color:{TEXT_MUTED};">'

        '<span style="display:inline-block; '
        'width:11px; height:11px; '

        f'background:{f1_color}; '
        'border-radius:3px; '
        'margin-right:6px;">'
        '</span>'

        'Macro F1</span>'

        '</div>'
    )


    rows = ""


    for model, results in model_results.items():

        star = (

            f' <span style="color:#B87945; '
            'font-weight:700;">★</span>'

            if model == final_model

            else ""
        )


        acc = (
            results["accuracy"]
            * 100.0
        )

        f1 = (
            results["macro_f1"]
            * 100.0
        )


        rows += (

            '<div style="display:flex; '
            'align-items:center; gap:14px; '
            'margin:11px 0;">'

            f'<div style="width:150px; '
            'min-width:150px; '
            'font-size:0.88rem; '
            f'color:{TEXT_DARK}; '
            'font-weight:600;">'
            f'{model}{star}</div>'

            '<div style="flex:1;">'

            '<div style="height:9px; '
            'background:#E8EDF2; '
            'border-radius:999px; '
            'margin:3px 0; '
            'overflow:hidden;">'

            f'<div style="width:{acc:.1f}%; '
            f'height:100%; '
            f'background:{acc_color}; '
            'border-radius:999px;">'
            '</div>'

            '</div>'

            '<div style="height:9px; '
            'background:#E8EDF2; '
            'border-radius:999px; '
            'overflow:hidden;">'

            f'<div style="width:{f1:.1f}%; '
            'height:100%; '
            f'background:{f1_color}; '
            'border-radius:999px;">'
            '</div>'

            '</div>'

            '</div>'

            f'<div style="width:118px; '
            'min-width:118px; '
            'text-align:right; '
            'font-size:0.78rem; '
            f'color:{TEXT_MUTED};">'

            f"<b style='color:{acc_color};'>"
            f'{acc:.2f}%</b> &middot; '

            f'{f1:.2f}% F1'

            '</div>'

            '</div>'
        )


    return legend + rows


# --------------------------------------------------
# About page components
# --------------------------------------------------

def pipeline_html(steps):
    """Horizontal step pipeline with connectors."""

    items = ""


    for index, (icon, name) in enumerate(steps):

        connector = (

            ""

            if index == len(steps) - 1

            else (

                '<div style="flex:1; height:3px; '
                'background:repeating-linear-gradient('
                '90deg,#B8C5D1 0 6px,'
                'transparent 6px 12px); '
                'align-self:flex-start; '
                'margin-top:30px;"></div>'
            )
        )


        items += (

            '<div style="display:flex; '
            'flex-direction:column; '
            'align-items:center; '
            'min-width:86px;">'

            f'<div style="width:58px; '
            'height:58px; '
            'border-radius:50%; '
            'background:#E9EEF3; '
            f'border:2px solid {ACCENT}; '
            'display:flex; '
            'align-items:center; '
            'justify-content:center; '
            'font-size:1.4rem; '
            'position:relative;">'

            f'{icon}'

            f'<span style="position:absolute; '
            'top:-8px; right:-8px; '
            f'background:{ACCENT}; '
            'color:#fff; '
            'font-size:0.68rem; '
            'font-weight:700; '
            'width:20px; height:20px; '
            'border-radius:50%; '
            'display:flex; '
            'align-items:center; '
            'justify-content:center;">'
            f'{index + 1}</span>'

            '</div>'

            f'<div style="margin-top:9px; '
            'font-size:0.78rem; '
            'font-weight:600; '
            f'color:{TEXT_DARK}; '
            'text-align:center; '
            'max-width:96px;">'
            f'{name}</div>'

            '</div>'

            + connector
        )


    return (

        '<div style="display:flex; '
        'align-items:flex-start; '
        'overflow-x:auto; '
        'padding:6px 2px; '
        'gap:4px;">'

        + items

        + '</div>'
    )


def team_card_html(member):

    initials = "".join(
        part[0]
        for part in member["name"].split()
    )[:2].upper()


    return panel_html(

        '<div style="display:flex; '
        'align-items:center; gap:14px;">'

        f'<div style="width:52px; '
        'height:52px; '
        'min-width:52px; '
        'border-radius:50%; '

        f'background:linear-gradient(135deg,'
        f'{ACCENT},{METRIC_COLORS["purple"]}); '

        'color:#FFFFFF; '
        'font-weight:700; '
        'font-size:1.05rem; '
        'display:flex; '
        'align-items:center; '
        'justify-content:center;">'

        f'{initials}'

        '</div>'

        '<div>'

        f'<div style="font-weight:700; '
        f'color:{TEXT_DARK};">'
        f'{member["name"]}</div>'

        f'<div style="font-size:0.78rem; '
        f'color:{TEXT_MUTED};">'
        f'ID: {member["sid"]}</div>'

        f'<div style="font-size:0.8rem; '
        f'color:{ACCENT}; '
        'margin-top:2px;">'
        f'{member["role"]}</div>'

        '</div></div>'
    )


def model_badge_html(
    model_name,
    model_type,
    is_final,
):

    final_chip = (

        ' <span style="background:#F4E8D4; '
        'color:#8A642F; '
        'font-size:0.7rem; '
        'font-weight:700; '
        'padding:3px 8px; '
        'border-radius:999px; '
        'margin-left:8px;">'
        '🏆 FINAL</span>'

        if is_final

        else ""
    )


    type_color = (
        METRIC_COLORS["purple"]
        if model_type == "DL"
        else ACCENT
    )


    return (

        '<div style="display:flex; '
        'justify-content:space-between; '
        'align-items:center; '
        'padding:9px 2px; '
        'border-bottom:1px dashed #D9E1E8;">'

        f'<span style="font-size:0.9rem; '
        f'color:{TEXT_DARK}; '
        'font-weight:600;">'

        f'{model_name}{final_chip}'

        '</span>'

        f'<span style="font-size:0.72rem; '
        f'font-weight:700; '
        f'color:{type_color}; '
        f'background:{type_color}18; '
        'padding:3px 9px; '
        'border-radius:999px;">'

        f'{model_type}'

        '</span>'

        '</div>'
    )


# --------------------------------------------------
# Results table styling
# --------------------------------------------------

def style_results_table(result_df):
    """Color-code the Predicted Sentiment column."""

    def _cell_style(value):

        color = (

            SENTIMENT_COLORS[value]

            if value in SENTIMENT_COLORS

            else INVALID_COLOR
        )

        return (
            f"color: {color}; "
            "font-weight: 600;"
        )


    return (

        result_df.style.map(
            _cell_style,
            subset=["Predicted Sentiment"],
        )

        .format(
            lambda value:
                f"{sentiment_emoji(value)} {value}",
            subset=["Predicted Sentiment"],
        )
    )
