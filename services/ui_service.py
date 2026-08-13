"""Shared UI helpers for the Streamlit app."""

import os
import base64
import math
import streamlit as st


# ==================================================
# Theme-aware colors
# ==================================================

ACCENT = "var(--st-primary-color)"
BG = "var(--st-background-color)"
CARD = "var(--st-secondary-background-color)"
TEXT_DARK = "var(--st-text-color)"
TEXT_MUTED = "var(--st-gray-text-color)"
BORDER = "var(--st-border-color)"

NAVY = "#10244F"
NAVY_2 = "#173468"
ACCENT_LIGHT = "#60A5FA"

CARD_ALT = (
    "color-mix(in srgb, "
    "var(--st-secondary-background-color) 92%, "
    "var(--st-text-color) 8%)"
)

SOFT_BG = (
    "color-mix(in srgb, "
    "var(--st-primary-color) 10%, "
    "var(--st-background-color))"
)

BAR_BG = (
    "color-mix(in srgb, "
    "var(--st-text-color) 12%, transparent)"
)

# Keep old names if another page imports them.
TEXT_LIGHT = TEXT_DARK
INPUT_BG = CARD


# ==================================================
# Sentiment
# ==================================================

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


def _soft(color, amount=14):
    return f"color-mix(in srgb, {color} {amount}%, transparent)"


# ==================================================
# App theme
# ==================================================

_THEME_CSS = """
<style>
[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2.2rem;
}

[data-testid="stMetric"],
[data-testid="stFileUploaderDropzone"],
[data-testid="stExpander"] {
    border-radius: 12px;
}

[data-testid="stPageLink"] a {
    border-radius: 10px !important;
}
</style>
"""


def apply_theme():
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def render_brand():
    st.logo("assets/logo.svg", size="large")


# ==================================================
# Header / footer
# ==================================================

def render_page_header(title, subtitle=None):
    from config.project_data import GROUP_NAME

    sub = (
        f'<div style="color:{TEXT_MUTED};font-size:.95rem;'
        f'margin-top:3px">{subtitle}</div>'
        if subtitle else ""
    )

    st.markdown(
        f'<div style="text-align:right;margin-bottom:5px">'
        f'<span style="background:{NAVY};color:white;font-weight:600;'
        f'font-size:.8rem;padding:6px 12px;border-radius:999px">'
        f'🧠 {GROUP_NAME}</span></div>'

        f'<div style="font-size:1.85rem;font-weight:800;'
        f'color:{TEXT_DARK}">{title}</div>{sub}',
        unsafe_allow_html=True,
    )

    st.write("")


