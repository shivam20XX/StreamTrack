import streamlit as st
from tmdb.api import (
    get_movie_details,
    get_tv_details,
    get_movie_cast,
    get_tv_cast
)

st.set_page_config(layout="wide")

selected = st.session_state.get("selected_media")

if not selected:
    st.warning("No media selected")
    st.stop()

media_id = selected["id"]
media_type = selected["type"]

# --- Loads Correct Data ---
if media_type == "movie":
    details = get_movie_details(media_id)
    cast = get_movie_cast(media_id)

if media_type == "tv":
    details = get_tv_details(media_id)
    cast = get_tv_cast(media_id)

# --- Back Button ---
# if st.button("⬅ Back"):
#     st.switch_page("app.py")

# ---------- BACKDROP ----------
if details.get("backdrop"):
    backdrop_url = f"https://image.tmdb.org/t/p/w1280{details['backdrop']}"

    st.markdown(f"""
    <div style="
        position: relative;
        height: 300px;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 30px;
    ">
        <img src="{backdrop_url}"
             style="width:100%; height:100%; object-fit:cover; filter:brightness(30%);">

        <div style="
            position:absolute;
            bottom:20px;
            left:30px;
            color:white;
        ">
            <h1 style="
                margin:0;
                font-size:2.4rem;
                font-weight:700;
            ">
                {details['title']}
            </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Prepare Fields ---
poster_url = (
    f"https://image.tmdb.org/t/p/w300{details['poster']}"
    if details.get("poster") else None
)

year = (
    details.get("release_date", "")[:4]
    if details.get("release_date") else "N/A"
)
if media_type == "tv":
    seasons = details.get("number_of_seasons")
else:
    seasons = None

runtime = details.get("runtime", "N/A")
genres = " • ".join(details.get("genres", []))
rating = details.get("rating", "N/A")
origin = details.get("origin_country")
status = details.get("status")

# ?---------- tv run time details---------
seasons = details.get("seasons")
episodes = details.get("episodes")
runtime = details.get("runtime")

if media_type == "tv":
    season_text = f"{seasons} Season" if seasons == 1 else f"{seasons} Seasons" if seasons else ""
    episode_text = f"{episodes} Episodes" if episodes else ""
    info_parts = [year, season_text, episode_text, status]
    info_line = " • ".join(part for part in info_parts if part)

else:
    info_parts = [year, f"{runtime} min" if runtime else "", status]
    info_line = " • ".join(part for part in info_parts if part)

# ? --- Layout -----------------------------

col1, col2 = st.columns([1, 2])

with col1:
    if poster_url:
        st.image(poster_url, use_container_width='stretch')

with col2:
    st.title(details["title"])

    st.markdown(
        f"""
    <div style="color:#9ca3af; font-size:0.95rem; margin-bottom:10px;">
        {info_line}
    </div>
    """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:White;
            color:black;
            padding:6px 12px;
            border-radius:6px;
            font-weight:600;
            margin:10px 0;
        ">
        ⭐ {rating}/10
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(details.get("overview", "No overview available"))

# ----- Smaller Starring Section--------------------------------

    names = ", ".join(person["name"] for person in cast[:6])
    st.write("Starring :", names)

# -------------------- Overview of tiles ---------------------------------------------
    if details.get("creators"):
        st.markdown(
            f"**Creator{'s' if len(details['creators']) > 1 else ''} :** {', '.join(details['creators'])}")

    if details.get("writers"):
        st.markdown(f"**Writers :** {', '.join(details['writers'])}")

    if media_type == "tv":
        season_text = f"{seasons} Season" if seasons == 1 else f"{seasons} Seasons"
        info_line = f"{year}  {season_text} • {episodes} Episodes • {status}"

    else:
        info_line = f"{year}  {runtime} min  {status}"

    if details.get("origin_country"):
        st.markdown(f"Country : {origin[0]}")

    st.markdown(f"**Status :** {details.get('status', 'Unknown')}")
    if details.get("genres"):
        genres = " , ".join(details["genres"])
    st.markdown(f"**Genre :** {genres}")

# --- Cast Section ----------------------------------------------------
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
st.markdown("### Top Cast")

cols = st.columns(10)

for i, person in enumerate(cast[:10]):
    with cols[i]:
        if person.get("profile_path"):
            profile_url = f"https://image.tmdb.org/t/p/w185{person['profile_path']}"
            st.image(profile_url, width=110)
        else:
            st.markdown("👤")

        st.caption(person["name"])


# --- Trailer section ---------
st.markdown("<div style= 'margin-top:80px;'></div>", unsafe_allow_html=True)
st.markdown("#### Watch Teasers & Trailers")
if details.get("trailer_key"):
    trailer_url = f"https://www.youtube.com/watch?v={details['trailer_key']}"
    st.video(trailer_url)
