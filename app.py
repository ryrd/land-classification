# python detect.py --weights klasifikasi-lahan-yolo5.pt --conf 0.25 --source image_sample/land.JPG

# load libraries 
import os
import tempfile
from PIL import Image
import streamlit as st

# import yolov5 detect function
from detect import run

def main():
    st.set_page_config(
        page_title="land classification - YOLOv5",
    )
    st.title("LAND CLASSIFICATION - YOLOv5")

    # put model into constant
    WEIGHT = 'klasifikasi-lahan-yolo5.pt'

    # temp file location
    tempfile.tempdir = "/temp"
    print(tempfile.gettempdir())

    # st.checkbox('use GPU')

    form = st.form("file_input")
    form_file = form.file_uploader('import file', type=['jpg','jpeg','mp4'], accept_multiple_files=True)
    preview_btn = form.form_submit_button("preview")

    detect_btn = st.button('detect')

    if preview_btn:
        if form_file is not None:
            for f in form_file:
                if f.type == 'image/jpeg':
                    image_file = Image.open(f)
                    form.image(image_file, width=200)

                elif f.type == 'video/mp4':
                    video_temp.write(f.read())
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    form.video(video_bytes)

    if detect_btn:
        if form_file is not None:
            for f in form_file:
                if f.type == 'image/jpeg':
                    image_file = Image.open(f)
                    form.image(image_file, width=200)

                    print('--------------ngaran:',f)

                    photo_temp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

                    photo_temp.write(f.read())
                    tp_file = open(photo_temp.name, 'rb')
                    run(weights=WEIGHT, source='./image_sample/land.jpg')
                    
                elif f.type == 'video/mp4':
                    video_temp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
                    video_temp.write(f.read())
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    form.video(video_bytes)



# -----------main function-------------
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass