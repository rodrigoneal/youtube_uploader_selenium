from youtube_uploader_selenium import YouTubeUploader
video_path = "video.mp4"
metadata_path = "meta.json"


uploader = YouTubeUploader(video_path, metadata_path)
was_video_uploaded, video_id = uploader.upload()
assert was_video_uploaded

