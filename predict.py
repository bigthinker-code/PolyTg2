from datetime import datetime

import pandas as pd
import streamlit as st

from core.engine import get_engine
from core.ui import EXAMPLES, page_header, render_result

page_header(
    "Predict",
    "Enter the repeat unit of a polymer and mark both ends with [*]. For example, polystyrene is [*]CC([*])c1ccccc1.",
)

st.session_state.setdefault("history", [])
st.session_state.setdefault("psmiles_input", "")
st.session_state.setdefault("last_result", None)

try:
    engine = get_engine()
except Exception as e:
    st.error(f"The model could not be loaded: {e}")
    st.stop()


def set_example(value: str):
    st.session_state.psmiles_input = value


def record(label: str, result: dict):
    st.session_state.history.append(
        {"time": datetime.now().strftime("%H:%M:%S"), "label": label or result["psmiles"], **result}
    )


single, batch = st.tabs(["Single polymer", "Batch from CSV"])

with single:
    st.caption("Try an example")
    cols = st.columns(len(EXAMPLES))
    for col, (name, smi) in zip(cols, EXAMPLES.items()):
        col.button(name, key=f"ex_{name}", on_click=set_example, args=(smi,), use_container_width=True)

    psmiles = st.text_input("Polymer SMILES", key="psmiles_input", placeholder="[*]CC([*])c1ccccc1")
    label = st.text_input("Name (optional)", placeholder="For example, my polymer A")

    if st.button("Predict Tg", type="primary"):
        try:
            with st.spinner("Calculating features and predicting..."):
                result = engine.predict(psmiles)
            st.session_state.last_result = result
            known = {v: k for k, v in EXAMPLES.items()}
            record(label or known.get(result["psmiles"], ""), result)
        except Exception as e:
            st.session_state.last_result = None
            st.error(str(e))

    if st.session_state.last_result:
        st.write("")
        render_result(st.session_state.last_result)
        st.page_link("views/summary.py", label="See all results", icon=":material/table_chart:")

with batch:
    st.write("Upload a CSV with a column named psmiles. An optional name column is used as the label. Up to 200 rows.")
    file = st.file_uploader("CSV file", type="csv")
    if file is not None:
        df = pd.read_csv(file)
        if "psmiles" not in df.columns:
            st.error("The file needs a column named psmiles.")
        else:
            df = df.head(200)
            if st.button("Run batch", type="primary"):
                rows, bar = [], st.progress(0.0)
                for i, row in enumerate(df.itertuples(index=False), start=1):
                    smi = str(getattr(row, "psmiles"))
                    name = str(getattr(row, "name", "")) if hasattr(row, "name") else ""
                    try:
                        res = engine.predict(smi)
                        record(name, res)
                        rows.append({"name": name or smi, **res, "error": ""})
                    except Exception as e:
                        rows.append({"name": name or smi, "psmiles": smi, "error": str(e)})
                    bar.progress(i / len(df))
                out = pd.DataFrame(rows)
                st.dataframe(out, use_container_width=True, hide_index=True)
                st.download_button("Download results", out.to_csv(index=False), "polytg_batch.csv", "text/csv")
