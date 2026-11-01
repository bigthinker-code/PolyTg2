import streamlit as st

EXAMPLES = {
    "Polyethylene": "[*]CC[*]",
    "Polystyrene": "[*]CC([*])c1ccccc1",
    "PMMA": "[*]CC([*])(C)C(=O)OC",
    "PVC": "[*]CC([*])Cl",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
html, body, .stApp, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
h1, h2, h3, .pt-display, .pt-big { font-family: 'Sora', sans-serif; letter-spacing: -0.02em; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1080px; padding-top: 2.4rem; }

.pt-hero { padding: 1.2rem 0 1.6rem 0; }
.pt-hero h1 { font-size: 2.7rem; line-height: 1.12; margin: 0 0 .8rem 0; max-width: 18ch; }
.pt-hero p { font-size: 1.1rem; color: #4A5868; max-width: 56ch; line-height: 1.6; margin: 0; }

.pt-head h1 { font-size: 2rem; margin: 0 0 .3rem 0; }
.pt-head p { color: #4A5868; margin: 0 0 1.4rem 0; max-width: 62ch; }

.pt-card { background: #fff; border: 1px solid #E1E5EB; border-radius: 10px; padding: 1.1rem 1.2rem; height: 100%; }
.pt-card h4 { margin: 0 0 .35rem 0; font-family: 'Sora', sans-serif; font-size: 1rem; }
.pt-card p { margin: 0; color: #4A5868; font-size: .95rem; line-height: 1.55; }

.pt-big { font-size: 4rem; font-weight: 700; line-height: 1; color: #14202E; }
.pt-big span { font-size: 1.4rem; font-weight: 500; color: #6B7A8C; margin-left: .3rem; }
.pt-sub { color: #4A5868; font-size: 1.05rem; margin-top: .3rem; }

.pt-scale { margin: 1.6rem 0 2.2rem 0; }
.pt-track { position: relative; height: 16px; border-radius: 8px;
  background: linear-gradient(90deg, #D6E3FB 0%, #EFE7E1 55%, #F6D5BF 100%); }
.pt-band { position: absolute; top: -4px; height: 24px; border-radius: 6px;
  background: rgba(43,91,222,.22); border: 1.5px solid #2B5BDE; }
.pt-mark { position: absolute; top: -9px; width: 4px; height: 34px; margin-left: -2px;
  background: #E8590C; border-radius: 2px; }
.pt-ticks { position: relative; height: 22px; margin-top: 12px; }
.pt-ticks span { position: absolute; transform: translateX(-50%); font-size: .78rem; color: #6B7A8C; }
.pt-ends { display: flex; justify-content: space-between; font-size: .8rem; color: #6B7A8C; margin-top: 2px; }

.pt-stat { background: #fff; border: 1px solid #E1E5EB; border-radius: 10px; padding: .9rem 1.1rem; }
.pt-stat .k { color: #6B7A8C; font-size: .85rem; }
.pt-stat .v { font-family: 'Sora', sans-serif; font-size: 1.35rem; font-weight: 600; margin-top: .15rem; }

.pt-mol { background: #fff; border: 1px solid #E1E5EB; border-radius: 10px; padding: .6rem; text-align: center; }
.pt-step { display: flex; gap: 1rem; padding: .9rem 0; border-top: 1px solid #E1E5EB; }
.pt-step:first-child { border-top: none; }
.pt-step .n { font-family: 'Sora', sans-serif; font-weight: 700; color: #2B5BDE; width: 1.6rem; }
.pt-step h4 { margin: 0 0 .2rem 0; font-size: 1rem; }
.pt-step p { margin: 0; color: #4A5868; font-size: .95rem; line-height: 1.55; }
a.pt-link { display: inline-block; margin: 0 .5rem .5rem 0; padding: .45rem .9rem; border: 1px solid #C9D1DC;
  border-radius: 8px; color: #14202E; text-decoration: none; font-weight: 500; background: #fff; }
a.pt-link:hover { border-color: #2B5BDE; color: #2B5BDE; }
@media (max-width: 700px) { .pt-hero h1 { font-size: 2rem; } .pt-big { font-size: 3rem; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def page_header(title: str, text: str):
    st.markdown(f'<div class="pt-head"><h1>{title}</h1><p>{text}</p></div>', unsafe_allow_html=True)


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
