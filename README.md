# DorkSweep

## Overview

This project is a comprehensive tool for performing Google Dorking across multiple search engines (Google, Bing, DuckDuckGo, Yahoo). It supports both custom and automated dorking with the ability to export results to a CSV file.

## Features

- Randomizes User-Agent and Headers for each request
- Supports Google, Bing, DuckDuckGo, and Yahoo search engines
- **Custom Dorking**: Allows experienced users to input their own queries.
- **Automated Dorking**: Provides pre-defined queries across different categories such as Database, Network and Security Information, Technical Information, and Web Vulnerability.
- **Multi-Threading**: Utilizes multi-threading to fetch results concurrently from multiple search engines.
- **CSV Export**: Saves the search results to a CSV file with relevant details.

## Setup

1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_directory>
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Ensure the CSV files for each category are in the scripts/ directory.


## Usage

1. Run the Tool:

```bash
python dorking_tool.py
```

2. Commands:

- `help`: Displays available commands.
- `exit`: Terminates the program.
- `custom`: Enter Custom Google Dorking (for experienced users).
- `auto`: Enter Automated Google Dorking.

3. Automated Google Dorking Commands:

- `show`: Shows available categories for dorking.
- `set <category>`: Sets the category.
- `back`: Go back to mode selection.

After choosing a category:

- `list`: Lists all available options under the chosen category.
- `use <option>`: Uses/sets the option you want to perform a search on.
- `dsweep`: Executes Google Dorking with selected query.

## Example Queries for Custom Dorking
- `intext:"kyle santos" site:linkedin.com`: Chained query.
- `inurl:admin`: Find admin pages.
- `intitle:"index of"`: Find directory listings.
- `inurl:login`: Find login pages.
- `filetype:pdf`: Find PDF files.
- `site:example.com`: Search within a specific site.

## Code Explanation
### Main Functions
- get_random_headers: Randomizes user-agents and Accept-Language headers to avoid detection.
- load_data: Loads CSV data for each category into a dictionary.
- print_banner: Displays the tool banner.
- print_help: Prints available commands.
- print_categories: Displays available categories for automated dorking.
- print_queries: Lists all available options under a chosen category.
- get_input: Handles user input.
- extract_results: Extracts search results from the HTML response using BeautifulSoup.
- google_dork: Performs a Google search with the given query.
- bing_dork: Performs a Bing search with the given query.
- duckduckgo_dork: Performs a DuckDuckGo search with the given query.
- yahoo_dork: Performs a Yahoo search with the given query.
- aggregate_dork: Aggregates results from all search engines using multi-threading.
- dork_sweep: Handles dork search and result printing.
- auto_dork: Handles automated Google Dorking mode.
- category_selected: Manages the chosen category for automated dorking.
- main: Main function to run the tool.

### Example CSV Export
The search results are saved to a CSV file dork_results.csv with the following headers:
- position: Position of the result.
- title: Title of the result.
- link: Link to the result.
- domain: Domain of the result.
- search_engine: The search engine used to find the result.

## Notes
- Use the tool responsibly and adhere to the legal and ethical guidelines for web scraping and data usage.
- Automated search queries can trigger CAPTCHA challenges or temporary blocks from search engines.