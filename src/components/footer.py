import streamlit as st

def footer_home(): #footer logo, footer
    logo_url = "https://i.pinimg.com/1200x/04/c2/32/04c23259de100bce953530beed503a96.jpg"
    
    st.markdown(f"""
        <div style="margin-top:2rem;
                    display:flex;
                    gap:6px;
                    align-item:center;
                    justify-content:center">
                 
        <p style="font-weight:bold; color:black;"> 
                Created with ❤️ by  
                <img src="{logo_url}" style="max-height:25px;" />
        </p>
            
        </div>
    """, unsafe_allow_html=True)