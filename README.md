# Applied AI Music Recommender

## Project Summary

This project extends my earlier **Music Recommender Simulation (Module 3)** into a more reliable applied AI system.

The original project implemented a **content-based recommender** that ranked songs based on feature similarity (genre, mood, energy, tempo, and valence). It calculated a weighted score for each song and returned the highest ranked recommendations along with explanations.

This extended version adds a **reliability and testing layer** that evaluates recommendation quality, checks for contradictory user inputs, and logs system behavior to make the AI system more transparent and trustworthy.

---

## Why This Project Matters

Recommendation systems influence what people watch, read, and listen to every day. Even simple algorithms can produce convincing results, but they may also introduce bias or unreliable outputs.

This project demonstrates how to move from a simple prototype toward a **trustworthy AI system** by adding validation, guardrails, and explainability to the recommendation process.

---

## System Architecture

The system is organized as a modular pipeline where user preferences and song data flow through several components.

![System Architecture](assets/system_architecture.png)

### Component Overview

**User Preferences**\
Input describing the user's taste (genre, mood, energy level, etc.)

**Song Loader**\
Loads the song catalog from `songs.csv`.

**Scoring Engine**\
Calculates similarity scores between user preferences and each song.

**Ranking and Diversity Layer**\
Ranks songs by score and applies a diversity penalty to avoid repetitive
results.

**Reliability Checker**\
Evaluates recommendation quality, detects contradictory preferences, and
assigns confidence warnings if needed.

**Output Layer**\
Displays final recommendations with explanations and reliability
messages.

**Testing / Evaluation Profiles**\
Predefined test profiles used to check consistency and system behavior.

**Human Review**\
Allows developers or users to inspect results and judge recommendation
quality.

---

## Setup Instructions

Clone the repository:

``` bash
git clone https://github.com/minh1608/applied-ai-music-recommender.git
cd applied-ai-music-recommender
```

Create a virtual environment (optional):

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the recommender:

``` bash
python -m src.main
```

---

## Sample Interactions

### Example 1. High Energy Pop Listener

Input:

    genre = pop
    mood = happy
    energy = 0.9

Output:

    1. Sunrise City – Score: 6.18
       Reason: genre match, mood match, energy similarity

    2. Rooftop Lights – Score: 4.94
       Reason: mood match, energy similarity

---

### Example 2. Chill Lofi Listener

Input:

    genre = lofi
    mood = chill
    energy = 0.35

Output:

    1. Library Rain – Score: 6.50
       Reason: genre match, mood match, energy similarity

    2. Midnight Coding – Score: 5.72
       Reason: genre match, mood match, energy similarity

---

### Example 3. Conflicting Preferences

Input:

    genre = ambient
    mood = intense
    energy = 0.9

Output:

    Warning: user preferences may be contradictory.

    Recommendations returned with lower confidence.

---

## Design Decisions

Several design choices were made to keep the system understandable while improving reliability.

**Content-based filtering** was chosen because the dataset is small and does not include user listening history.

A **weighted scoring system** was used instead of machine learning to keep the model interpretable.

A **diversity penalty** was introduced to reduce repetitive recommendations from the same genre.

A **reliability checker** was added to detect contradictory preferences and provide warnings when recommendations may be weak or inconsistent.

These choices prioritize **transparency and explainability** over complexity.

---

## Testing Summary

The system was evaluated using several user preference profiles, including:

-   high-energy pop listeners
-   chill lofi listeners
-   rock listeners
-   conflicting preference profiles

Testing showed that the recommender produced consistent rankings for well-defined profiles. However, contradictory inputs sometimes produced weaker matches, which motivated the addition of the reliability checker.

---

## Reliability and Evaluation

The system was tested with four user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting ambient-intense profile.

Clear and consistent profiles produced stronger recommendations and received **HIGH confidence** scores. For example, Chill Lofi and Deep Intense Rock both produced top recommendation scores above 6.0 and were labeled as high-confidence outputs.

The conflicting profile triggered warning messages because the requested genre, mood, and energy level did not align well. In that case, the system returned recommendations with **LOW confidence** and explicitly noted that the profile contained contradictory preferences.

This reliability layer makes the recommender more trustworthy by helping users understand not only what was recommended, but also how dependable those recommendations are.

---

## Reflection

This project showed how even simple recommendation algorithms can feel intelligent when they combine structured data with ranking logic.

More importantly, it highlighted how **AI systems need reliability checks and transparency**. Without evaluation and guardrails, recommendation systems can easily produce misleading outputs or reinforce bias.

Building this system reinforced the importance of explainability, testing, and responsible design when creating AI-driven applications.
