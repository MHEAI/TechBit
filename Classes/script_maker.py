import json
import re 

import ollama


class Scriptor:
    def __init__(self):
        pass

    def generate_script(self, topic):
        prompt = f"""
        You are a content creator making high-energy YouTube Shorts focused on beginner coding tips and hacks. The final output will be read using a voice generator  and synced with fast-paced visuals.

        For the topic: "{topic}", generate a JSON object following the structure below. This script will be automatically turned into audio and video — so everything must be voice-ready.

        🟢 Voice Style: Energetic, friendly, Gen Z tone. Use short, punchy sentences. Speak like a real person, not a textbook. Contractions are great. Add rhythm. Make it fun.

        🟢 Timing: The total spoken script (all sections) must take between 50–60 seconds when read naturally. Use natural phrasing to hit the right pace.

        🟢 Code Snippet (solution.code): 
        - Must be beginner-friendly.
        - 3 to 6 lines max.
        - Use plain text with `\n` for new lines.
        - Do NOT include comments or explanations.
        - The code should demonstrate the core solution clearly.

        🟢 Emphasis: Use CAPS to emphasize key words (e.g., “This is a GAME-CHANGER.”) for vocal emphasis. Additionally do not use emjos in your answer

        🟢 Pauses: Add `[...]` (3 dots in brackets) to indicate short dramatic pauses.

        🟢 Visual cues: Keep "visual", "visual_tags", "sfx_tags", and "music_mood" fields simple and creative — they help the video editor layer sound and visuals.

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
        "outro": "", 
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
    def seperate_items(self,file):
        with open(file, "r") as f:
            data = json.load(f)

        topic = data["topic"]
        hook = data["hook"]
        intro = data["intro"]
        problem_text = data["problem"]["text"]
        text = data["solution"]["text"]
        visual = data["problem"]["visual"]
        code = data["solution"]["code"]
        emphasize_words = data["problem"]["emphasize"] + data["solution"]["emphasize"]
        outro = data["outro"]

        return topic, hook, intro, problem_text,text, visual, code, emphasize_words, outro