import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('YT_API_KEY')
    # api_key = "AIzaSyALba89mzPGZqd4BHZh7Qd8_ywt-hlALmE"
    # youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # api_key: str = os.getenv('YT_API_KEY')
        self._channel_id = channel_id
        result = self.get_service().channels().list(id=self._channel_id, part='snippet,statistics').execute()
        self.title = result["items"][0]["snippet"]["title"]
        self.description = result["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.subscribers = int(result["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(result["items"][0]["statistics"]["videoCount"])
        self.views_count = int(result["items"][0]["statistics"]['viewCount'])

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __eq__(self, other):
        return self.subscribers == other.subscribers

    @property
    def channel_id(self) -> str:
        return self._channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name: str) -> None:
        output_data = {
            "chanel_id": self._channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views_count": self.views_count
        }
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

