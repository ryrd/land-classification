# python detect.py --weights klasifikasi-lahan-yolo5.pt --conf 0.25 --source image_sample/land.JPG
# load libraries 
import os
import tempfile
import glob
import streamlit as st

# import yolov5 detect function
from detect import run

def main():
    st.set_page_config(page_title="land classification - YOLOv5")
    st.title("LAND CLASSIFICATION - YOLOv5")

    delete_cache = st.button('delete cache files')
    if delete_cache:
        temp_files = glob.glob('./temp/*')
        for f in temp_files:
            os.remove(f)
        detected_files = glob.glob('./detect/exp/*')
        for f in detected_files:
            os.remove(f)

    # reference model as constant variable
    WEIGHT = 'klasifikasi-lahan-yolo5.pt'

    form = st.form("file_input")
    form_file = form.file_uploader('import file', type=['jpg','jpeg','mp4'], accept_multiple_files=True)
    preview_btn = form.form_submit_button("preview")

    detect_btn = st.button('detect')

    if preview_btn:
        if form_file is not None:
            for f in form_file:
                if f.type == 'image/jpeg':
                    photo_temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='./temp', delete=False)
                    photo_temp.write(f.read())
                    tp_file = open(photo_temp.name, 'rb')
                    temp_name = tp_file.name.split("\\")[-1]
                    form.image(f"./temp/{temp_name}", width=200)

                elif f.type == 'video/mp4':
                    video_temp = tempfile.NamedTemporaryFile(suffix='.mp4',dir='./temp', delete=False)
                    video_temp.write(f.read())
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    form.video(video_bytes)

    if detect_btn:
        if form_file is not None:
            for f in form_file:
                if f.type == 'image/jpeg':
                    photo_temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='./temp', delete=False)
                    photo_temp.write(f.read())
                    tp_file = open(photo_temp.name, 'rb')
                    temp_name = tp_file.name.split("\\")[-1]
                    form.image(f"./temp/{temp_name}", width=200)
                    
                    run(weights=WEIGHT, source=f"./temp/{temp_name}")
                    st.image(f"./detect/exp/{temp_name}")

                    with open(f"./detect/exp/{temp_name}", "rb") as detected_file:
                        st.download_button(label="download detected file", data=detected_file, file_name="detected.jpg", mime="image/jpg")
      
                elif f.type == 'video/mp4':
                    video_temp = tempfile.NamedTemporaryFile(suffix='.mp4',dir='./temp', delete=False)
                    video_temp.write(f.read())
                    video_file = open(video_temp.name, 'rb')
                    video_bytes = video_file.read()
                    temp_name = video_file.name.split("\\")[-1]
                    form.video(f"./temp/{temp_name}")
                    
                    run(weights=WEIGHT, source=f"./temp/{temp_name}")
                    
                    st.video(f"./detect/exp/{temp_name}")
                    
                    col1, col2, col3 = st.columns(3)
                    with open(f"./detect/exp/{temp_name}", "rb") as detected_file:
                        col2.download_button(label="download detected file", data=detected_file, file_name="detected.mp4", mime="video/mp4")
                    

# -----------main function-------------
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass