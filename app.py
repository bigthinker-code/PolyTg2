import streamlit as st

from core.ui import inject_css

st.set_page_config(page_title="PolyTg", page_icon="🌿", layout="wide")
inject_css()

pages = [
    st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/predict.py", title="Predict", icon=":material/science:"),
    st.Page("views/summary.py", title="Results Summary", icon=":material/table_chart:"),
    st.Page("views/model.py", title="Model and Method", icon=":material/schema:"),
    st.Page("views/engineer.py", title="ML Engineer", icon=":material/person:"),
]

with st.sidebar:
    st.markdown(
        '<div class="pt-brand"><svg width="28" height="28" viewBox="0 0 24 24">'
        '<path d="M12 2l8.66 5v10L12 22l-8.66-5V7z" fill="none" stroke="#8FD14F" stroke-width="2"/>'
        '<circle cx="12" cy="12" r="3" fill="#8FD14F"/></svg><span>PolyTg</span></div>'
        '<div class="pt-tag">Polymer glass transition temperature, with an honest range.</div>',
        unsafe_allow_html=True,
    )
import core.ui as _ui
st.sidebar.caption("ui has: " + str([n for n in dir(_ui) if n in ("quick_result", "compare_scale", "verdict", "big_number")]))
st.navigation(pages).run()
