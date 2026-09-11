import streamlit as st

from supabase import create_client, client
# supabase ka ek instant ban gaya ab is se querie run kar sakte hai
supabase: client= create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
