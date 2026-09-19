import streamlit as st
import segno
import io #to handle binary data


@st.dialog("Share Class Link")       #this is used for creating dialog box jo upar se  aata hai
def share_subject_dialog(sub_name,sub_code):
    # app_domain= "http://10.2.0.2:8501/"  # filhaal streamlit wali hi url daal di , deploy kkarne ke baad asli daal denge
    app_domain= "mkclass-main.streamlit.app"
    join_url=f"{app_domain}/?join-code={sub_code}" #<<<<<<<f string print ke alawa bhi use ka sakte  hai

    st.header("Scan to Join")

    qr=segno.make(join_url)
    output=io.BytesIO()
    qr.save(output, kind='png',scale=10,border=1)

    col1,col2=st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language='text')   #st.code taki aasani se copy ho jaye
        st.code(sub_code, language='text')
        st.info("copy this link to share this on whatsapp or Email")
    
    with col2:
        st.markdown("### Scan to Join")
        st.image(output.getvalue(),caption="QR Code for Class joining")