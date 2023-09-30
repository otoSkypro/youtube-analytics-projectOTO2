import json
import os
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    __API_KEY: str = os.getenv('YT_API_KEY')
    service = build('youtube', 'v3', developerKey=__API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        pass
        self.channel_id = channel_id
        self._init_from_api()

    def __str__(self):
        """Возвращает строковое представление канала в формате "<название_канала> (<ссылка_на_канал>)"."""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Выполняет сложение двух каналов по количеству подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Выполняет вычитание двух каналов по количеству подписчиков"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        """Сравнивает два канала по количеству подписчиков и возвращает True, если они равны, иначе False"""
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __lt__(self, other):
        """
        Сравнивает два канала по количеству подписчиков и возвращает True,
        если текущий канал имеет меньше подписчиков, иначе False
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Сравнивает два канала по количеству подписчиков и возвращает True,
        если текущий канал имеет меньше или равно подписчиков, иначе False
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """
        Сравнивает два канала по количеству подписчиков и возвращает True,
        если текущий канал имеет больше подписчиков, иначе False
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Сравнивает два канала по количеству подписчиков и возвращает True,
        если текущий канал имеет больше или равно подписчиков, иначе False
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def _init_from_api(self) -> None:
        channel_info = self.service.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_info = channel_info['items'][0]

        self.id = channel_info['id']
        self.title = channel_info['snippet']['title']
        self.description = channel_info['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.id}'
        self.subscriber_count = channel_info['statistics']['subscriberCount']
        self.video_count = channel_info['statistics']['videoCount']
        self.view_count = channel_info['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return cls.service

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }



        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

