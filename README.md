# Reddit Media Publisher API

A lightweight FastAPI service that allows programmatic posting of images and videos to Reddit using PRAW.

## 🔧 Features

- `POST /publishImage` — post an image to a subreddit
- `POST /publishVideo` — post a video to a subreddit
- Accepts JSON input with media URL
- Uses Reddit's official API with refresh token authentication
- Basic Authentication layer for endpoint security

---

## 📦 API Endpoints

### `POST /publishImage`

Uploads an image to Reddit.

#### Request (application/json):
{
  "oauth_token": "token-placeholder",
  "subreddit": "exampleSubreddit",
  "title": "Your post title",
  "body_text": "Optional post text",
  "media_url": "https://example.com/image.jpg"
}
