def home_screen():
    home_layout()             #---the sequence of calling fn is imp
    home_bg() 
    header_home() #fn called

    col1,col2 = st.columns(2 , gap="large")
    with col1:
        st.header("I'm a Teacher")
        st.image("https://i.pinimg.com/1200x/d1/11/ba/d111ba73542116f35f268de3cb136c07.jpg",width=145)
        if st.button("Teacher Portal" ,type="primary", icon=':material/arrow_outward:',icon_position='right'):  
                                                    #material-google material se liya aur icon position text ke righ me kar di (remember ::)
            st.session_state['login_type']="teacher"
            st.rerun()

    with col2:
        st.header("I'm a Student")
        st.image("https://i.pinimg.com/736x/04/f2/4e/04f24e6c28d0d756ec24657ff7a0d370.jpg",width=145)
        if st.button("Student Portal" , type="primary", icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']="student"
            st.rerun()  
