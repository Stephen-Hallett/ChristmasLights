import streamlit as st
from utils.make_tree import make_tree

st.set_page_config(layout="wide")

st.title("Chirstmas Lights Controller")

pattern = ["#fffb82"]
n = st.slider(label="Number of lights", min_value=10, max_value=500, step=1, value=100)
st.pyplot(make_tree(n, pattern))
