#!/usr/bin/python3

""" mars_rover.py: Learn about Mars Rover by calling Mars Rovers Photos API """

__author__ = "Ali Soltani"
__version__ = "1.0"
__email__ = "alirsm@gmail.com"
__status__ = "Development"

# Standard Modules
import os
import collections
from urllib.error import URLError
import requests
from urllib.request import urlopen
import urllib.request
import mars_rover_conf as conf_file


def get_rover_info():
    """
    Create a list of Rover names with their Camera names
    :param:
    :return:
    """

    # dictionary of Rovers with their total photos
    rover_total_photos_dict = {}
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={}".format(conf_file.API_KEY)
    resp = requests.get(url)
    jsonResponse = resp.json()

    print ("--- list of Rover - Camera names ---")

    # extract Rovers' name with their Cameras' name
    rover_camera_dict = collections.defaultdict(list)

    try:
        for _rover in jsonResponse["rovers"]:
            rover_total_photos_dict[_rover["name"]] = _rover["total_photos"]
            for _camera in _rover["cameras"]:
                rover_camera_dict[_rover["name"]].append(_camera["name"])

        # sort dictionary based on the length of list of values
        for rover, cameras in dict(sorted(rover_camera_dict.items(), key=lambda i: -len(i[1]))).items():
            for camera in cameras:
                print (rover + " - # " + camera)
    except IndexError:
        print("IndexError")

    # print out Rover and Camera names, sorted by number of Cameras descending
    rover_with_most_photos = max(rover_total_photos_dict, key=rover_total_photos_dict.get)
    print ("-------------------------------------------")
    print ("Rover with most photos: {} Num Of Photos: {}".format(rover_with_most_photos, rover_total_photos_dict[rover_with_most_photos]))


def download_rover_photo():
    """
    Downalod Rover Photo files
    :param:
    :return:
    """

    # URL for rover "curiosity" and camera "MAST" on sol=1000
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=MAST&api_key={}".format(conf_file.API_KEY)
    resp = requests.get(url)
    jsonResponse = resp.json()

    photoFileSizeList = []
    for _photo in jsonResponse["photos"]:
        try:
            imgURL = _photo["img_src"]
        except IndexError:
            print ("IndexError")

        # to download photos, the URL must be modified
        if imgURL.startswith('http://'): imgURL = imgURL.replace('http://', 'https://')
        imgURL = imgURL.replace(".jpl", '')

        # extract image filename from URLs
        photoFile = conf_file.PHOTO_FILE_PATH + imgURL.split('/')[-1]

        # download photos to local storage
        try:
            urllib.request.urlretrieve(imgURL, photoFile)
        except URLError as e:
            print ("URLError: {}".format(e))
        print ("photo file {} is downloaded.".format(photoFile))
        photoFileSizeList.append(os.path.getsize(photoFile))
        if (len(photoFileSizeList) == 10):
            break

    # print out the difference between the minimum and maximum file size
    print ("-------------------------------------------")
    print("difference between the minimum and maximum file size: {} bytes".format(max(photoFileSizeList) - min(photoFileSizeList)))

if __name__ == '__main__':
    get_rover_info()
    download_rover_photo()