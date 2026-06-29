import streamlit as st

def home_bg():
    st.markdown("""
        <style>
        .stApp{
                background: #4E8975!important;    /*dull sea green*/
                }

            .stApp div[data-testid="stColumn"]{         /*---------teacher aur student wale bg dabbe*/
                background-color:#B3D9D9 !important;    /*light teal*/
                padding:2.5rem !important;
                border-radius:5rem !important;
                }
                
        button{
            background:teal!important;
                }
                
        </style>
""",unsafe_allow_html=True)
    
def tr_bg():
    st.markdown("""
        <style>
                .stApp{
                background: #306754 !important;
                }
        </style>
""",unsafe_allow_html=True)
    
def st_bg():
    st.markdown("""
    <style>
            .stApp{
                background: #306754!important;
                }
    </style>
""",unsafe_allow_html=True)
    
def home_layout():         #overwriten the existings styles
    st.markdown(""" 
        <style>
                @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');            /*-------climate font imported*/
                @import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');  /*-------normal*/
                /*hide top bar*/ 
                    #mainmenu, header, footer {
                        visibility:hidden;            /*---------streanlit ka upar wala part hat jayega unke ads nahi dikhenge*/
                }
                .block-container{
                    padding-top:1.5rem !important;      /*---------is se hymne upar shift kar diya content ko*/
                }

                button[kind="primary"]{                     /*-------------alag alag button ki properties define kar di */
                    border-radius:1.5rem !important;
                    color:white !important;                       /*this is the font colour in the button*/
                    padding:10px 20px !important;
                    border:none !important;
                    transition:transform 0.25s ease-in-out !important;
                    background: #045F5F !important;
                }
                
                button[kind="secondary"]{
                    border-radius:1.5rem !important;
                    color:white !important;                       /*--------------this is the font colour in the button*/
                    padding:10px 20px !important;
                    border:none !important;
                    transition:transform 0.25s ease-in-out !important;
                    background: #045F5F !important;
                }

                button[kind="tertiary"]{
                    border-radius:1.5rem !important;
                    color:black !important;                       /*this is the font colour in the button*/
                    padding:10px 20px !important;
                    border:none !important;
                    transition:transform 0.25s ease-in-out !important;
                    background: #045F5F !important;
                }

                button:hover{                   /*---------is se wo button wala transition hota hai*/
                    transform:scale(1.05)
                }

                h1{                                           /*-------------fonts define ki ------------*/
                    font-family:'Climate Crisis' ,sans-serif !important;
                    font-size: 3.5rem !important;
                    line-height:0.9 !important;
                    margin-bottom: 0rem !important;
                }

                h2{
                    font-family:'Climate Crisis', sans-serif !important;
                    font-size: 2rem !important;
                    line-height:0.9 !important;
                    margin-bottom: 0rem !important;
                }

                h3,h4,p{
                    font-family : 'Raleway',sans-serif ;
                }
                
        </style>
""",unsafe_allow_html=True)