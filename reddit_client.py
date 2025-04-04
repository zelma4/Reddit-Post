import praw
from praw.exceptions import APIException, WebSocketException
from typing import Optional
import time

class RedditPoster:
    def __init__(self, client_id, client_secret, refresh_token, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            user_agent=user_agent,
        )

    def post_image(self, subreddit_name: str, title: str, image_path: str) -> str:
        subreddit = self.reddit.subreddit(subreddit_name)
        try:
            submission = subreddit.submit_image(title=title, image_path=image_path)
            return submission.url
        except APIException as e:
            raise Exception(f"Reddit API Error: {e}")

    def post_video(self, subreddit_name: str, title: str, video_path: str, thumbnail_path: Optional[str] = None) -> str:
        subreddit = self.reddit.subreddit(subreddit_name)
        try:
            submission = subreddit.submit_video(title=title, video_path=video_path, thumbnail_path=thumbnail_path)
            return submission.url
        except WebSocketException as e:
            for _ in range(2):
                time.sleep(5)
                new_posts = list(subreddit.new(limit=5))
                for post in new_posts:
                    if title.lower() in post.title.lower():
                        return post.url
            raise Exception("WebSocket error — video may have been posted but cannot confirm.")
        except APIException as e:
            raise Exception(f"Reddit API Error: {e}")