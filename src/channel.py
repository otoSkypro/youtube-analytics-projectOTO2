import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = "AIzaSyALba89mzPGZqd4BHZh7Qd8_ywt-hlALmE"
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        pass
        # api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey='AIzaSyALba89mzPGZqd4BHZh7Qd8_ywt-hlALmE')
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.subscribers = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.url = f'https://www.youtube.com/channel/{channel_id}'

    @classmethod
    def get_service(cls):
        return  cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pass
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        data = {"channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "video_count": self.video_count,
                "subscribers": self.subscribers,
                "url": self.url

                }
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)