def render_footer():
    from config.project_data import COURSE, COPYRIGHT_YEAR, GROUP_NAME

    st.write("")

    st.markdown(
        f'<div style="text-align:center;color:{TEXT_MUTED};'
        f'font-size:.78rem;padding:16px 0 5px;'
        f'border-top:1px solid {BORDER}">'
        f'© {COPYRIGHT_YEAR} {GROUP_NAME} | {COURSE}</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# General panels
# ==================================================

def panel_html(body, title=None, icon=None):
    heading = (
        f'<div style="font-size:1rem;font-weight:700;'
        f'color:{TEXT_DARK};margin-bottom:11px">'
        f'{icon + " " if icon else ""}{title}</div>'
        if title else ""
    )

    return (
        f'<div style="background:{CARD};'
        f'border:1px solid {BORDER};'
        f'border-radius:12px;padding:18px 20px;'
        f'margin-bottom:13px">'
        f'{heading}{body}</div>'
    )


def stat_card_html(icon, label, value, sublabel, color):
    return panel_html(
        f'<div style="display:flex;align-items:center;gap:13px">'

        f'<div style="width:44px;height:44px;min-width:44px;'
        f'border-radius:10px;background:{_soft(color)};'
        f'color:{color};font-size:1.3rem;display:flex;'
        f'align-items:center;justify-content:center">'
        f'{icon}</div>'

        f'<div>'
        f'<div style="font-size:.78rem;color:{TEXT_MUTED};'
        f'font-weight:600">{label}</div>'

        f'<div style="font-size:1.2rem;font-weight:800;'
        f'color:{TEXT_DARK}">{value}</div>'

        f'<div style="font-size:.74rem;color:{TEXT_MUTED}">'
        f'{sublabel}</div>'

        f'</div></div>'
    )


def render_stat_cards(cards):
    for col, card in zip(st.columns(len(cards)), cards):
        with col:
            st.markdown(
                stat_card_html(*card),
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
            f'<circle cx="70" cy="70" r="{radius}" fill="none" '
            f'stroke="{sentiment_color(label)}" stroke-width="16" '
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

            f'<span style="font-size:.88rem;color:{TEXT_DARK};'
            f'font-weight:600">{label}</span>'

            f'<span style="font-size:.82rem;color:{TEXT_MUTED}">'
            f'({percent:.1f}%)</span>'

            f'</div>'
        )

    return (
        f'<div style="display:flex;align-items:center;'
        f'gap:24px;flex-wrap:wrap">'

        f'<div style="position:relative;width:150px;height:150px">'

        f'<svg width="150" height="150" viewBox="0 0 140 140" '
        f'style="transform:rotate(-90deg)">'

        f'<circle cx="70" cy="70" r="52" fill="none" '
        f'stroke="{BAR_BG}" stroke-width="16"/>'

        f'{_donut_segments(parts)}</svg>'

        f'<div style="position:absolute;inset:0;display:flex;'
        f'flex-direction:column;align-items:center;'
        f'justify-content:center">'

        f'<div style="font-size:1.2rem;font-weight:800;'
        f'color:{TEXT_DARK}">{center_value}</div>'

        f'<div style="font-size:.74rem;color:{TEXT_MUTED}">'
        f'{center_label}</div>'

        f'</div></div>'

        f'<div>{legend}</div></div>'
    )


# ==================================================
# Vertical sentiment chart
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

            f'<div style="font-size:.78rem;color:{TEXT_MUTED};'
            f'font-weight:600">{label}</div>'

            f'<div style="font-size:.7rem;color:{TEXT_MUTED}">'
            f'({share:.1f}%)</div>'

            f'</div>'
        )

    return (
        f'<div style="display:flex;align-items:flex-end;gap:18px;'
        f'padding:6px 10px 0;border-bottom:2px solid {BAR_BG}">'
        f'{bars}</div>'
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

            f'<span style="font-weight:600;color:{TEXT_DARK}">'
            f'{sentiment_emoji(label)} {label}</span>'

            f'<span style="font-weight:600;color:{color}">'
            f'{count} · {percent:.0f}%</span></div>'

            f'<div style="background:{BAR_BG};height:12px;'
            f'border-radius:999px;overflow:hidden">'

            f'<div style="width:{width:.1f}%;height:100%;'
            f'background:{color}"></div></div></div>'
        )

    return rows


def render_sentiment_distribution(counts):
    st.markdown(
        sentiment_distribution_html(counts),
        unsafe_allow_html=True,
    )


# ==================================================
# Prediction components
# ==================================================

def _placeholder_result_html():
    return (
        f'<div style="text-align:center;padding:10px 0 16px">'

        f'<div style="width:84px;height:84px;margin:auto;'
        f'border-radius:50%;border:2px dashed {BORDER};'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-size:2rem;color:{TEXT_MUTED}">?</div>'

        f'<div style="margin-top:12px;color:{TEXT_MUTED};'
        f'font-size:.92rem">'
        f'Run a prediction to see the result</div></div>'
    )


def result_card_html(result):
    if not result:
        return panel_html(
            _placeholder_result_html(),
            "Prediction Result",
            "🎯",
        )

    label = result["label"]
    pct = result.get("confidence", 0) * 100
    color = sentiment_color(label)

    body = (
        f'<div style="text-align:center">'

        f'<div style="width:84px;height:84px;margin:auto;'
        f'border-radius:50%;background:{_soft(color)};'
        f'border:3px solid {color};display:flex;'
        f'align-items:center;justify-content:center;'
        f'font-size:2.1rem">'
        f'{sentiment_face(label)}</div>'

        f'<div style="font-size:1.45rem;font-weight:800;'
        f'color:{color};margin-top:10px">{label}</div>'

        f'<div style="color:{TEXT_MUTED};font-size:.84rem;'
        f'margin-top:13px">Confidence Score</div>'

        f'<div style="font-size:1.35rem;font-weight:800;'
        f'color:{color}">{pct:.2f}%</div>'

        f'<div style="background:{BAR_BG};height:9px;'
        f'border-radius:999px;margin:8px 6px 2px;overflow:hidden">'

        f'<div style="width:{pct:.1f}%;height:100%;'
        f'background:{color}"></div></div>'

        f'<div style="display:flex;justify-content:space-between;'
        f'font-size:.72rem;color:{TEXT_MUTED};margin:0 6px">'
        f'<span>0%</span><span>50%</span><span>100%</span></div>'

        f'</div>'
    )

    return panel_html(body, "Prediction Result", "🎯")


def prob_panel_html(result):
    probs = (
        result["probabilities"]
        if result
        else {"Negative": 0, "Neutral": 0, "Positive": 0}
    )

    rows = ""

    for label in ["Positive", "Neutral", "Negative"]:
        color = sentiment_color(label)
        pct = probs.get(label, 0) * 100

        rows += (
            f'<div style="display:flex;align-items:center;'
            f'gap:12px;margin:11px 0">'

            f'<div style="width:74px;color:{TEXT_DARK};'
            f'font-size:.88rem;font-weight:600">{label}</div>'

            f'<div style="flex:1;background:{BAR_BG};'
            f'height:9px;border-radius:999px;overflow:hidden">'

            f'<div style="width:'
            f'{max(pct, 1.2) if pct else 0:.1f}%;'
            f'height:100%;background:{color}"></div></div>'

            f'<div style="width:58px;text-align:right;'
            f'color:{TEXT_MUTED};font-size:.82rem;'
            f'font-weight:600">{pct:.2f}%</div></div>'
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

        f'<span style="color:{TEXT_MUTED};font-size:.86rem">'
        f'{key}</span>'

        f'<span style="color:{TEXT_DARK};font-size:.86rem;'
        f'font-weight:600;text-align:right">{value}</span>'

        f'</div>'
        for key, value in model_info.items()
    )

    return panel_html(rows, "Model Information", "🤖")


def render_sentiment_result(label, heading="Predicted Sentiment"):
    color = sentiment_color(label)

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:15px;'
        f'background:{_soft(color)};border:2px solid {color};'
        f'border-radius:12px;padding:15px 20px;margin:4px 0 8px">'

        f'<div style="font-size:2.3rem">'
        f'{sentiment_emoji(label)}</div>'

        f'<div>'
        f'<div style="font-size:.75rem;font-weight:700;'
        f'letter-spacing:.1em;text-transform:uppercase;'
        f'color:{TEXT_MUTED}">{heading}</div>'

        f'<div style="font-size:1.75rem;font-weight:800;'
        f'color:{color}">{label}</div></div></div>',
        unsafe_allow_html=True,
    )


# ==================================================
# Bulk components
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
        f'<span style="font-size:.86rem;color:{TEXT_DARK}">'
        f'{line}</span></div>'
        for line in lines
    )

    return panel_html(body, "CSV Requirements", "📋")


def example_csv_html():
    cell = (
        f'border:1px solid {BORDER};'
        f'padding:6px 10px;font-size:.82rem;'
        f'color:{TEXT_DARK}'
    )

    head = (
        f'{cell};background:{CARD_ALT};'
        f'color:{TEXT_MUTED};text-align:left'
    )

    return panel_html(
        f'<table style="border-collapse:collapse;width:100%">'

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

        f'</table>',
        "Example CSV Format",
        "📄",
    )


# ==================================================
# Dashboard
# ==================================================

def model_comparison_html(model_results, final_model):
    accuracy_color = ACCENT
    f1_color = METRIC_COLORS["cyan"]

    rows = (
        f'<div style="display:flex;gap:18px;margin-bottom:13px">'
        f'<span style="color:{TEXT_MUTED}">'
        f'<b style="color:{accuracy_color}">■</b> Accuracy</span>'
        f'<span style="color:{TEXT_MUTED}">'
        f'<b style="color:{f1_color}">■</b> Macro F1</span></div>'
    )

    for model, result in model_results.items():
        accuracy = result["accuracy"] * 100
        f1 = result["macro_f1"] * 100
        star = " ⭐" if model == final_model else ""

        rows += (
            f'<div style="display:flex;align-items:center;'
            f'gap:13px;margin:10px 0">'

            f'<div style="width:150px;color:{TEXT_DARK};'
            f'font-weight:600">{model}{star}</div>'

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
            f'font-size:.76rem;color:{TEXT_MUTED}">'
            f'<b style="color:{accuracy_color}">{accuracy:.2f}%</b> '
            f'· {f1:.2f}% F1</div></div>'
        )

    return rows


# ==================================================
# About
# ==================================================

def pipeline_html(steps):
    items = ""

    for index, (icon, name) in enumerate(steps):
        connector = (
            f'<div style="flex:1;height:2px;background:{BORDER};'
            f'margin-top:29px"></div>'
            if index < len(steps) - 1 else ""
        )

        items += (
            f'<div style="display:flex;flex-direction:column;'
            f'align-items:center;min-width:86px">'

            f'<div style="width:56px;height:56px;border-radius:50%;'
            f'background:{SOFT_BG};border:2px solid {ACCENT};'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:1.35rem;position:relative">{icon}'

            f'<span style="position:absolute;top:-7px;right:-7px;'
            f'background:{ACCENT};color:white;font-size:.65rem;'
            f'font-weight:700;width:19px;height:19px;border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center">'
            f'{index + 1}</span></div>'

            f'<div style="margin-top:8px;font-size:.76rem;'
            f'font-weight:600;color:{TEXT_DARK};text-align:center">'
            f'{name}</div></div>{connector}'
        )

    return (
        f'<div style="display:flex;align-items:flex-start;'
        f'overflow-x:auto;gap:4px">{items}</div>'
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
            f'style="width:54px;height:54px;border-radius:50%;'
            f'object-fit:cover;display:block">'
        )

    else:
        initials = "".join(
            part[0]
            for part in member["name"]
            .replace("(Leader)", "")
            .split()
        )[:2].upper()

        photo = (
            f'<div style="width:54px;height:54px;border-radius:50%;'
            f'background:{ACCENT};color:white;font-weight:700;'
            f'display:flex;align-items:center;justify-content:center">'
            f'{initials}</div>'
        )

    return panel_html(
        f'<div style="display:flex;align-items:center;gap:13px">'

        f'<div style="width:54px;height:54px;min-width:54px">'
        f'{photo}</div>'

        f'<div>'

        f'<div style="font-weight:700;color:{TEXT_DARK}">'
        f'{member["name"]}</div>'

        f'<div style="font-size:.76rem;color:{TEXT_MUTED}">'
        f'ID: {member["sid"]}</div>'

        f'<div style="font-size:.78rem;color:{ACCENT}">'
        f'{member["role"]}</div>'

        f'</div></div>'
    )


def model_badge_html(model_name, model_type, is_final):
    color = (
        METRIC_COLORS["purple"]
        if model_type == "DL"
        else ACCENT
    )

    final = (
        f' <span style="color:{SENTIMENT_COLORS["Neutral"]};'
        f'background:{_soft(SENTIMENT_COLORS["Neutral"])};'
        f'padding:3px 7px;border-radius:999px;font-size:.68rem">'
        f'🏆 FINAL</span>'
        if is_final else ""
    )

    return (
        f'<div style="display:flex;justify-content:space-between;'
        f'align-items:center;padding:8px 2px;'
        f'border-bottom:1px dashed {BORDER}">'

        f'<span style="color:{TEXT_DARK};font-weight:600">'
        f'{model_name}{final}</span>'

        f'<span style="color:{color};background:{_soft(color)};'
        f'padding:3px 8px;border-radius:999px;font-size:.7rem;'
        f'font-weight:700">{model_type}</span></div>'
    )


# ==================================================
# Results table
# ==================================================

def style_results_table(result_df):
    def cell_style(value):
        color = SENTIMENT_COLORS.get(value, INVALID_COLOR)
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
