import streamlit as st
from scraper import extract_paa
import requests
import time

st.title("Google 'People Also Ask' Scraper")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Scraping data..."):
            paa_data = extract_paa(query)
        
        st.success("Scraping complete!")
        
        for item in paa_data:
            st.subheader(item['question'])
            st.write(item['answer'])
            st.markdown("---")
        
        # Send data to webhook
        webhook_url = 'https://hook.eu2.make.com/6nf4ik99a38lcvfuq8mmdq0zmvehh32c'
        payload = {
            "questionsAndAnswers": paa_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(webhook_url, json=payload)
        st.write(f"Webhook response status: {response.status_code}")
        st.write(f"Webhook response content: {response.text}")
        
    else:
        st.warning("Please enter a search query.")
