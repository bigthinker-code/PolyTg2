import pandas as pd
import streamlit as st

from core import config
from core.ui import page_header, stat

page_header(
    "Model and Method",
    "How PolyTg turns a repeat unit into a temperature, how well it did on unseen polymers, and where it is weaker.",
)

steps = [
    ("1", "Read the structure", "The polymer SMILES is parsed with RDKit and checked for the two [*] end markers."),
    ("2", "Compute features", "PolyMetriX turns the repeat unit into numeric descriptors at the backbone, side chain and whole polymer level. The columns are matched to the ones used in training."),
    ("3", "Predict Tg", "An Extra Trees regressor with 700 trees returns the glass transition temperature in Kelvin."),
    ("4", "Add an interval", "A conformal threshold from the calibration set is added and subtracted to give a 90% range around the prediction."),
    ("5", "Check the domain", "The features are scaled and compared with their nearest neighbour in the training set. A distance above the threshold flags the polymer as outside the domain."),
]
st.markdown(
    "".join(
        f'<div class="pt-step"><div class="n">{n}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
        for n, t, d in steps
    ),
    unsafe_allow_html=True,
)

st.subheader("Test set performance")
cols = st.columns(len(config.MODEL_STATS))
for col, (k, v) in zip(cols, config.MODEL_STATS.items()):
    col.markdown(stat(k, v), unsafe_allow_html=True)
st.caption("Measured on 1,105 polymers the model never saw. Interval coverage is the share of true values that fell inside the 90% conformal interval.")

st.subheader("Evaluation details")
st.dataframe(
    pd.DataFrame(config.EVAL_DETAILS, columns=["Item", "Result"]),
    use_container_width=True,
    hide_index=True,
)

st.subheader("How well it generalises")
g = st.columns(len(config.GROUPED_CV))
for col, (k, v) in zip(g, config.GROUPED_CV.items()):
    col.markdown(stat(f"Grouped cross-validation {k}", v), unsafe_allow_html=True)
st.write("")
st.warning(
    "Performance drops when the evaluation separates polymer classes (R² falls from 0.879 to 0.639). "
    "Polymer classes that are rare in the training data are harder to predict, so treat those results with extra care."
)

st.subheader("Applicability domain")
a = st.columns(len(config.AD_STATS))
for col, (name, n, mae) in zip(a, config.AD_STATS):
    col.markdown(stat(name, f"{n}<br><span style='font-size:1rem;font-weight:500'>{mae}</span>"), unsafe_allow_html=True)
st.caption(config.AD_NOTE)

st.subheader("Reading the result")
st.markdown(
    "- The interval is a range for the true Tg at 90% coverage, not a standard deviation. It averages about 125 K wide.\n"
    "- The domain flag and the interval are caution signals. Neither guarantees an accurate prediction.\n"
    "- The model predicts from the repeat unit only. Molecular weight, tacticity and processing history are not inputs."
)
