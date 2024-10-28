import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Author: Roshan Naik

# Spotify API credentials
load_dotenv('cred.env')  # Load variables from .env
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8888/callback'  


# Set up Spotify API authorization with the required scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-library-read user-top-read"
))

# Streamlit app

# Load Spotify logo
logo = Image.open("spotify_logo.png")  # Adjust path if necessary
logo = logo.resize((600, 300))  # Set width and height to 60x60 pixels

# Create two columns with a 60:40 ratio
col1, col2 = st.columns([3, 2])

with col1:
    st.title("Spotify Song and Artist Recommender")

with col2:
    st.image(logo, use_column_width=True)  # logo in the right column

# Section 1: Song Matches based on Words
st.header("Get Song Matches Based on Your Specific Word:")
data_source = st.radio("Choose Data Source:", ("All of Spotify", "My Liked Songs"))
mood_input = st.text_input("Enter a word from the song title or artist:")
song_limit = 10

if st.button("Show Songs"):
    if data_source == "All of Spotify":
        results = sp.search(q=mood_input, type="track", limit=song_limit)
        songs = [(track['name'], track['artists'][0]['name']) for track in results['tracks']['items']]
    else:
        results = sp.current_user_saved_tracks(limit=50)
        songs = [
            (item['track']['name'], item['track']['artists'][0]['name']) 
            for item in results['items'] 
            if mood_input.lower() in item['track']['name'].lower() or 
            mood_input.lower() in item['track']['artists'][0]['name'].lower()
        ]
        songs = songs[:song_limit]
        
        if not songs:
            st.write(f"No liked songs found with the mood/word '{mood_input}'. Try a different word.")

    st.write("Here are some songs:")
    for idx, (song, artist) in enumerate(songs, start=1):
        st.write(f"{idx}. {song} by {artist}")

st.divider()

# Section 2: Display User's Top Artists
st.header("View Your Top Artists")

# Use radio buttons instead of a dropdown for time range selection
time_range = st.radio("Choose Time Range:", ("Short Term", "Medium Term", "Long Term"))
time_mapping = {"Short Term": "short_term", "Medium Term": "medium_term", "Long Term": "long_term"}
top_artists_limit = st.number_input("How many top artists would you like to see?", min_value=1, max_value=50, value=10)

if st.button("Show My Top Artists", key="show_top_artists"):
    top_artists = sp.current_user_top_artists(limit=top_artists_limit, time_range=time_mapping[time_range])
    st.write(f"Your Top {top_artists_limit} Artists:")
    
    artist_names = [artist['name'] for artist in top_artists['items']]
    artist_popularity = [artist['popularity'] for artist in top_artists['items']]
    
    for idx, artist in enumerate(top_artists['items'], start=1):
        st.write(f"{idx}. {artist['name']} (Popularity: {artist['popularity']})")
    
    # Plotting
    fig, ax = plt.subplots()
    ax.plot(artist_names, artist_popularity, marker='o', linestyle='-', color='#1DB954')
    ax.set_xlabel("Artists")
    ax.set_ylabel("Popularity Score")
    ax.set_ylim([0,100])
    ax.set_title("Top Artists and Their (Global) Popularity Scores")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Display plot in Streamlit
    st.pyplot(fig)

st.divider()

# Section 3: Global Top Artists and Artist's Top Songs in Columns
st.header("Explore Global and Artist-Specific Top Songs")

# Create two columns with a 1:2 ratio for Global Artists and Artist Search
col1, col2 = st.columns([1, 2])

# Column 1: Global Top Artists
with col1:
    st.subheader("Top Global Artists")
    global_artists_limit = st.number_input("How many global top artists would you like to see?", min_value=1, max_value=50, value=10, key="global_artists_limit")
    # Mock global top artists list
    top_global_artists = ["Drake", "Taylor Swift", "Ariana Grande", "Ed Sheeran", "The Weeknd", "Billie Eilish", "Justin Bieber", "Post Malone", "Dua Lipa", "Kanye West"][:global_artists_limit]
    for idx, artist_name in enumerate(top_global_artists, start=1):
        st.write(f"{idx}. {artist_name}")

# Column 2: Search for an Artist and Display Top Songs
with col2:
    st.subheader("Find Top Songs of an Artist")
    artist_input = st.text_input("Enter Artist Name:")
    top_songs_limit = st.number_input("How many top songs would you like to see?", min_value=1, max_value=20, value=10)

    # Automatically display artist's top songs when artist name is entered
    if artist_input:
        results = sp.search(q=f"artist:{artist_input}", type="artist")
        if results['artists']['items']:
            artist_id = results['artists']['items'][0]['id']
            top_tracks = sp.artist_top_tracks(artist_id)
            st.write(f"Top {top_songs_limit} Songs by {artist_input}:")
            for idx, track in enumerate(top_tracks['tracks'][:top_songs_limit], start=1):
                st.write(f"{idx}. {track['name']} (Popularity: {track['popularity']})")
        else:
            st.write("Artist not found. Please try a different name.")
