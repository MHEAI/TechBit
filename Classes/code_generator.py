from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments.styles import monokai  # You can change the style
from io import BytesIO
from PIL import Image

class CodeGenerator:
    def __init__(self):
        pass
    def generate_code(self,code):
        formatter = ImageFormatter(
            font_size=20,
            style='monokai',
            image_format='PNG'
        )

        img_data = BytesIO()
        highlight(code, PythonLexer(), formatter, img_data)
        img_data.seek(0)

        # Save or display
        img = Image.open(img_data)
        img.save('code_snippet.png')
        return "code_snippet.png"






