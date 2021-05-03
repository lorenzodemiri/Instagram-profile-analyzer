import instaloader
from instaloader import Post
import pandas as pd
from sentiment_analysis import SentimentAnalysis

class instascraper():
    def __init__(self, username=None, password=None, session_user=None):
        self.L = instaloader.Instaloader(
            dirname_pattern="posts/{profile}/{date}")
        self.analizer = SentimentAnalysis()
        if session_user is None and username and password is not None:
            print('logging in ... ')
            try:
                self.L.login(username, password)
                print('logged in -> ', username)
                self.Logged = 'logged'
            except Exception as ex:
                print(ex)
                self.Logged = ex
        elif session_user is not None:
            self.L.load_session_from_file(session_user)
        else:
            pass
    
    #SET PROFILE FOR THE CURRENT SESSION
    def set_profile(self ,username_profile):
        self.profile = instaloader.Profile.from_username(self.L.context, username_profile)
        print("PROFILE -->", self.profile)
        return self.profile
    
    #RETURN PROFILE DATA
    def get_profile_data( self, profile = None):
        if profile is None:
            profile = self.profile
        if profile.is_private == True:
            print('PRIVINFO NOT AVAILABLE')
            return

        temp_vect = []

        try:
            temp_has_public_story = profile.has_public_story
            temp_has_viewable_story = profile.has_viewable_story
        except Exception as ex:
            print("EXECPTION -->", ex)
            temp_has_public_story = None
            temp_has_viewable_story = None
        dict_profile_data = {
            'user_id': profile.userid,
            'username': profile.username,
            'followed_by_viewer': profile.followed_by_viewer,
            'post_count': profile.mediacount,
            'igtv_count': profile.igtvcount,
            'n_follower': profile.followers,
            'n_followees': profile.followees,
            'external_url': profile.external_url,
            'is_bussines': profile.is_business_account,
            'business_Category': profile.business_category_name,
            'biography': profile.biography,
            'blocked_by_viewer': profile.blocked_by_viewer,
            'follows_viewer': profile.follows_viewer,
            'full_name': profile.full_name,
            'has_blocked_viewer': profile.has_blocked_viewer,
            'has_public_story': temp_has_public_story,
            'has_viewable_story': temp_has_viewable_story,
            'has_requested_viewer': profile.has_requested_viewer,
            'is_verified': profile.is_verified,
            'requested_by_viewer': profile.requested_by_viewer,
            'profile_pic_url': profile.profile_pic_url,
            'has_higlighted_reels': profile.has_highlight_reels,
            'followed_by_viewer': profile.followed_by_viewer
        }
        temp_vect.append(dict_profile_data)
        profile_data = pd.DataFrame(temp_vect, index = ['data_profile'])

        return profile_data

    # GET DATA POST FROM SHORTCODE
    def get_post_from_shortcode( self, SHORTCODE: str, MAX_COMMENT: int):
        post = Post.from_shortcode(self.L.context, SHORTCODE)
        try:
            accessibility_caption = str(post._asdict()['accessibility_caption'])
        except Exception as ex:
            print(ex)
        try:
            location = post.location
        except Exception as ex:
            print(ex)
            location = None
            #INFORMATION OF THE POST GOING INTO THE CSV
            post_info_dict = {
                'title': post.title,
                'owner_username': post.owner_username,
                'date_and_time': post.date,
                'type_of_post': post.typename,
                'mediacount': post.mediacount,
                'caption': post.caption,
                'n_caption_hashatags': len(post.caption_hashtags),
                'caption_hashtags': post.caption_hashtags,
                'n_mentions_post': len(post.caption_mentions),
                'n_tagged_users': len(post.tagged_users),
                'is_video': post.is_video,
                'n_likes': post.likes,
                'n_comments': post.comments,
                'is_sponsored': post.is_sponsored,
                'sponsors': post.sponsor_users,
                'location': location,
                'url_link': post.url,
                'url_insta': 'instagram.com/p/{}/'.format(post.shortcode),
                'description_of_post': accessibility_caption,
            }
            comments_vect = []
            # DOWNLOAD AND STORE COMMENT
            print('Start Comments', end='')

            comment_count = 0
            for comment in post.get_comments():
                answer_count = 0
                for answer in comment.answers:
                    answer_count += 1
                    if answer_count == 50:
                        break
                analisys, score = self.analizer.return_sentiment(
                    str(comment.text).strip())
                comment_info_dict = {
                    'date_and_time': comment.created_at_utc,
                    'profile': comment.owner.username,
                    'text': str(comment.text).strip(),
                    'n_likes': comment.likes_count,
                    'answer_count': answer_count,
                    'sentiment_analysis': analisys,
                    'score': score
                }

                comments_vect.append(comment_info_dict)
                if comment_count == MAX_COMMENT:
                    break
                comment_count += 1
                print('.', end='')
            print('End Comments')
            comment_df = pd.DataFrame(comments_vect)
            post_df = pd.DataFrame([post_info_dict])

            return post_df, comment_df

    #GET POST OF THE SETTET PROFILE OR SET profile input to set a new one
    def get_post_and_comment(self, MAX_COMMENT: int, L = None, MAX_POST=5, profile=None):
        if profile is None:
            profile = self.profile
        if L is None:
            L = self.L
        counter_post = 1
        post_profile = {"profile": profile.username, 'posts': []}
        for post in profile.get_posts():
            print("POST n:", counter_post, "MAX_COMMENT_SET:", MAX_COMMENT)
            comments_vect = []
            try:
                accessibility_caption = str(
                    post._asdict()['accessibility_caption'])
            except Exception as ex:
                print(ex)
                accessibility_caption = None
            try:
                location = post.location
            except Exception as ex:
                print(ex)
                location = None
            #INFORMATION OF THE POST GOING INTO THE CSV
            post_info_dict = {
                'title': post.title,
                'owner_username': post.owner_username,
                'date_and_time': post.date,
                'type_of_post': post.typename,
                'mediacount': post.mediacount,
                'caption': post.caption,
                'n_caption_hashatags': len(post.caption_hashtags),
                'caption_hashtags': post.caption_hashtags,
                'n_mentions_post': len(post.caption_mentions),
                'n_tagged_users': len(post.tagged_users),
                'is_video': post.is_video,
                'n_likes': post.likes,
                'n_comments': post.comments,
                'is_sponsored': post.is_sponsored,
                'sponsors': post.sponsor_users,
                'location': location,
                'url_link' : post.url,
                'url_insta': 'instagram.com/p/{}/'.format(post.shortcode),
                'description_of_post': accessibility_caption,
                'engagement_rate': ((int(post.likes) + int(post.comments)) / int(profile.followers))   * 100
            }

            # DOWNLOAD AND STORE COMMENT
            print('Start Comments')

            comment_count = 0
            for comment in post.get_comments():
                answer_count = 0
                """
                for answer in comment.answers:
                    answer_count += 1
                    if answer_count == 5:
                        break
                """
                analisys, score = self.analizer.return_sentiment(
                    str(comment.text).strip())
                comment_info_dict = {
                    'date_and_time': comment.created_at_utc,
                    'profile': comment.owner.username,
                    'text': str(comment.text).strip(),
                    'n_likes': comment.likes_count,
                   # 'answer_count': answer_count,
                    'sentiment_analysis': analisys,
                    'score': score
                }


                comments_vect.append(comment_info_dict)
                if comment_count == MAX_COMMENT:
                    print("MAX COMMENT")
                    break
                comment_count += 1
                print(comment_count, '.', end='')
            
            print('End Comments')

            #L.download_pic(path_pic_jpg, post.url, post.date_utc)

            #STORING DATA SCRAPED AND UPLOAD RELATIVE CSVs
            comment_df = pd.DataFrame(comments_vect)
            post_df = pd.DataFrame([post_info_dict], index=['post_data'])

            post = {'post_info': post_df, 'comments': comment_df}
            post_profile['posts'].append(post)
            print("END__POST")
            #IF MAX POST DOWNLOADED BREAK
            if counter_post % MAX_POST == 0:
                print('Post Reached')
                break
            counter_post += 1

        return post_profile

if __name__ == '__main__':
    scraper = instascraper(username='test_lorenz', password='provaprova')
    profile = scraper.set_profile(username_profile="joridelli")
    print(scraper.get_profile_data())
    post_profile = scraper.get_post_and_comment(scraper, 50, 5, profile)
    print(post_profile['posts'][1]['comments'])
