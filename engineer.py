import os

import streamlit as st

from core import config
from core.ui import page_header

page_header("ML Engineer", "The person who built PolyTg.")

e = config.ENGINEER
photo = e.get("photo")
if photo and os.path.exists(photo):
    left, right = st.columns([1, 2.5], gap="large")
    left.image(photo, use_container_width=True)
else:
    right = st.container()

with right:
    st.markdown(f"## {e['name']}")
    st.markdown(f"**{e['role']}**")
    st.write(e["bio"])
    links = "".join(
        f'<a class="pt-link" href="{url}" target="_blank">{name}</a>'
        for name, url in config.LINKS.items()
        if url
    )
    if links:
        st.markdown(links, unsafe_allow_html=True)
