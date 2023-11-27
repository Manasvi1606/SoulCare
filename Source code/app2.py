import numpy as np
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
from keras.models import load_model
import av
import time
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode
from tensorflow.keras.utils import img_to_array
from streamlit_extras.stodo import to_do
from matplotlib import rcParams
import openai
import cv2
import tensorflow as tf
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import firebase_admin
from firebase_admin import credentials, auth, firestore
import re

# Check if the Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("soulcare-2ec40-firebase-adminsdk-i1ocu-5eb2985e19.json")
    # firebase_admin.initialize_app(cred, options={"projectId": "soulcare-2ec40"})

# Initialize Firestore
db = firestore.client()


def is_username_taken(username):
    # Check if the username already exists in Firestore
    user_ref = db.collection('users').where('username', '==', username).limit(1)
    return len(list(user_ref.stream())) > 0


def login_signup_app():
    st.title('Welcome to :violet[SoulCare]!')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password', key='signup_password')

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            location = st.text_input("Location")

            if st.button('Create my account'):
                # Password validation
                if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
                    st.warning(
                        "Password must be at least 8 characters with a capital letter, a lowercase letter, and a digit.")
                else:
                    # Check if the username is already taken
                    if is_username_taken(username):
                        st.warning('Username already taken. Please choose another username.')
                    else:
                        # Create user with email and password
                        user = auth.create_user(email=email, password=password)

                        # Store additional user information in Firestore
                        user_ref = db.collection('users').document(user.uid)
                        user_ref.set({
                            'email': email,
                            'username': username,
                            'firstName': first_name,
                            'lastName': last_name,
                            'location': location,
                        })

                        st.success('Account created successfully!')
                        st.markdown('Please Login using your email and password')
                        st.balloons()
        else:
            st.button('Login', on_click=f)

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)


# constants
starttime = datetime.now()
# page settings
st.set_page_config(page_title="IIT", page_icon=":speech_balloon:", layout="wide")


# COLOR = "#1f1f2e"
# BACKGROUND_COLOR = "#d1d1e0"


# @st.cache(hash_funcs={tf_agents.utils.object_identity.ObjectIdentityDictionary: load_model})
# def load_model_cache(model):
#     return load_model(model)

# @st.cache
def log_file(txt=None):
    with open("log.txt", "a") as f:
        datetoday = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"{txt} - {datetoday};\n")


# @st.cache


