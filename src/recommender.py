import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py

    Fields used in scoring:
        target_energy       -- weight 0.35
        target_acousticness -- weight 0.30
        preferred_mood      -- weight 0.20 (binary match)
        target_valence      -- weight 0.10
        target_tempo        -- weight 0.05 (normalized 0–1)

    Fields stored but not scored:
        favorite_genre
    """
    favorite_genre: str
    preferred_mood: str
    target_energy: float
    target_acousticness: float
    target_valence: float
    target_tempo: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """
        Scoring recipe:
          +2.0  genre match  (discrete bonus — genre is a stronger signal than mood)
          +1.0  mood match   (discrete bonus)
          +0–1  energy similarity: 1 - |song.energy - user.target_energy|
        """
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append(f"genre match ({song.genre}) +2.0")

        if song.mood == user.preferred_mood:
            score += 1.0
            reasons.append(f"mood match ({song.mood}) +1.0")

        energy_sim = round(1.0 - abs(song.energy - user.target_energy), 2)
        score += energy_sim
        reasons.append(f"energy similarity {energy_sim:.2f}")

        return round(score, 4), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            songs.append({
                'id':            int(row['id']),
                'title':         row['title'],
                'artist':        row['artist'],
                'genre':         row['genre'],
                'mood':          row['mood'],
                'energy':        float(row['energy']),
                'tempo_bpm':     float(row['tempo_bpm']),
                'valence':       float(row['valence']),
                'danceability':  float(row['danceability']),
                'acousticness':  float(row['acousticness']),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Scoring recipe:
      +2.0  genre match  (discrete — genre is a stronger identity signal than mood)
      +1.0  mood match   (discrete)
      +0–1  energy similarity: 1 - |song['energy'] - user_prefs['target_energy']|

    Max possible score: 4.0 (genre + mood + perfect energy alignment).
    The 2:1 genre-to-mood ratio reflects that genre defines listening context
    while mood is a softer, more fluid preference.
    """
    score = 0.0
    reasons = []

    if song['genre'] == user_prefs['favorite_genre']:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if song['mood'] == user_prefs['preferred_mood']:
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    energy_sim = round(1.0 - abs(song['energy'] - user_prefs['target_energy']), 2)
    score += energy_sim
    reasons.append(f"energy similarity {energy_sim:.2f} (target {user_prefs['target_energy']}, song {song['energy']})")

    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
