import requests
from bs4 import BeautifulSoup
import time
import threading
from urllib.parse import urlparse

# Define the banner
def print_banner():
    banner = """
    ############################################
    #                                          #
    #         Automated Google Dorking         #
    #                                          #
    ############################################
    """
    print(banner)

# Function to perform Google Dorking
def google_dork(query, num_results=10):
    total = 0

    # Initialize Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Method': 'GET'
    }
    
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for div in soup.find_all('div'):
            try:
                # Find all anchor tags within each div
                links = div.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    
                    # Validate the link if its not a directory or irrelevant
                    if href and not href.startswith('/'):
                        parsed_url = urlparse(href)
                        if parsed_url.scheme and parsed_url.netloc:
                            # Try to get the title
                            title = link.get_text(strip=True) if link.get_text(strip=True) else "No title"
                            results.append({'title': title, 'link': href})
            except:
                pass
        return results
    else:
        return None

# Thread function to handle dork search and result printing
def thread_function(dork):
    results = google_dork(dork)
    if results:
        print(f"\nResults for dork: {dork}\n")
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
        time.sleep(2)  # To avoid getting blocked by Google
    else:
        print("No results found or an error occurred.")

# Main function
def main():
    print_banner()
    
    # dorks = [
    #     'inurl:admin',  # Find admin pages
    #     'intitle:"index of"',  # Find directory listings
    #     'inurl:login',  # Find login pages
    #     'filetype:pdf',  # Find PDF files
    #     'site:example.com'  # Search within a specific site
    # ]

    dorks = [
        'intext:"kyle santos" site:linkedin.com',  
    ]
    
    threads = []
    
    # Create and start threads
    for dork in dorks:
        thread = threading.Thread(target=thread_function, args=(dork,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
