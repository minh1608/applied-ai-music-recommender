import csv
from typing import List, Dict, Tuple
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
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and convert numeric fields to numbers.
    """
    songs: List[Dict] = []

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Calculate a weighted recommendation score for one song and explain why.
    """
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs["genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append("mood match (+1.5)")

    energy_similarity = 1 - abs(song["energy"] - user_prefs["energy"])
    energy_points = energy_similarity * 4.0
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    if "tempo" in user_prefs:
        tempo_similarity = 1 - min(abs(song["tempo_bpm"] - user_prefs["tempo"]) / 100, 1)
        tempo_points = tempo_similarity * 1.5
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    if "valence" in user_prefs:
        valence_similarity = 1 - abs(song["valence"] - user_prefs["valence"])
        valence_points = valence_similarity * 1.0
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Score songs, apply a simple diversity penalty, and return the top k results.
    """
    base_scored_songs: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        base_scored_songs.append((song, score, reasons))

    remaining_songs = sorted(
        base_scored_songs,
        key=lambda item: item[1],
        reverse=True,
    )

    selected_recommendations: List[Tuple[Dict, float, str]] = []
    used_artists = set()
    used_genres = set()

    while remaining_songs and len(selected_recommendations) < k:
        best_candidate = None
        best_adjusted_score = float("-inf")
        best_explanation = ""

        for song, base_score, reasons in remaining_songs:
            adjusted_score = base_score
            adjusted_reasons = reasons.copy()

            if song["artist"] in used_artists:
                adjusted_score -= 0.75
                adjusted_reasons.append("artist diversity penalty (-0.75)")

            if song["genre"] in used_genres:
                adjusted_score -= 0.50
                adjusted_reasons.append("genre diversity penalty (-0.50)")

            if adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_candidate = (song, base_score, reasons)
                best_explanation = ", ".join(adjusted_reasons)

        if best_candidate is None:
            break

        chosen_song, _, _ = best_candidate
        selected_recommendations.append((chosen_song, best_adjusted_score, best_explanation))
        used_artists.add(chosen_song["artist"])
        used_genres.add(chosen_song["genre"])

        remaining_songs = [
            item for item in remaining_songs
            if item[0]["id"] != chosen_song["id"]
        ]

    return selected_recommendations


def detect_profile_warnings(user_prefs: Dict) -> List[str]:
    """
    Detect contradictory or risky user preference combinations.
    """
    warnings: List[str] = []

    chill_genres = {"ambient", "lofi", "jazz"}
    intense_moods = {"intense", "aggressive"}
    calm_moods = {"chill", "relaxed", "peaceful"}

    if user_prefs["genre"] in chill_genres and user_prefs["mood"] in intense_moods:
        warnings.append("User preferences may be contradictory: calm genre with intense mood.")

    if user_prefs["genre"] == "ambient" and user_prefs["energy"] >= 0.8:
        warnings.append("User preferences may be contradictory: ambient music usually has lower energy.")

    if user_prefs["mood"] in calm_moods and user_prefs["energy"] >= 0.85:
        warnings.append("User preferences may be contradictory: calm mood with very high energy.")

    return warnings


def calculate_confidence(
    recommendations: List[Tuple[Dict, float, str]],
    warnings: List[str]
) -> Tuple[str, float]:
    """
    Estimate confidence based on top recommendation strength and warnings.
    """
    if not recommendations:
        return "LOW", 0.0

    top_score = recommendations[0][1]

    if warnings:
        if top_score >= 5.5:
            return "MEDIUM", 0.65
        return "LOW", 0.35

    if top_score >= 5.5:
        return "HIGH", 0.90
    if top_score >= 4.0:
        return "MEDIUM", 0.70
    return "LOW", 0.45


def evaluate_recommendations(
    user_prefs: Dict,
    recommendations: List[Tuple[Dict, float, str]]
) -> Dict:
    """
    Run reliability checks and return warnings, confidence, and evaluation notes.
    """
    warnings = detect_profile_warnings(user_prefs)
    confidence_label, confidence_score = calculate_confidence(recommendations, warnings)

    notes: List[str] = []

    if recommendations:
        top_score = recommendations[0][1]
        notes.append(f"Top recommendation score: {top_score:.2f}")

        top_genres = [song["genre"] for song, _, _ in recommendations[:3]]
        if len(set(top_genres)) == 1:
            notes.append("Top results are concentrated in one genre.")

    if warnings:
        notes.append("One or more user preference contradictions were detected.")

    return {
        "warnings": warnings,
        "confidence_label": confidence_label,
        "confidence_score": confidence_score,
        "notes": notes,
    }