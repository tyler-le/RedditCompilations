# Reddit Video Compilation Bot

This bot automates the process of fetching, merging, and preparing Reddit videos for batch upload.

## Features

- Downloads top videos from specified subreddits.
- Merges downloaded videos into a single compilation.
- Stores batch upload details in a JSON file.
- Automatically increments episode numbers for tracking.

## Requirements

- Python 3.8+
- Reddit API access (if using a wrapper for video fetching)
- FFmpeg installed (for video merging and encoding)

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/your-repo/reddit-video-bot.git
   cd reddit-video-bot
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up subreddit configurations in `/configs/subreddit_config.json` following this format:

   ```json
   {
       "<Subreddit>": {
           "title": "Some title",
           "description": "Some description",
           "category": "20",
           "privacy": "private",
           "episode": 1,
           "duration_in_seconds": 600,
           "publish_day": "Monday"
       }
   }
   ```


4. Upload your Google OAuth2 credentials secret in `/configs/config.json` (See https://developers.google.com/youtube/registering_an_application)

5. Upload your PRAW credentials in `.env`.(See https://praw.readthedocs.io/en/stable/getting_started/authentication.html)
```
REDDIT_CLIENT_ID=<...>
REDDIT_CLIENT_SECRET=<...>
REDDIT_USER_AGENT=<...>

```

## Usage

1. Run the bot:

   ```sh
   python main.py
   ```

2. The bot will:
   - Load subreddit configurations from `/configs/subreddit_config.json`.
   - Fetch and download top videos from each subreddit.
   - Merge and re-encode the downloaded videos.
   - Save the batch upload details to `batch_upload.json`.

3. To upload the processed videos, run:

   ```sh
   python scripts/batch_upload.py
   ```

   This script will read `batch_upload.json` and upload all compiled videos.

## Configuration

- Modify `src/constants/constants.py` to change paths or settings.
- Subreddit configurations are managed via `/configs/subreddit_config.json`.

## Error Handling

- If an error occurs during processing, the bot will log it and continue with the next subreddit.

## Future Improvements

- Extend to other platforms
- Add error logging and retry mechanisms.
- Implement advanced video editing features (e.g., transitions, watermarks).

## License

This project is licensed under the MIT License.
