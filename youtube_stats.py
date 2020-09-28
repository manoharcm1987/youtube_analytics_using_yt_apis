import requests
import json


class YouTubeStats:
    def __init__(self, api_key, channel_id, o_auth_token=None):
        self.api_key = api_key
        self.channel_id = channel_id
        self.o_auth_token = o_auth_token
        self.channel_statistics = None

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

    def save_to_file(self, channel_name):

        channel_name = channel_name.replace(" ","_").lower()
        with open(channel_name+".json", "w") as output:
            #output.write(self.channel_statistics)
            json.dump(self.channel_statistics, output, indent=4)

    def get_channel_data(self, order_by="date", limit=5):
        # Get channel video ids
        channel_videos = self._get_channel_videos(order_by, limit)

    def _get_channel_videos(self, _order_by, _limit):
        url = f"https://www.googleapis.com/youtube/v3/search?part=id&id={self.channel_id}&key={self.api_key}&order={_order_by}&maxResults={str(_limit)}"
        print(url)
        # channel_videos = requests.get(url)
        # channel_data = json.loads(channel_videos.text)
        # return channel_data


