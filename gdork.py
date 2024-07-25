import requests
from bs4 import BeautifulSoup
import time
import threading
from urllib.parse import urlparse

# COLORS
RED = '\033[31m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Define the banner
def print_banner():
    banner = """
#########################################################################################
#                                                                                       #
#                                                                                       #
#    ██████╗  ██████╗ ██████╗ ██╗  ██╗    ███████╗██╗    ██╗███████╗███████╗██████╗     #
#    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗    #
#    ██║  ██║██║   ██║██████╔╝█████╔╝     ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝    #
#    ██║  ██║██║   ██║██╔══██╗██╔═██╗     ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝     #
#    ██████╔╝╚██████╔╝██║  ██║██║  ██╗    ███████║╚███╔███╔╝███████╗███████╗██║         #
#    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝         #
#                                                                                       #
#                                                                                       #
#########################################################################################
    """
    print(f"{RED}{banner}{RESET}")

def print_help():
    help = f"""
COMMAND OPTIONS:

   {RED}help{RESET} - displays available commands
   {RED}exit{RESET} - terminates the program
   {RED}classic{RESET} - classic google dorking (for experienced users)
   {RED}auto{RESET} - automated google dorking   

   Automated Google Dorking Commands:
   {RED}show{RESET} - shows available categories for dorking
   {RED}set <category>{RESET} - sets the category
       
   After Choosing a Category:
       {RED}list{RESET} - lists all available options under chosen category
       {RED}use <option>{RESET} - uses/sets the option you want to perform search on
       {RED}dsweep{RESET} - executes google dorking
    """
    print(f"{RED}{help}{RESET}")


def print_categories():
    categories = f"""
CATEGORIES FOR AUTOMATED DSWEEP:

   {RED}DB | Databases{RESET} - sweeps databases such as mongoDB, mariaDB, Postgre
   {RED}VW | Vulnerable-Websites{RESET} - sweeps admin pages, SQL injection vulnerabilities, config files
   {RED}NS | Network-and-Security-Information{RESET} - sweeps server info, open ports and services, network devices
   {RED}TI | Technical-Information{RESET} - sweeps API keys, Encryption keys
    """
    print(f"{RED}{categories}{RESET}")


def get_input(cont=""):
    return input(f"{GREEN}DorkSweep{cont} {RESET}> ")


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


# Function to handle dork search and result printing
def dork_sweep(dork):
    results = google_dork(dork)
    if results:
        print(f"\nResults for dork: {dork}\n")
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
        print()
        time.sleep(2)  # To avoid getting blocked by Google
    else:
        print(f"No results found or an error occurred for dork: {dork}")


# Automated Google Dorking Function
def auto_dork():
    print(f"\nYou Have Selected Automated Google Dorking.")
    print(f"\nYou can type 'show' to display list of categories")
    print_categories()
    user_input = get_input(" (Auto)").split(" ")
    match user_input[0]:
        case 'exit':
            return 0
        case 'show':
            print_categories()
        case 'set':
            print()
            user_query = get_input(f" Auto({user_input[1]})")

        case _:
            print("\nNo such command. (Type help to see available commands)\n")


# Main function
def main():
    print_banner()
    print_help()
    print()

    while (True):
        user_input = get_input().lower()
        match user_input:
            case 'exit':
                return 0
            case 'classic':
                print(f"\nBonjour! You experienced G Dorker :)")
                print("\nYou should enter your query!")
                print("\n[Query Samples]")
                print(f'{RED}   intext:"kyle santos" site:linkedin.com{RESET}   # chained query')
                print(f'{RED}   inurl:admin{RESET}   # Find admin pages')
                print(f'{RED}   intitle:"index of"{RESET}   # Find directory listings')
                print(f'{RED}   inurl:login{RESET}   # Find login pages')
                print(f'{RED}   filetype:pdf{RESET}   # Find PDF files')
                print(f'{RED}   site:example.com{RESET}   # Search within a specific site\n')

                user_query = get_input(" (Classic)")
                dork_sweep(user_query)
            case 'auto':
                auto_dork()
            case 'help':
                print_help()
            case _:
                print("\nNo such command. (Type help to see available commands)\n")

if __name__ == "__main__":
    main()
