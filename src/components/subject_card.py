import streamlit as st

def subject_card(name,section, code, stats=None,footer_callback=None):
    html =f"""
        <div style="background:#84b2a2;
        border-left: 8px solid #EB459E;
        padding:25px;
        border-radius:20px;
        border: 1px solid black;
        margin-bottom: 20px;">

        <h3 style="margin:0;
        color:#004e4e;
        font-size:1.5 rem">{name}
        </h3>
        
        <p style ='color:#035f5e;
        margin:10px 0;">
        
        Code:<span style="background:#338382;
        Color:#212f2a;
        padding:2px 8px;
        border-radius:5px;">{code}</span> | section:{section}
        </p>
        """
    if stats:
        html+="""
        <div style="display:flex;
        gap:8px;
        flex-wrap:wrap;">
        """     
        for icon,label,value in stats:
            html+=f'<div style="background:#EB459E10; padding:5px 12px;border -radius:12px; font-size:0.9rem">{icon}<b{value}</b>{label}</div>'
        html+="</div>"

    st.markdown(html, unsafe_allow_html=True)
    if footer_callback:
        footer_callback()