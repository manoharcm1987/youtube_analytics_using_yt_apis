from youtube_stats import YouTubeStats
from app_constants import AppConstants as Constants


yt = YouTubeStats(Constants.API_KEY, Constants.tech_with_tim)
data = yt.get_channel_statistics()
print(data)
yt.get_channel_data()
yt.save_to_file()
yt.get_channel_data(order_by="date", limit=50)