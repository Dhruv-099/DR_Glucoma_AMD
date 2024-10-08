import streamlit as st
import joblib
from PIL import Image
model = joblib.load('model.pkl')
st.title("ML Model Dashboard")
uploaded_file = st.file_uploader("Choose an image...", type="jpg")


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    # Call your prediction function here