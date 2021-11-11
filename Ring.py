# https://github.com/tchellomello/python-ring-doorbell

import json
import os
from pathlib import Path
from pprint import pprint
from datetime import datetime
from dateutil import parser

from oauthlib.oauth2 import MissingTokenError
from ring_doorbell import Ring, Auth

cache_file = Path("test_token.cache")
last_video_downloaded = Path("lastvideodownloaded")
password = Path("pwd")

def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

def seak_start_id(backyard, start_datetime_object):
    keep_going = True
    while(keep_going):
        for event in backyard.history(limit=100, kind="motion"):
            print('ID:       %s' % event['id'])
            print('Kind:     %s' % event['kind'])
            print('Answered: %s' % event['answered'])
            print('When:     %s' % event['created_at'])
            last_video_downloaded.write_text('%s' % event['id'])
            datetime_object = parser.parse('%s' % event['created_at'])
            keep_going = datetime_object > start_datetime_object
            if not keep_going:
                break;
            print("Seaking Keep Going: %s" % keep_going)
            print('--' * 50)


def download_videos_create_jpg(backyard, end_datetime_object):
    keep_going = True
    while keep_going:
        older_than = last_video_downloaded.read_text()
        for event in backyard.history(limit=100, older_than=older_than, kind="motion"):
            print('ID:       %s' % event['id'])
            print('Kind:     %s' % event['kind'])
            print('Answered: %s' % event['answered'])
            print('When:     %s' % event['created_at'])
            print('Downloading: %s' % event['id'])
            filename = 'videos/%s.mp4' % event['id']
            try:
                backyard.recording_download(event['id'], filename=filename, override=True)
            except Exception as e:
                print("Download Failed")
            print('Downloaded: %s' % event['id'])
            last_video_downloaded.write_text('%s' % event['id'])
            datetime_object = parser.parse('%s' % event['created_at'])
            keep_going = datetime_object > end_datetime_object
            print("Keep Going: %s" % keep_going)
            print('--' * 50)

        #Make JPEGs
        os.system('./ffmpeg.sh')
        os.system('rm -rf videos')
        os.system('mkdir videos')

def main():
    # Adjust Time Days you want to pull video
    start_datetime_object = parser.parse("2021-11-10 23:30:38+00:00")
    end_datetime_object = parser.parse("2021-11-10 02:30:38+00:00")

    if cache_file.is_file():
        auth = Auth("myproject", json.loads(cache_file.read_text()), token_updated)
    else:
        username = "YOUR USERNAME"
        auth = Auth("myproject", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()

    #Adjust to your account
    devices = ring.devices()
    pprint(devices)
    backyard = devices['stickup_cams'][0]
    if backyard.device_id == '64694e12562c':
        backyard = devices['stickup_cams'][1]

    seak_start_id(backyard, start_datetime_object)
    download_videos_create_jpg(backyard, end_datetime_object)


if __name__ == "__main__":
    main()
