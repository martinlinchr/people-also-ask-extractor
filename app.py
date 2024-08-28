import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

def extract_paa(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Failed to fetch URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    paa_data = []
    paa_elements = soup.select('div.related-question-pair')
    
    st.info(f"Found {len(paa_elements)} PAA elements")

    for element in paa_elements[:20]:  # Limit to 20 questions
        question = element.select_one('div.match-mod-horizontal-padding')
        answer = element.select_one('div.mod')
        
        if question and answer:
            paa_data.append({
                "question": question.get_text(strip=True),
                "answer": answer.get_text(strip=True)
            })
            st.info(f"Extracted question: {question.get_text(strip=True)}")
        else:
            st.warning("Found a PAA element but couldn't extract question or answer")
        
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between requests
    
    if not paa_data:
        st.warning("No PAA data extracted. Showing a sample of the page content for debugging.")
        st.code(response.text[:1000], language="html")
    
    return paa_data

st.title("Google 'People Also Ask' Scraper")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Scraping data..."):
            paa_data = extract_paa(query)
        
        st.success("Scraping complete!")
        
        if paa_data:
            for item in paa_data:
                st.subheader(item['question'])
                st.write(item['answer'])
                st.markdown("---")
        else:
            st.warning("No 'People Also Ask' questions found. This could be due to Google's anti-bot measures or changes in their HTML structure.")
            
        # Send data to webhook
        webhook_url = 'https://hook.eu2.make.com/6nf4ik99a38lcvfuq8mmdq0zmvehh32c'
        payload = {
            "questionsAndAnswers": paa_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(webhook_url, json=payload)
        st.write(f"Webhook response status: {response.status_code}")
        st.write(f"Webhook response content: {response.text}")
        
        # Display debug info
        st.subheader("Debug Information")
        st.text(f"Number of PAA questions found: {len(paa_data)}")
        
    else:
        st.warning("Please enter a search query.")
