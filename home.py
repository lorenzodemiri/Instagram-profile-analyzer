import streamlit as st
import pandas as df
import time
def scrape_profile(username_text, scraper):
    
    #st.text("Scraping profile: {}".format(username_text))
    profile = scraper.set_profile(username_profile=username_text)
    return scraper.get_profile_data()
    

def scrape_post(shortcode_text, shortcode):
    shortcode.empty()
    st.text("SCRAPE POST {}".format(shortcode_text))
    #if st.button("CONT"):
        
def app(username, scraper):

    st.markdown("""
    # Hello {}
    """.format(username), unsafe_allow_html=True)
    print("PROFILE")
    
    username_text = st.text_input(
        "Type the Username profile that do you want to scrape")
    if st.button("Continue"):
        #username.empty()
        st.text("Scraping profile: {}".format(username_text))
        profile_df = scrape_profile(username_text, scraper)
        st.dataframe(profile_df)
    '''
    elif button_box_a and checkbox_b:
        print("POST")
        shortcode = st.empty()y
        button = st.empty
        button_option = button.button("Continue")
        shortcode_text = shortcode.text_input(
            "Type the Username profile that do you want to scrape", value="@myprofile")
        if button_option:
            scrape_post(shortcode_text, shortcode)
    '''
