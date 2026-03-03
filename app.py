import streamlit as st
from tmdb.api import get_trending_movies, get_discover_titles, get_trending_shows, get_movie_cast, get_movie_details, get_popular_titles, get_upcoming_titles
import time

# st.cache_data.clear()


st.set_page_config(
    page_title="StreamTrack",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------this will check titles their id and their type before going on details page--

query_params = st.query_params

if "id" in query_params:
    st.session_state.selected_media = {
        "id": int(query_params["id"]),
        "type": query_params["type"]
    }
    st.switch_page("pages/Titles_Details.py")

st.markdown("""
<style>
@media (max-width: 768px) {
    img {
        height: 200px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# ? Get trending movies
movies = get_trending_movies()

# This changes the featured movies in every 2 hour to limit the api call
if movies:
    bucket = int(time.time() // 7200)  # 7200 = 2 hours
    index = bucket % len(movies)

    # ? this will find random movies from trending charts on tmdb api
    featured = movies[index]

    # --------------------------- Get details for current movie--------------------------------------------
    details = get_movie_details(featured['id'])
    cast = get_movie_cast(featured['id'])
    # ? this combines two dictionaries - here in case featured content and their details
    featured = {**featured, **details}

    # -------------------------- for getting logo ---------------------------------------------------------
    if details.get("logo"):
        logo_url = f"https://image.tmdb.org/t/p/original{details['logo']}"
        title_content = f'<img src="{logo_url}" style="max-height:100px;">'
    else:
        title_content = f'<div style="margin:0; font-size:3rem; font-weight:bold; color:white;">{details["title"]}</div>'

    # ------------------------------ Backdrop image -------------------------------
    if featured.get('backdrop'):
        backdrop_url = f"https://image.tmdb.org/t/p/w1920{featured['backdrop']}"

        html_content = f"""
        <div style="position: relative; width: 100%; height:520px; overflow: hidden; border-radius: 20px;">
            <img src="{backdrop_url}" style="width: 100%; height: 100%; object-fit:cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 150px; background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 100%);"></div>
            <div style="position: absolute; bottom: 80px; left: 40px;">
                <div style="margin: 0; text-shadow: 3px 3px 6px rgba(0,0,0,0.9);">{title_content}</div>
            </div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.warning("Backdrop image not available")
else:
    st.info("Featured content is temporarily unavailable. Please check TMDB API configuration and try again.")


# st.button("Add to library") # todo have to make the library functionality

# ---------------------------------------------------------------------------------------------------------

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

# ? Cast section
# st.markdown("### 🎭 Cast")

# cast_cols = st.columns(8)

# for i, person in enumerate(cast[:8]):
#     with cast_cols[i]:
#         if person['profile_path']:
#             profile_url = f"https://image.tmdb.org/t/p/w185{person['profile_path']}"

#             # HTML/CSS for circular image
#             st.markdown(f"""
#                 <div style="text-align: center;">
#                     <img src="{profile_url}"
#                          style="width: 120px;
#                                 height: 120px;
#                                 border-radius: 20%;
#                                 object-fit: cover;
#                                 margin-x :auto;
#                                 ">
#                 </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("👤")

#         st.markdown(f"**{person['name']}**")
#         st.caption(person['character'])

st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
st.subheader(" Trending Movies")

trending_movies = get_trending_movies()

# ? gets few trending movies of the week from tmdb api

movie_cols = st.columns(8)

for i, movie in enumerate(trending_movies[:8]):
    with movie_cols[i]:

        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster']}"

        st.markdown(f"""
        <a href="?id={movie['id']}&type=movie" target="_self">
            <img src="{poster_url}" style="width:100%; border-radius:14px;">
        </a>
        """, unsafe_allow_html=True)

        st.markdown(f"**{movie['title']}**")
        st.caption(f"⭐ {movie['rating']}/10")

        # Remove default button styling
        st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            background: none;
            border: none;
            padding: 0;
        }
        </style>
        """, unsafe_allow_html=True)


# -------------------------------- this gets trending tv shows ----------------------------------

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
st.subheader("🌠 Trending TV shows ")

trending_shows = get_trending_shows()

show_cols = st.columns(8)

for i, show in enumerate(trending_shows[:8]):
    with show_cols[i]:
        if show['poster']:
            poster_url = f"https://image.tmdb.org/t/p/w500{show['poster']}"

        st.markdown(f"""
        <a href="?id={show['id']}&type=tv" target="_self">
            <img src="{poster_url}" 
                 style="width:100%; border-radius:14px;">
        </a>
        """, unsafe_allow_html=True)

        st.markdown(f"**{show['title']}**")
        st.caption(f"⭐ {show['rating']}/10")


# ---------------------- this gets popular titles from tmdb --------------------------------------

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

popular_titles = get_popular_titles()

st.subheader("🌠 Popular right now")

cols = st.columns(8)

for i, item in enumerate(popular_titles[:8]):
    with cols[i]:
        if item["poster"]:
            poster_url = f"https://image.tmdb.org/t/p/w500{item['poster']}"

        st.markdown(f"""
<a href="?id={item['id']}&type={item['type']}" target="_self">
    <img src="{poster_url}" style="width:100%; border-radius:14px;">
</a>
""", unsafe_allow_html=True)

        st.markdown(f"**{item['title']}**")
        st.caption(f"⭐ {item['rating']}/10")

# ---------------------- this gets  titles from tmdb --------------------------------------
if st.button("View", key=f"{item['id']}"):
    st.session_state.selected_media = {
        "id": item["id"],
        "type": item["type"]
    }
    st.switch_page("Pages/Titles_Details.py")

# --------------- Upcoming Media ------------------------------------------------------------

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

st.subheader("📅 Upcoming Movies & Shows")
upcoming_titles = get_upcoming_titles()

# ----- Carousel State -----
if "upcoming_index" not in st.session_state:
    st.session_state.upcoming_index = 0

items_per_page = 8
total_items = len(upcoming_titles)

# Controls Row
left_col, mid_col, right_col = st.columns([1, 8, 1])

with left_col:
    if st.button("<-", key="upcoming_left"):
        st.session_state.upcoming_index = max(
            0,
            st.session_state.upcoming_index - items_per_page
        )

with right_col:
    if st.button("->", key="upcoming_right"):
        if st.session_state.upcoming_index + items_per_page < total_items:
            st.session_state.upcoming_index += items_per_page


# Display Window
start = st.session_state.upcoming_index
end = start + items_per_page

visible_items = upcoming_titles[start:end]

cols = st.columns(items_per_page)

for i, item in enumerate(visible_items):
    with cols[i]:
        if item["poster"]:
            poster_url = f"https://image.tmdb.org/t/p/w500{item['poster']}"

            st.markdown(f"""
<a href="?id={item['id']}&type={item['type']}" target="_self">
    <img src="{poster_url}" style="width:100%; border-radius:14px;">
</a>
""", unsafe_allow_html=True)

        st.markdown(f"**{item['title']}**")
        st.caption(f"⭐ {item['rating']}/10")
