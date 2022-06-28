#!/usr/bin/env python

import os
import sys
import time
from os import path
from PIL import Image
import numpy as np

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

targetMaxFontSize = 20

def main(inputFolderPath, resultFolderPath, textContent):
    stopwords = set(STOPWORDS)
    stopwords.add("in")
    for filename in os.listdir(inputFolderPath):
        if filename.endswith(".png"):
            print("Generating word cloud for " + filename + "...")
            # read the mask / color image taken from
            image_coloring = np.array(Image.open(path.join(inputFolderPath, filename)))

            wc = WordCloud(background_color="black", max_words=2000, mask=image_coloring,
                        stopwords=stopwords, max_font_size=targetMaxFontSize)
            # generate word cloud
            wc.generate(textContent)

            # create coloring from image
            image_colors = ImageColorGenerator(image_coloring)

            # save to file
            wc.recolor(color_func=image_colors).to_file(path.join(resultFolderPath, filename))

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

if __name__ == "__main__":
    # get dragged file(s) path
    try :
        sys.argv[1]
        # check if the file is a video
        if sys.argv[1].split(".")[-1] != "mp4" and sys.argv[1].split(".")[-1] != "mov" and sys.argv[1].split(".")[-1] != "mkv" and sys.argv[1].split(".")[-1] != "m4v" and sys.argv[1].split(".")[-1] != "webm":
            raise TypeError
    except IndexError:
        print("Please drag a valid videos into this script.")
        os.system("pause")

    try:
        # Read the whole text.
        # text = open(path.join(d, 'content.txt')).read()
        # fix this error: 'charmap' codec can't decode byte 0x8f in position 11142: character maps to <undefined>
        textContent = open(path.join(d, 'content.txt'), encoding="utf8").read()
    except Exception as e:
        print(e)
        os.system("pause")

    currentTime = str(int(time.time()))
    targetFrameRate = 15

    try:
        filePath = sys.argv[1].split("/")[-1].split(".")[0]
        resultFolderPath = filePath + "_" + currentTime + "_result"

        if filePath.endswith("_result"):
            currentTime = filePath.split("_")[-2]
            resultFolderPath = filePath

        # ensure directory exists
        if not os.path.exists(resultFolderPath):
            os.makedirs(resultFolderPath)

        if not filePath.endswith("_result"):
            inputFolderPath = filePath

            # ensure directory exists
            if not os.path.exists(inputFolderPath):
                os.makedirs(inputFolderPath)
                print("Splitting the video into frames...")
                os.system("ffmpeg -r 1 -i " + sys.argv[1] + " -r 1 \"" + inputFolderPath + "/input%03d.png\"")

            print(inputFolderPath)
            print("The video has been split into frames.")

            tryTargetMaxFontSize = input("Please enter the target font size of the word cloud (default: " + str(targetMaxFontSize) + "): ")
            if tryTargetMaxFontSize != "" and int(tryTargetMaxFontSize) > 0:
                targetMaxFontSize = int(tryTargetMaxFontSize)
            
            print("The word cloud is being generated...")
            main(inputFolderPath, resultFolderPath, textContent)
            print("The word cloud has been generated.")
        else:
            print("The input file name ends in _result. This means that the video has already been split into frames and the word cloud has already been generated.")
            targetFrameRate = int(input("Please enter the target frame rate of the video: "))

        print("The video is being generated...")
        os.system("ffmpeg -y -r " + str(targetFrameRate) + " -i " + resultFolderPath + "/input%03d.png -r " + str(targetFrameRate) + " -c:v libx264 -pix_fmt yuv420p \"" + resultFolderPath + ".mp4\"")

        # open the file
        os.system("start " + resultFolderPath + ".mp4")
    except Exception as e:
        print(e)
        os.system("pause")