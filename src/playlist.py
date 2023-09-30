from googleapiclient.errors import HttpError
from src.video import PLVideo
from src.channel import Channel
import datetime


class PlayList:
    def __init__(self, playlist_id):
        """Инициализирует объект PlayList с указанным идентификатором плейлиста"""
        self.playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self):
        """Инициализирует атрибуты объекта PlayList, получая данные через YouTube API"""
        try:
            playlist_info = Channel.service.playlists().list(id=self.playlist_id, part='snippet').execute()
            playlist_info = playlist_info['items'][0]['snippet']

            self.title = playlist_info['title']
            self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

            playlist_items = Channel.service.playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails').execute()
            self.video_ids = [item['contentDetails']['videoId'] for item in playlist_items['items']]
        except HttpError as e:
            print(f'An error occurred while fetching data from YouTube API: {str(e)}')

    @property
    def videos(self):
        """Возвращает список объектов PLVideo, представляющих видео в плейлисте"""
        videos = []
        for video_id in self.video_ids:
            video = PLVideo(video_id, self.playlist_id)
            videos.append(video)
        return videos

    @property
    def total_duration(self):
        """Возвращает суммарную длительность плейлиста в виде объекта datetime.timedelta"""
        total_seconds = sum(video.duration.total_seconds() for video in self.videos)
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео в плейлисте (по количеству лайков)"""
        best_video = max(self.videos, key=lambda video: video.like_count)
        return best_video.url