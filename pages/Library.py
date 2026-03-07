import sqlite3
import streamlit as st

def get_connection():
    return sqlite3.connect("database/streamtrack.db")

def get_library():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM library")
    rows = cursor.fetchall()

    conn.close()
    return rows


library = get_library()

watching = []
completed = []
planned = []

for item in library:

    status = item[5]   # status column

    if status == "watching":
        watching.append(item)

    elif status == "completed":
        completed.append(item)

    else:
        planned.append(item)
        
def show_section(title, items):

    if not items:
        return

    st.subheader(title)

    cols = st.columns(6)

    for i, item in enumerate(items):

        with cols[i % 6]:

            poster = item[4]

            if poster:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster}"
                st.image(poster_url)

            st.caption(item[2])  # title        
            
show_section("Watching", watching)
show_section("Completed", completed)
show_section("Planned", planned)            