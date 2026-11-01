from datetime import datetime

import streamlit as st

from core.ui import EXAMPLES, card, quick_result

st.session_state.setdefault("history", [])
st.session_state.setdefault("home_result", None)
st.session_state.setdefault("home_psmiles", "[*]CC([*])c1ccccc1")

st.markdown(
    '<div class="pt-banner"><h1>Predict polymer Tg and know how far to trust it.</h1>'
    "<p>PolyTg reads the repeat unit of a polymer and returns its glass transition temperature "
    "with a conformal interval and a check against the training data.</p>"
    '<div class="pt-chips"><span>Conformal interval</span><span>Applicability domain</span>'
    "<span>Batch CSV</span></div></div>",
    unsafe_allow_html=True,
)

st.subheader("Try it now")
a, b = st.columns([3, 1], vertical_alignment="bottom")
smi = a.text_input("Polymer SMILES", key="home_psmiles", help="Mark both ends of the repeat unit with [*]")
go = b.button("Predict Tg", type="primary", use_container_width=True)

if go:
    try:
        from core.engine import get_engine

        with st.spinner("Predicting..."):
            result = get_engine().predict(smi)
        known = {v: k for k, v in EXAMPLES.items()}
        st.session_state.home_result = result
        st.session_state.last_result = result
        st.session_state.history.append(
            {"time": datetime.now().strftime("%H:%M:%S"), "label": known.get(result["psmiles"], result["psmiles"]), **result}
        )
    except Exception as e:
        st.session_state.home_result = None
        st.error(str(e))

if st.session_state.home_result:
    quick_result(st.session_state.home_result)
    st.page_link("views/predict.py", label="Open the full result", icon=":material/science:")

st.write("")
c1, c2, c3 = st.columns(3, gap="medium")
c1.markdown(
    card("Enter a repeat unit", "Type a polymer SMILES with a [*] at each end, or pick an example. You can also upload a CSV for many polymers at once."),
    unsafe_allow_html=True,
)
c2.markdown(
    card("Read the result", "You get Tg in Kelvin and Celsius, placed on a scale from flexible to rigid chains, with the interval drawn around it."),
    unsafe_allow_html=True,
)
c3.markdown(
    card("Check the domain", "Every prediction is compared with the training data. If the polymer is too far from it, PolyTg tells you."),
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pt-note">Screening candidate polymers on screen before making them saves reagents, '
    "solvent and bench time. That makes PolyTg a small step toward greener materials work.</div>",
    unsafe_allow_html=True,
)
