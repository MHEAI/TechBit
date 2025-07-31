import json
import re 
import os 

import ollama


class Scriptor:
    def __init__(self):
        pass

    def generate_script(self, topic):
        prompt = f"""
            You are a content creator making high-energy YouTube Shorts focused on beginner coding tips and hacks. The final output will be read using a voice generator and synced with fast-paced visuals.

            For the topic: "{topic}", generate a JSON object following the structure below. This script will be automatically turned into audio and video — so everything must be voice-ready.

            🟢 Voice Style: Energetic, friendly, Gen Z tone. Use short, punchy sentences. Speak like a real person, not a textbook. Contractions are great. Add rhythm. Make it fun.

            🟢 Timing: The total spoken script (all sections) must take between 50–60 seconds when read naturally. Use natural phrasing to hit the right pace.

            🟢 Code Snippet (solution.code): 
            - Must be beginner-friendly.
            - 3 to 6 lines max.
            - Use plain text with `\\n` for new lines.
            - Do NOT include comments or explanations.
            - The code should demonstrate the core solution clearly.

            🟢 Content Length Requirements:
            - Intro: Write 2 to 3 engaging sentences introducing the topic.
            - Problem: Explain the problem clearly in 3 slightly longer sentences, including why it matters.
            - Solution: Provide a detailed explanation in 3 to 4 sentences, plus the code snippet.
            - Why it matters: Explain in 2 to 3 sentences why this tip is important for beginners.
            - Common Mistakes: List 2 common beginner mistakes related to this topic in 1-2 sentences each.

            🟢 Emphasis: Use CAPS to emphasize key words (e.g., “This is a GAME-CHANGER.”) for vocal emphasis. Do NOT use emojis in your answer.

            🟢 Pauses: Add `[...]` (3 dots in brackets) to indicate short dramatic pauses.

            🟢 Visual cues: In the visual things give one word answer and keep into account that this keyword is going to be passed into a stock image Api

            Return ONLY the valid JSON below. Do NOT include anything else.

            {{
            "topic": "",
            "hook": "",
            "intro": "",
            "problem": {{
                "text": "",
                "visual": "",
                "emphasize": []
            }},
            "solution": {{
                "text": "",
                "code": "",
                "emphasize": []
            }},
            "why_it_matters": "",
            "common_mistakes": [
                "",
                ""
            ],
            "outro": "",
            "tone": "",
            "visual_tags": [],
            "music_mood": ""
            }}
        """

        full_reply = ""

        response_stream = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )

        for chunk in response_stream:
            partial_text = chunk['message']['content']
            print(partial_text, end='', flush=True)  
            full_reply += partial_text

        match = re.search(r'```json(.*?)```', full_reply, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            try:
                script_json = json.loads(json_str)
            except json.JSONDecodeError:
                print("\nFailed to parse JSON response:")
                print(json_str)
                return None
        else:
            print("\nNo JSON block found in the response.")
            return None

        if script_json:
            print("\n\nGenerated TechBit Script:")
            print(json.dumps(script_json, indent=2))
            print(script_json["topic"])
        else:
            print("\nNo valid script generated.")
            
        with open("script.json","w") as f:
            json.dump(script_json,f,indent=2)
    def seperate_items(self, file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        topic = data["topic"]
        hook = data["hook"]
        intro = data["intro"]
        problem_text = data["problem"]["text"]
        problem_visual = data["problem"]["visual"]
        solution_text = data["solution"]["text"]
        solution_code = data["solution"]["code"]
        emphasize_words = data["problem"]["emphasize"] + data["solution"]["emphasize"]
        why_it_matters = data["why_it_matters"]
        common_mistakes = data["common_mistakes"]
        outro = data["outro"]
        tone = data["tone"]
        visual_tags = data["visual_tags"]
        music_mood = data["music_mood"]

        
        return (
            topic,
            hook,
            intro,
            problem_text,
            problem_visual,
            solution_text,
            solution_code,
            emphasize_words,
            why_it_matters,
            common_mistakes,
            outro,
            tone,
            visual_tags,
            music_mood
        )

    
