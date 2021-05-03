from instagram_scraper import instascraper
import streamlit as st
import urllib.request
import numpy as np
import pandas as pd
from datetime import datetime

def is_authenticated(username, password):
    try:
        scraper = instascraper(username=username, password=password)
        print(scraper)
        return scraper
    except Exception:
        return None

def download_pic(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    namefile = "image_streamlit/profile.jpg"
    with open(namefile, "wb") as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())
    return namefile

    #SCRAPE DATA ABOUT THE PROFILE

def scrape_profile(scraper, profile):
    placeholder_image_loading = st.image('image_streamlit/giphy.gif')
    placeholder_text_loading = st.text("Please wait loading profile.......")

    profile_information = scraper.get_profile_data()

    placeholder_image_loading.empty()
    placeholder_text_loading.empty()
    
    col1, col2 = st.beta_columns(2)
    col1.markdown("""
        # Data about @{}
        <br/><br/>
        ## Followers: {}
        ## Followees: {}
        ## Number of posts: {}
        <br/><br/>
        More information available in the Dataframe here:
        """.format(
        profile.username,
        profile.followers,
        profile.followees,
        profile.mediacount), unsafe_allow_html=True)
    col2.image(download_pic(profile.profile_pic_url), width=300)
    st.dataframe(profile_information.T)
    return

    #SCRAPE DATA ABOUT THE POST AND COMMENTS

def scrape_post_comments(scraper, profile):
    placeholder_image_2 = st.image('image_streamlit/giphy.gif')
    placeholder_text_2 = st.text("Please wait loading posts......")
    
    post_profile = scraper.get_post_and_comment(MAX_COMMENT=number_comment_post,
                                                L=None,
                                                MAX_POST=int(number_post),
                                                profile=profile)
    placeholder_image_2.empty()
    placeholder_text_2.empty()

    data_to_df = []
    for post in post_profile['posts']:
        with st.beta_expander("Post n.{}".format(
            np.datetime_as_string(
                post['post_info']['date_and_time'].values[0])
        )):
            st.image(download_pic(
                post['post_info']['url_link'].values[0]), width=400)
            st.dataframe(post['post_info'].T)
            #print(type(post['post_info']['date_and_time'].values[0]))
            post_info = {
                'date_of_post': post['post_info']['date_and_time'].values[0],
                'n_likes': int(post['post_info']['n_likes'].values[0]),
                'n_comments': int(post['post_info']['n_comments'].values[0]),
                'engagement_rate': post['post_info']['engagement_rate'].values[0]}

            data_to_df.append(post_info)

            eng_rate = post['post_info']['engagement_rate'].values[0]

            st.dataframe(post['comments'])
            st.bar_chart(post['comments']['sentiment_analysis'])
            pos_neg_count = post['comments']['sentiment_analysis'].value_counts(
            )
            print(type(pos_neg_count))
            col1, col2, col3 = st.beta_columns(3)
            col1.markdown("""
            <p><h3>Positie comments</h3><h3 style="color:green;">{}</h3></p>""".format(
                pos_neg_count["POSITIVE"] if 'POSITIVE' in pos_neg_count else 0), unsafe_allow_html=True)
            col2.markdown("""
            <p><h3>Negative comments</h3><h3 style="color:red;">{}</h3></p>""".format(
                pos_neg_count["NEGATIVE"] if 'NEGATIVE' in pos_neg_count else 0), unsafe_allow_html=True)
            col3.markdown("""
            <p><h3>Engagemente rate</h3><h3 style="color:{};">{}%</h3></p>""".format(
                'red' if round(eng_rate, 2) < 3 else 'green',
                round(eng_rate, 2)), unsafe_allow_html=True)


    df_temp = pd.DataFrame(data_to_df)
    df_temp.set_index('date_of_post')
    df_temp['date_of_post'] = pd.to_datetime(df_temp['date_of_post'])
    df_temp = df_temp.sort_values(by="date_of_post")

    with st.beta_expander("Post analisys over time"):
        st.dataframe(df_temp)
        st.line_chart(df_temp[['n_likes']])
        st.line_chart(df_temp[['n_comments']])
        st.line_chart(df_temp[['engagement_rate']])
    
    return

st.sidebar.markdown(
    """
    Insert the data required to start the analytics.
    """
    )
text_username = st.sidebar.empty()
username_input = text_username.text_input("Username", value = "")
text_password = st.sidebar.empty()
password = text_password.text_input("Password:", value="", type="password")

st.sidebar.markdown(
    """
    NB: None of your sensitive information are stored or saved.
    """
)
username_scrape = st.sidebar.text_input(
    "Type the Username profile that do you want to scrape")

text = st.sidebar.markdown("Please be aware to set a reasonable value for comments and posts, cause IG might stop us if we try to download a large amout of data.")

number = st.sidebar.empty()
number_post = number.number_input("How many post do you want to download ?", min_value = 2, max_value = 50)

number_comment = st.sidebar.empty()
number_comment_post = number_comment.number_input(
    "How comments per posts do you want to download ?", min_value=10, max_value=200)

button = st.sidebar.empty()
button_login = button.button("Get the Data")

st.title("Instagram profile Analizer")
st.image("https://images.ctfassets.net/00i767ygo3tc/6WyeFtbZHW0wPtuuxvU18/1cd877a07ccb3eff2b0c087ee0ac015f/instagram-analytics-insights.png?w=1800&q=50")
st.markdown(
    """
    Welcome to my instagram profile analizer,
    to Scrape a profile please use your instagram profile to log in 
    and get the data from the profiles that are public or you follow.
    PS. If you want you can avoid the login part just by leaving the fields of username and password empty, but you will be able onlt to scrape public profiles without comments.
    """
)


if button_login:
    
    if username_input and password != "":
        scraper = is_authenticated(username_input, password)
        
        if scraper.Logged == 'logged':
            
            profile = scraper.set_profile(username_profile=username_scrape)
            scrape_profile(profile=profile, scraper= scraper)
            scrape_post_comments(profile = profile, scraper = scraper)

        elif password:
            st.info(str(scraper.Logged) if 'fail' not in str(
                scraper.Logged) else str(scraper.Logged) + " To many logins done.")
    else:

        scraper = instascraper()
        profile = scraper.set_profile(username_profile=username_scrape)
        scrape_profile(profile=profile, scraper=scraper)
        #scrape_post_comments(profile=profile, scraper=scraper)
        st.markdown("""
        ### If you want more information about the profiles(posts and comments) searched please log-in with your IG profile.
        """)


st.sidebar.markdown(
    """
    For more information about this tool check out my repository on github:
    """
)


