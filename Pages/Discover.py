import streamlit as st
from tmdb.api import get_discover_titles

st.set_page_config(layout="wide")

# -----------------------------
# Handle clickable poster navigation
# -----------------------------
query_params = st.query_params

if "id" in query_params:
    st.session_state.selected_media = {
        "id": int(query_params["id"]),
        "type": query_params["type"]
    }
    st.query_params.clear()
    st.switch_page("pages/Titles_Details.py")
    st.stop()


st.title("🔍 Discover & Browse Movies / Shows")

# -----------------------------
# Filters
# -----------------------------
type_option = st.selectbox("Type", ["All", "Movies", "TV"])
sort_option = st.selectbox("Sort By", ["Popularity", "Rating", "Release Date"])

sort_map = {
    "Popularity": "popularity.desc",
    "Rating": "vote_average.desc",
    "Release Date": "primary_release_date.desc"
}

media_map = {
    "All": "all",
    "Movies": "movie",
    "TV": "tv"
}

# -----------------------------
# Reset When Filters Change
# -----------------------------
if "last_type" not in st.session_state:
    st.session_state.last_type = type_option

if "last_sort" not in st.session_state:
    st.session_state.last_sort = sort_option

if (
    st.session_state.last_type != type_option
    or st.session_state.last_sort != sort_option
):
    st.session_state.discover_page = 1
    st.session_state.discover_titles = []
    st.session_state.last_type = type_option
    st.session_state.last_sort = sort_option

# -----------------------------
# Session Init
# -----------------------------
if "discover_page" not in st.session_state:
    st.session_state.discover_page = 1

if "discover_titles" not in st.session_state:
    st.session_state.discover_titles = []

# -----------------------------
# Fetch New Page Data
# -----------------------------
new_titles = get_discover_titles(
    media_type=media_map[type_option],
    sort_by=sort_map[sort_option],
    page=st.session_state.discover_page
)

# Append correctly
if st.session_state.discover_page == 1:
    st.session_state.discover_titles = new_titles
else:
    st.session_state.discover_titles += new_titles

titles = st.session_state.discover_titles

# -----------------------------
# Render Grid
# -----------------------------
cols_per_row = 6

for i in range(0, len(titles), cols_per_row):
    row = titles[i:i + cols_per_row]
    cols = st.columns(cols_per_row)

    for col, item in zip(cols, row):
        with col:

            if item["poster"]:
                poster_url = f"https://image.tmdb.org/t/p/w500{item['poster']}"

                badge_text = "Movie" if item["type"] == "movie" else "TV"
                badge_color = "rgba(0,0,0,0.75)" if item["type"] == "movie" else "rgba(0,0,0,0.8)"
                rating = item.get("rating", 0)
                rating_text = f"{rating:.1f}" if rating else "N/A"

                st.markdown(f"""
<a href="?id={item['id']}&type={item['type']}" target="_self" style="text-decoration:none;">
    <div style="position:relative;">
        <img src="{poster_url}" style="width:100%; border-radius:14px; height:270px; object-fit:cover;">
        <div style="position:absolute; top:8px; left:8px; background:{badge_color}; color:white; padding:4px 8px; font-size:11px; font-weight:600; border-radius:6px;">{badge_text}</div>
        <div style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.75); color:white; padding:4px 8px; font-size:11px; font-weight:600; border-radius:6px;">⭐ {rating_text}</div>
    </div>
</a>
""", unsafe_allow_html=True)

            st.markdown(
                f"<div style='font-weight:600; margin-bottom:20px;margin-top:8px; justify-text:center'>{item['title']}</div>",
                unsafe_allow_html=True
            )

# -----------------------------
# Load More
# -----------------------------

st.markdown("<div style='margin-top:20px; text-align:center;'> </div>",
            unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 3])

with col2:
    if st.button("Load More"):
        st.session_state.discover_page += 1
        st.rerun()
