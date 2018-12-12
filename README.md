# bing_daily_photo_downloader
Simple python script to download most recent images from Bing Photo of the Day.

## Installation
Required python version: 3.6 or more

Required modules: requests

## Usage
To be used as a standalone script. Requires two args:
1) Number of images to look for. One per day starting from today and going back. So it's the number of days to go back in time. Actually Bing API limits it to 8.
2) Destination folder where to save images and log file

eg. /> python bing_downloader.py 1 .



* Images whose width is lower that 1920 will be skipped.
* Images whose height is lower that 1080 will be skipped.
* Images already present in the destination folder will be overwritten.

Thought for automated execution at startup.
