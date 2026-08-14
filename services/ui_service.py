"""Shared UI helpers."""

import os
import base64
import math
import streamlit as st


# ==================================================
# Simple shared colors
# ==================================================

ACCENT = "#3B82F6"
ACCENT_LIGHT = "#60A5FA"

NAVY = "#10244F"
NAVY_2 = "#173468"

# Important:
# Custom text inherits Streamlit's current Light/Dark text color.
TEXT_DARK = "inherit"
TEXT_MUTED = "inherit"
TEXT_LIGHT = "inherit"

# Neutral transparent surfaces work in BOTH themes.
CARD = "rgba(127,127,127,0.06)"
CARD_ALT = "rgba(127,127,127,0.10)"
BORDER = "rgba(127,127,127,0.30)"
BAR_BG = "rgba(127,127,127,0.18)"
SOFT_BG = "rgba(127,127,127,0.10)"

BG = "transparent"
INPUT_BG = "transparent"


SENTIMENT_COLORS = {
    "Negative": "#D95C5C",
    "Neutral": "#D89A3A",
    "Positive": "#3F9B70",
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
    "cyan": "#4F9FB5",
    "purple": "#8069B8",
    "orange": "#D88B4A",
    "green": "#3F9B70",
    "yellow": "#D89A3A",
    "red": "#D95C5C",
}


def sentiment_color(label):
    return SENTIMENT_COLORS.get(label, INVALID_COLOR)


def sentiment_emoji(label):
    return SENTIMENT_EMOJIS.get(label, INVALID_EMOJI)


def sentiment_face(label):
    return SENTIMENT_FACES.get(label, "🙂")


def _soft(color):
    return f"color-mix(in srgb, {color} 14%, transparent)"


# ==================================================
# Small CSS only
# ==================================================

_THEME_CSS = f"""
<style>

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stMainBlockContainer"] {{
    padding-top: 2.2rem;
}}

/* Native Streamlit elements */
[data-testid="stMetric"],
[data-testid="stFileUploaderDropzone"],
[data-testid="stExpander"] {{
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

/* Sidebar selected page */
[data-testid="stSidebarNavLink"][aria-current="page"] {{
    background: {ACCENT} !important;
}}

[data-testid="stSidebarNavLink"][aria-current="page"] * {{
    color: white !important;
}}

/* Explore Application button */
[data-testid="stPageLink"] a {{
    background: {ACCENT} !important;
    border-radius: 10px !important;
    padding: .55rem 1rem;
}}

[data-testid="stPageLink"] a * {{
    color: white !important;
    font-weight: 600;
}}

</style>
"""


def apply_theme():
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def render_brand():
    st.logo("assets/logo.svg", size="large")


# ==================================================
# Header / Footer
# ==================================================

def render_page_header(title, subtitle=None):
    from config.project_data import GROUP_NAME

    sub = (
        f'<div style="opacity:.65;font-size:.95rem;margin-top:3px">'
        f'{subtitle}</div>'
        if subtitle else ""
    )

    st.markdown(
        f'<div style="text-align:right;margin-bottom:5px">'
        f'<span style="background:{NAVY};color:white;font-weight:600;'
        f'font-size:.8rem;padding:6px 12px;border-radius:999px">'
        f'🧠 {GROUP_NAME}</span></div>'

        f'<div style="font-size:1.85rem;font-weight:800">'
        f'{title}</div>'

        f'{sub}',
        unsafe_allow_html=True,
    )

    st.write("")


