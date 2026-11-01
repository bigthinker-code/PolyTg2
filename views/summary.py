import pandas as pd
import streamlit as st

from core.ui import compare_scale, page_header, render_result, stat

page_header("Results Summary", "Everything you have predicted in this session, in one place.")

history = st.session_state.get("history", [])

if not history:
    st.info("No predictions yet. Run one on the Predict page and it will appear here.")
    st.page_link("views/predict.py", label="Go to Predict", icon=":material/science:")
    st.stop()

df = pd.DataFrame(history)
inside = int(df["in_domain"].sum())

c1, c2, c3 = st.columns(3)
c1.markdown(stat("Predictions", str(len(df))), unsafe_allow_html=True)
c2.markdown(stat("Inside the domain", f"{inside} of {len(df)}"), unsafe_allow_html=True)
c3.markdown(stat("Tg range", f'{df["tg_k"].min():.0f} to {df["tg_k"].max():.0f} K'), unsafe_allow_html=True)

st.write("")
st.subheader("Compare on one scale")
st.caption("Each marker is a predicted Tg and the box around it is its conformal interval. Showing the latest 12.")
st.markdown(compare_scale(history[-12:]), unsafe_allow_html=True)

st.subheader("Latest result")
render_result(history[-1])

st.subheader("All predictions")
table = df[["time", "label", "psmiles", "tg_k", "tg_c", "lower", "upper", "in_domain"]].rename(
    columns={
        "time": "Time", "label": "Name", "psmiles": "Polymer SMILES", "tg_k": "Tg (K)",
        "tg_c": "Tg (°C)", "lower": "Lower (K)", "upper": "Upper (K)", "in_domain": "Inside domain",
    }
)
st.dataframe(table, use_container_width=True, hide_index=True)

d1, d2, _ = st.columns([1, 1, 3])
d1.download_button("Download CSV", table.to_csv(index=False), "polytg_results.csv", "text/csv")
if d2.button("Clear history"):
    st.session_state.history = []
    st.session_state.last_result = None
    st.session_state.home_result = None
    st.rerun()
