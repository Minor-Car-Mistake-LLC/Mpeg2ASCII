import cv2
import os
from PIL import Image
from PIL import ImageDraw
import re
import contextlib


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
    asciis = list("""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)1}]?-_+~>i!lI;:,"^`'.""")
    image = ""
    for row in img_list:
        row_str = [str(p) for p in row]
        for item in row_str:
            int(item)
            image += asciis[int(item)]
        image += r"\n"
    image= image.split(r"\n")
    img = Image.new('RGB', (height*6, width*6+4), (255,255,255))
    d = ImageDraw.Draw(img)
    for i, line in enumerate(image):
        d.text((0, i*6), line, fill=(0,0,0))
    img.save("ascii.jpg", "jpeg")
else:
    os.mkdir("mcm_frames")
    os.mkdir("heatsch")
    os.system(f'ffmpeg -i "{video}" "mcm_frames/test-%03d.jpg"')
    cam = cv2.VideoCapture(video)
    fps = int(cam.get(cv2.CAP_PROP_FPS))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    lst = sorted_alphanumeric(os.listdir("mcm_frames"))
    for g, file in enumerate(lst):
        print(file)
        img = cv2.imread(f"mcm_frames/{file}", cv2.IMREAD_GRAYSCALE)
        img //= 4
        img_list = img.tolist()
        asciis = list("""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)1}]?-_+~>i!lI;:,"^`'.""")
        image = []
        cache = ""
        for row in img_list:
            row_str = [str(p) for p in row]
            for item in row_str:
                cache += asciis[int(item)]
            image.append(cache)
            cache = ""
        img = Image.new('RGB', (width*6, height*6+4), (255,255,255))
        d = ImageDraw.Draw(img)
        for i, line in enumerate(image):
            d.multiline_text((0, i), line, fill=(0,0,0), spacing=0)
        img.save(f"heatsch/{str(g)}.jpg", "jpeg")
    os.system(f'ffmpeg -i "{video}" mcm_frames/audio.mp3')
    os.system(f'ffmpeg -framerate {fps} -i heatsch/%d.jpg -i mcm_frames/audio.mp3 -start_number 0 -r {fps} ascii.mp4')
    for _ in range(100):
        with contextlib.suppress(Exception):
            os.remove("heatsch")
            os.remove("mcm_frames")
