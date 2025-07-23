from Classes.script_maker import Scriptor
from Classes.code_generator import CodeGenerator
from Classes.uploader import Uploader
from Classes.photo_finder import PhotoFinder
from Classes.video_editor import VideoEditor
from Classes.voice_over import VoiceOver


def main():
    
    scriptor = Scriptor()
    code_generator = CodeGenerator()
    uploader = Uploader()
    photo_finder = PhotoFinder()
    video_editor = VideoEditor()
    voice_over = VoiceOver()
    
    
    
    scriptor.generate_script()
    
    topic, hook,intro, text,visual, code, emphasize_words,outro = scriptor.seperate_characters()
    
    voice_over_path = voice_over.generate_voiceover(topic,hook,intro,text,emphasize_words,outro)
    
    code_snippet = code_generator.generate_code_snippet(code)
    
    photos_paths =  photo_finder.find_photos(visual)
    
    video_path = video_editor.generate_video()
    
    uploader.upload_video(video_path)
    
if __name__ == "__main__":
    main()