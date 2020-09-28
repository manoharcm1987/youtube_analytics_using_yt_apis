from youtube_stats import YouTubeStats
from app_constants import AppConstants as Constants


yt = YouTubeStats(Constants.API_KEY, Constants.tv_5_kannada)
data = yt.get_channel_statistics()
print(data)
yt.save_to_file("mkbhd")
yt.get_channel_data(order_by="date", limit=10)