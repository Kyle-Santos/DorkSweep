import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import csv

# COLORS
RED = '\033[31m'
GREEN = '\033[92m'
RESET = '\033[0m'

# CSV
script_dir = "scripts/"
categories = ["Database", "Network_and_Security_Information", "Technical_Information", "Web_Vulnerability"]
data_auto = {} # Initialize an empty dictionary to store the CSV data

# Load CSVs
def load_data(): 
    for category in categories:
        # Initialize the nested dictionary for each category
        data_auto[category] = {}

        # Open and read the CSV file
        with open(script_dir + category + ".csv", mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # row number
            row_num = 1

            # Iterate over each row in the CSV
            for row in reader:
                search = row['search']
                query = row['query']
                data_auto[category][search] = query
                data_auto[category][str(row_num)] = query
                row_num += 1

        # Print the resulting dictionary
        # for search, query in data_auto[category].items():
        #     print(f"Search: {search}, Query: {query}")


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


# Print help command
def print_help():
    help = f"""
COMMAND OPTIONS:

   {RED}help{RESET} - displays available commands
   {RED}exit{RESET} - terminates the program
   {RED}custom{RESET} - custom google dorking (for experienced users)
   {RED}auto{RESET} - automated google dorking   

   Automated Google Dorking Commands:
   {RED}show{RESET} - shows available categories for dorking
   {RED}set <category>{RESET} - sets the category
   {RED}back{RESET} - go back to mode selection
       
   After Choosing a Category:
       {RED}list{RESET} - lists all available options under chosen category
       {RED}use <option>{RESET} - uses/sets the option you want to perform search on
       {RED}dsweep{RESET} - executes google dorking
    """
    print(f"{RED}{help}{RESET}")


# Print show command
def print_categories():
    categories = f"""
CATEGORIES FOR AUTOMATED DSWEEP:

   {RED}DB | Database{RESET} - sweeps databases such as mongoDB, mariaDB, Postgre
   {RED}VW | Vulnerable_Websites{RESET} - sweeps admin pages, SQL injection vulnerabilities, config files
   {RED}NS | Network_and_Security_Information{RESET} - sweeps server info, open ports and services, network devices
   {RED}TI | Technical_Information{RESET} - sweeps API keys, Encryption keys
    """
    print(f"{RED}{categories}{RESET}")


# Print list command
def print_queries(category):
    row = 1
    even = False
    print(f"\nQueries for {category.replace("_", " ").upper()}\n")
    # Print the scripts of a category
    for search, query in data_auto[category].items():
        if even:
            even = False
            continue
        print(f"   [{row}] Search: {RED}{search}{RESET}, Query: {query}")
        even = True
        row += 1
    
    print()


def get_input(cont=""):
    return input(f"{GREEN}DorkSweep{cont} {RESET}> ")



# Function to perform Google Dorking
def google_dork(query, num_results=30, proxy=None):
    total = 0

    # Initialize Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Method': 'GET'
    }
    
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    response = requests.get(search_url, headers=headers, proxies=proxies)
    
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

    while True:
        user_input = get_input(" (Auto)").split(" ")
        match user_input[0]:
            case 'exit':
                exit()
            case 'back':
                return
            case 'show':
                print_categories()
            case 'help':
                print_help()
            case 'set':
                print()
                category = user_input[1].lower()
                while True:
                    if category in ['db', 'database']:
                        category_selected(f"Database")
                    elif category in ['vw', 'Vulnerable_Websites']:
                        category_selected(f"Vulnerable Websites")
                    if category in ['ns', 'network_and_security_information']:
                        category_selected(f"Network_and_Security_Information")
                    if category in ['ti', 'technical_information']:
                        category_selected(f"Technical_Information")
                    else:
                        print("\nNo such category. (Type show to see available categories)\n")
            case _:
                print("\nNo such command. (Type help to see available commands)\n")


def category_selected(category):
    query = ""
    while True:
        user_query = get_input(f" Auto({category.replace("_", " ")})").split(" ")
        match user_query[0]:
            case 'list':
                print_queries(category)
            case 'back':
                break
            case 'help':
                print_help()
            case 'use':
                query = data_auto[category][user_query[1]]

                if not query or query == "":
                    print(f"\nInvalid Query. (Type list to see available queries)\n")
                else:
                    print(f"\nQuery Selected: {query}\n")

            case 'dsweep':
                if not query or query == "":
                    print("\nChoose a query first. example: use mongoDB\n")
                dork_sweep(query)
            case _:
                print("\nNo such command. (Type help to see available commands)\n")



# Main function
def main():
    load_data()
    print_banner()
    print_help()
    print()

    while (True):
        user_input = get_input().lower()
        match user_input:
            case 'exit':
                return 0
            case 'custom':
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
