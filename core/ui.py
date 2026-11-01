import streamlit as st

EXAMPLES = {
    "Polyethylene": "[*]CC[*]",
    "Polystyrene": "[*]CC([*])c1ccccc1",
    "PMMA": "[*]CC([*])(C)C(=O)OC",
    "PVC": "[*]CC([*])Cl",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap');
:root { --spruce:#0E2F2A; --fern:#1F7A52; --sprout:#8FD14F; --mist:#EAF1EB; --line:#D2E1D6; --ink:#12261F; --soft:#4B6358; --sun:#E07B00; }
html, body, .stApp, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
h1, h2, h3, .pt-display, .pt-big { font-family: 'Bricolage Grotesque', sans-serif; letter-spacing: -0.02em; color: var(--spruce); }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1080px; padding-top: 2rem; }

/* sidebar */
[data-testid="stSidebar"] { background: var(--spruce); }
[data-testid="stSidebar"] * { color: #DCEBE1; }
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] { border-radius: 8px; }
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover { background: rgba(255,255,255,.07); }
[data-testid="stSidebar"] a[aria-current="page"] { background: rgba(143,209,79,.18); }
[data-testid="stSidebar"] a[aria-current="page"] * { color: #fff; font-weight: 600; }
.pt-brand { display: flex; align-items: center; gap: .6rem; margin: .4rem 0 .2rem 0; }
.pt-brand span { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.5rem; font-weight: 700; color: #fff; }
.pt-tag { font-size: .85rem; color: #9DB8A8; line-height: 1.45; margin-bottom: .8rem; }

/* hero */
.pt-banner { border-radius: 18px; padding: 3rem 2.6rem; margin-bottom: 1.6rem; color: #fff;
  background:
    linear-gradient(100deg, #0E2F2A 38%, rgba(14,47,42,0) 100%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'><path d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='%238FD14F' stroke-opacity='0.30' stroke-width='1.5'/><path d='M28 0L28 -34M0 50L-28 66M56 50L84 66' fill='none' stroke='%238FD14F' stroke-opacity='0.30' stroke-width='1.5'/></svg>"),
    #0E2F2A; }
.pt-banner h1 { color: #fff; font-size: 2.9rem; line-height: 1.1; margin: 0 0 1rem 0; max-width: 17ch; }
.pt-banner p { color: #C8DDD0; font-size: 1.1rem; line-height: 1.6; max-width: 52ch; margin: 0 0 1.4rem 0; }
.pt-chips span { display: inline-block; margin: 0 .5rem .5rem 0; padding: .3rem .8rem; border-radius: 999px;
  border: 1px solid rgba(143,209,79,.55); color: #D9F0B8; font-size: .85rem; }

.pt-head h1 { font-size: 2.1rem; margin: 0 0 .5rem 0; }
.pt-head .rule { width: 52px; height: 4px; border-radius: 2px; background: var(--fern); margin-bottom: .8rem; }
.pt-head p { color: var(--soft); margin: 0 0 1.4rem 0; max-width: 62ch; line-height: 1.55; }

.pt-card { background: #fff; border: 1px solid var(--line); border-top: 4px solid var(--fern); border-radius: 12px; padding: 1.1rem 1.2rem; height: 100%; }
.pt-card h4 { margin: 0 0 .35rem 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.1rem; color: var(--spruce); }
.pt-card p { margin: 0; color: var(--soft); font-size: .95rem; line-height: 1.55; }

.pt-note { background: #F6FAEF; border: 1px solid #D7E8BF; border-radius: 12px; padding: 1.1rem 1.3rem; margin-top: 1.4rem; color: var(--ink); line-height: 1.6; }

.pt-big { font-size: 4.2rem; font-weight: 700; line-height: 1; color: var(--fern); }
.pt-big span { font-size: 1.4rem; font-weight: 500; color: var(--soft); margin-left: .3rem; }
.pt-sub { color: var(--soft); font-size: 1.05rem; margin-top: .3rem; }

.pt-scale { margin: 1.6rem 0 2.2rem 0; }
.pt-track { position: relative; height: 16px; border-radius: 8px;
  background: linear-gradient(90deg, #CDE9D8 0%, #E9F0CF 50%, #F6DFA8 100%); }
.pt-band { position: absolute; top: -4px; height: 24px; border-radius: 6px;
  background: rgba(31,122,82,.22); border: 1.5px solid var(--fern); }
.pt-mark { position: absolute; top: -9px; width: 4px; height: 34px; margin-left: -2px; background: var(--sun); border-radius: 2px; }
.pt-ticks { position: relative; height: 22px; margin-top: 12px; }
.pt-ticks span { position: absolute; transform: translateX(-50%); font-size: .78rem; color: var(--soft); }
.pt-ends { display: flex; justify-content: space-between; font-size: .8rem; color: var(--soft); margin-top: 2px; }

.pt-stat { background: #fff; border: 1px solid var(--line); border-left: 4px solid var(--sprout); border-radius: 10px; padding: .9rem 1.1rem; }
.pt-stat .k { color: var(--soft); font-size: .85rem; }
.pt-stat .v { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.35rem; font-weight: 600; margin-top: .15rem; color: var(--spruce); }

.pt-mol { background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: .6rem; text-align: center; }
.pt-step { display: flex; gap: 1rem; padding: .9rem 0; border-top: 1px solid var(--line); }
.pt-step:first-child { border-top: none; }
.pt-step .n { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; color: var(--fern); width: 1.6rem; font-size: 1.2rem; }
.pt-step h4 { margin: 0 0 .2rem 0; font-size: 1.05rem; color: var(--spruce); }
.pt-step p { margin: 0; color: var(--soft); font-size: .95rem; line-height: 1.55; }
a.pt-link { display: inline-block; margin: 0 .5rem .5rem 0; padding: .5rem 1rem; border: 1px solid var(--line);
  border-radius: 8px; color: var(--spruce); text-decoration: none; font-weight: 600; background: #fff; }
a.pt-link:hover { border-color: var(--fern); color: var(--fern); }

/* widgets */
.stButton > button { border-radius: 10px; font-weight: 600; }
.stButton > button[kind="primary"] { background: var(--fern); border-color: var(--fern); color: #fff; padding: .55rem 1.4rem; }
.stButton > button[kind="primary"]:hover { background: #17613F; border-color: #17613F; }
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { color: var(--fern); }
.stTextInput input { border-radius: 10px; }
@media (max-width: 700px) { .pt-banner { padding: 2rem 1.4rem; } .pt-banner h1 { font-size: 2.1rem; } .pt-big { font-size: 3rem; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def page_header(title: str, text: str):
    st.markdown(f'<div class="pt-head"><h1>{title}</h1><div class="rule"></div><p>{text}</p></div>', unsafe_allow_html=True)


def card(title: str, text: str) -> str:
    return f'<div class="pt-card"><h4>{title}</h4><p>{text}</p></div>'


def stat(label: str, value: str) -> str:
    return f'<div class="pt-stat"><div class="k">{label}</div><div class="v">{value}</div></div>'


def tg_scale(r: dict, lo: int = 150, hi: int = 700) -> str:
    def pos(v):
        return max(0.0, min(100.0, (v - lo) / (hi - lo) * 100))

    left, right = pos(r["lower"]), pos(r["upper"])
    ticks = "".join(
        f'<span style="left:{pos(t):.1f}%">{t} K</span>' for t in range(200, hi + 1, 100)
    )
    return (
        '<div class="pt-scale"><div class="pt-track">'
        f'<div class="pt-band" style="left:{left:.1f}%;width:{max(right - left, 0.8):.1f}%"></div>'
        f'<div class="pt-mark" style="left:{pos(r["tg_k"]):.1f}%"></div></div>'
        f'<div class="pt-ticks">{ticks}</div>'
        '<div class="pt-ends"><span>Flexible chains</span><span>Rigid chains</span></div></div>'
    )


def mol_svg(psmiles: str) -> str:
    try:
        from rdkit import Chem
        from rdkit.Chem.Draw import rdMolDraw2D

        mol = Chem.MolFromSmiles(psmiles)
        d = rdMolDraw2D.MolDraw2DSVG(420, 280)
        d.drawOptions().clearBackground = False
        d.DrawMolecule(mol)
        d.FinishDrawing()
        return d.GetDrawingText().replace("\n", "")
    except Exception:
        return ""


def render_result(r: dict):
    left, right = st.columns([1, 1.5], gap="large")
    with left:
        svg = mol_svg(r["psmiles"])
        if svg:
            st.markdown(f'<div class="pt-mol">{svg}</div>', unsafe_allow_html=True)
        st.caption(r["psmiles"])
    with right:
        st.markdown(
            f'<div class="pt-big">{r["tg_k"]:.1f}<span>K</span></div>'
            f'<div class="pt-sub">{r["tg_c"]:.1f} °C predicted glass transition</div>',
            unsafe_allow_html=True,
        )
        st.markdown(tg_scale(r), unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(stat("Conformal interval", f'{r["lower"]:.0f} to {r["upper"]:.0f} K'), unsafe_allow_html=True)
    c2.markdown(stat("Interval width", f'{r["width"]:.0f} K'), unsafe_allow_html=True)
    c3.markdown(
        stat("Distance to training data", f'{r["distance"]:.2f} of {r["threshold"]:.2f} allowed'),
        unsafe_allow_html=True,
    )
    st.write("")
    if r["in_domain"]:
        st.success("Inside the applicability domain. This polymer looks similar to what the model was trained on.")
    else:
        st.warning(
            "Outside the applicability domain. This polymer is further from the training data than "
            "the allowed limit, so treat the value as a rough guide only."
        )
