# python detect.py --weights klasifikasi-lahan-yolo5.pt --conf 0.25 --source image_sample/land.JPG

# load libraries 
# import platform
# import sys
# from pathlib import Path
# import argparse
# import torch
import os
import tempfile

# from models.common import DetectMultiBackend
# from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
# from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
#                            increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
# from utils.plots import Annotator, colors, save_one_box
# from utils.torch_utils import select_device, smart_inference_mode

from PIL import Image
import streamlit as st

from detect import run

WEIGHT = 'klasifikasi-lahan-yolo5.pt'

def main():
    st.title("LAND CLASSIFICATION - YOLOv5")

    # st.checkbox('use GPU')

    form = st.form("file_input")
    form_file = form.file_uploader('import file', type=['jpg','jpeg','mp4'])
    form.form_submit_button("Detect")

    tfflie = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)

    if form_file is not None:
        # print(form_file)
        if form_file.type == 'image/jpeg':
            image_file = Image.open(form_file)
            form.image(image_file, width=200)
            run(weights=WEIGHT, source='./image_sample/land2.jpg')
        elif form_file.type == 'video/mp4':
            tfflie.write(form_file.read())
            video_file = open(tfflie.name, 'rb')
            video_bytes = video_file.read()

            form.video(video_bytes)

    if form_file:
        st.write('uploaded')
    else:
        st.write('not uploaded')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass