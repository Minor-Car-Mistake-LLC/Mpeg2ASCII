import cv2
import os
from PIL import Image
from PIL import ImageDraw
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

video = input("Video or image:\n")

if "png" in video or "jpg" in video:
    img = cv2.imread(video, cv2.IMREAD_GRAYSCALE)
    width,height = img.shape
    img //= 4
    img_list = img.tolist()
    result = ""
    asciis = list("""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)1}]?-_+~>i!lI;:,"^`'.""")
    h = ""
    for row in img_list:
        row_str = [str(p) for p in row]
        for item in row_str:
            int(item)
            h += asciis[int(item)]
        h += r"\n"

    h = h.split(r"\n")
    img = Image.new('RGB', (height*6, width*6+4), (255,255,255))
    d = ImageDraw.Draw(img)
    iterarion = 0
    for line in h:
        d.multiline_text((0, iterarion), line, fill=(0,0,0), spacing=0)
        iterarion += 6
    img.save("ascii.png", "png")
else:
    os.mkdir("mcm_frames")
    os.mkdir("heatsch")
    os.system(f'ffmpeg -i "{video}" -vf scale=32:-1 "mcm_frames/test-%03d.jpg"')
    
    cam = cv2.VideoCapture(video)
    fps = int(cam.get(cv2.CAP_PROP_FPS))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))

    g = 0

    lst = sorted_alphanumeric(os.listdir("mcm_frames"))

    for file in lst:
        print(file)
        img = cv2.imread("mcm_frames/" + file, cv2.IMREAD_GRAYSCALE)
        img //= 4
        img_list = img.tolist()
        result = ""
        asciis = list("""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)1}]?-_+~>i!lI;:,"^`'.""")
        h = ""
        for row in img_list:
            row_str = [str(p) for p in row]
            for item in row_str:
                int(item)
                h += asciis[int(item)]
            h += r"\n"

        h = h.split(r"\n")
        img = Image.new('RGB', (width*6, height*6+4), (255,255,255))
        d = ImageDraw.Draw(img)
        iterarion = 0
        for line in h:
            d.multiline_text((0, iterarion), line, fill=(0,0,0), spacing=0)
            iterarion += 6
        img.save("heatsch/" + str(g) + ".png", "png")
        g += 1

    os.system(f"ffmpeg -i {video} mcm_frames/audio.mp3")
    os.system(f'ffmpeg -framerate {fps} -i heatsch/%d.png -i mcm_frames/audio.mp3 -start_number 0 -r {fps} ascii.mp4"')
    os.remove("mcm_frames")
    os.remove("heatsch")
