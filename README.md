# Reddit Video Compilation Bot

This bot automates the process of fetching, merging, and preparing Reddit videos for batch upload.

## Features

- Downloads top videos from specified subreddits.
- Merges downloaded videos into a single compilation.
- Stores batch upload details in a JSON file.
- Adds the reddit title in each clip
- Automatically increments episode numbers for tracking.
- Upload schedule logic to post on the nearest day (if you select Monday, it will post next Monday)

## Requirements

- Python 3.8+
- PRAW (Reddit) API access
- Youtube API Access (https://developers.google.com/youtube/v3)

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/tyler-le/RedditCompilations
   cd RedditCompilations
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up subreddit configurations in `/configs/<...>.json` following this format:

   ```json
   {
       "<Subreddit>": {
           "title": "Some title",
           "description": "Some description",
           "category": "20", // view the categories here - https://gist.github.com/dgp/1b24bf2961521bd75d6c
           "privacy": "private", // only private is supported
           "episode": 1,
           "duration_in_seconds": 600,
           "publish_day": "Monday"
       }
   }
   ```


4. Upload your Google OAuth2 client credentials in `/configs/config.json` (See https://developers.google.com/youtube/registering_an_application)

5. Upload your PRAW credentials in `.env`.(See https://praw.readthedocs.io/en/stable/getting_started/authentication.html)
```
REDDIT_CLIENT_ID=<...>
REDDIT_CLIENT_SECRET=<...>
REDDIT_USER_AGENT=<...>
```

## Usage

1. Run the bot:

   ```sh
   cd RedditCompilations
   python main.py
   ```

2. The bot will:
   - Prompt you to load your custom subreddit configs at `/configs`
   - Fetch and download top videos from each subreddit based on the config.
   - Merge and re-encode the downloaded videos.
   - Save the videos and batch-upload details to `output/`.

3. To upload the processed videos, run:

   ```sh
   cd RedditCompilations
   python3 -m src.scripts.batch_upload
   ```

   This script will read from `output/batch_upload.json` and upload all compiled videos.

## Configuration

- There is an episode counter built into the title
- The videos will have a text overlay with the original Reddit post title 
- Subreddit configurations are managed via `/configs/<...>.json`.

## Error Handling

- If an error occurs during processing, the bot will log it and continue with the next subreddit.

## Future Improvements

- Extend to other platforms
- Add error logging and retry mechanisms.
- Implement advanced video editing features (e.g., transitions, watermarks).

## License

This project is licensed under the MIT License.