def render_footer():
    from config.project_data import COPYRIGHT_YEAR

    st.write("")

    st.markdown(
        f'<div style="text-align:center;opacity:.60;font-size:.78rem;'
        f'padding:16px 0 5px;border-top:1px solid {BORDER}">'
        f'© {COPYRIGHT_YEAR} ThinkLab Team. All rights reserved.</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# Panels
# ==================================================

def panel_html(body, title=None, icon=None):
    heading = (
        f'<div style="font-size:1rem;font-weight:700;'
        f'margin-bottom:11px">'
        f'{icon + " " if icon else ""}{title}</div>'
        if title else ""
    )

    return (
        f'<div style="color:inherit;'
        f'background:{CARD};'
        f'border:1px solid {BORDER};'
        f'border-radius:12px;'
        f'padding:18px 20px;'
        f'margin-bottom:13px">'
        f'{heading}{body}</div>'
    )


def stat_card_html(icon, label, value, sublabel, color):

    value_size = "1.05rem" if len(str(value)) > 18 else "1.2rem"

    return (
        f'<div style="'
        f'box-sizing:border-box;'
        f'min-height:140px;'
        f'background:{CARD};'
        f'border:1px solid {BORDER};'
        f'border-radius:12px;'
        f'padding:18px;'
        f'display:flex;'
        f'align-items:center;'
        f'gap:14px;'
        f'color:inherit;'
        f'">'

        # Icon
        f'<div style="'
        f'width:46px;'
        f'height:46px;'
        f'min-width:46px;'
        f'border-radius:11px;'
        f'background:{_soft(color)};'
        f'color:{color};'
        f'font-size:1.3rem;'
        f'display:flex;'
        f'align-items:center;'
        f'justify-content:center;'
        f'">'
        f'{icon}'
        f'</div>'

        # Text
        f'<div style="'
        f'flex:1;'
        f'min-width:120px;'
        f'">'

        f'<div style="'
        f'font-size:.78rem;'
        f'opacity:.65;'
        f'font-weight:600;'
        f'margin-bottom:5px;'
        f'">'
        f'{label}'
        f'</div>'

        f'<div style="'
        f'font-size:{value_size};'
        f'font-weight:800;'
        f'line-height:1.3;'
        f'margin-bottom:5px;'
        f'word-break:normal;'
        f'overflow-wrap:normal;'
        f'">'
        f'{value}'
        f'</div>'

        f'<div style="'
        f'font-size:.74rem;'
        f'opacity:.65;'
        f'line-height:1.3;'
        f'">'
        f'{sublabel}'
        f'</div>'

        f'</div>'
        f'</div>'
    )


def render_stat_cards(cards):

    cards_html = "".join(
        stat_card_html(*card)
        for card in cards
    )

    st.markdown(
        f'''
        <div style="
            display:grid;
            grid-template-columns:repeat(
                auto-fit,
                minmax(230px, 1fr)
            );
            gap:16px;
            width:100%;
            align-items:stretch;
        ">
            {cards_html}
        </div>
        ''',
        unsafe_allow_html=True,
    )


# ==================================================
# Donut chart
# ==================================================

def _donut_segments(parts):
    radius = 52
    circumference = 2 * math.pi * radius
    offset = 0
    circles = []

    for label, percent in parts:
        length = max(
            0,
            percent / 100 * circumference
            - (1.5 if percent else 0),
        )

        circles.append(
            f'<circle cx="70" cy="70" r="{radius}" '
            f'fill="none" '
            f'stroke="{sentiment_color(label)}" '
            f'stroke-width="16" '
            f'stroke-dasharray="{length:.2f} {circumference:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}"/>'
        )

        offset += percent / 100 * circumference

    return "".join(circles)


def donut_chart_html(parts, center_value, center_label):
    legend = ""

    for label, percent in parts:
        color = sentiment_color(label)

        legend += (
            f'<div style="display:flex;align-items:center;'
            f'gap:8px;margin:7px 0">'

            f'<span style="width:10px;height:10px;border-radius:50%;'
            f'background:{color};display:inline-block"></span>'

            f'<span style="font-size:.88rem;font-weight:600">'
            f'{label}</span>'

            f'<span style="font-size:.82rem;opacity:.60">'
            f'({percent:.1f}%)</span>'

            f'</div>'
        )

    return (
        f'<div style="display:flex;align-items:center;'
        f'gap:24px;flex-wrap:wrap;color:inherit">'

        f'<div style="position:relative;width:150px;height:150px">'

        f'<svg width="150" height="150" viewBox="0 0 140 140" '
        f'style="transform:rotate(-90deg)">'

        f'<circle cx="70" cy="70" r="52" fill="none" '
        f'stroke="{BAR_BG}" stroke-width="16"/>'

        f'{_donut_segments(parts)}'
        f'</svg>'

        f'<div style="position:absolute;inset:0;display:flex;'
        f'flex-direction:column;align-items:center;justify-content:center">'

        f'<div style="font-size:1.2rem;font-weight:800">'
        f'{center_value}</div>'

        f'<div style="font-size:.74rem;opacity:.60">'
        f'{center_label}</div>'

        f'</div></div>'

        f'<div>{legend}</div></div>'
    )


# ==================================================
# Vertical chart
# ==================================================

def vbar_chart_html(counts):
    values = [
        int(counts.get(label, 0))
        for label in SENTIMENT_COLORS
    ]

    total = sum(values)
    maximum = max(max(values, default=0), 1)
    bars = ""

    for label, value in zip(SENTIMENT_COLORS, values):
        color = sentiment_color(label)
        height = max(3, 100 * value / maximum) if value else 0
        share = 100 * value / total if total else 0

        bars += (
            f'<div style="flex:1;display:flex;flex-direction:column;'
            f'align-items:center;justify-content:flex-end;height:190px">'

            f'<div style="font-size:.84rem;font-weight:700;'
            f'color:{color}">{value:,}</div>'

            f'<div style="width:42px;'
            f'height:{190 * height / 100:.0f}px;'
            f'background:{color};border-radius:7px 7px 4px 4px;'
            f'margin:6px 0"></div>'

            f'<div style="font-size:.78rem;font-weight:600">'
            f'{label}</div>'

            f'<div style="font-size:.7rem;opacity:.60">'
            f'({share:.1f}%)</div>'

            f'</div>'
        )

    return (
        f'<div style="display:flex;align-items:flex-end;gap:18px;'
        f'padding:6px 10px 0;border-bottom:2px solid {BAR_BG};'
        f'color:inherit">{bars}</div>'
    )


def sentiment_distribution_html(counts):
    total = (
        sum(
            int(counts.get(label, 0))
            for label in SENTIMENT_COLORS
        )
        or 1
    )

    rows = ""

    for label, color in SENTIMENT_COLORS.items():
        count = int(counts.get(label, 0))
        percent = 100 * count / total
        width = max(percent, 2) if count else 0

        rows += (
            f'<div style="margin-bottom:13px">'

            f'<div style="display:flex;justify-content:space-between;'
            f'margin-bottom:5px">'

            f'<span style="font-weight:600">'
            f'{sentiment_emoji(label)} {label}</span>'

            f'<span style="font-weight:600;color:{color}">'
            f'{count} · {percent:.0f}%</span>'

            f'</div>'

            f'<div style="background:{BAR_BG};height:12px;'
            f'border-radius:999px;overflow:hidden">'

            f'<div style="width:{width:.1f}%;height:100%;'
            f'background:{color}"></div>'

            f'</div></div>'
        )

    return (
        f'<div style="color:inherit">{rows}</div>'
    )


def render_sentiment_distribution(counts):
    st.markdown(
        sentiment_distribution_html(counts),
        unsafe_allow_html=True,
    )


# ==================================================
# Prediction
# ==================================================

def _placeholder_result_html():
    return (
        f'<div style="text-align:center;padding:10px 0 16px">'

        f'<div style="width:84px;height:84px;margin:auto;'
        f'border-radius:50%;border:2px dashed {BORDER};'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-size:2rem;opacity:.35">?</div>'

        f'<div style="margin-top:12px;opacity:.65;'
        f'font-size:.92rem">'
        f'Run a prediction to see the result</div>'

        f'</div>'
    )


def result_card_html(result):
    if not result:
        return panel_html(
            _placeholder_result_html(),
            "Prediction Result",
            "🎯",
        )

    label = result["label"]
    percent = result.get("confidence", 0) * 100
    color = sentiment_color(label)

    body = (
        f'<div style="text-align:center">'

        f'<div style="width:84px;height:84px;margin:auto;'
        f'border-radius:50%;background:{_soft(color)};'
        f'border:3px solid {color};display:flex;'
        f'align-items:center;justify-content:center;'
        f'font-size:2.1rem">{sentiment_face(label)}</div>'

        f'<div style="font-size:1.45rem;font-weight:800;'
        f'color:{color};margin-top:10px">{label}</div>'

        f'<div style="font-size:.84rem;opacity:.65;'
        f'margin-top:13px">Confidence Score</div>'

        f'<div style="font-size:1.35rem;font-weight:800;'
        f'color:{color}">{percent:.2f}%</div>'

        f'<div style="background:{BAR_BG};height:9px;'
        f'border-radius:999px;margin:8px 6px 2px;overflow:hidden">'

        f'<div style="width:{percent:.1f}%;height:100%;'
        f'background:{color}"></div>'

        f'</div>'

        f'<div style="display:flex;justify-content:space-between;'
        f'font-size:.72rem;opacity:.60;margin:0 6px">'
        f'<span>0%</span><span>50%</span><span>100%</span>'
        f'</div></div>'
    )

    return panel_html(
        body,
        "Prediction Result",
        "🎯",
    )


def prob_panel_html(result):
    probabilities = (
        result["probabilities"]
        if result
        else {
            "Negative": 0,
            "Neutral": 0,
            "Positive": 0,
        }
    )

    rows = ""

    for label in ["Positive", "Neutral", "Negative"]:
        color = sentiment_color(label)
        percent = probabilities.get(label, 0) * 100

        rows += (
            f'<div style="display:flex;align-items:center;'
            f'gap:12px;margin:11px 0">'

            f'<div style="width:74px;font-size:.88rem;'
            f'font-weight:600">{label}</div>'

            f'<div style="flex:1;background:{BAR_BG};'
            f'height:9px;border-radius:999px;overflow:hidden">'

            f'<div style="width:'
            f'{max(percent, 1.2) if percent else 0:.1f}%;'
            f'height:100%;background:{color}"></div></div>'

            f'<div style="width:58px;text-align:right;'
            f'opacity:.65;font-size:.82rem;font-weight:600">'
            f'{percent:.2f}%</div>'

            f'</div>'
        )

    return panel_html(
        rows,
        "Prediction Probabilities",
        "📈",
    )


def model_info_html(model_info):
    rows = "".join(
        f'<div style="display:flex;justify-content:space-between;'
        f'padding:8px 2px;border-bottom:1px dashed {BORDER}">'

        f'<span style="opacity:.65;font-size:.86rem">'
        f'{key}</span>'

        f'<span style="font-size:.86rem;font-weight:600;'
        f'text-align:right">{value}</span>'

        f'</div>'
        for key, value in model_info.items()
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
    color = sentiment_color(label)

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:15px;'
        f'background:{_soft(color)};border:2px solid {color};'
        f'border-radius:12px;padding:15px 20px;margin:4px 0 8px;'
        f'color:inherit">'

        f'<div style="font-size:2.3rem">'
        f'{sentiment_emoji(label)}</div>'

        f'<div>'

        f'<div style="font-size:.75rem;font-weight:700;'
        f'letter-spacing:.1em;text-transform:uppercase;'
        f'opacity:.65">{heading}</div>'

        f'<div style="font-size:1.75rem;font-weight:800;'
        f'color:{color}">{label}</div>'

        f'</div></div>',
        unsafe_allow_html=True,
    )


# ==================================================
# Bulk
# ==================================================

def bulk_requirements_html(row_limit, candidates):
    lines = [
        "CSV must contain a column with the review text",
        "Supported column names: " + ", ".join(candidates),
        "File should use UTF-8 or Latin-1 encoding",
        f"Maximum {row_limit:,} reviews are processed per file",
    ]

    body = "".join(
        f'<div style="display:flex;gap:9px;margin:8px 0">'
        f'<span style="color:{METRIC_COLORS["green"]};'
        f'font-weight:800">✓</span>'
        f'<span style="font-size:.86rem">{line}</span>'
        f'</div>'
        for line in lines
    )

    return panel_html(
        body,
        "CSV Requirements",
        "📋",
    )


def example_csv_html():
    cell = (
        f'border:1px solid {BORDER};'
        f'padding:6px 10px;'
        f'font-size:.82rem'
    )

    head = (
        f'{cell};'
        f'background:{CARD_ALT};'
        f'text-align:left;'
        f'opacity:.75'
    )

    table = (
        f'<table style="border-collapse:collapse;width:100%;'
        f'color:inherit">'

        f'<tr>'
        f'<th style="{head}">Review Text</th>'
        f'<th style="{head}">other columns...</th>'
        f'</tr>'

        f'<tr>'
        f'<td style="{cell}">This is a great product!</td>'
        f'<td style="{cell}">123</td>'
        f'</tr>'

        f'<tr>'
        f'<td style="{cell}">Very bad quality...</td>'
        f'<td style="{cell}">466</td>'
        f'</tr>'

        f'<tr>'
        f'<td style="{cell}">Average product, it\'s ok</td>'
        f'<td style="{cell}">789</td>'
        f'</tr>'

        f'</table>'
    )

    return panel_html(
        table,
        "Example CSV Format",
        "📄",
    )


# ==================================================
# Model comparison
# ==================================================

def model_comparison_html(model_results, final_model):
    accuracy_color = ACCENT
    f1_color = METRIC_COLORS["cyan"]

    rows = (
        f'<div style="display:flex;gap:18px;margin-bottom:13px">'
        f'<span style="opacity:.65">'
        f'<b style="color:{accuracy_color}">■</b> Accuracy</span>'
        f'<span style="opacity:.65">'
        f'<b style="color:{f1_color}">■</b> Macro F1</span>'
        f'</div>'
    )

    for model, result in model_results.items():
        accuracy = result["accuracy"] * 100
        f1 = result["macro_f1"] * 100
        star = " ⭐" if model == final_model else ""

        rows += (
            f'<div style="display:flex;align-items:center;'
            f'gap:13px;margin:10px 0">'

            f'<div style="width:150px;font-weight:600">'
            f'{model}{star}</div>'

            f'<div style="flex:1">'

            f'<div style="height:8px;background:{BAR_BG};'
            f'border-radius:999px;margin:3px 0">'
            f'<div style="width:{accuracy:.1f}%;height:100%;'
            f'background:{accuracy_color};border-radius:999px"></div>'
            f'</div>'

            f'<div style="height:8px;background:{BAR_BG};'
            f'border-radius:999px">'
            f'<div style="width:{f1:.1f}%;height:100%;'
            f'background:{f1_color};border-radius:999px"></div>'
            f'</div></div>'

            f'<div style="width:115px;text-align:right;'
            f'font-size:.76rem;opacity:.65">'
            f'<b style="color:{accuracy_color};opacity:1">'
            f'{accuracy:.2f}%</b> · {f1:.2f}% F1'
            f'</div></div>'
        )

    return (
        f'<div style="color:inherit">{rows}</div>'
    )


# ==================================================
# About
# ==================================================

def pipeline_html(steps):
    items = ""

    for index, (icon, name) in enumerate(steps):
        connector = (
            f'<div style="flex:1;height:2px;'
            f'background:{BORDER};margin-top:29px"></div>'
            if index < len(steps) - 1
            else ""
        )

        items += (
            f'<div style="display:flex;flex-direction:column;'
            f'align-items:center;min-width:86px">'

            f'<div style="width:56px;height:56px;border-radius:50%;'
            f'background:{SOFT_BG};border:2px solid {ACCENT};'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:1.35rem;position:relative">'

            f'{icon}'

            f'<span style="position:absolute;top:-8px;right:-8px;'
            f'background:{ACCENT};color:white;font-size:.65rem;'
            f'font-weight:700;width:20px;height:20px;border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center;'
            f'z-index:2">'
            f'{index + 1}</span>'

            f'</div>'

            f'<div style="margin-top:8px;font-size:.76rem;'
            f'font-weight:600;text-align:center">'
            f'{name}</div>'

            f'</div>{connector}'
        )

    return (
        f'<div style="display:flex;align-items:flex-start;'
        f'overflow-x:auto;padding:12px 2px 5px;'
        f'gap:4px;color:inherit">'
        f'{items}</div>'
    )
def team_card_html(member):
    path = member.get("photo", "")

    if path and os.path.exists(path):
        with open(path, "rb") as image_file:
            data = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        extension = os.path.splitext(path)[1].lower()

        mime = {
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }.get(extension, "image/jpeg")

        photo = (
            f'<img src="data:{mime};base64,{data}" '
            f'style="width:54px;height:54px;'
            f'border-radius:50%;object-fit:cover;display:block">'
        )

    else:
        initials = "".join(
            part[0]
            for part in member["name"]
            .replace("(Leader)", "")
            .split()
        )[:2].upper()

        photo = (
            f'<div style="width:54px;height:54px;'
            f'border-radius:50%;background:{ACCENT};'
            f'color:white;font-weight:700;display:flex;'
            f'align-items:center;justify-content:center">'
            f'{initials}</div>'
        )

    return panel_html(
        f'<div style="display:flex;align-items:center;gap:13px">'

        f'<div style="width:54px;height:54px;min-width:54px">'
        f'{photo}</div>'

        f'<div>'

        f'<div style="font-weight:700">'
        f'{member["name"]}</div>'

        f'<div style="font-size:.76rem;opacity:.60">'
        f'ID: {member["sid"]}</div>'

        f'<div style="font-size:.78rem;color:{ACCENT}">'
        f'{member["role"]}</div>'

        f'</div></div>'
    )


def model_badge_html(
    model_name,
    model_type,
    is_final,
):
    color = (
        METRIC_COLORS["purple"]
        if model_type == "DL"
        else ACCENT
    )

    final = (
        f' <span style="color:{SENTIMENT_COLORS["Neutral"]};'
        f'background:{_soft(SENTIMENT_COLORS["Neutral"])};'
        f'padding:3px 7px;border-radius:999px;'
        f'font-size:.68rem">🏆 FINAL</span>'
        if is_final
        else ""
    )

    return (
        f'<div style="display:flex;justify-content:space-between;'
        f'align-items:center;padding:8px 2px;'
        f'border-bottom:1px dashed {BORDER};color:inherit">'

        f'<span style="font-weight:600">'
        f'{model_name}{final}</span>'

        f'<span style="color:{color};background:{_soft(color)};'
        f'padding:3px 8px;border-radius:999px;'
        f'font-size:.7rem;font-weight:700">'
        f'{model_type}</span>'

        f'</div>'
    )


# ==================================================
# Results table
# ==================================================

def style_results_table(result_df):

    def cell_style(value):
        color = SENTIMENT_COLORS.get(
            value,
            INVALID_COLOR,
        )
        return f"color:{color};font-weight:600;"

    return (
        result_df.style
        .map(
            cell_style,
            subset=["Predicted Sentiment"],
        )
        .format(
            lambda value:
                f"{sentiment_emoji(value)} {value}",
            subset=["Predicted Sentiment"],
        )
    )
