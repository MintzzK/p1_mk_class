import streamlit as st

def header_home():
    logo_url = "https://i.pinimg.com/736x/82/92/d7/8292d7783cec70bd9e0671f9230eb1c0.jpg"

    st.markdown(f"""
            <div style = "display:flex;
                      flex-direction:column;
                      align-items:center;
                      justify-content:center; 
                      margin-bottom:30px ; 
                      margin-top:30px">       
                   
            <img src="{logo_url}" style="height:100px;" />
            <h1 style='text-align:center; color:#CFECEC'>M K<br/> CLASS </h1>
            </div>
""", unsafe_allow_html=True)
    
