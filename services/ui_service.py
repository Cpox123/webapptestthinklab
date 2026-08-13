"""Shared UI helpers."""

import base64, math, os
import streamlit as st

ACCENT, NAVY = "#3B82F6", "#10244F"
CARD, BORDER, TRACK = "rgba(127,127,127,.06)", "rgba(127,127,127,.30)", "rgba(127,127,127,.18)"
SOFT = "rgba(127,127,127,.10)"
TEXT_DARK = TEXT_MUTED = TEXT_LIGHT = "inherit"
BG = INPUT_BG = "transparent"
NAVY_2, ACCENT_LIGHT, CARD_ALT, BAR_BG, SOFT_BG = "#173468", "#60A5FA", SOFT, TRACK, SOFT

SENTIMENT_COLORS = {"Negative":"#D95C5C","Neutral":"#D89A3A","Positive":"#3F9B70"}
SENTIMENT_EMOJIS = {"Negative":"🔴","Neutral":"🟡","Positive":"🟢"}
SENTIMENT_FACES = {"Negative":"😞","Neutral":"😐","Positive":"😊"}
INVALID_COLOR, INVALID_EMOJI = "#8994A5", "⚪"

METRIC_COLORS = {
    "blue":ACCENT,"cyan":"#4F9FB5","purple":"#8069B8",
    "orange":"#D88B4A","green":"#3F9B70","yellow":"#D89A3A","red":"#D95C5C"
}

def sentiment_color(x): return SENTIMENT_COLORS.get(x, INVALID_COLOR)
def sentiment_emoji(x): return SENTIMENT_EMOJIS.get(x, INVALID_EMOJI)
def sentiment_face(x): return SENTIMENT_FACES.get(x, "🙂")
def _soft(c): return f"color-mix(in srgb,{c} 14%,transparent)"

CSS=f"""<style>
[data-testid="stHeader"]{{background:transparent}}
[data-testid="stMainBlockContainer"]{{padding-top:2.2rem}}
[data-testid="stMetric"],[data-testid="stFileUploaderDropzone"],[data-testid="stExpander"]{{border:1px solid {BORDER}!important;border-radius:12px!important}}
[data-testid="stSidebarNavLink"][aria-current="page"]{{background:{ACCENT}!important}}
[data-testid="stSidebarNavLink"][aria-current="page"] *{{color:white!important}}
[data-testid="stPageLink"] a{{background:{ACCENT}!important;border-radius:10px!important}}
[data-testid="stPageLink"] a *{{color:white!important;font-weight:600}}
.tl-card{{color:inherit;background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;margin-bottom:13px}}
.tl-title{{font-size:1rem;font-weight:700;margin-bottom:11px}}
.muted{{opacity:.65}}
.track{{background:{TRACK};border-radius:999px;overflow:hidden}}
</style>"""

def apply_theme(): st.markdown(CSS, unsafe_allow_html=True)
def render_brand(): st.logo("assets/logo.svg", size="large")

def render_page_header(title, subtitle=None):
    from config.project_data import GROUP_NAME
    sub=f'<div class="muted" style="font-size:.95rem">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div style="text-align:right"><span style="background:{NAVY};color:white;padding:6px 12px;border-radius:999px;font-size:.8rem">🧠 {GROUP_NAME}</span></div>'
        f'<div style="font-size:1.85rem;font-weight:800">{title}</div>{sub}',
        unsafe_allow_html=True
    )
    st.write("")

def render_footer():
    from config.project_data import COURSE,COPYRIGHT_YEAR,GROUP_NAME
    st.markdown(
        f'<div class="muted" style="text-align:center;font-size:.78rem;padding:16px 0 5px;border-top:1px solid {BORDER}">'
        f'© {COPYRIGHT_YEAR} {GROUP_NAME} | {COURSE}</div>',
        unsafe_allow_html=True
    )

def panel_html(body, title=None, icon=None):
    h=f'<div class="tl-title">{icon+" " if icon else ""}{title}</div>' if title else ""
    return f'<div class="tl-card">{h}{body}</div>'

def stat_card_html(icon,label,value,sublabel,color):
    return panel_html(
        f'<div style="display:flex;align-items:center;gap:13px">'
        f'<div style="width:44px;height:44px;border-radius:10px;background:{_soft(color)};color:{color};display:flex;align-items:center;justify-content:center">{icon}</div>'
        f'<div><div class="muted" style="font-size:.78rem">{label}</div><b>{value}</b>'
        f'<div class="muted" style="font-size:.74rem">{sublabel}</div></div></div>'
    )

def render_stat_cards(cards):
    for col,card in zip(st.columns(len(cards)),cards):
        with col: st.markdown(stat_card_html(*card), unsafe_allow_html=True)

def _donut_segments(parts):
    r,c,o=52,2*math.pi*52,0; out=[]
    for label,p in parts:
        n=max(0,p/100*c-(1.5 if p else 0))
        out.append(f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{sentiment_color(label)}" stroke-width="16" stroke-dasharray="{n:.2f} {c:.2f}" stroke-dashoffset="{-o:.2f}"/>')
        o+=p/100*c
    return "".join(out)

def donut_chart_html(parts, center_value, center_label):
    legend="".join(
        f'<div style="margin:7px 0"><span style="color:{sentiment_color(l)}">●</span> <b>{l}</b> '
        f'<span class="muted">({p:.1f}%)</span></div>' for l,p in parts
    )
    return (
        f'<div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap">'
        f'<div style="position:relative;width:150px;height:150px">'
        f'<svg width="150" height="150" viewBox="0 0 140 140" style="transform:rotate(-90deg)">'
        f'<circle cx="70" cy="70" r="52" fill="none" stroke="{TRACK}" stroke-width="16"/>{_donut_segments(parts)}</svg>'
        f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
        f'<b>{center_value}</b><span class="muted">{center_label}</span></div></div><div>{legend}</div></div>'
    )

def vbar_chart_html(counts):
    vals=[int(counts.get(x,0)) for x in SENTIMENT_COLORS]
    total=sum(vals); mx=max(max(vals,default=0),1); bars=""
    for label,v in zip(SENTIMENT_COLORS,vals):
        c=sentiment_color(label); h=max(3,100*v/mx) if v else 0; s=100*v/total if total else 0
        bars+=f'<div style="flex:1;text-align:center"><b style="color:{c}">{v:,}</b><div style="height:{190*h/100:.0f}px;width:42px;background:{c};margin:6px auto"></div><b>{label}</b><div class="muted">({s:.1f}%)</div></div>'
    return f'<div style="display:flex;align-items:flex-end;gap:18px;border-bottom:2px solid {TRACK}">{bars}</div>'

def sentiment_distribution_html(counts):
    total=sum(int(counts.get(x,0)) for x in SENTIMENT_COLORS) or 1; rows=""
    for label,c in SENTIMENT_COLORS.items():
        n=int(counts.get(label,0)); p=100*n/total; w=max(p,2) if n else 0
        rows+=f'<div style="margin-bottom:13px"><div style="display:flex;justify-content:space-between"><b>{sentiment_emoji(label)} {label}</b><b style="color:{c}">{n} · {p:.0f}%</b></div><div class="track" style="height:12px"><div style="width:{w:.1f}%;height:100%;background:{c}"></div></div></div>'
    return rows

def render_sentiment_distribution(counts):
    st.markdown(sentiment_distribution_html(counts), unsafe_allow_html=True)

def _placeholder_result_html():
    return f'<div style="text-align:center"><div style="width:84px;height:84px;margin:auto;border:2px dashed {BORDER};border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2rem">?</div><div class="muted">Run a prediction to see the result</div></div>'

def result_card_html(result):
    if not result: return panel_html(_placeholder_result_html(),"Prediction Result","🎯")
    label=result["label"]; p=result.get("confidence",0)*100; c=sentiment_color(label)
    body=f'<div style="text-align:center"><div style="font-size:2.1rem">{sentiment_face(label)}</div><div style="font-size:1.45rem;font-weight:800;color:{c}">{label}</div><div class="muted">Confidence Score</div><b style="color:{c}">{p:.2f}%</b><div class="track" style="height:9px"><div style="width:{p:.1f}%;height:100%;background:{c}"></div></div></div>'
    return panel_html(body,"Prediction Result","🎯")

def prob_panel_html(result):
    probs=result["probabilities"] if result else {"Negative":0,"Neutral":0,"Positive":0}; rows=""
    for label in ["Positive","Neutral","Negative"]:
        c=sentiment_color(label); p=probs.get(label,0)*100; w=max(p,1.2) if p else 0
        rows+=f'<div style="display:flex;align-items:center;gap:12px;margin:11px 0"><div style="width:74px"><b>{label}</b></div><div class="track" style="flex:1;height:9px"><div style="width:{w:.1f}%;height:100%;background:{c}"></div></div><div class="muted" style="width:58px;text-align:right">{p:.2f}%</div></div>'
    return panel_html(rows,"Prediction Probabilities","📈")

def model_info_html(info):
    rows="".join(
        f'<div style="display:flex;justify-content:space-between;padding:8px 2px;border-bottom:1px dashed {BORDER}">'
        f'<span class="muted">{k}</span><b>{v}</b></div>' for k,v in info.items()
    )
    return panel_html(rows,"Model Information","🤖")

def render_sentiment_result(label, heading="Predicted Sentiment"):
    c=sentiment_color(label)
    st.markdown(
        f'<div style="background:{_soft(c)};border:2px solid {c};border-radius:12px;padding:15px 20px">'
        f'{sentiment_emoji(label)} <span class="muted">{heading}</span> <b style="color:{c}">{label}</b></div>',
        unsafe_allow_html=True
    )

def bulk_requirements_html(row_limit,candidates):
    lines=[
        "CSV must contain a column with the review text",
        "Supported column names: "+", ".join(candidates),
        "File should use UTF-8 or Latin-1 encoding",
        f"Maximum {row_limit:,} reviews are processed per file"
    ]
    return panel_html("".join(f'<div>✓ {x}</div>' for x in lines),"CSV Requirements","📋")

def example_csv_html():
    s=f'border:1px solid {BORDER};padding:6px 10px'
    rows=[("This is a great product!","123"),("Very bad quality...","466"),("Average product, it's ok","789")]
    body=f'<table style="border-collapse:collapse;width:100%"><tr><th style="{s}">Review Text</th><th style="{s}">other columns...</th></tr>'+''.join(f'<tr><td style="{s}">{a}</td><td style="{s}">{b}</td></tr>' for a,b in rows)+'</table>'
    return panel_html(body,"Example CSV Format","📄")

def model_comparison_html(results,final_model):
    rows=f'<div class="muted"><b style="color:{ACCENT}">■</b> Accuracy &nbsp; <b style="color:{METRIC_COLORS["cyan"]}">■</b> Macro F1</div>'
    for model,r in results.items():
        a,f=r["accuracy"]*100,r["macro_f1"]*100; star=" ⭐" if model==final_model else ""
        rows+=f'<div style="display:flex;gap:13px;align-items:center;margin:10px 0"><div style="width:150px"><b>{model}{star}</b></div><div style="flex:1"><div class="track" style="height:8px"><div style="width:{a:.1f}%;height:100%;background:{ACCENT}"></div></div><div class="track" style="height:8px"><div style="width:{f:.1f}%;height:100%;background:{METRIC_COLORS["cyan"]}"></div></div></div><div class="muted">{a:.2f}% · {f:.2f}% F1</div></div>'
    return rows

def pipeline_html(steps):
    items=""
    for i,(icon,name) in enumerate(steps):
        connector=f'<div style="flex:1;height:2px;background:{BORDER};margin-top:29px"></div>' if i<len(steps)-1 else ""
        items+=f'<div style="text-align:center;min-width:86px"><div style="width:56px;height:56px;margin:auto;border:2px solid {ACCENT};border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative">{icon}<span style="position:absolute;top:-8px;right:-8px;background:{ACCENT};color:white;width:20px;height:20px;border-radius:50%">{i+1}</span></div><b style="font-size:.76rem">{name}</b></div>{connector}'
    return f'<div style="display:flex;align-items:flex-start;overflow-x:auto;padding:12px 2px 5px;gap:4px">{items}</div>'

def team_card_html(member):
    path=member.get("photo","")
    if path and os.path.exists(path):
        data=base64.b64encode(open(path,"rb").read()).decode()
        ext=os.path.splitext(path)[1].lower()
        mime={".png":"image/png",".webp":"image/webp",".gif":"image/gif"}.get(ext,"image/jpeg")
        photo=f'<img src="data:{mime};base64,{data}" style="width:54px;height:54px;border-radius:50%;object-fit:cover">'
    else:
        initials="".join(x[0] for x in member["name"].replace("(Leader)","").split())[:2].upper()
        photo=f'<div style="width:54px;height:54px;border-radius:50%;background:{ACCENT};color:white;display:flex;align-items:center;justify-content:center">{initials}</div>'
    return panel_html(
        f'<div style="display:flex;gap:13px;align-items:center">{photo}<div><b>{member["name"]}</b>'
        f'<div class="muted">ID: {member["sid"]}</div><div style="color:{ACCENT}">{member["role"]}</div></div></div>'
    )

def model_badge_html(name,kind,is_final):
    c=METRIC_COLORS["purple"] if kind=="DL" else ACCENT
    final=" 🏆 FINAL" if is_final else ""
    return f'<div style="display:flex;justify-content:space-between;padding:8px 2px;border-bottom:1px dashed {BORDER}"><b>{name}{final}</b><span style="color:{c}">{kind}</span></div>'

def style_results_table(df):
    return df.style.map(
        lambda v:f"color:{SENTIMENT_COLORS.get(v,INVALID_COLOR)};font-weight:600;",
        subset=["Predicted Sentiment"]
    ).format(
        lambda v:f"{sentiment_emoji(v)} {v}",
        subset=["Predicted Sentiment"]
    )
