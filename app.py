import streamlit as st

from core.ui import inject_css

st.set_page_config(page_title="PolyTg", page_icon="🧪", layout="wide")
inject_css()

pages = [
    st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/predict.py", title="Predict", icon=":material/science:"),
    st.Page("views/summary.py", title="Results Summary", icon=":material/table_chart:"),
    st.Page("views/model.py", title="Model and Method", icon=":material/schema:"),
    st.Page("views/engineer.py", title="ML Engineer", icon=":material/person:"),
]

with st.sidebar:
    st.markdown("### PolyTg")
    st.caption("Polymer glass transition temperature, with an honest range.")

st.navigation(pages).run()
