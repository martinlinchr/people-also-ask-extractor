import requests
from bs4 import BeautifulSoup
import time
import random

def extract_paa(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    paa_data = []
    paa_elements = soup.select('div.related-question-pair')
    
    for element in paa_elements[:20]:  # Limit to 20 questions
        question = element.select_one('div.match-mod-horizontal-padding')
        answer = element.select_one('div.mod')
        
        if question and answer:
            paa_data.append({
                "question": question.get_text(strip=True),
                "answer": answer.get_text(strip=True)
            })
        
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between requests
    
    return paa_data

if __name__ == "__main__":
    print(extract_paa("example query"))
