#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to download bing images
Created on Wed Dec 12 10:39:05 2018

@author: luca
"""

import requests
import sys
import os
import re
import hashlib

def main():
    print("Download most recent images from Bing Photo of the Day.")
    print("Only images 1920x1080 or bigger are downloaded")
    print("Two parameters must be provided:")
    print("- Number of images to download")
    print("- Destination folder")
    
    #print(len(sys.argv))
    #print(str(sys.argv))
    
    if len(sys.argv)!=3:
        print("Error: Wrong param number")
        sys.exit(1)
    try:
        img_num = int(sys.argv[1])
    except ValueError:
        print("Provided image number is not a number. Using default value: 1")
        img_num = 1
    if img_num <1 or img_num>1000:
        img_num = max(img_num, 1)
        img_num = min(img_num, 1000)
        print(f"Provided image number out of valid range. Clipped to {img_num}")
    
    out_dir = sys.argv[2]
    if not os.path.isdir(out_dir):
        print("Error: Invalid output folder")
        sys.exit(1)
    if not os.access(out_dir, os.W_OK):
        print("Error: No write permission in output folder")
        sys.exit(1)
    
    #Get images metadata
    url = f'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={img_num}&mkt=en-US'
    r = requests.get(url)
    body = r.json()
    print("Found ", len(body['images']), " images")
    skipped = 0
    with open("bing_daily_photo_log.txt", "a") as logfile:
        for img in body['images']:
            url = img['url']
            size = re.split('_|\.|x',url)[-3:-1]
            if int(size[0])<1920 or int(size[1])<1080:
                skipped += 1
                continue
            url = 'https://bing.com' + url
            hash_str = int(hashlib.sha1(img['title'].encode('utf-8')).hexdigest(), 16) % (10 ** 8)
            name = img['startdate'] + "_" + str(hash_str) + "_" + url.split('_')[-1]
            if os.path.isfile(os.path.join(out_dir,name)):
                skipped += 1
                continue
            img_data = requests.get(url)
            print("Saving " + name + "\n\t" + img['title'] + "\n\t" + img['copyright'])
            logfile.write(name + " , " + img['title'] + " , " + img['copyright']+"\n")
            open(os.path.join(out_dir,name), "wb").write(img_data.content)
    if skipped>0:
        print(f"Skipped {skipped} images because of low resolution or already existing")

if __name__ == "__main__":
    # execute only if run as a script
    main()
