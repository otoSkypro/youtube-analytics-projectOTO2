import os
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


class Video:
    __API_KEY: str = os.getenv('YT_API_KEY')
    service = build('youtube', 'v3', developerKey=__API_KEY)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self._init_from_api()

    def __str__(self):
        return f"{self.title}"

    def _init_from_api(self) -> None:
        video_info = self.service.videos().list(id=self.video_id, part='snippet,statistics').execute()
        video_info = video_info['items'][0]

        self.id = video_info['id']
        self.title = video_info['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id}'
        self.view_count = video_info['statistics']['viewCount']
        self.like_count = video_info['statistics']['likeCount']


class PLVideo(Video):


    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"

    def _init_from_api(self) -> None:
        super()._init_from_api()
        self.like_count = None