def main():
    import streamlit as st
    # side_img = Image.open("images/logos.png")
    # with st.sidebar:
    #   st.image(side_img, width=200)
    st.markdown("""
    <style>
           .block-container {
                padding-top: 25px;
                padding-bottom: 0rem;
                padding-left: 12px;
                padding-right: 12px;
            }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        .st-emotion-cache-16txtl3{
        padding: 30px 10px;
        
        }
    </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        website_menu = option_menu("Menu", ["Home", "Text Analysis", "MindScan", "Mind Lift", "Login/Register",
                                            "Our team"],
                                   menu_icon="app-indicator", default_index=0,
                                   styles={
                                       "menu-title": {"color": "#F1EAE3"},
                                       "container": {"border-radius": "2px", "padding": "5!important", "background-color": "#333", "height": "850px", "margin": "0px"},
                                       "icon": {"color": "orange", "font-size": "25px"},
                                       "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                    "--hover-color": "#325343", "color": "#F1EAE3"},
                                       "nav-link-selected": {"background-color": "#F1EAE3", "color": "#325343"},
                                   }
                                   )
    st.set_option('deprecation.showfileUploaderEncoding', False)

    if website_menu == "Home":
        import streamlit as st
        import streamlit.components.v1 as com

        home_image1 = Image.open("images/home-image.jpg")
        arrow_image = Image.open("images/arrow.png")
        home_image2 = Image.open("images/home-image2.jpeg")
        home_image3 = Image.open("images/home-image3.jpeg")

        with open("home.css") as f:
            design = f.read()


        com.html(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Scrollable Landing Page</title>
        </head>
    
        <body>
        <style>{design}</style>
          <header>
            <nav class="navbar">
              <div class="logo">
                <a href="#home">S O U L C A R E</a>
              </div>
              <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About Us</a></li>
                <li><a href="#services">Process</a></li>
                <li><a href="#contact">Contact Us</a></li>
                <li>Log in</li>
              </ul>
            </nav>
          </header>
           <main class="main-page">
            <div id="home" class="page">
                <div class="content">
                    <div class="image-section">
                    
                        <img src="https://i.pinimg.com/564x/5e/a3/24/5ea324c293ab96eda32c81abb90f1484.jpg" alt="Image" class="left-image">
                    </div>
                    <div class="text-section">
                        <h1>SOUL CARE: Discovering Serenity in Digital Reflections</h1>
                        <div>
                            <p>Reflect. Empower. Evolve. At Soul Care, we embrace the journey of self-discovery.</p>
                            <p>Through innovative social media analysis, we illuminate paths to mental wellness.
                            Our mission? Empower you to evolve, offering personalized resources and unwavering
                            support on your transformative voyage.</p>
                        </div>
                        <h2>GET STARTED</h2>
                    </div>
                </div>
            </div>
            <div id="about" class="about-us-page">
                <div class="about-section">
                    <div class="left-images">
                        <img src="https://i.pinimg.com/564x/24/d6/80/24d6809d97caa997298c7d2c2adf7b8d.jpg" alt="Image 1" class="image1">
                        <img src="https://i.pinimg.com/564x/db/36/c8/db36c86a73dc4f1f5b3fa10191634c3d.jpg" alt="Image 2" class="image2">
                    </div>
                    <div class="text-container">
                        <h1>ABOUT US</h1>
                        <p>Cultivating Kindness in Digital Spaces, Fostering Growth Within: Embracing the ethos
                             of compassion in the digital realm, we advocate for kindness to others on the
                             internet as an integral part of our mission. </p>
                           <p> We believe in the transformative power of self-realization and growth, encouraging
                             individuals to embark on a journey towards personal understanding and empowerment.
                              By nurturing a space of empathy, we pave the way for holistic well-being—one where
                              kindness to oneself mirrors kindness to others, creating a harmonious path towards
                              individual and collective growth.
                        </p>
                    </div>
                    <div class="right-image">
                        <img src="https://i.pinimg.com/474x/f8/81/96/f881967da735578630af0e3dfe61a877.jpg " alt="Image 3" class="image3">
                    </div>
                  </div>
            </div>
            <div id="services" class="short-page">
                <div class="short-page-container">
                    <h2>Trust The Process</h2>
                    <div class="services-container">
                    <div class="service">
                        <h3>1. Data Collection and Analysis</h3>
                        <p>Data Gathering: Collects user-provided information or accesses social media accounts.
                            Analysis Algorithms: Utilizes advanced algorithms like natural language processing (NLP)
                            or machine learning to detect mental health indicators.</p>
                    </div>
                    <div class="service">
                        <h3>2. Personalized Insights and Recommendations</h3>
                        <p>Insight Generation: Generates personalized insights based on the analysis of user data.
                            Resource Recommendations: Offers tailored mental health resources, support, or guidance
                            based on identified indicators.</p>
                    </div>
                    <div class="service">
                        <h3>3. Empowering User Support and Engagement</h3>
                        <p>Supportive Environment: Creates a safe and supportive space for users seeking mental
                            health assistance.
                            Resource Accessibility: Provides access to various mental health resources, including
                            helplines or professional services.</p>
                    </div>
                    </div>
                </div>
              </div>
              <div id="contact" class="contact-page">
                <h2>Get in Touch</h2>
                <p>We would love to hear from you</p>
                <div class="contact-container">
                    <form>
                        <div class="name-email-container">
                            <div class="name-container">
                                <label for="name">Name:</label>
                                <input type="text" id="name" name="name" placeholder="Enter your name">
                            </div>
                            <div class="email-container">
                                <label for="email">Email:</label>
                                <input type="email" id="email" name="email" placeholder="Enter your email">
                            </div>
                        </div>
                        <label for="message">Message:</label>
                        <textarea class="message-textarea" id="message" name="message" placeholder="Enter your message"></textarea>
                        <input type="submit" value="Submit">
                    </form>
                </div>
              </div>
            </main>
            <footer>
            <p>&copy; 2023 SOULCARE. All rights reserved.</p>
            </footer>
          </body>
          </html>
        """, height=2995)
        # st.markdown('<h2 style="color: black;text-align:center;">hello</h2>', unsafe_allow_html=True)

        # with open('home.html', 'r') as file:
        #     external_html = file.read()
        # st.markdown("""<style>@import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600;700&display=swap');@import url('https://fonts.googleapis.com/css2?family=Ephesis&family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600&display=swap');body,h1,h2,h3,p{margin:0;padding:0;}body{letter-spacing:2px;font-family:'Raleway',sans-serif;line-height:1.6;}header{background-color:#325343;color:#F1EAE3;position:fixed;top:0;width:100%;font-size:large;z-index:999;}.navbar{display:flex;justify-content:space-between;align-items:center;padding:15px 20px;}.logo a{margin-left:15px;color:#F1EAE3;text-decoration:none;font-size:1.7em;font-weight:500;}.nav-links{list-style:none;display:flex;font-weight:bold;}.nav-links li{margin:0 20px;font-size:1.2rem;font-weight:bold;}.nav-links a{color:#F1EAE3;text-decoration:none;transition:color 0.3s ease;}.nav-links a:hover{color:#ffcc00;}main{padding-top:80px;}.page{height:95vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}.short-page{height:50vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}#home{background-color:#325343;color:#F1EAE3;}.content{display:flex;align-items:center;justify-content:center;padding:50px;}.image-section{flex:1;position:relative;margin-right:20px;}.left-image{width:580px;height:830px;display:block;border-radius:5px;}.text-section{display:flex;flex-direction:column;justify-content:space-evenly;}.text-section h1{position:absolute;font-weight:300;font-size:3em;margin:0px 150px 600px -300px;}.text-section div{font-size:1.2em;font-weight:100;text-align:start;margin:370px 120px 200px;}.text-section div p{padding:20px;}.text-section h2{font-weight:500;font-size:1.6em;margin-top:-150px;margin-left:-100px;}.arrow-image{margin-top:-6px;margin-left:390px;width:190px;height:30px;filter:invert(90%) sepia(13%) saturate(296%) hue-rotate(325deg) brightness(108%) contrast(89%);;}#about{background-color:#F1EAE3;color:#325343;}.about-section{display:flex;justify-content:center;align-items:center;padding:50px;}.left-images{position:relative;}.image1{width:300px;height:350px;position:absolute;margin-left:260px;margin-top:180px;top:0;left:0;}.image2{width:400px;height:500px;margin-right:200px;margin-top:-50px;margin-left:100px;}.text-container{width:500px;margin:30px 70px 30px 20px;}.text-container h1{font-family:'Courier New',Courier,monospace;}.text-container p{font-size:16px;margin:30px;color:#325343;text-align:justify;font-family:'Raleway',sans-serif;font-weight:500;}.right-image{margin-left:20px;}.image3{width:250px;height:300px;margin-bottom:400px;margin-left:30px;}#services{background-color:#325343;color:#F1EAE3;}.short-page-container{display:flex;height:220px;margin-bottom:190px;flex-direction:column;justify-content:space-between;align-content:space-between;}.short-page-container h2{font-size:2rem;margin-bottom:60px;font-family:'Courier New',Courier,monospace;}.services-container{display:flex;justify-content:space-between;position:relative;}.service{flex:1;position:relative;padding:0 80px;text-align:start;}.service h3{font-family:'Ephesis',cursive;font-size:2rem;}.service:not(:last-child)::after{content:"";position:absolute;top:50%;transform:translateY(-50%);right:0;width:1px;height:100%;background-color:#ccc;}.contact-page{height:70vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}.contact-container{width:400px;margin:50px auto;padding:20px;border:2px solid #ccc;border-radius:8px;}.contact-container label{display:block;margin-bottom:6px;}.contact-container .name-email-container{display:flex;justify-content:space-between;}.contact-container input[type="text"],.contact-container input[type="email"],.contact-container textarea{width:calc(50% - 6px);padding:8px;margin-bottom:10px;border-radius:4px;border:1px solid #ccc;box-sizing:border-box;}.contact-container input[type="submit"]{padding:8px 16px;border:none;border-radius:4px;background-color:#007bff;color:#fff;cursor:pointer;}.contact-container input[type="submit"]:hover{background-color:#0056b3;}.contact-container textarea{width:calc(100% - 22px);height:120px;}footer{text-align:center;padding:20px 0;background:#333;color:#fff;position:relative;}</style><body><header><nav class="navbar"><div class="logo"><a href="#home">S O U L C A R E</a></div><ul class="nav-links"><li><a href="#home">Home</a></li><li><a href="#about">About Us</a></li><li><a href="#services">Process</a></li><li><a href="#contact">Contact Us</a></li><li>Log in</li></ul></nav></header><main><section id="home" class="page"><div class="content"><div class="image-section"><img alt="Image" class="left-image"></div><div class="text-section"><h1>SOUL CARE: Discovering Serenity in Digital Reflections</h1><div><p>Reflect. Empower. Evolve. At Soul Care, we embrace the journey of self-discovery.</p><p>Through innovative social media analysis, we illuminate paths to mental wellness. Our mission? Empower you to evolve, offering personalized resources and unwavering support on your transformative voyage.</p></div><h2>GET STARTED</h2><img alt="arrow" class="arrow-image"></div></div></section><section id="about" class="page"><div class="about-section"><div class="left-images"><img alt="Image 1" class="image1"><img alt="Image 2" class="image2"></div><div class="text-container"><h1>ABOUT US</h1><p>Cultivating Kindness in Digital Spaces, Fostering Growth Within: Embracing the ethos of compassion in the digital realm, we advocate for kindness to others on the internet as an integral part of our mission.</p><p>We believe in the transformative power of self-realization and growth, encouraging individuals to embark on a journey towards personal understanding and empowerment. By nurturing a space of empathy, we pave the way for holistic well-being—one where kindness to oneself mirrors kindness to others, creating a harmonious path towards individual and collective growth.</p></div><div class="right-image"><img alt="Image 3" class="image3"></div></div></section><section id="services" class="short-page"><div class="short-page-container"><h2>The Process</h2><div class="services-container"><div class="service"><h3>1. Data Collection and Analysis</h3><p>Data Gathering: Collects user-provided information or accesses social media accounts. Analysis Algorithms: Utilizes advanced algorithms like natural language processing (NLP) or machine learning to detect mental health indicators.</p></div><div class="service"><h3>2. Personalized Insights and Recommendations</h3><p>Insight Generation: Generates personalized insights based on the analysis of user data. Resource Recommendations: Offers tailored mental health resources, support, or guidance based on identified indicators.</p></div><div class="service"><h3>3. Empowering User Support and Engagement</h3><p>Supportive Environment: Creates a safe and supportive space for users seeking mental health assistance. Resource Accessibility: Provides access to various mental health resources, including helplines or professional services.</p></div></div></div></section><section id="contact" class="contact-page"><div class="contact-container"><h2>Get in Touch</h2><p>We would love to hear from you</p><form><div class="name-email-container"><div><label for="name">Name:</label><input type="text" id="name" name="name" placeholder="Enter your name"></div><div><label for="email">Email:</label><input type="email" id="email" name="email" placeholder="Enter your email"></div></div><label for="message">Message:</label><textarea id="message" name="message" placeholder="Enter your message"></textarea><input type="submit" value="Submit"></form></div></section></main><footer><p>&copy; 2023 SOULCARE. All rights reserved.</p></footer></body>""", unsafe_allow_html=True)
        # st.markdown(external_html, unsafe_allow_html=True)

    elif website_menu == "Text Analysis":
        if 'username' not in st.session_state or not st.session_state.username:
            st.warning('Please Login or Register to access this feature.')

        # st.markdown(""" <style>
        #                 .font {
        #                 font-size:35px ; font-family: 'Raleway', sans-serif; color: #FF9633;}
        #                 </style> """, unsafe_allow_html=True)
        # st.markdown('<p class="font">DEPARTMENT OF COMPUTER SCIENCE AND ENGG.</p>', unsafe_allow_html=True)
        # st.markdown("## Name of Supervisor:  Dr. Saurabh Shukla")
        #
        # # Imports
        # import streamlit as st
        #
        # st.write("Depression and Anxiety Detection Based on Twitter Data")
        # input = st.text_input("Share a brief message for a thoughtful reflection on your
        # feelings (up to 40 characters).")
        # st.write("Only input text please! No links, no emojis!")

        else:
            st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Ephesis&family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600&display=swap');
    
            .st-bw {
                background-color: #F1EAE3 ;
                color: #333;
                border-radius: 5px;
            }
            .st-emotion-cache-uf99v8 {
                 margin: 0px 10px 0px -10px;
                 
            }
            .st-emotion-cache-z5fcl4 {
                margin: 0px 30px;
                height: 95vh;
                background-color:#325343 ;
                padding: 20px 50px;
                
            }
            .text-analysis-container {
                margin: 20px 40px;
                color: #F1EAE3;
                
            }
            .text-analysis-container h1 {
                color: #F1EAE3;
                text-align: center;
                font-family:'Courier New', Courier, monospace;
                margin-bottom: 40px;
                
            }
            .text-analysis-container p {
                color: #F1EAE3;
                text-align: center;
                font-size: 20px;
                font-weight: 500;
                font-family: 'Raleway', sans-serif;
            }
            </style>
            <div class="text-analysis-container">
                <h1>Text Analysis</h1>
                <p>Your mental health matters. Input (up to 40 characters) your recent history from Social Media Platforms like Twitter and we will
                 analyse and determine what issue needs immediate attention. We are here for you to reflect on your social 
                 media presence. </p>
            </div>
                 
            """, unsafe_allow_html=True)
            input = st.text_input(
                " ", "Enter your text...")

            st.markdown(
                """
                <style>
                input[type="text"] {
                    padding: 20px;
                    font-size: 23px;
                    font-weight: 700;
                    color: #333;
                    font-family:'Courier New', Courier, monospace;
                }
                 input[type="text"]:focus {
                    color: #333;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Predicting the Depression Level from given input text
            import contractions # Expand contractions
            contr_func = lambda x: [contractions.fix(word) for word in x.split()]
            input = contr_func(input)
            # join list back to string with spaces in between
            input = ' '.join(input)
            # remove mentions, hashtags, punctuation in that order
            input = input.replace('@[A-Za-z0-9_]+', '')
            input = input.replace('#[A-Za-z0-9_]+', '')
            input = input.replace('[^\w\s]', '')
            # turn all to lowercase
            input = input.lower()
            # lemmatizer
            from nltk.stem.wordnet import WordNetLemmatizer
            lmtzr = WordNetLemmatizer()
            lemm_func = lambda x: ' '.join([lmtzr.lemmatize(word, 'v') for word in x.split()])
            # padding and tokenizing
            import tensorflow as tf
            from tensorflow.keras.preprocessing.text import Tokenizer
            from tensorflow.keras.preprocessing.sequence import pad_sequences
            # hyperparams
            vocab_size = 5000
            embedding_dim = 50
            max_length = 40
            trunc_type = 'post'
            padding_type = 'post'
            oov_tok = '<OOV>'
            # import tokenizer from pickle
            import pickle
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            text_seq = tokenizer.texts_to_sequences([input])
            pad_seq = pad_sequences(text_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
            # Predicting
            # import model
            model = tf.keras.models.load_model('twi.h5')
            # predict on sequence
            pred_func = lambda x: model.predict(x)
            pred_prob = pred_func(pad_seq)
            pred_prob = pred_prob[0][0]
            pred_prob = pred_prob * 100
            pred_prob = round(pred_prob, 2)
            # output probability
            st.markdown(f"""
            <style>
            h5 {{
                color: #F1EAE3;
            }}
            </style>
            <h5>
                {str(pred_prob)}  percent chance to be depressed
            </h5>
            """, unsafe_allow_html=True)

    elif website_menu == "MindScan":
        if 'username' not in st.session_state or not st.session_state.username:
            st.warning('Please Login or Register to access this feature.')
        import streamlit as st
        import time
        from streamlit_extras.app_logo import add_logo
        from streamlit_extras.let_it_rain import rain

        def get_score(response):
            score_mapping = {
                'Strongly Agree': 1.0,
                'Agree': 0.8,
                'Neutral': 0.6,
                'Disagree': 0.4,
                'Strongly Disagree': 0.2
            }
            return score_mapping.get(response, 0.0)

        def create_question(question, key):
            st.radio(question, ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree'), key=key,
                     horizontal=True)

        def analyse():
            msg = st.toast('Gathering data...')
            time.sleep(1)
            msg.toast('Analyzing...')
            time.sleep(1)
            msg.toast('Ready!')

        def assess_depression(result):
            if result <= 1.4:
                return "You are not depressed.", "🥰"
            elif 1.5 <= result <= 2.8:
                return "You are mildly depressed.", "🙂"
            elif 2.9 <= result <= 4.2:
                return "You are moderately depressed.", "🙁"
            elif 4.3 <= result <= 5.6:
                return "You are moderately severe depressed.", "😔"
            else:
                st.warning('Please seek immediate help', icon="⚠️")
                return "You are severely depressed.", "😰"

        st.title("Insightful Behavior Analysis Quiz")
        st.sidebar.success("Behavioural Pattern Analysis has been selected")
        st.write("This behavioral pattern provides a scoring mechanism derived from the MindScan presented below.")
        st.write("The score is computed based on the user's responses.")

        st.markdown(
            """<style>
        div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 18px;
        }
            </style>
            """, unsafe_allow_html=True)

        with st.form("my_form"):
            output = 0
            create_question(
                "*1. Do you often have feelings of sadness, hopelessness, or irritability that interfere with how you think and experience everyday activities such as sleeping, eating, and managing your daily tasks?*",
                "q1")
            output += get_score(st.session_state.q1)

            create_question("*2. Has medication and traditional therapy helped alleviate your symptoms in the past?*",
                            "q2")
            output += get_score(st.session_state.q2)

            create_question(
                "*3. Has your appetite changed from what it used to be, either eating a lot less or a lot more than usual? Have you recently lost or gained weight without trying to do so?*",
                "q3")
            output += get_score(st.session_state.q3)

            create_question("*4. Do you have thoughts of suicide?*", "q4")
            output += get_score(st.session_state.q4)
            st.write(
                "If you are having thoughts of suicide and are thinking of engaging in any unsafe behaviors, please seek immediate help")

            create_question("*5. Are you having difficulty concentrating or making decisions?*", "q5")
            output += get_score(st.session_state.q5)

            create_question("*6. Is your mood or behavior affecting relationships with your family and friends?*", "q6")
            output += get_score(st.session_state.q6)

            create_question("*7. Have you lost interest in many activities you used to enjoy?*", "q7")
            output += get_score(st.session_state.q7)

            if st.form_submit_button('Submit'):
                analyse()
                result = output
                result_text, emoji = assess_depression(result)
                st.subheader(result_text)
                time.sleep(1)
                rain(
                    emoji=emoji,
                    font_size=67,
                    falling_speed=5,
                    animation_length="infinite",
                )

    elif website_menu == "Mind Lift":
        if 'username' not in st.session_state or not st.session_state.username:
            st.warning('Please Login or Register to access this feature.')

        else:
            import cv2
            import numpy as np
            import streamlit as st
            import tensorflow as tf
            from keras.models import load_model
            import av
            import time
            import pandas as pd
            import matplotlib.pyplot as plt
            from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode
            from tensorflow.keras.utils import img_to_array
            from streamlit_extras.stodo import to_do
            from matplotlib import rcParams
            import openai
            import streamlit.components.v1 as com

            # openai.api_key = st.secrets["api_key"]

            # rcParams['font.family'] = "'Raleway', sans-serif"
            # Emotion labels
            emotion_dict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
            detected_emotions = []
            detection_times = []
            RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            emotion_df = pd.DataFrame(columns=["Emotion", "Time"])

            new_df = pd.DataFrame(columns=['Emotion', 'Time'])
            st.session_state.my_variable = new_df
            # Load face cascade
            try:
                face_cascade = cv2.CascadeClassifier(
                    r"/Users/manasviagrawal/Downloads/Final project/Source code/haarcascade_frontalface_default.xml")
            except Exception:
                st.write("Error loading cascade classifiers")
            # load my model
            my_mental_health = load_model(
                r"/Users/manasviagrawal/Downloads/Final project/Source code/model.h5")

            class Face_emotion(VideoTransformerBase):
                def __init__(self):
                    self.emotion_df = pd.DataFrame(columns=["Emotion", "Time"])

                def recv(self, frame):
                    img = frame.to_ndarray(format="bgr24")
                    # Convert image to grayscale
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(image=img_gray, scaleFactor=1.3, minNeighbors=5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
                        roi_gray = img_gray[y:y + h, x:x + w]
                        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                        if np.sum([roi_gray]) != 0:
                            roi = roi_gray.astype('float') / 255.0
                            roi = img_to_array(roi)
                            roi = np.expand_dims(roi, axis=0)
                            prediction = my_mental_health.predict(roi)[0]
                            maxindex = int(np.argmax(prediction))
                            finalout = emotion_dict[maxindex]
                            emotion = str(finalout)
                            detection_time = time.strftime('%Y-%m-%d %H:%M:%S')
                            self.emotion_df.loc[len(self.emotion_df)] = [emotion, detection_time]

                        label_position = (x, y)
                        cv2.putText(img, emotion, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    return av.VideoFrame.from_ndarray(img, format="bgr24")

            # upliftting message function
            def generate_uplifting_message(emotion):
                response = openai.Completion.create(
                    prompt=f"can you write an uplifting small simple one-sentence message for someone who is feeling {emotion}?with an emoji",
                    engine="text-davinci-003",
                    temperature=0.8,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    echo=False
                )

                message = response.choices[0].text.strip()
                return message

            # function for plots
            def further_analysis(emotion_df):
                # 1-plot the bar chart for the detected emotions between start and stop of the webcam
                def display_bar_plot():
                    title1 = "Your emotions Today"
                    st.markdown(f'<h2 style="color: black;text-align:center;">{title1}</h2>', unsafe_allow_html=True)
                    emotion_counts = emotion_df['Emotion'].value_counts()

                    fig, ax = plt.subplots()
                    fig, ax = plt.subplots(figsize=(8, 3))
                    ax.bar(emotion_counts.index, emotion_counts.values, color='palevioletred')
                    ax.set_xlabel('Emotion')
                    ax.set_ylabel('Count')
                    # ax.set_title('Detected Emotions')
                    fig.patch.set_facecolor("none")
                    fig.patch.set_alpha(0.0)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['bottom'].set_visible(False)
                    ax.spines['left'].set_visible(False)
                    ax.tick_params(axis='x', colors='black')
                    ax.tick_params(axis='y', colors='black')
                    ax.yaxis.label.set_color('black')
                    ax.xaxis.label.set_color('black')
                    ax.title.set_color('black')
                    ax.set_facecolor('#FBF2F7')
                    st.pyplot(fig)

                def display_pie_chart():
                    # Load data from CSV
                    data = pd.read_csv('new_emotion.csv')
                    max_emotions = data.groupby("Emotion").count().reset_index()
                    max_emotion = max_emotions.sort_values('Time', ascending=False)['Emotion'].iloc[1]

                    first_date = data['Time'].min()
                    last_date = data['Time'].max()

                    title1 = "Emotion Distribution"
                    title2 = f"from {first_date} to {last_date}"

                    st.markdown(f'<h2 style="color: black;text-align:center;">{title1}</h2>', unsafe_allow_html=True)
                    st.markdown(f'<h2 style="color: black; text-align: center; font-size: 16px;">{title2}</h2>',
                                unsafe_allow_html=True)

                    # Create pie chart
                    # Load data from CSV
                    data = pd.read_csv('new_emotion.csv')
                    emotion_counts = data['Emotion'].value_counts()

                    explode = tuple([0.1] * len(emotion_counts))  # Set explode length dynamically

                    fig, ax = plt.subplots(figsize=(6, 6))
                    ax.pie(emotion_counts, labels=emotion_counts.index, autopct='%1.1f%%', explode=explode,
                           colors=['#D8BFD8', '#87CEFA', '#FF7F50', '#FFD700', '#98FB98', '#FF69B4'], radius=0.9,
                           textprops={'fontsize': 12})
                    fig.set_facecolor('#FBF2F7')

                    # Display the pie chart
                    st.pyplot(fig)

                    # Display the pie chart in the first column
                    col1, col2 = st.columns(2)
                    with col1:
                        st.pyplot(fig)

                    # Display the message in the second column
                    with col2:
                        if max_emotion == 'sad':
                            st.markdown('<div class="chat-bubble"><p>I\'ve noticed that you\'ve been feeling sad lately. '
                                        'It\'s important to take care of your emotional well-being. Reach out to someone you trust, '
                                        'engage in activities that uplift your mood, and remember that brighter days are ahead.</p></div>',
                                        unsafe_allow_html=True)
                        elif max_emotion == 'angry':
                            st.markdown(
                                '<div class="chat-bubble"><p>I\'ve noticed that you\'ve been feeling angry recently. '
                                'It\'s natural to experience anger, but it\'s important to find healthy ways to manage it. '
                                'Take a moment to breathe deeply, practice relaxation techniques, and consider expressing your '
                                'feelings in a constructive manner.</p></div>', unsafe_allow_html=True)
                        elif max_emotion == 'fear':
                            st.markdown(
                                '<div class="chat-bubble"><p>I\'ve noticed that you\'ve been feeling fearful lately. '
                                'Remember that fear is a normal human emotion, but it\'s essential not to let it control you. '
                                'Take small steps to face your fears, seek support from loved ones, and focus on positive '
                                'aspects to build resilience.</p></div>', unsafe_allow_html=True)
                        elif max_emotion == 'happy':
                            st.markdown(
                                '<div class="chat-bubble"><p>I\'m glad to see that you\'ve been feeling happy! Embrace this '
                                'positive emotion and continue to engage in activities that bring you joy and fulfillment. '
                                'Spread your happiness to others and cherish these moments of positivity.</p></div>',
                                unsafe_allow_html=True)
                        elif max_emotion == 'neutral':
                            st.markdown('<div class="chat-bubble"><p>I see that you\'ve been feeling neutral recently. '
                                        'It\'s alright to have moments of calm and neutrality. Take this time to reflect, find balance '
                                        'in your life, and consider exploring new opportunities or hobbies to add more excitement.</p></div>',
                                        unsafe_allow_html=True)
                        elif max_emotion == 'surprise':
                            st.markdown('<div class="chat-bubble"><p>You seem to be feeling surprised lately. '
                                        'Embrace the unexpected and be open to new experiences. Enjoy the thrill and wonder that '
                                        'surprises bring!</p></div>', unsafe_allow_html=True)

                    # Apply CSS styles
                    st.markdown(
                        """
                        <style>
                    
                        .chat-bubble {
                            background-color: #D8BFD8;
                            color: black;
                            border-radius: 10px;
                            padding: 10px;
                            margin-bottom: 10px;
                            display: inline-block;
                            max-width: 80%;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                col1, col2 = st.columns(2)

                # Button to display bar plot
                if col1.button("Your Emotions Today", key="bar_plot"):
                    display_bar_plot()

                # Button to display pie chart
                if col2.button("Your Emotions Tracker", key="pie_chart"):
                    display_pie_chart()

            def main():
                st.markdown(
                    """
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600;700&display=swap');
                    @import url('https://fonts.googleapis.com/css2?family=Ephesis&family=Playfair+Display&family=Raleway:wght@100;200;300;400;500;600&display=swap');
    
                    .title-style {
                        white-space: nowrap;
                        font-family: 'Raleway', sans-serif;
                        margin-left: 520px;
                        margin-bottom: 30px;
                        color: #325343;
                    }
                    .st-emotion-cache-uf99v8 {
                        background-color: #F1EAE3;
                        margin: 10px 10px;
                        padding: 0px 30px;
                        font-family: 'Raleway', sans-serif;
                    }
                    .appview-container {
                        font-family: 'Raleway', sans-serif;
                    }
                    
                    .st-emotion-cache-hk2fyb iframe {
                    border: 1.5px solid #325343;
                    border-radius: 5px;
                    padding: 0 10px;
                    }
                
                    .css-1dm0a9e {
                        margin: 0px 20px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown('<h1 class="title-style"> MIND LIFT </h1>', unsafe_allow_html=True)
                # Rest of your code
                # to do list
                app_mode = st.sidebar.selectbox("Choose the app mode",
                                                ["Live detection", "Track your emotions"])

                if app_mode == "Live detection":
                    with st.sidebar:
                        st.sidebar.header("How was your day?")
                        to_do(
                            [(st.write, "Have you chosen the path of happiness?")],
                            "happy",
                        )
                        to_do(
                            [(st.write, "Have you acknowledged the extraordinary power that resides within you today?")],
                            "strong",
                        )
                        to_do(
                            [(st.write, "Have you graced the world with enough smiles today?")],
                            "smile",
                        )

                    st.markdown(
                        """
                        <style>
                        .header-style {
                            color:black;
                            background-color: transparent;
                        }
                        .chat-bubble {
                            background-color: #D8BFD8;
                            padding: 10px;
                            margin: 10px;
                            border-radius: 10px;
                            display: inline-block;
                        }
                        .chat-bubble p {
                            margin: 0;
                            color: black;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True)

                    # st.markdown('<h1 class="header-style">Webcam Live Feed</h1>', unsafe_allow_html=True)
                    # starting the webcam
                    st.markdown("""
                    <style>
                        .mindlift-text {
                        font-size: 20px;
                        font-family: 'Raleway', sans-serif;
                        }
                        .css-1dm0a9e {
                        margin: 0px 20px;
                    }
                    </style>
                    <p class="mindlift-text">Click on start to use webcam and detect your face emotion<p>
                    """, unsafe_allow_html=True)
                    webrtc_ctx = webrtc_streamer(
                        key="example",
                        mode=WebRtcMode.SENDRECV,
                        rtc_configuration=RTC_CONFIGURATION,
                        video_processor_factory=Face_emotion
                    )
                    click_me = st.button("I have something to tell you 👇")
                    if webrtc_ctx.video_processor:
                        while True:
                            try:
                                time.sleep(1)
                                emotion_df = webrtc_ctx.video_transformer.emotion_df
                                emotion_df.to_csv('new_emotion.csv', index=False)
                                try:
                                    existing_df = pd.read_csv('emotion_data.csv')
                                except FileNotFoundError:
                                    existing_df = pd.DataFrame(columns=['Emotion', 'Time'])

                                if click_me:
                                    click_me = False  # Reset button state
                                    updated_df = existing_df.append(emotion_df, ignore_index=True)
                                    updated_df.to_csv('emotion_data.csv', index=False)

                                    emotion_counts = emotion_df['Emotion'].value_counts()
                                    most_prevalent_emotion = emotion_counts.index[0]
                                    uplifting_message = generate_uplifting_message(most_prevalent_emotion)
                                    st.markdown(f'<div class="chat-bubble"><p>{uplifting_message}</p</div>',
                                                unsafe_allow_html=True)

                            except Exception as e:
                                break

                    else:
                        st.write("No emotions detected yet")
                if app_mode == "Track your emotions":
                    further_analysis(pd.read_csv(
                        r"/Users/manasviagrawal/Downloads/Final project/Source code/new_emotion.csv"))

            if __name__ == "__main__":
                main()

    elif website_menu == "Our team":
        st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
                        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Our team</p>', unsafe_allow_html=True)
        st.balloons()
        col1, col2 = st.columns([3, 2])
        with col1:
            st.info("Manasvi Agrawal: lit2020029@iiitl.ac.in")
            st.info("Harshitha Doppalapudi: lcs2020026@iiitl.ac.in")
            st.info("Molugurum Asita: lci2020074@iiitl.ac.in")
        with col2:
            liimg = Image.open("images/LI-Logo.png")
            st.image(liimg)
            st.markdown(
                f""":speech_balloon: [Supervisor: Dr. Saurabh Shukla](https://www.linkedin.com/in/dr-saurabh-shukla-6767b5116/)""",
                unsafe_allow_html=True)
            st.markdown(
                f""":speech_balloon: [Team Lead: Manasvi Agrawal]( https://www.linkedin.com/in/manasvi-agrawal-14bb67200/)""",
                unsafe_allow_html=True)
            st.markdown(
                f""":speech_balloon: [Team Member: Harshitha Doppalapudi]( https://www.linkedin.com/in/harshitha-doppalapudi/)""",
                unsafe_allow_html=True)
            st.markdown(
                f""":speech_balloon: [Team Member: Molugurum Asita]( https://www.linkedin.com/in/asita-molugurum/)""",
                unsafe_allow_html=True)

    elif website_menu == "Login/Register":
        login_signup_app()


if __name__ == '__main__':
    main()