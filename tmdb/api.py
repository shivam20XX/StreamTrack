import requests
from config import TMDB_KEY
import streamlit as st


BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE = 'https://image.tmdb.org/t/p'


# * this function get trending movies from tmdb api
@st.cache_data(ttl=7200)
def get_trending_movies():

    url = f'{BASE_URL}/trending/movie/week'
    params = {"api_key": TMDB_KEY}

    # * api request
    response = requests.get(url, params=params)
    data = response.json().get('results', [])

    # ? appending data in movies
    movies = []
    for movie in data:
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "release": movie["release_date"],
            "poster": movie["poster_path"],
            "backdrop": movie["backdrop_path"],
            "overview": movie["overview"],
            "rating": movie["vote_average"],
        })
    # print("Total trending Movies:",len(movies))
    return movies



# ? function to get movie cast details
@st.cache_data(ttl=3600)
def get_movie_cast(id):

    url = f'{BASE_URL}/movie/{id}/credits'
    params = {"api_key": TMDB_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    cast_list = data.get("cast", [])
    credit_cast = []

    for cast in cast_list:
        credit_cast.append({
            "id": cast["id"],
            "name": cast["name"],
            "character": cast["character"],
            "profile_path": cast["profile_path"]
        })
    # print("total cast ",len(credit_cast))
    return credit_cast


# * this function get a movies details from tmdb api
@st.cache_data(ttl=7200)
def get_movie_details(id):
    url = f'{BASE_URL}/movie/{id}'
    params = {
        "api_key": TMDB_KEY,
        "append_to_response": "credits,videos"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    crew = data.get("credits", {}).get("crew", [])
    
    directors = [c["name"] for c in crew if c.get("job") == "Director"]

    writers = [
    c["name"] for c in crew
    if c.get("job") in ["Writer", "Screenplay", "Story"]
    ]

    producers = [
    c["name"] for c in crew
     if c.get("job") in ["Producer", "Executive Producer"]
    ]

    # ? logo enpoints
    images_response = requests.get(
        f"{BASE_URL}/movie/{id}/images", params={"api_key": TMDB_KEY})
    images_data = images_response.json()

    logos = images_data.get("logos", [])
    logo_path = None

    for logo in logos:
        if logo.get("iso_639_1") == "en":
            logo_path = logo.get("file_path")
            break
        if not logo_path and logos:
            logo_path = logos[0].get("file_path")

    crew = data.get("credits", {}).get("crew", [])

    # Get directors
    directors = [c["name"] for c in crew if c.get("job") == "Director"]

    # Get writers (multiple job titles)
    writers = [c["name"] for c in crew if c.get(
        "job") in ["Writer", "Screenplay", "Story"]]

    writers = list(set(writers))

    # Get trailer key from videos
    trailer_key = None
    videos = data.get("videos", {}).get("results", [])
    for video in videos:
        if video.get("type") == "Trailer" and video.get("site") == "YouTube":
            trailer_key = video.get("key")
            break

    return {
        "id": data["id"],
        "title": data["title"],
        "overview": data.get("overview", ""),
        "poster": data.get("poster_path"),
        "backdrop": data.get("backdrop_path"),
        "rating": data.get("vote_average"),
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime"),
        "status": data.get("status"),
        "budget": data.get("budget"),
        "origin_country":data.get("origin_country"),
        "revenue": data.get("revenue"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "cast": data.get("credits", {}).get("cast", [])[:10],
        "directors": directors,
        "writers": writers,
        "trailer_key": trailer_key,
        "logo": logo_path,
        "creators": [],
    }

# ? this function get trending shows list from tmdb api

@st.cache_data(ttl=3600)
def get_trending_shows():

    url = f'{BASE_URL}/trending/tv/week'
    params = {"api_key": TMDB_KEY}

    response = requests.get(url, params=params)
    data = response.json().get('results', [])

    shows = []
    for show in data:
        shows.append({
            "id": show["id"],
            "title": show["name"],
            "poster": show["poster_path"],
            "backdrop": show["backdrop_path"],
            "rating": show["vote_average"],
            "overview": show.get("overview", ""),
            "first_air_date": show.get("first_air_date", "")
        })

    return shows

# ? this function gets tv details

@st.cache_data
def get_tv_details(id):
    url = f'{BASE_URL}/tv/{id}'
    params = {
        "api_key": TMDB_KEY,
        "append_to_response": "credits,videos"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # ? this Extracts crew details
    crew = data.get("credits", {}).get("crew", [])
    creators = [c["name"] for c in data.get("created_by", [])]
    crew = data.get("credits", {}).get("crew", [])
    
    directors = [c["name"] for c in crew if c.get("job") == "Director"]

    writers = [
    c["name"] for c in crew
    if c.get("job") in ["Writer", "Screenplay", "Story"]
    ]

    producers = [
    c["name"] for c in crew
    if c.get("job") in ["Producer", "Executive Producer"]
    ]   
    
    
#-----------------------------------------------------------
     # ? this Extracts Videos/trailer details from series
    videos = data.get("videos", {}).get("results", [])
    trailer_key = None

    for video in videos:
      if video.get("site") == "YouTube" and video.get("type") == "Trailer":
        trailer_key = video.get("key")
        break
#-------------------------------------------------------------
    return {
    "id": data["id"],
    "title": data.get("name"),
    "overview": data.get("overview", ""),
    "poster": data.get("poster_path"),
    "backdrop": data.get("backdrop_path"),
    "rating": data.get("vote_average"),
    "release_date": data.get("first_air_date"),
    "last_air_date": data.get("last_air_date"),
    "status": data.get("status"),
    "origin_country": data.get("origin_country"),
    "seasons": data.get("seasons", []),
    "number_of_seasons": data.get("number_of_seasons"),
    "number_of_episodes": data.get("number_of_episodes"),
    "genres": [g["name"] for g in data.get("genres", [])],
    "cast": data.get("credits", {}).get("cast", [])[:10],
    "trailer_key": trailer_key,

    # Crew
    "creators": creators,
    "directors": directors,
    "writers": list(set(writers)),
    "producers": list(set(producers)),
}
    

# ? this function gets TV show cast
@st.cache_data(ttl=7200)
def get_tv_cast(id):
    url = f'{BASE_URL}/tv/{id}/credits'
    params = {"api_key": TMDB_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    cast_list = data.get("cast", [])

    credit_cast = []
    for cast in cast_list:
        credit_cast.append({
            "id": cast["id"],
            "name": cast["name"],
            "character": cast["character"],
            "profile_path": cast["profile_path"]
        })

    return credit_cast


# ? this function gets popular titles form tmdb api
@st.cache_data
def get_popular_titles():
    popular_tv_url = f"{BASE_URL}/tv/popular"
    popular_movie_url = f"{BASE_URL}/movie/popular"
    params = {"api_key": TMDB_KEY}

    # --- Movies ---
    movie_response = requests.get(popular_movie_url, params=params)
    movie_data = movie_response.json().get("results", [])

    # --- TV ---
    tv_response = requests.get(popular_tv_url, params=params)
    tv_data = tv_response.json().get("results", [])

    movie_list = []
    for movie in movie_data:
        movie_list.append({
            "id": movie["id"],
            "title": movie.get("title"),
            "poster": movie.get("poster_path"),
            "rating": movie.get("vote_average"),
            "release_date": movie.get("release_date"),
            "popularity": movie.get("popularity", 0),
            "type": "movie"
        })

    tv_list = []
    for show in tv_data:
        tv_list.append({
            "id": show["id"],
            "title": show.get("name"),  
            "poster": show.get("poster_path"),
            "rating": show.get("vote_average"),
            "release_date": show.get("first_air_date"),
            "popularity": show.get("popularity", 0),
            "type": "tv"
        })

    # --- Combine details ---
    combined = movie_list + tv_list
    combined = sorted(combined, key=lambda x: x["popularity"], reverse=True)

    return combined

@st.cache_data
def get_upcoming_titles():
    upcoming_movie_url=f"{BASE_URL}/movie/upcoming"
    upcoming_tv_url=f"{BASE_URL}/tv/on_the_air"
    
    params = {"api_key": TMDB_KEY}
    
     # --- Movies ---
    upcoming_movie_response = requests.get(upcoming_movie_url, params=params)
    upcoming_movie_data = upcoming_movie_response.json().get("results", [])

    # --- TV ---
    upcoming_tv_response = requests.get(upcoming_tv_url, params=params)
    upcoming_tv_data = upcoming_tv_response.json().get("results", [])
    
    movie_list = []
    for movie in upcoming_movie_data:
        movie_list.append({
            "id": movie["id"],
            "title": movie.get("title"),
            "poster": movie.get("poster_path"),
            "rating": movie.get("vote_average"),
            "release_date": movie.get("release_date"),
            "popularity": movie.get("popularity", 0),
            "type": "movie"
        })

    tv_list = []
    for show in upcoming_tv_data:
        tv_list.append({
            "id": show["id"],
            "title": show.get("name"),  
            "poster": show.get("poster_path"),
            "rating": show.get("vote_average"),
            "release_date": show.get("first_air_date"),
            "popularity": show.get("popularity", 0),
            "type": "tv"
        })
        
        combined = movie_list + tv_list
        combined = sorted(combined, key=lambda x: x["popularity"], reverse=True)

    return combined


#? this function gets discover endpoint from tmdbs api
@st.cache_data(ttl=3600)
def get_discover_titles(media_type="all", sort_by="popularity.desc", page=1):
    params = {
        "api_key": TMDB_KEY,
        "sort_by": sort_by,
        "page": page
    }

    results = []

    if media_type in ["all", "movie"]:
        movie_res = requests.get(f"{BASE_URL}/discover/movie", params=params)
        movies = movie_res.json().get("results", [])

        for movie in movies:
            results.append({
                "id": movie["id"],
                "title": movie.get("title"),
                "poster": movie.get("poster_path"),
                "rating": movie.get("vote_average"),
                "release_date": movie.get("release_date"),
                "type": "movie"
            })

    if media_type in ["all", "tv"]:
        tv_res = requests.get(f"{BASE_URL}/discover/tv", params=params)
        shows = tv_res.json().get("results", [])

        for show in shows:
            results.append({
                "id": show["id"],
                "title": show.get("name"),
                "poster": show.get("poster_path"),
                "rating": show.get("vote_average"),
                "release_date": show.get("first_air_date"),
                "type": "tv"
            })
    return results

##? gets today's airing tv items from tmdb
@st.cache_data(ttl=7200)
def get_tv_today():
    tv_today_url=f"{BASE_URL}/tv/airing_today"
    params = {"api_key": TMDB_KEY}
    
    tv_today_response=requests.get(tv_today_url,params=params)
    tv_today_data=tv_today_response.json().get("results",[])
    
    tv_today_list = []
    
    for tv_today in tv_today_data:
        tv_today_list.append({
            "id": tv_today["id"],
            "title": tv_today.get("name"),
            "poster": tv_today.get("poster_path"),
            "rating": tv_today.get("vote_average"),
            "release_date": tv_today.get("release_date"),
            "popularity": tv_today.get("popularity", 0),
            "type": "tv",
            "overview":tv_today.get("overview"),
        })
        
    return tv_today_list