import streamlit as st
#st.set_option('deprecation.showfileUploaderEncoding', False)

#import itertools
import os
#import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
#import streamlit.components.v1 as stc

#import io
#file_buffer = st.file_uploader(...)
#text_io = io.TextIOWrapper(file_buffer)

from tensorflow.keras.models import load_model

# File Processing Pkgs
# import pandas as pd
from PIL import Image  


# Fxn
@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img 

def prediksi(im):
    input_size = (224,224)
    channel = (3,)
    input_shape = input_size + channel
    labels = ['COVID', 'Lung_Opacity', 'Normal', 'Viral Pneumonia']

    def preprocess(img,input_size):
        nimg = img.convert('RGB').resize(input_size, resample= 0)
        img_arr = (np.array(nimg))/255
        return img_arr

    def reshape(imgs_arr):
        return np.stack(imgs_arr, axis=0)

    from tensorflow.keras.models import load_model
    MODEL_PATH = 'model.h5'
    model = load_model(MODEL_PATH,compile=False, custom_objects={'KerasLayer': hub.KerasLayer})
    
    # read image
    #im = Image.open(data_uji)
    X = preprocess(im,input_size)
    X = reshape([X])
    y = model.predict(X)
    
    HasilPrediksi=labels[np.argmax(y)],  
    #print()
    #print('Keterangan = ',labels)
    #print()
    #st.write( 'HasilPrediksi = ', HasilPrediksi)
    return HasilPrediksi


st.title("Diagnosa COVID-19 Chest X-Ray")
image_file = st.sidebar.file_uploader("Upload Image",type=['png','jpeg','jpg'])
#image_file = image_file_upload.read()

#uploaded_file = st.sidebar.file_uploader(type="xls", encoding =None, key = 'a')   
#bytes_data = uploaded_file.read()

if image_file is not None:
    file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
    st.write(file_details)
        
    img_uji = load_image(image_file)   

    st.write("HASIL PREDIKSI = ",prediksi(img_uji))

    st.image(img_uji)  # ,width=250,height=250)
    

else:
    st.header("About")
    st.info("Prediksi diagnosa ini dilakukan dengan metoda Deep Learning Convolutional Neural Network, model yang dipergunakan adalah hasil trainning dari 10.300 image dengan nilai akurasi > 90'%")
    st.info("Adh1t10.2@gmail.com")
    st.text("Terimakasih, semoga bermanfaat di era pandemi ini")
