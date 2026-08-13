"""Shared UI helpers for the Streamlit app."""

import os
import base64
import math
import streamlit as st


# -------------------- Theme --------------------

ACCENT = "var(--st-primary-color, var(--primary-color, #5B73C7))"
BG = "var(--st-background-color, var(--background-color, #F4F6F9))"
CARD = "var(--st-secondary-background-color, var(--secondary-background-color, #FFFFFF))"
TEXT_DARK = "var(--st-text-color, var(--text-color, #263449))"

TEXT_MUTED = (
    "var(--st-gray-text-color, "
    "color-mix(in srgb, "
    "var(--st-text-color, var(--text-color, #263449)) "
    "65%, transparent))"
)

BORDER = (
    "var(--st-border-color, "
    "color-mix(in srgb, "
    "var(--st-text-color, var(--text-color, #263449)) "
    "18%, transparent))"
)

CARD_ALT = (
    "color-mix(in srgb, "
    "var(--st-secondary-background-color, "
    "var(--secondary-background-color, #FFFFFF)) 92%, "
    "var(--st-text-color, var(--text-color, #263449)) 8%)"
)

SOFT_BG = CARD_ALT

BAR_BG = (
    "color-mix(in srgb, "
    "var(--st-text-color, var(--text-color, #263449)) "
    "12%, transparent)"
)

# Existing pages may already use these names.
NAVY = "#24324A"
NAVY_2 = "#30415E"
ACCENT_LIGHT = "#7188D8"
TEXT_LIGHT = TEXT_DARK
INPUT_BG = CARD


# -------------------- Sentiment --------------------

SENTIMENT_COLORS = {
    "Negative": "#D45A5A",
    "Neutral": "#C58A32",
    "Positive": "#3F8F6B",
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
    "green": "#3F8F6B",
    "yellow": "#C58A32",
    "red": "#D45A5A",
}


def sentiment_color(label):
    return SENTIMENT_COLORS.get(label, INVALID_COLOR)


def sentiment_emoji(label):
    return SENTIMENT_EMOJIS.get(label, INVALID_EMOJI)


def sentiment_face(label):
    return SENTIMENT_FACES.get(label, "🙂")


def _soft(color, amount=14):
    return f"color-mix(in srgb, {color} {amount}%, transparent)"


# -------------------- App style --------------------

_THEME_CSS = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: {BG};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stMainBlockContainer"] {{
    padding-top: 2.2rem;
}}

[data-testid="stMetric"] {{
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px 14px;
}}

[data-testid="stFileUploaderDropzone"],
[data-testid="stExpander"] {{
    border-color: {BORDER};
    border-radius: 12px;
}}

[data-testid="stPageLink"] a {{
    border-radius: 10px !important;
}}
</style>
"""


def apply_theme():
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def render_brand():
    st.logo("assets/logo.svg", size="large")


# -------------------- Header / Footer --------------------

def render_page_header(title, subtitle=None):
    from config.project_data import GROUP_NAME

    sub = (
        f'<div style="color:{TEXT_MUTED};font-size:.95rem;'
        f'margin-top:3px">{subtitle}</div>'
        if subtitle
        else ""
    )

    st.markdown(
        f'<div style="text-align:right;margin-bottom:5px">'
        f'<span style="background:{NAVY};color:#fff;'
        f'font-weight:600;font-size:.8rem;padding:6px 12px;'
        f'border-radius:999px">🧠 {GROUP_NAME}</span>'
        f'</div>'
        f'<div style="font-size:1.85rem;font-weight:800;'
        f'color:{TEXT_DARK}">{title}</div>'
        f'{sub}',
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
        f'© {COPYRIGHT_YEAR} {GROUP_NAME} | {COURSE}'
        f'</div>',
        unsafe_allow_html=True,
    )


# -------------------- Panels --------------------

def panel_html(body, title=None, icon=None):
    heading = (
        f'<div style="font-size:1rem;font-weight:700;'
        f'color:{TEXT_DARK};margin-bottom:11px">'
        f'{icon + " " if icon else ""}{title}</div>'
        if title
        else ""
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


# -------------------- Donut chart --------------------

def _donut_segments(parts):
    radius = 52
    circumference = 2 * math.pi * radius
    offset = 0.0
    segments = []

    for label, percent in parts:
        length = max(
            0.0,
            percent / 100 * circumference
            - (1.5 if percent > 0 else 0),
        )

        segments.append(
            f'<circle cx="70" cy="70" r="{radius}" '
            f'fill="none" '
            f'stroke="{sentiment_color(label)}" '
            f'stroke-width="16" '
            f'stroke-dasharray="{length:.2f} '
            f'{circumference:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}"/>'
        )

        offset += percent / 100 * circumference

    return "".join(segments)


def donut_chart_html(parts, center_value, center_label):
    legend = "".join(
        f'<div style="display:flex;align-items:center;'
        f'gap:8px;margin:7px 0">'
        f'<span style="width:10px;height:10px;'
        f'border-radius:50%;background:{sentiment_color(label)};'
        f'display:inline-block"></span>'
        f'<span style="font-size:.88rem;color:{TEXT_DARK};'
        f'font-weight:600">{label}</span>'
        f'<span style="font-size:.82rem;color:{TEXT_MUTED}">'
        f'({percent:.1f}%)</span>'
        f'</div>'
        for label, percent in parts
    )

    return (
        f'<div style="display:flex;align-items:center;'
        f'gap:24px;flex-wrap:wrap">'

        f'<div style="position:relative;width:150px;'
        f'height:150px;min-width:150px">'

        f'<svg width="150" height="150" '
        f'viewBox="0 0 140 140" '
        f'style="transform:rotate(-90deg)">'

        f'<circle cx="70" cy="70" r="52" '
        f'fill="none" stroke="{BAR_BG}" '
        f'stroke-width="16"/>'

        f'{_donut_segments(parts)}'
        f'</svg>'

        f'<div style="position:absolute;inset:0;'
        f'display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center">'

        f'<div style="font-size:1.2rem;font-weight:800;'
        f'color:{TEXT_DARK}">{center_value}</div>'

        f'<div style="font-size:.74rem;color:{TEXT_MUTED}">'
        f'{center_label}</div>'

        f'</div></div>'

        f'<div>{legend}</div>'
        f'</div>'
    )


# -------------------- Vertical chart --------------------

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

        height = (
            max(3, 100 * value / maximum)
            if value
            else 0
        )

        share = (
            100 * value / total
            if total
            else 0
        )

        bars += (
            f'<div style="flex:1;display:flex;'
            f'flex-direction:column;align-items:center;'
            f'justify-content:flex-end;height:190px">'

            f'<div style="font-size:.84rem;font-weight:700;'
            f'color:{color}">{value:,}</div>'

            f'<div style="width:42px;'
            f'height:{190 * height / 100:.0f}px;'
            f'background:{color};'
            f'border-radius:7px 7px 4px 4px;'
            f'margin:6px 0"></div>'

            f'<div style="font-size:.78rem;'
            f'color:{TEXT_MUTED};font-weight:600">'
            f'{label}</div>'

            f'<div style="font-size:.7rem;color:{TEXT_MUTED}">'
            f'({share:.1f}%)</div>'

            f'</div>'
        )

    return (
        f'<div style="display:flex;align-items:flex-end;'
        f'gap:18px;padding:6px 10px 0;'
        f'border-bottom:2px solid {BAR_BG}">'
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

            f'<div style="display:flex;'
            f'justify-content:space-between;'
            f'margin-bottom:5px">'

            f'<span style="font-weight:600;color:{TEXT_DARK}">'
            f'{SENTIMENT_EMOJIS[label]} {label}</span>'

            f'<span style="font-weight:600;color:{color}">'
            f'{count} &middot; {percent:.0f}%</span>'

            f'</div>'

            f'<div style="background:{BAR_BG};'
            f'border-radius:999px;height:12px;overflow:hidden">'

            f'<div style="width:{width:.1f}%;height:100%;'
            f'background:{color};border-radius:999px"></div>'

            f'</div></div>'
        )

    return rows


def render_sentiment_distribution(counts):
    st.markdown(
        sentiment_distribution_html(counts),
        unsafe_allow_html=True,
    )


# -------------------- Prediction --------------------

def _placeholder_result_html():
    return (
        f'<div style="text-align:center;padding:10px 0 16px">'

        f'<div style="width:84px;height:84px;'
        f'margin:auto;border-radius:50%;'
        f'border:2px dashed {BORDER};'
        f'display:flex;align-items:center;'
        f'justify-content:center;font-size:2rem;'
        f'color:{TEXT_MUTED}">?</div>'

        f'<div style="margin-top:12px;'
        f'color:{TEXT_MUTED};font-size:.92rem">'
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
    pct = result.get("confidence", 0) * 100
    color = sentiment_color(label)

    body = (
        f'<div style="text-align:center">'

        f'<div style="width:84px;height:84px;'
        f'margin:auto;border-radius:50%;'
        f'background:{_soft(color)};'
        f'border:3px solid {color};display:flex;'
        f'align-items:center;justify-content:center;'
        f'font-size:2.1rem">'
        f'{sentiment_face(label)}</div>'

        f'<div style="font-size:1.45rem;'
        f'font-weight:800;color:{color};'
        f'margin-top:10px">{label}</div>'

        f'<div style="color:{TEXT_MUTED};'
        f'font-size:.84rem;margin-top:13px">'
        f'Confidence Score</div>'

        f'<div style="font-size:1.35rem;'
        f'font-weight:800;color:{color}">'
        f'{pct:.2f}%</div>'

        f'<div style="background:{BAR_BG};'
        f'border-radius:999px;height:9px;'
        f'margin:8px 6px 2px;overflow:hidden">'

        f'<div style="width:{pct:.1f}%;height:100%;'
        f'background:{color};border-radius:999px"></div>'

        f'</div>'

        f'<div style="display:flex;'
        f'justify-content:space-between;'
        f'font-size:.72rem;color:{TEXT_MUTED};'
        f'margin:0 6px">'
        f'<span>0%</span>'
        f'<span>50%</span>'
        f'<span>100%</span>'
        f'</div></div>'
    )

    return panel_html(
        body,
        "Prediction Result",
        "🎯",
    )


def prob_panel_html(result):
    probs = (
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
        pct = probs.get(label, 0) * 100

        rows += (
            f'<div style="display:flex;align-items:center;'
            f'gap:12px;margin:11px 0">'

            f'<div style="width:74px;color:{TEXT_DARK};'
            f'font-size:.88rem;font-weight:600">'
            f'{label}</div>'

            f'<div style="flex:1;background:{BAR_BG};'
            f'border-radius:999px;height:9px;overflow:hidden">'

            f'<div style="width:'
            f'{max(pct, 1.2) if pct else 0:.1f}%;'
            f'height:100%;background:{color};'
            f'border-radius:999px"></div>'

            f'</div>'

            f'<div style="width:58px;text-align:right;'
            f'color:{TEXT_MUTED};font-size:.82rem;'
            f'font-weight:600">{pct:.2f}%</div>'

            f'</div>'
        )

    return panel_html(
        rows,
        "Prediction Probabilities",
        "📈",
    )


def model_info_html(model_info):
    rows = "".join(
        f'<div style="display:flex;'
        f'justify-content:space-between;'
        f'padding:8px 2px;'
        f'border-bottom:1px dashed {BORDER}">'

        f'<span style="color:{TEXT_MUTED};'
        f'font-size:.86rem">{key}</span>'

        f'<span style="color:{TEXT_DARK};'
        f'font-size:.86rem;font-weight:600;'
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
        f'<div style="display:flex;align-items:center;'
        f'gap:15px;background:{_soft(color)};'
        f'border:2px solid {color};'
        f'border-radius:12px;padding:15px 20px;'
        f'margin:4px 0 8px">'

        f'<div style="font-size:2.3rem">'
        f'{sentiment_emoji(label)}</div>'

        f'<div>'

        f'<div style="font-size:.75rem;'
        f'font-weight:700;letter-spacing:.1em;'
        f'text-transform:uppercase;'
        f'color:{TEXT_MUTED}">{heading}</div>'

        f'<div style="font-size:1.75rem;'
        f'font-weight:800;color:{color}">'
        f'{label}</div>'

        f'</div></div>',
        unsafe_allow_html=True,
    )


# -------------------- Bulk page --------------------

def bulk_requirements_html(
    row_limit,
    candidates,
):
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
        f'<span style="font-size:.86rem;'
        f'color:{TEXT_DARK}">{line}</span>'
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
        f'<td style="border:1px solid {BORDER};'
        f'padding:6px 10px;font-size:.82rem;'
        f'color:{TEXT_DARK}">'
    )

    head = (
        f'text-align:left;'
        f'border:1px solid {BORDER};'
        f'background:{CARD_ALT};'
        f'padding:6px 10px;'
        f'font-size:.78rem;'
        f'color:{TEXT_MUTED}'
    )

    table = (
        f'<table style="border-collapse:collapse;width:100%">'

        f'<tr>'
        f'<th style="{head}">Review Text</th>'
        f'<th style="{head}">other columns...</th>'
        f'</tr>'

        f'<tr>'
        f'{cell}This is a great product!</td>'
        f'{cell}123</td>'
        f'</tr>'

        f'<tr>'
        f'{cell}Very bad quality...</td>'
        f'{cell}466</td>'
        f'</tr>'

        f'<tr>'
        f'{cell}Average product, it\'s ok</td>'
        f'{cell}789</td>'
        f'</tr>'

        f'</table>'
    )

    return panel_html(
        table,
        "Example CSV Format",
        "📄",
    )


# -------------------- Dashboard --------------------

def model_comparison_html(
    model_results,
    final_model,
):
    acc_color = ACCENT
    f1_color = METRIC_COLORS["cyan"]

    legend = (
        f'<div style="display:flex;gap:18px;'
        f'margin-bottom:13px">'

        f'<span style="font-size:.82rem;'
        f'color:{TEXT_MUTED}">'
        f'<b style="color:{acc_color}">■</b> Accuracy'
        f'</span>'

        f'<span style="font-size:.82rem;'
        f'color:{TEXT_MUTED}">'
        f'<b style="color:{f1_color}">■</b> Macro F1'
        f'</span>'

        f'</div>'
    )

    rows = ""

    for model, result in model_results.items():
        acc = result["accuracy"] * 100
        f1 = result["macro_f1"] * 100

        star = (
            f' <span style="color:'
            f'{SENTIMENT_COLORS["Neutral"]}">★</span>'
            if model == final_model
            else ""
        )

        rows += (
            f'<div style="display:flex;'
            f'align-items:center;gap:13px;'
            f'margin:10px 0">'

            f'<div style="width:150px;'
            f'min-width:150px;font-size:.86rem;'
            f'color:{TEXT_DARK};font-weight:600">'
            f'{model}{star}</div>'

            f'<div style="flex:1">'

            f'<div style="height:8px;'
            f'background:{BAR_BG};'
            f'border-radius:999px;'
            f'margin:3px 0;overflow:hidden">'

            f'<div style="width:{acc:.1f}%;'
            f'height:100%;background:{acc_color};'
            f'border-radius:999px"></div>'

            f'</div>'

            f'<div style="height:8px;'
            f'background:{BAR_BG};'
            f'border-radius:999px;overflow:hidden">'

            f'<div style="width:{f1:.1f}%;'
            f'height:100%;background:{f1_color};'
            f'border-radius:999px"></div>'

            f'</div></div>'

            f'<div style="width:115px;'
            f'text-align:right;font-size:.76rem;'
            f'color:{TEXT_MUTED}">'

            f'<b style="color:{acc_color}">'
            f'{acc:.2f}%</b> '

            f'&middot; {f1:.2f}% F1'

            f'</div></div>'
        )

    return legend + rows


# -------------------- About page --------------------

def pipeline_html(steps):
    items = ""

    for index, (icon, name) in enumerate(steps):
        connector = (
            f'<div style="flex:1;height:2px;'
            f'background:{BORDER};'
            f'margin-top:29px"></div>'
            if index < len(steps) - 1
            else ""
        )

        items += (
            f'<div style="display:flex;'
            f'flex-direction:column;'
            f'align-items:center;min-width:86px">'

            f'<div style="width:56px;height:56px;'
            f'border-radius:50%;'
            f'background:{SOFT_BG};'
            f'border:2px solid {ACCENT};'
            f'display:flex;align-items:center;'
            f'justify-content:center;'
            f'font-size:1.35rem;position:relative">'

            f'{icon}'

            f'<span style="position:absolute;'
            f'top:-7px;right:-7px;'
            f'background:{ACCENT};color:#fff;'
            f'font-size:.65rem;font-weight:700;'
            f'width:19px;height:19px;'
            f'border-radius:50%;display:flex;'
            f'align-items:center;justify-content:center">'
            f'{index + 1}</span>'

            f'</div>'

            f'<div style="margin-top:8px;'
            f'font-size:.76rem;font-weight:600;'
            f'color:{TEXT_DARK};text-align:center;'
            f'max-width:96px">{name}</div>'

            f'</div>{connector}'
        )

    return (
        f'<div style="display:flex;'
        f'align-items:flex-start;'
        f'overflow-x:auto;'
        f'padding:5px 2px;gap:4px">'
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
            f'border-radius:50%;object-fit:cover;'
            f'display:block" '
            f'alt="Team member photo">'
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
            f'color:#fff;font-weight:700;'
            f'display:flex;align-items:center;'
            f'justify-content:center">'
            f'{initials}</div>'
        )

    return panel_html(
        f'<div style="display:flex;'
        f'align-items:center;gap:13px">'

        f'<div style="width:54px;height:54px;'
        f'min-width:54px;border-radius:50%;'
        f'overflow:hidden">{photo}</div>'

        f'<div>'

        f'<div style="font-weight:700;'
        f'color:{TEXT_DARK}">'
        f'{member["name"]}</div>'

        f'<div style="font-size:.76rem;'
        f'color:{TEXT_MUTED}">'
        f'ID: {member["sid"]}</div>'

        f'<div style="font-size:.78rem;'
        f'color:{ACCENT};margin-top:2px">'
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
        f' <span style="background:'
        f'{_soft(SENTIMENT_COLORS["Neutral"], 16)};'
        f'color:{SENTIMENT_COLORS["Neutral"]};'
        f'font-size:.68rem;font-weight:700;'
        f'padding:3px 7px;border-radius:999px">'
        f'🏆 FINAL</span>'
        if is_final
        else ""
    )

    return (
        f'<div style="display:flex;'
        f'justify-content:space-between;'
        f'align-items:center;padding:8px 2px;'
        f'border-bottom:1px dashed {BORDER}">'

        f'<span style="font-size:.87rem;'
        f'color:{TEXT_DARK};font-weight:600">'
        f'{model_name}{final}</span>'

        f'<span style="font-size:.7rem;'
        f'font-weight:700;color:{color};'
        f'background:{_soft(color, 12)};'
        f'padding:3px 8px;border-radius:999px">'
        f'{model_type}</span>'

        f'</div>'
    )


# -------------------- Results table --------------------

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
