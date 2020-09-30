import requests
import json

class YouTubeStats:
    def __init__(self, api_key, channel_id, o_auth_token=None):
        self.api_key = api_key
        self.channel_id = channel_id
        self.o_auth_token = o_auth_token
        self.channel_statistics = None
        self.video_data = None


    def get_channel_statistics(self):
        
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        response_data = requests.get(url)
        data = json.loads(response_data.text)
        try:
            data = data["items"][0]["statistics"]
            self.channel_statistics = data
        except Exception as e:
            data = None
        return data


    def save_to_file(self):
        """
        Saves channel statistics and video data in a single json file
        """

        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return
        channel_data = {self.channel_id : {"channel_statistics":self.channel_statistics, "video_data":self.video_data}}
        channel_name = self.video_data.popitem()[1].get('channelTitle', self.channel_id) 
        channel_name = channel_name.replace(" ","_").lower()
        with open(channel_name+".json", "w") as output:
            #output.write(self.channel_statistics)
            json.dump(channel_data, output, indent=4)
        print(f"Data written into {channel_name}.json file.")


    def get_channel_data(self, order_by="date", limit=5):
        '''
        # Get channel video ids of the requested channel
        '''

        channel_videos = self._get_channel_videos(order_by, limit)
        print(f"Length of the videos: {len(channel_videos)}")
        # part = statistics, snippet, contentDetails
        parts = ['snippet', 'statistics', 'contentDetails']
        for video_id in channel_videos:
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
        self.video_data = channel_videos
        return self.video_data

    def _get_single_video_data(self, video_id, part):
        url = f"https://www.googleapis.com/youtube/v3/videos?key={self.api_key}&id={video_id}&part={part}"
        response = requests.get(url)
        json_data = json.loads(response.text)
        try:
            data = json_data['items'][0][part]
        except KeyError as error:
            print("Error in getting key")
            return dict()
        return data

    def _get_channel_videos(self, _order_by, _limit):
        '''
        Get list of videos for the requested channel
        '''

        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order={_order_by}&maxResults={str(_limit)}"
        print(url)

        videos, next_page_token = self._get_channel_videos_per_page(url)
        index = 0
        while next_page_token is not None and index < 0:
            next_page_url = f'{url}&pageToken={next_page_token}'
            print(f"Next page url : {next_page_url}")
            next_video, next_page_token = self._get_channel_videos_per_page(next_page_url)
            videos.update(next_video)
            index += 1
        return videos

    def _get_channel_videos_per_page(self, url):
        '''
        Get all video ids per page
        '''
        response = requests.get(url)
        json_data = json.loads(response.text)
        channel_videos = dict()
        if 'items' not in json_data:
            return json_data, None
        
        next_page_token = json_data.get('nextPageToken', None)
        for item in json_data['items']:
            try:
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError as error:
                print("Error retrieving key")
        return channel_videos, next_page_token



