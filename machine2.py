import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


col3, col4, col5  = st.columns(3)
col3.metric("Temp", "70*", "1.2")
col4.metric("Wind", "9 mph", "-8")
col5.metric("Humidity", "86%", "4%")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lt_login = load_lottiefile(r"C:\Users\user\source\repos\rps_game\dash\image\login.json")

col1, col2 = st.columns([3,3])

with col1:
    st.title("This is an example")

with col2:
    st_lottie(
        lt_login,
        speed = 1,
        reverse = False,
        loop = True,
        height=120,
        width=225
    )
