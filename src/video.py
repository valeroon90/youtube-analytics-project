from googleapiclient.discovery import build
import os


class Video:

    def __init__(self, video_id):
        self.__video_id__ = video_id
        youtube = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.__video_id__}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        youtube = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50,).execute()