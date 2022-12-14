# python detect.py --weights klasifikasi-lahan-yolo5.pt --conf 0.25 --source image_sample/land.JPG
# load libraries 
import os
import tempfile
import glob
import zipfile
import pathlib
import streamlit as st

# import yolov5 detect function
from detect import run

# to delete cache files from detect and preview function
def delete_caches():
    temp_files = glob.glob('./temp/[!README]*')
    for f in temp_files:
        os.remove(f)
    detected_files = glob.glob('./detect/exp/[!README]*')
    for f in detected_files:
        os.remove(f)
    if os.path.isfile('./detected-files.zip'):
        os.remove('./detected-files.zip')

def main():
    # reference model as constant variable
    WEIGHT = 'klasifikasi-lahan-yolo5.pt'

    st.set_page_config(page_title="land classification - YOLOv5")
    st.title("LAND CLASSIFICATION - YOLOv5")

    # delete cache btn
    delete_cache = st.button('delete cache files')
    if delete_cache:
        delete_caches()

    form = st.form("file_input")
    form_file = form.file_uploader('import file', type=['jpg','jpeg','mp4'], accept_multiple_files=True)
    preview_btn = form.form_submit_button("preview")
    detect_btn = st.button('detect')

    # preview function
    if preview_btn:
        if form_file is not None:
            delete_caches()     # delete previous cache before create new preview cache

            for f in form_file:
                if f.type == 'image/jpeg':
                    photo_temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='./temp', delete=False)  # create new temp file
                    photo_temp.write(f.read())  # write detect file to temp file
                    tp_file = open(photo_temp.name, 'rb')
                    temp_name = tp_file.name.split("\\")[-1] # select file name only from full path
                    form.image(f"./temp/{temp_name}", width=200) # show file to browser

                elif f.type == 'video/mp4':
                    video_temp = tempfile.NamedTemporaryFile(suffix='.mp4',dir='./temp', delete=False)  # create new temp file
                    video_temp.write(f.read())  # write detect file to temp file
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    form.video(video_bytes)     # show file to browser

    if detect_btn:
        if form_file is not None:
            delete_caches()     # delete previous cache before create new detect file cache
            
            for f in form_file:
                if f.type == 'image/jpeg':
                    # same function as preview
                    photo_temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='./temp', delete=False)
                    photo_temp.write(f.read())
                    tp_file = open(photo_temp.name, 'rb')
                    temp_name = tp_file.name.split("\\")[-1]
                    form.image(f"./temp/{temp_name}", width=200)
                    
                    # YOLOv5 detect function
                    run(weights=WEIGHT, source=f"./temp/{temp_name}")
                    st.image(f"./detect/exp/{temp_name}")
      
                elif f.type == 'video/mp4':
                    # same function as preview
                    video_temp = tempfile.NamedTemporaryFile(suffix='.mp4',dir='./temp', delete=False)
                    video_temp.write(f.read())
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    temp_name = video_file.name.split("\\")[-1]
                    form.video(f"./temp/{temp_name}")
                    
                    # YOLOv5 detect function
                    run(weights=WEIGHT, source=f"./temp/{temp_name}")
                    st.video(f"./detect/exp/{temp_name}")
                    col1, col2, col3 = st.columns(3) # to put download detected video file to center

            # select detected video
            detected_to_download = glob.glob('./detect/exp/[!README]*')
            
            # if more than single file to detect save as zip
            if len(detected_to_download) > 1:
                # save to zip
                with zipfile.ZipFile('detected-files.zip', 'w') as zipF:
                    for f in detected_to_download:
                        zipF.write(f, compress_type=zipfile.ZIP_DEFLATED)
                # show download zip button
                with open('./detected-files.zip', 'rb') as zip:
                    st.download_button(label='download detected zip files', data=zip, file_name="detected-files.zip", mime="application/zip")
            
            # if only one file to detect
            else:
                to_download = detected_to_download[0].split("\\")[-1]   # select file name only from full path
                extension = to_download.split(".")[-1]  # select extension from file
                if extension == 'jpg':
                    with open(f"./detect/exp/{to_download}", "rb") as download_photo:
                        st.download_button(label="download detected photo", data=download_photo, file_name=f"{temp_name}", mime="image/jpg")
                elif extension == 'mp4':
                    with open(f"./detect/exp/{to_download}", "rb") as detected_video:
                        col2.download_button(label="download detected video", data=detected_video, file_name=f"{temp_name}", mime="video/mp4")

# -----------main function-------------
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass