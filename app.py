import streamlit as st
from tmdb.api import get_trending_movies, get_trending_shows, get_movie_cast, get_movie_details, get_popular_titles, get_upcoming_titles
import time
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""", unsafe_allow_html=True)
# st.cache_data.clear()

st.markdown("""

""", unsafe_allow_html=True)

st.set_page_config(
    page_title="StreamTrack",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

@media (max-width:768px){

.scroll-row{
display:flex;
overflow-x:auto;
gap:14px;
padding-bottom:10px;
}

.scroll-row > div{
min-width:140px;
flex-shrink:0;
}

.scroll-row::-webkit-scrollbar{
display:none;
}

}

</style>
""", unsafe_allow_html=True)




# ------this will check titles their id and their type before going on details page--

query_params = st.query_params

if "id" in query_params:
    st.session_state.selected_media = {
        "id": int(query_params["id"]),
        "type": query_params["type"]
    }
    st.switch_page("pages/Titles_Details.py")


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
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; font-size:24px; margin-bottom:20px;">
<span> 
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-stars" viewBox="0 0 16 16">
  <path d="M7.657 6.247c.11-.33.576-.33.686 0l.645 1.937a2.89 2.89 0 0 0 1.829 1.828l1.936.645c.33.11.33.576 0 .686l-1.937.645a2.89 2.89 0 0 0-1.828 1.829l-.645 1.936a.361.361 0 0 1-.686 0l-.645-1.937a2.89 2.89 0 0 0-1.828-1.828l-1.937-.645a.361.361 0 0 1 0-.686l1.937-.645a2.89 2.89 0 0 0 1.828-1.828zM3.794 1.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387A1.73 1.73 0 0 0 4.593 5.69l-.387 1.162a.217.217 0 0 1-.412 0L3.407 5.69A1.73 1.73 0 0 0 2.31 4.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387A1.73 1.73 0 0 0 3.407 2.31zM10.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.16 1.16 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.16 1.16 0 0 0-.732-.732L9.1 2.137a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732z"/>
</svg>
</span>
<span> Trending Movies </span>
</div>
""", unsafe_allow_html=True)

trending_movies = get_trending_movies()

# ?------------------ gets few trending movies of the week from tmdb api----------------------
st.markdown('<div class="scroll-row">', unsafe_allow_html=True)
movie_cols = st.columns(8)


for i, movie in enumerate(trending_movies[:8]):
    with movie_cols[i]:
        if movie['poster']:
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster']}"

            st.markdown(f"""
        <a href="?id={movie['title']}&type=movie" target="_self" style="text-decoration:none;">
            <div style="position:relative;">
                <img src="{poster_url}" style="width:100%; border-radius:14px;">
                <div style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.8); color:#FFD700; padding:4px 8px; border-radius:8px; font-size:13px; font-weight:300;">
                    <i class="bi bi-star-fill"></i>  {movie['rating']}
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

            st.markdown(f"**{movie['title']}**")
st.markdown('</div>', unsafe_allow_html=True)

# ? -------------------------------- this gets trending tv shows ----------------------------------

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:10px; font-size:24px; margin-bottom:20px;">
<span> 
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-stars" viewBox="0 0 16 16">
  <path d="M7.657 6.247c.11-.33.576-.33.686 0l.645 1.937a2.89 2.89 0 0 0 1.829 1.828l1.936.645c.33.11.33.576 0 .686l-1.937.645a2.89 2.89 0 0 0-1.828 1.829l-.645 1.936a.361.361 0 0 1-.686 0l-.645-1.937a2.89 2.89 0 0 0-1.828-1.828l-1.937-.645a.361.361 0 0 1 0-.686l1.937-.645a2.89 2.89 0 0 0 1.828-1.828zM3.794 1.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387A1.73 1.73 0 0 0 4.593 5.69l-.387 1.162a.217.217 0 0 1-.412 0L3.407 5.69A1.73 1.73 0 0 0 2.31 4.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387A1.73 1.73 0 0 0 3.407 2.31zM10.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.16 1.16 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.16 1.16 0 0 0-.732-.732L9.1 2.137a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732z"/>
</svg>
</span>
<span> Trending shows </span>
</div>
""", unsafe_allow_html=True)

trending_shows = get_trending_shows()

show_cols = st.columns(8)

for i, show in enumerate(trending_shows[:8]):
    with show_cols[i]:
        if show['poster']:
            poster_url = f"https://image.tmdb.org/t/p/w500{show['poster']}"

            st.markdown(f"""
        <a href="?id={show['id']}&type=tv" target="_self" style="text-decoration:none;">
            <div style="position:relative;">
                <img src="{poster_url}" style="width:100%; border-radius:14px;">
                <div style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.8); color:#FFD700; padding:4px 8px; border-radius:8px; font-size:13px; font-weight:600;">
                    ⭐ {show['rating']}
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

            st.markdown(f"**{show['title']}**")


# ? ---------------------- this gets popular titles from tmdb --------------------------------------

st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

popular_titles = get_popular_titles()

st.markdown("""
<div style="display:flex; align-items:center; gap:10px; font-size:24px; margin-bottom:20px;">
<span> 
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up-arrow" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M0 0h1v15h15v1H0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V4.9l-3.613 4.417a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61L13.445 4H10.5a.5.5 0 0 1-.5-.5"/>
</svg>
</span>
<span> Popular right now </span>
</div>
""", unsafe_allow_html=True)

cols = st.columns(8)

for i, item in enumerate(popular_titles[:8]):
    with cols[i]:
        if item["poster"]:
            poster_url = f"https://image.tmdb.org/t/p/w500{item['poster']}"

            st.markdown(f"""
<a href="?id={item['id']}&type={item['type']}" target="_self" style="text-decoration:none;">
    <div style="position:relative;margin-bottom:10px; text-align:center;">
        <img src="{poster_url}" 
             style="width:100%; border-radius:14px;">
        <div style="
            position:absolute;
            top:8px;
            right:8px;
            background:rgba(0,0,0,0.75);
            color:#FFD700;
            padding:4px 8px;
            border-radius:8px;
            font-size:13px;
            font-weight:600;
        ">
            ⭐ {item['rating']}
        </div>
    </div>
</a>
""", unsafe_allow_html=True)

            st.markdown(f"**{item['title']}**")

# ? ---------------------- this gets  titles from tmdb --------------------------------------


# ? --------------- Upcoming Media ------------------------------------------------------------

st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:10px; font-size:20px;">
<span> 
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar2-week" viewBox="0 0 16 16">
  <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M2 2a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"/>
  <path d="M2.5 4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5zM11 7.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5zm-3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5zm-5 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5zm3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5z"/>
</svg>
</span>
<span>Upcoming Movies & Shows</span>
</div>
""", unsafe_allow_html=True)


upcoming_titles = get_upcoming_titles()

# ? ----- Carousel State -----
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
<a href="?id={item['id']}&type={item['type']}" target="_self" style="text-decoration:none;">
    <div style="position:relative;">
        <img src="{poster_url}" style="width:100%; border-radius:14px; margin-bottom:10px;">
        <div style="
            position:absolute;
            top:8px;
            right:8px;
            background:rgba(0,0,0,0.75);
            color:#FFD700;
            padding:4px 8px;
            border-radius:8px;
            font-size:13px;
            font-weight:600;
            backdrop-filter: blur(4px);
        ">
            ⭐ {item['rating']}
        </div>
    </div>
</a>
""", unsafe_allow_html=True)

            st.markdown(f"**{item['title']}**")
