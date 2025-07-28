import json
import os 
import pytest 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.script_maker import Scriptor

def test_seperate_items():
    
    dummy_data = {
        "topic": "Simple Random Generator Game 🚀",
        "hook": "Are you READY to level up your coding skills? Let's make a GAME!",
        "intro": "Today, we're gonna create a fun little random number generator game. This is gonna be a BLAST!",
        "problem": {
            "text": "Ever wanted to generate a random number quickly? Well, here's your solution!",
            "visual": "Random Number Generator",
            "emphasize": ["Ever", "quickly"]
        },
        "solution": {
            "text": "Let's code it! In Python:",
            "code": "import random\nprint(random.randint(1, 100))",
            "emphasize": ["Let's", "Python"]
        },
        "why_it_matters": "This is a GAME-CHANGER because it opens up endless possibilities for creating interactive applications!",
        "outro": "Don't forget to subscribe for more coding tips and tricks! See you next time, coders! 👋",
        "tone": "Energetic, short-form, beginner-friendly",
        "visual_tags": ["Coding", "Random Number Generator", "Python Logo"],
        "music_mood": "Upbeat, Playful"
    }
    
    with open("dummy_script.json","w") as f:
        json.dump(dummy_data,f)
    scriptor = Scriptor()
    
    result = scriptor.seperate_items("dummy_script.json")
    
    expected = (
        dummy_data["topic"],
        dummy_data["hook"],
        dummy_data["intro"],
        dummy_data["problem"]["text"],
        dummy_data["problem"]["visual"],
        dummy_data["solution"]["code"],
        dummy_data["problem"]["emphasize"] + dummy_data["solution"]["emphasize"],
        dummy_data["outro"]
        
    )
    
    assert result == expected
    