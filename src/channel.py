import json
import os
import requests
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.info["items"][0]["snippet"]["title"]
        self.description = self.info["items"][0]["snippet"]["description"]
        self.url = self.info["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriberCount = self.info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.info["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.info["items"][0]["statistics"]["viewCount"]






    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))



    def to_json(self, filename):
        result = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriberCount,
            'video_count': self.video_count,
            'viewCount': self.viewCount
        }
        file = open(filename, "w", encoding='utf-8')
        json.dump(result, file)
        file.close()

    @staticmethod
    def get_service():
        return Channel.youtube