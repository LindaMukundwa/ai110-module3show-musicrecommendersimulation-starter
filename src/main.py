"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: "Late-Night Study Session"
    # Models a listener who wants quiet, acoustic, emotionally steady music at a slow pace.
    # tempo_bpm ~80 normalized: (80 - 56) / (168 - 56) ≈ 0.21
    #   (56 and 168 are the min/max bpm values in the current catalog)
    user_prefs = {
        "favorite_genre":    "lofi",   # stored for display; not used in scoring
        "preferred_mood":    "chill",  # binary match — weight 0.20
        "target_energy":      0.38,    # low energy              — weight 0.35
        "target_acousticness": 0.80,   # strongly prefers acoustic — weight 0.30
        "target_valence":     0.60,    # moderately positive tone — weight 0.10
        "target_tempo":       0.21,    # ~80 bpm, normalized      — weight 0.05
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
