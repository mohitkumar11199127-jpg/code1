# from googlesearch import search
# import csv

# def scrape_google_pdf_links(query, filetype, num_results=20, output_csv="output.csv"):

    
#     full_query = f"{query} filetype:{filetype}"
#     print(f"Searching Google for: {full_query}")

    
#     pdf_links = []
#     try:
#         for link in search(query=full_query, stop=num_results, pause=2):
#             pdf_links.append(link)  
#     except Exception as e:
#         print(f"Error while searching Google: {e}")
#         return

#     # Save the links to a CSV file
#     with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
#         csvwriter = csv.writer(csvfile)
#         for link in pdf_links:
#             if link.endswith(".pdf"):  
#                 csvwriter.writerow([link])

#     print(f"Finished scraping! Links saved to {output_csv}")



# if __name__ == "__main__":
#     scrape_google_pdf_links(
#         query="FOIA request form -handbook -guide filetype:pdf", 
#         filetype="pdf",          
#         num_results=100,           
#         output_csv="C:\\Users\\DeepakChigal\\Desktop\\python\\CASB_saas_keyword_model\\Output_links.csv" 
#     )


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def fetch_pdf_links(category, output_file):
    """
    Fetch PDF links related to the provided category using Bing search and save them to a CSV file.
    """
    # Configure Selenium WebDriver options
    options = Options()
    options.add_argument("--headless")  # Run browser in the background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    
    # Bing search query and URL
    query = f"{category} filetype:pdf"
    url = f"https://www.bing.com/search?q={query}&source=web&cvid=5D26DC3E73DF4BD19A9F2D501A4D0A0A"
    print(f"Navigating to: {url}")
    
    try:
        # Navigate to Bing search results
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # Save the page HTML for debugging
        with open("bing_debug.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print("Saved Bing page source for debugging to bing_debug.html")
        
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2 a[href], li.b_algo a[href]")))

        # Extract PDF links
        pdf_links = []
        elements = driver.find_elements(By.CSS_SELECTOR, "h2 a[href], li.b_algo a[href]")
        for element in elements:
            href = element.get_attribute("href")
            if href and ".pdf" in href.lower():  # Ensure it's a PDF link
                pdf_links.append(href)

        # Save links to CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "PDF Link"])  # Write header row
            for link in pdf_links:
                writer.writerow([category, link])
        
        print(f"Saved {len(pdf_links)} PDF links to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Example usage
category = "medical history"  # Replace with the category you want PDF links for
output_file = "C:\\Users\\DeepakChigal\\Desktop\\python\\Download_pdf_links\\pdf_links.csv"  # Output CSV file
fetch_pdf_links(category, output_file)

# Example usage
