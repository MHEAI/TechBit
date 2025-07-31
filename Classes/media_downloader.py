import requests
import os
import logging
import re
from dotenv import load_dotenv

class MediaDownloader:
    def __init__(self) -> None:
        """
        Initialize the MediaDownloader instance by loading environment variables,
        setting up API key and headers, and configuring the logger.
        """
        load_dotenv()
        self.pexels_api_key: str | None = os.getenv("PEXELS_API_KEY")
        self.headers = {"Authorization": self.pexels_api_key}

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize the given filename by replacing any character that is not
        alphanumeric, underscore, or dash with an underscore.

        Args:
            name (str): The original filename string.

        Returns:
            str: The sanitized filename string.
        """
        return re.sub(r'[^A-Za-z0-9_\-]', '_', name)

    def _get_video_url(self, keyword: str) -> str:
        """
        Retrieve the URL of the first video matching the keyword from Pexels API.

        Args:
            keyword (str): The search term to query videos.

        Returns:
            str: The video URL.

        Raises:
            ValueError: If no video is found in the response.
        """
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=1"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        try:
            video_url = data["videos"][0]["video_files"][0]["link"]
            self.logger.info(f"Found video URL: {video_url}")
            return video_url
        except (KeyError, IndexError):
            self.logger.warning("No video found")
            raise ValueError("No video found")

    def _get_image_url(self, keyword: str) -> str:
        """
        Retrieve the URL of the first image matching the keyword from Pexels API.

        Args:
            keyword (str): The search term to query images.

        Returns:
            str: The image URL.

        Raises:
            ValueError: If no image is found in the response.
        """
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=1"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        try:
            image_url = data["photos"][0]["src"]["original"]
            self.logger.info(f"Found image URL: {image_url}")
            return image_url
        except (KeyError, IndexError):
            self.logger.warning("No image found")
            raise ValueError("No image found")

    def _download_file(self, url: str, filename: str) -> str:
        """
        Download the content from the given URL and save it to the specified filename.

        Args:
            url (str): The direct URL to the media file.
            filename (str): The local filename to save the file as.

        Returns:
            str: The filename where the file was saved.

        Raises:
            HTTPError: If the request for the media file fails.
        """
        self.logger.info(f"Downloading from {url} to {filename}")
        response = requests.get(url, headers=self.headers, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.logger.info(f"Download complete: {filename}")
        else:
            self.logger.error(f"Failed to download file: Status code {response.status_code}")
            response.raise_for_status()
        return filename

    def download(self, keyword: str) -> str | None:
        """
        Try to download a video for the given keyword. If no video is found or
        download fails, fallback to downloading an image.

        Args:
            keyword (str): The search term for media.

        Returns:
            str | None: The filename of the downloaded media file, or None if both fail.
        """
        safe_keyword = self._sanitize_filename(keyword)
        video_filename = f"{safe_keyword}.mp4"
        image_filename = f"{safe_keyword}.jpg"
        stock: str | None = None

        try:
            video_url = self._get_video_url(keyword)
            self.logger.info("Starting video download...")
            stock = self._download_file(video_url, video_filename)
        except Exception as e:
            self.logger.error(f"Video download failed: {e}")
            try:
                image_url = self._get_image_url(keyword)
                self.logger.info("Starting image download as fallback...")
                stock = self._download_file(image_url, image_filename)
            except Exception as e:
                self.logger.error(f"Image download failed: {e}")

        return stock
