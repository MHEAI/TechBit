from Classes.script_maker import Scriptor
from Classes.code_generator import CodeGenerator
from Classes.uploader import Uploader
from Classes.photo_finder import PhotoFinder
from Classes.video_editor import VideoEditor
from Classes.voice_over import VoiceOver
from Classes.utils import Utilities

def main():
    
    Utilizer = Utilities()
    scriptor = Scriptor()
    code_generator = CodeGenerator()
    uploader = Uploader()
    photo_finder = PhotoFinder()
    video_editor = VideoEditor()
    voice_over = VoiceOver()
    
    topic = "any cool python fact"
    
    Utilizer.ensure_ollama_running()
    scriptor.generate_script(topic)
    
    topic, hook,intro, problem_text,text,visual, code, emphasize_words,outro = scriptor.seperate_items("script.json")
    
    
    topic_audio = voice_over.create_voiceover(topic,"topic")
    hook_audio = voice_over.create_voiceover(hook,"hook")
    intro_audio = voice_over.create_voiceover(intro,"intro")
    problem_text_audio = voice_over.create_voiceover(problem_text,"problem_text")
    text_audio = voice_over.create_voiceover(text,"text")
    outro_audio = voice_over.create_voiceover(outro,"outro")
    

    # voice_over_path = voice_over.generate_voiceover(topic,hook,intro,text,emphasize_words,outro)
    
    # code_snippet = code_generator.generate_code_snippet(code)
    
    # photos_paths =  photo_finder.find_photos(visual)
    
    # video_path = video_editor.generate_video()
    
    # uploader.upload_video(video_path)
    
if __name__ == "__main__":
    main()