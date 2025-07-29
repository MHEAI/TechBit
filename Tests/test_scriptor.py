import json
import os 
import pytest 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.script_maker import Scriptor

def test_seperate_items():
    dummy_data = {
        "topic": "Using the Random Library",
        "hook": "Need a magic trick up your sleeve? Let's code one!",
        "intro": "Today, we're diving into an essential Python library that adds some fun to our coding: The Random Library!",
        "problem": {
            "text": "Imagine creating a game with predictable outcomes... Boring, right? Let's make our programs more exciting by introducing unpredictability!",
            "visual": " Dice rolling animation",
            "emphasize": ["BORING"]
        },
        "solution": {
            "text": "First, import the Random library...\nThen, use the randint function to generate a number between 1 and 10!",
            "code": "import random\nrandom.randint(1, 10)",
            "emphasize": ["IMPORT", "RANDOM.RANDINT"]
        },
        "why_it_matters": "This is a GAME-CHANGER! Randomness makes your code dynamic and adds excitement to games and applications.",
        "common_mistakes": [
            "Using the wrong range (e.g., random.randint(10, 5))",
            "Forgetting to import the library"
        ],
        "outro": "Remember: Randomness can make your code more enjoyable! Keep practicing and let's level up together!",
        "tone": "Energetic, Friendly, Gen Z",
        "visual_tags": ["Coding UI", "Dice rolling"],
        "music_mood": "Upbeat, Fast-paced"
    }

    with open("dummy_script.json", "w", encoding="utf-8") as f:
        json.dump(dummy_data, f, ensure_ascii=False, indent=2)

    scriptor = Scriptor()
    result = scriptor.seperate_items("dummy_script.json")

    expected = (
        dummy_data["topic"],
        dummy_data["hook"],
        dummy_data["intro"],
        dummy_data["problem"]["text"],
        dummy_data["problem"]["visual"],
        dummy_data["solution"]["text"],
        dummy_data["solution"]["code"],
        dummy_data["problem"]["emphasize"] + dummy_data["solution"]["emphasize"],
        dummy_data["why_it_matters"],
        dummy_data["common_mistakes"],
        dummy_data["outro"],
        dummy_data["tone"],
        dummy_data["visual_tags"],
        dummy_data["music_mood"]
    )

    os.remove("dummy_script.json")

    
    assert result == expected
