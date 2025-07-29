import os
from pathlib import Path 
import re 

import logging
from dotenv import load_dotenv


from pydub import AudioSegment
from gtts import gTTS


load_dotenv()


class VoiceOver:
    def __init__(self):
        pass
    def create_voiceover(self,text: str,filename: str) -> Path | str:
       """
       Creates a voiceover mp3 from text and saves to a filename. 
       Saves it to a folder called Voice Overs
       """
       if not self._validate_text(text):
           return None
       
       path = self._prepare_path()
       filename = self._format_filename(filename)
       full_path = path / filename
        
       logging.info(f"Beginning voiceover with text : {text} and filename {filename} ")
                   
       try:
           temp_path = self._generate_tts(text,full_path)
           self._increase_speed(temp_path)
           logging.info(f"Successfully saved voiceover to {full_path}")
           return full_path
       except Exception as e:
           logging.error(f"Error while creating voiceover. Error: {e}")
           return None
       
       
    def _generate_tts(self, text: str, path: Path) -> str:
       tts = gTTS(text)
       tts.save(path) 
       return path
   
    def _increase_speed(self,path : Path):
        
       increase_speed = 1.5
       audio =  AudioSegment.from_file(path)
       faster_audio = audio.speedup(playback_speed=increase_speed)
       
       
       temp_path =  path.with_name(path.stem + "_fast.mp3")
       faster_audio.export(temp_path,format = "mp3")
       os.remove(path)
       
       temp_path.rename(path)
    
    
    def _prepare_path(self) -> Path:
        
        logging.info("Preparing Path ")
        path = Path("Voice Overs")
        try:
            path.mkdir(exist_ok=True)
        except Exception as e:
            logging.error(f"Could not create directory {path}: {e}")
            raise
        return path
        
    def _format_filename(self, filename: str) -> str:
        filename = filename.strip()
        p = Path(filename)
        if p.suffix.lower() != ".mp3":
            filename = filename + ".mp3"
        filename = re.sub(r'[^\w\-.]', '_', filename)
        return filename
        
    def _validate_text(self,text: str) -> bool:
        
        stripped = text.strip()
        
        if not stripped:
            logging.error("Voiceover text is empty")
            return False
        
        if len(stripped) < 5:
            logging.error("Voiceover text is too short")
            return False
        
        if len(stripped) > 5000:
            logging.error("Voiceover text is too long.")
            return False
        
        if not any(c.isalpha() for c in stripped):
            logging.error("Voiceover text must contain letters.")
            return False
    
        if any(char.isdigit() for char in stripped):
            logging.warning("Voiceover text contains numbers")

        return True
    
