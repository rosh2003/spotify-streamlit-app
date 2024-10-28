# Spotify Mood and Artist Explorer 🎶

Explore Spotify's vast music library by typing in moods, feelings, or specific artist preferences, and get song recommendations tailored to your input. This app provides a user-friendly interface to interact with Spotify’s data through the [Spotify Web API](https://developer.spotify.com/documentation/web-api/).

## Live App

Check out the live app here: [Spotify Mood and Artist Explorer](https://spotify-app-app-zhrnowrmawtiapdddth9dl.streamlit.app)

## Features

- **Mood-Based Song Recommendations**: Enter a word or feeling to get 10 songs that match your input.
- **Liked Songs and All Spotify Options**: Choose between recommendations based on all Spotify songs or your liked songs.
- **Artist Popularity Overview**: View your top 10 artists in short, medium, or long terms.
- **Search for Top Songs by Artist**: Look up a specific artist to see their most popular tracks.

## Setup

To run this app locally, you'll need the following:

1. **Spotify Developer Account**: Register on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an app to obtain your `Client ID` and `Client Secret`.
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/spotify-streamlit-app.git
   cd spotify-streamlit-app
   ```
3. **Environment Variables**:
   - Sign up on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) to obtain your own API keys.
   - Create a `.env` file in the root directory with the following:
     ```plaintext
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the App**:
   ```bash
   streamlit run spotify_app.py
   ```

## Tech Stack

- **Streamlit**: For building the interactive web interface.
- **Spotipy**: For handling interactions with the Spotify Web API.
- **Python-dotenv**: For securely loading environment variables.

## License

This project is licensed under the MIT License.

---
