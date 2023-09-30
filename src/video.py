import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


class Video:
    """Класс для видео на YouTube"""
    __API_KEY: str = os.getenv('YT_API_KEY')
    service = build('youtube', 'v3', developerKey=__API_KEY)

    def __init__(self, video_id: str) -> None:
        """Инициализация видео по его ID"""
        self.video_id = video_id
        self._init_from_api()

    def __str__(self):
        """Возвращает строковое представление видео в формате "<название_видео> (<ссылка_на_видео>)"."""
        return f"{self.title}"

    def _init_from_api(self) -> None:
        try:
            video_info = self.service.videos().list(id=self.video_id, part='snippet,statistics').execute()
            video_info = video_info['items'][0]

            self.id = video_info['id']
            self.title = video_info['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={self.id}'
            self.view_count = video_info['statistics']['viewCount']
            self.like_count = video_info['statistics']['likeCount']

        except (HttpError, IndexError) as e:
            print(f'Произошла ошибка при получении данных из YouTube API: {str(e)}')
            # Устанавливаем все свойства, кроме video_id, в None
            self.id = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None


class PLVideo(Video):
    """Класс для видео в плейлисте на YouTube"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Инициализация видео с указанием ID видео и ID плейлиста"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def _init_from_api(self) -> None:
        video_info = self.service.videos().list(id=self.video_id, part='snippet,statistics,contentDetails').execute()
        video_info = video_info['items'][0]

        self.id = video_info['id']
        self.title = video_info['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id}'
        self.view_count = video_info['statistics']['viewCount']
        self.like_count = video_info['statistics']['likeCount']

        # Получаем длительность видео в секундах
        content_details = video_info.get('contentDetails', {})
        duration_iso = content_details.get('duration', '')
        self.duration = self.parse_duration(duration_iso)

    @staticmethod
    def parse_duration(duration_iso: str) -> datetime.timedelta:
        """Преобразует строку длительности из формата ISO 8601 в объект timedelta"""
        if not duration_iso:
            return datetime.timedelta()

        parts = duration_iso.split('T')
        time_parts = parts[-1].split('M')
        hours, minutes, seconds = 0, 0, 0

        if 'H' in time_parts[0]:
            hours = int(time_parts[0].split('H')[0])
            time_parts[0] = time_parts[0].split('H')[1]

        if 'S' in time_parts[0]:
            seconds = int(time_parts[0].split('S')[0])

        if len(time_parts) > 1:
            minutes = int(time_parts[0])
            if 'S' in time_parts[1]:
                seconds = int(time_parts[1].rstrip('S'))

        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)