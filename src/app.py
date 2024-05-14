import streamlit as st
from news_retriever import generate_multinews_summary
from prompt_generation import get_prompt_chain
from image_generation import generate_image

st.set_page_config(
    page_title='NewsLens',
    page_icon=':newspaper:',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown("""
    <style>
    /* Main app background and text color */
    .stApp {
        background-color: #121212;  /* Deep dark background */
        color: #e0e0e0;  /* Light grey text for readability */
    }
    
    /* Button label styling */
    .stButton>label {
        font-size: 16px;
        color: #4caf50;  /* A green color to make the button labels pop */
    }
    
    /* Text input field label and input text color */
    .stTextInput>label, .stTextInput>div>div>input {
        color: #bbb;  /* Slightly brighter grey for better visibility */
        font-size: 18px;  /* Larger font size for readability */
    }
    
    /* Centering the main container elements */
    .css-2trqyj {
        justify-content: center;
    }
    
    /* Additional padding for the top and bottom of the app container */
    .css-1d391kg {
        padding-top: 3rem;  /* Increased top padding for aesthetic spacing */
        padding-bottom: 3rem;  /* Same for bottom to balance the layout */
    }
    
    /* Banner styling for 'Welcome to NewsLens' */
    .banner {
        background-color: #1f1f1f;  /* Slightly lighter dark shade for the banner */
        color: #ffffff;  /* White text for contrast */
        padding: 10px;
        border-radius: 10px;  /* Rounded corners for a softer look */
        margin-bottom: 2rem;  /* Space below the banner */
        text-align: center;
    }
            
    /* Centering images specifically */
    .centered-image {
        display: flex;
        justify-content: center;
    }
            
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='banner'>
        <h1>Welcome to NewsLens</h1>
        <p>Discover news visually and contextually</p>
    </div>
""", unsafe_allow_html=True)


def generate_image_and_article(user_input):

    news_summary = generate_multinews_summary(user_input)
    prompt_chain = get_prompt_chain()
    prompt = prompt_chain(user_input)
    generate_image(prompt['result'])
    return news_summary

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.write("### What news are you looking for today?")
    user_input = st.text_input("", placeholder="Enter news summary or title")
    generate_button = st.button('Generate')

    if generate_button and user_input:
        summary = generate_image_and_article(user_input)
        st.image("generated_image.jpeg",  width=400)
        st.write(summary)
    elif generate_button:
        st.warning("Please enter a valid prompt to generate the image and article.")




