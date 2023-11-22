import datetime
import os
import isodate

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_videos = (PlayList.youtube.playlistItems().list
                                (playlistId=playlist_id, part='contentDetails,snippet', maxResults=50, ).execute())
        self.playlist_video = PlayList.youtube.playlists().list(id=playlist_id, part='snippet',
                                                                 maxResults=50, ).execute()

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(self.video_ids)).execute()
        self.playlist_id = playlist_id
        self.title = self.playlist_video['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        count_time = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            durations = isodate.parse_duration(iso_8601_duration)
            count_time.append(durations)
        duration = sum(count_time, datetime.timedelta())
        return duration

    def show_best_video(self):
        global id_video
        for id_video in self.video_ids:
            better_video = 0
            video_response = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=id_video).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > better_video:
                better_video = like_count
        return f"https://youtu.be/{id_video}"