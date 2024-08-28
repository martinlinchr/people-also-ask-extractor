from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import requests

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_paa(query):
    driver = setup_driver()
    driver.get(f"https://www.google.com/search?q={query}")
    
    paa_data = []
    
    try:
        # Wait for PAA box to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='N760b']"))
        )
        
        # Extract initial questions
        paa_elements = driver.find_elements(By.CSS_SELECTOR, "div[jsname='Cpkphb']")
        
        for element in paa_elements:
            question = element.find_element(By.CSS_SELECTOR, "div[jsname='jIA8B']").text
            
            # Click to expand answer
            element.find_element(By.CSS_SELECTOR, "div[jsname='gZjhIf']").click()
            
            # Wait for answer to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='F79BRe']"))
            )
            
            answer = element.find_element(By.CSS_SELECTOR, "div[jsname='F79BRe']").text
            
            paa_data.append({"question": question, "answer": answer})
            
            # Small delay to allow page to update
            time.sleep(1)
    
    finally:
        driver.quit()
    
    return paa_data

def send_to_webhook(data):
    webhook_url = 'https://hook.eu2.make.com/6nf4ik99a38lcvfuq8mmdq0zmvehh32c'
    payload = {
        "questionsAndAnswers": data,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    response = requests.post(webhook_url, json=payload)
    print(f"Webhook response status: {response.status_code}")
    print(f"Webhook response content: {response.text}")

if __name__ == "__main__":
    search_query = "guld"  # You can change this to any query
    paa_data = extract_paa(search_query)
    print(json.dumps(paa_data, indent=2, ensure_ascii=False))
    send_to_webhook(paa_data)
