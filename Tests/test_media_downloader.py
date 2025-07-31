import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.media_downloader import MediaDownloader 


@pytest.fixture
def downloader():
    with patch('Classes.media_downloader.os.getenv', return_value='fake_api_key'):
        yield MediaDownloader()


def test_sanitize_filename(downloader):
    assert downloader._sanitize_filename("hello world!") == "hello_world_"
    assert downloader._sanitize_filename("file-name_123") == "file-name_123"
    assert downloader._sanitize_filename("bad/chars\\test") == "bad_chars_test"


@patch("Classes.media_downloader.requests.get")
def test_get_video_url_success(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "videos": [{"video_files": [{"link": "http://video-url.mp4"}]}]
    }
    mock_get.return_value = mock_response

    url = downloader._get_video_url("test")
    assert url == "http://video-url.mp4"


@patch("Classes.media_downloader.requests.get")
def test_get_video_url_no_video(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.json.return_value = {"videos": []}
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        downloader._get_video_url("test")


@patch("Classes.media_downloader.requests.get")
def test_get_image_url_success(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "photos": [{"src": {"original": "http://image-url.jpg"}}]
    }
    mock_get.return_value = mock_response

    url = downloader._get_image_url("test")
    assert url == "http://image-url.jpg"


@patch("Classes.media_downloader.requests.get")
def test_get_image_url_no_image(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.json.return_value = {"photos": []}
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        downloader._get_image_url("test")


@patch("builtins.open", new_callable=mock_open)
@patch("Classes.media_downloader.requests.get")
def test_download_file_success(mock_get, mock_file, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content = MagicMock(return_value=[b"chunk1", b"chunk2"])
    mock_get.return_value = mock_response

    filename = downloader._download_file("http://some-url", "file.mp4")
    assert filename == "file.mp4"
    mock_file.assert_called_once_with("file.mp4", "wb")
    handle = mock_file()
    handle.write.assert_any_call(b"chunk1")
    handle.write.assert_any_call(b"chunk2")


@patch("Classes.media_downloader.requests.get")
def test_download_file_fail_raises(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("Fail")
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        downloader._download_file("http://bad-url", "file.mp4")


@patch.object(MediaDownloader, '_get_video_url')
@patch.object(MediaDownloader, '_get_image_url')
@patch.object(MediaDownloader, '_download_file')
def test_download_video_success(mock_download_file, mock_get_image_url, mock_get_video_url, downloader):
    mock_get_video_url.return_value = "http://video-url.mp4"
    mock_download_file.return_value = "test.mp4"

    result = downloader.download("test")
    mock_get_video_url.assert_called_once_with("test")
    mock_download_file.assert_called_once_with("http://video-url.mp4", "test.mp4")
    mock_get_image_url.assert_not_called()
    assert result == "test.mp4"


@patch.object(MediaDownloader, '_get_video_url')
@patch.object(MediaDownloader, '_get_image_url')
@patch.object(MediaDownloader, '_download_file')
def test_download_video_fail_image_success(mock_download_file, mock_get_image_url, mock_get_video_url, downloader):
    mock_get_video_url.side_effect = ValueError("No video")
    mock_get_image_url.return_value = "http://image-url.jpg"
    mock_download_file.return_value = "test.jpg"

    result = downloader.download("test")
    mock_get_video_url.assert_called_once_with("test")
    mock_get_image_url.assert_called_once_with("test")
    mock_download_file.assert_called_once_with("http://image-url.jpg", "test.jpg")
    assert result == "test.jpg"


@patch.object(MediaDownloader, '_get_video_url')
@patch.object(MediaDownloader, '_get_image_url')
@patch.object(MediaDownloader, '_download_file')
def test_download_fail_both(mock_download_file, mock_get_image_url, mock_get_video_url, downloader):
    mock_get_video_url.side_effect = ValueError("No video")
    mock_get_image_url.side_effect = ValueError("No image")

    result = downloader.download("test")
    mock_get_video_url.assert_called_once_with("test")
    mock_get_image_url.assert_called_once_with("test")
    mock_download_file.assert_not_called()
    assert result is None
