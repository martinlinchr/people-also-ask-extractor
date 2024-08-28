from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='N760b']"))
        )
        
        paa_elements = driver.find_elements(By.CSS_SELECTOR, "div[jsname='Cpkphb']")
        
        for element in paa_elements[:20]:  # Limit to 20 questions
            question = element.find_element(By.CSS_SELECTOR, "div[jsname='jIA8B']").text
            
            element.find_element(By.CSS_SELECTOR, "div[jsname='gZjhIf']").click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsname='F79BRe']"))
            )
            
            answer = element.find_element(By.CSS_SELECTOR, "div[jsname='F79BRe']").text
            
            paa_data.append({"question": question, "answer": answer})
            
            time.sleep(1)
    
    finally:
        driver.quit()
    
    return paa_data

if __name__ == "__main__":
    print(extract_paa("example query"))
