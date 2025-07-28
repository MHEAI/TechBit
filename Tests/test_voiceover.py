import os 
import shutil
from pathlib import Path
import sys

import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.voice_over import VoiceOver

@pytest.fixture(autouse=True)
def cleanup_voice_overs():
    path = Path("Voice Overs")
    if path.exists():
        shutil.rmtree(path)
    yield
    if path.exists():
        shutil.rmtree(path)

# ===== Unit tests on _validate_text  =====

@pytest.mark.parametrize("text,expected", [
    ("   ", False),              # empty after strip
    ("1234", False),             # too short, no letters
    ("a" * 6000, False),         # too long
    ("1234567890", False),       # no letters
    ("abc123", True),            # letters + digits
    ("Hello", True),             # valid text
    ("Hello 123", True),         # valid with numbers
])

def test_validate_text(text,expected):
    v = VoiceOver()
    assert v._validate_text(text) is expected
    
# ===== Integration tests on create_voiceover =====

def test_create_voiceover_creates_file_and_returns_path():
    v = VoiceOver()
    result = v.create_voiceover("Hello world from pytest","testfile")
    assert result is not None
    assert isinstance(result,Path)
    assert result.exists()
    assert result.suffix == ".mp3"   
    
@pytest.mark.parametrize("bad_text", [
    "   ",               # empty
    "1234",              # too short, no letters
    "a" * 6000,          # too long
    "1234567890",        # no letters
])
def test_create_voiceover_returns_none_for_invalid_text(bad_text):
    v = VoiceOver()
    assert v.create_voiceover(bad_text,"invalid_test") is None

def test_format_filename_sanitizes_and_adds_extension():
    vo = VoiceOver()
    f1 = vo._format_filename("testfile")
    assert f1 == "testfile.mp3"
    f2 = vo._format_filename("my file@name!.mp3")
    assert f2 == "my_file_name_.mp3"
    f3 = vo._format_filename("   spaced name  ")
    assert f3 == "spaced_name.mp3"
    f4 = vo._format_filename("already.mp3")
    assert f4 == "already.mp3"


def test_prepare_path_creates_directory():
    vo = VoiceOver()
    path = Path("Voice Overs")
    if path.exists():
        shutil.rmtree(path)
    p = vo._prepare_path()
    assert p.exists()
    assert p.is_dir()