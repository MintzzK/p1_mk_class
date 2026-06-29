import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

def main():
    st.header("Attendence app")
    name = st.text_input("Enter your name")
    cl1, cl2, cl3, cl4 = st.columns(4, gap='large')
    with cl1:
        if st.button("start",type="primary",key="btn1",use_container_width=True):
            st.write(f"Hello, {name}!") 
    with cl2: 
        if st.button("end",type="secondary",key="btn2",use_container_width=100):
            st.write(f"bye, {name}!") 

    st.markdown("""
        <div>
                <img src="https://imgs.search.brave.com/DlB8ooZYwiDhyHR1SXj_hW3xUCK2rKPioZJc9xxaUX4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzUxLzMw/LzY2LzUxMzA2NjVj/N2NiNDUzZmEwMWE5/YjQ2Yjg2Y2MzNjNm/LmpwZw" /img>
                <h1>"This is a cat"</h1>
                <style>
                    button{
                background:teal!important;
                }
                </style>
        </div>
""",unsafe_allow_html=True)