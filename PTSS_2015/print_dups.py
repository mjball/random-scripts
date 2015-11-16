#!/usr/bin/env python

import argparse
import os, os.path
import PIL, PIL.Image, PIL.ExifTags
from datetime import datetime, timedelta

THRESHOLD = timedelta(seconds=4)

__all__ = ('main',)

def main():
    args = parse_args()
    the_dir = args.directory
    sorted_image_info = gather_sorted_image_info(the_dir)
    print_potential_duplicates(sorted_image_info)

def gather_sorted_image_info(the_dir):
    file_info = []

    for filename in os.listdir(the_dir):
        if is_image(filename):
            filepath = os.path.join(the_dir, filename)
            timestamp = extract_exif_timestamp(filepath)
            file_info.append({
                'filepath': filepath,
                'timestamp': timestamp
            })

    return sorted(file_info, key = lambda x: x['timestamp'])

def is_image(the_file):
    # This is Good Enough for the files that come off the camera.
    # Mostly I need to ignore things like .DS_Store
    return the_file.endswith('.JPG')

def extract_exif_timestamp(the_path):
    img = PIL.Image.open(the_path)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    # ex: 2015:11:13 14:46:03
    exif_ts = exif['DateTimeOriginal']
    return datetime.strptime(exif_ts, '%Y:%m:%d %H:%M:%S')

def print_potential_duplicates(images):
    last_filepath = None
    last_timestamp = None

    for image in images:
        timestamp = image['timestamp']
        filepath = image['filepath']

        if last_timestamp:
            delta = timestamp - last_timestamp
            if delta <= THRESHOLD:
                print '{0} - {1} = {2}'.format(last_timestamp, timestamp, delta.seconds)

        last_filepath = filepath
        last_timestamp = timestamp

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    return parser.parse_args()

if __name__ == '__main__':
    main()
