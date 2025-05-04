import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model and dataset
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Laptop Price Predictor")

# Brand
company = st.selectbox('Brand', df['Company'].unique())

# Type
type = st.selectbox('Type', df['TypeName'].unique())

# RAM
ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

# Weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS', ['No', 'Yes'])

# Screen size
screen_size = st.slider('Screen size (in inches)', 10.0, 18.0, 13.0)

# Resolution
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
    '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])

# CPU
cpu = st.selectbox('CPU', df['Cpu brand'].unique())

# HDD
hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])

# SSD
ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])

# GPU
gpu = st.selectbox('GPU', df['Gpu brand'].unique())

# OS
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    # Encode binary fields
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    # Calculate PPI
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2 + Y_res**2)**0.5) / screen_size

    # Create input DataFrame
    query_df = pd.DataFrame([[company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]],
    columns=['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'ppi',
             'Cpu brand', 'HDD', 'SSD', 'Gpu brand', 'os'])


    # Predict
    prediction = pipe.predict(query_df)
    st.title("The price of this Laptop is ₹" + str(int(np.exp(prediction[0]))))