import streamlit as st

from core import config
from core.ui import page_header, stat

page_header(
    "Model and Method",
    "How PolyTg turns a repeat unit into a temperature, and how it decides how much to trust that number.",
)

steps = [
    ("1", "Read the structure", "The polymer SMILES is parsed with RDKit and checked for the two [*] end markers."),
    ("2", "Compute features", "PolyMetriX turns the repeat unit into a numeric feature vector. The columns are matched to the ones used in training."),
    ("3", "Predict Tg", "An Extra Trees regressor trained on polymer glass transition data returns the temperature in Kelvin."),
    ("4", "Add an interval", "A conformal threshold from calibration data is added and subtracted to give a range around the prediction."),
    ("5", "Check the domain", "The features are scaled and compared with their nearest neighbour in the training set. A distance above the threshold flags the polymer as outside the domain."),
]
html = "".join(
    f'<div class="pt-step"><div class="n">{n}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
    for n, t, d in steps
)
st.markdown(html, unsafe_allow_html=True)

st.subheader("Reported performance")
stats = {k: v for k, v in config.MODEL_STATS.items() if v is not None}
if stats:
    cols = st.columns(len(stats))
    for col, (k, v) in zip(cols, stats.items()):
        col.markdown(stat(k, str(v)), unsafe_allow_html=True)
else:
    st.caption("Add your test set metrics in core/config.py and they will show here.")

st.subheader("Reading the result")
st.markdown(
    "- The interval is a range for the true Tg, not a standard deviation.\n"
    "- A wide interval or an outside domain flag means the model is less certain about this structure.\n"
    "- The model predicts from the repeat unit only. Molecular weight, tacticity and processing history are not inputs."
)
