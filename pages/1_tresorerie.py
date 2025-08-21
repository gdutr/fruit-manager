import streamlit as st
from my_package.fruit_manager import *
import requests
import pandas as pd

st.header("Bienvenue dans la section trésorerie")
st.table(st.session_state.history)