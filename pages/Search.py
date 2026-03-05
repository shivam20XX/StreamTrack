import streamlit as st
from tmdb.api import search_titles
import time

query_params = st.query_params
if "id" in query_params and "type" in query_params:
    st.session_state.selected_media = {
        "id": int(query_params["id"]),
        "type": query_params["type"]
    }
    st.switch_page("pages/Titles_Details.py")

st.title("Search")

query = st.text_input("Search movies or TV shows")

results = []

if query and len(query) >= 3:
    time.sleep(0.4)
    results = search_titles(query)
    
if query and len(query) >= 2 and not results:
    st.warning("Oops!, No results found")

cols_per_row = 6

for i in range(0, len(results), cols_per_row):
    row = results[i:i+cols_per_row]
    cols = st.columns(cols_per_row)
    for col, item in zip(cols, row):
        with col:
            poster = item.get("poster")
            if poster:
                 poster_url = f"https://image.tmdb.org/t/p/w500{poster}"
            else:
                 poster_url = "https://via.placeholder.com/500x750?text=No+Image"
            st.markdown(f"""
             <a href="?id={item['id']}&type={item['type']}" target="_self" style="text-decoration:none;color:white;">
                 <img src="{poster_url}" style="width:100%; border-radius:12px;">
            </a>
            """, unsafe_allow_html=True)

            st.markdown(f"**{item['title']}**")
            st.caption(f"⭐ {item['rating']}/10")  