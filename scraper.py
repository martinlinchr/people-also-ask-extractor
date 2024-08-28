from playwright.sync_api import sync_playwright
import time

def extract_paa(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.google.com/search?q={query}")

        paa_data = []
        
        try:
            # Wait for PAA box to load
            page.wait_for_selector('div[jsname="N760b"]', timeout=10000)
            
            for i in range(20):  # Try to extract up to 20 questions
                paa_elements = page.query_selector_all('div[jsname="Cpkphb"]')
                if i >= len(paa_elements):
                    break
                
                element = paa_elements[i]
                question = element.query_selector('div[jsname="jIA8B"]').inner_text()
                
                # Click to expand answer
                element.query_selector('div[jsname="gZjhIf"]').click()
                
                # Wait for answer to load
                page.wait_for_selector('div[jsname="F79BRe"]', timeout=5000)
                
                answer = element.query_selector('div[jsname="F79BRe"]').inner_text()
                
                paa_data.append({"question": question, "answer": answer})
                
                time.sleep(1)
        
        finally:
            browser.close()
        
        return paa_data

if __name__ == "__main__":
    print(extract_paa("example query"))
