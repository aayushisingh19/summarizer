from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_comments(video_url):
    driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
    driver.get(video_url)
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(3)

    comments = []
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)

    comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")
    for element in comment_elements:
        comments.append(element.text)

    driver.quit()
    return comments
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def analyze_sentiments(comments):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for comment in comments:
        score = analyzer.polarity_scores(comment)
        if score['compound'] >= 0.05:
            sentiments['positive'] += 1
        elif score['compound'] <= -0.05:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1
    
    total_comments = len(comments)
    sentiments_percentage = {k: (v / total_comments) * 100 for k, v in sentiments.items()}
    return sentiments_percentage
import streamlit as st
import matplotlib.pyplot as plt

st.title("YouTube Comment Sentiment Analyzer")

video_url = st.text_input("Enter YouTube Video URL:")
if st.button("Analyze"):
    st.write("Fetching comments...")
    comments = get_comments(video_url)
    
    st.write("Analyzing sentiments...")
    sentiments = analyze_sentiments(comments)
    
    # Display results
    st.write("Sentiment Analysis Results:")
    st.write(sentiments)
    
    # Visualize
    fig, ax = plt.subplots()
    ax.pie(sentiments.values(), labels=sentiments.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
