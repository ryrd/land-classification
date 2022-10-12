# load libraries 
import os
from PIL import Image
import streamlit as st

def detect():
    return 'file uploaded'

def main():
    st.title("LAND CLASSIFICATION - YOLOv5")

    # st.checkbox('use GPU')

    form = st.form("file_input")
    detect_file = form.file_uploader('import file')
    form.form_submit_button("Detect")

    if detect_file is not None:
        # print(detect_file)
        if detect_file.type == 'image/jpeg':
            image = Image.open(detect_file)
            form.image(image, width=200)
        # ------video gk mau-------
        # elif detect_file.type == 'video/mp4':
        #     video_file = open(detect_file, 'rb')
        #     video_bytes = video_file.read()
        #     form.video(video_bytes)

    if detect_file:
        st.write('uploaded')
    else:
        st.write('not uploaded')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass