# Requirements: pip install selenium beautifulsoup4 webdriver-manager openpyxl
# Note: If you see import errors, install the above packages.
import argparse
import time
import sys
import logging
import csv
import getpass
import json
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup

# Optional: Use webdriver-manager for cross-platform driver management
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER = True
except ImportError:
    WEBDRIVER_MANAGER = False


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        if WEBDRIVER_MANAGER:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        logging.error("Error initializing Chrome WebDriver: %s", e)
        sys.exit(1)


def load_cookies(driver, cookies_path):
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    driver.get("https://www.linkedin.com")
    time.sleep(2)
    for cookie in cookies:
        # Remove fields not accepted by Selenium
        cookie.pop('sameSite', None)
        cookie.pop('storeId', None)
        cookie.pop('hostOnly', None)
        cookie.pop('id', None)
        cookie.pop('expirationDate', None)
        # Selenium expects expiry, not expirationDate
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        # LinkedIn cookies are for .www.linkedin.com or .linkedin.com
        if 'domain' in cookie and cookie['domain'].startswith('.linkedin.'):
            cookie['domain'] = '.linkedin.com'
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            logging.debug(f"Could not add cookie: {cookie.get('name')} - {e}")
    driver.refresh()
    time.sleep(2)
    logging.info("Loaded cookies from %s", cookies_path)


def login_linkedin(driver, username, password):
    login_url = "https://www.linkedin.com/login"
    driver.get(login_url)
    time.sleep(2)
    try:
        user_input = driver.find_element(By.ID, "username")
        pass_input = driver.find_element(By.ID, "password")
        user_input.clear()
        user_input.send_keys(username)
        pass_input.clear()
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(3)
        # Check for login errors
        if "login" in driver.current_url:
            logging.error("Login failed. Please check your credentials or if LinkedIn requires additional verification.")
            sys.exit(1)
        logging.info("Successfully logged in to LinkedIn.")
    except NoSuchElementException as e:
        logging.error("Login page structure not as expected: %s", e)
        sys.exit(1)


def linkedin_job_search_url(search_term, location=None):
    base_url = "https://www.linkedin.com/jobs/search/?"
    params = [f"keywords={search_term.replace(' ', '%20')}"]
    if location:
        params.append(f"location={location.replace(' ', '%20')}")
    params.append("geoId=103644278")  # US geoId, can be parameterized
    return base_url + "&".join(params)


def extract_companies_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    companies = set()
    for job_card in soup.find_all('li', class_='jobs-search-results__list-item'):
        company_elem = job_card.find('a', class_='hidden-nested-link')
        if not company_elem:
            company_elem = job_card.find('span', class_='job-search-card__company-name')
        if company_elem:
            company = company_elem.get_text(strip=True)
            if company:
                companies.add(company)
    # Fallback: try to find all company name spans
    if not companies:
        for span in soup.find_all('span', class_='job-search-card__company-name'):
            company = span.get_text(strip=True)
            if company:
                companies.add(company)
    return sorted(companies)


def scroll_to_load_jobs(driver, scroll_pause=2, max_scrolls=20):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        logging.info("Scrolled %d/%d", i+1, max_scrolls)


def export_companies(companies, output_file, export_format):
    if export_format == 'txt':
        with open(output_file, 'w', encoding='utf-8') as f:
            for company in companies:
                f.write(company + '\n')
    elif export_format == 'csv':
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Company'])
            for company in companies:
                writer.writerow([company])
    elif export_format == 'xlsx':
        if not OPENPYXL_AVAILABLE:
            logging.error("openpyxl is not installed. Please install it to export to Excel.")
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Companies'
        ws.append(['Company'])
        for company in companies:
            ws.append([company])
        wb.save(output_file)
    else:
        logging.error("Unknown export format: %s", export_format)


def interactive_cli():
    print("\n--- LinkFirmFinder Interactive CLI ---\n")
    search_term = input("Enter the job title or keyword to search for (e.g., Data Scientist): ").strip()
    location = input("Enter the location (optional, press Enter to skip): ").strip()
    default_output = f"{search_term.replace(' ', '_')}.txt"
    output_file = input(f"Enter output file name (default: {default_output}): ").strip() or default_output
    print("Select export format:")
    print("1. txt (plain text)")
    print("2. csv (spreadsheet)")
    print("3. xlsx (Excel)")
    export_choice = input("Enter choice [1-3]: ").strip()
    export_format = {"1": "txt", "2": "csv", "3": "xlsx"}.get(export_choice, "txt")
    headless = input("Run browser in headless mode? (y/n, default: y): ").strip().lower() or 'y'
    headless = headless == 'y'
    use_cookies = input("Use LinkedIn cookies for login? (y/n, default: n): ").strip().lower() or 'n'
    cookies_path = None
    username = None
    password = None
    if use_cookies == 'y':
        cookies_path = input("Enter path to your LinkedIn cookies JSON file: ").strip()
    else:
        username = input("Enter your LinkedIn username (email): ").strip()
        password = getpass.getpass("Enter your LinkedIn password: ")
    return search_term, location or None, output_file, headless, export_format, cookies_path, username, password


def main():
    setup_logger()
    parser = argparse.ArgumentParser(description="Find companies hiring for a specific role on LinkedIn.")
    parser.add_argument('--search', '-s', help='Search term (e.g., Data Scientist)')
    parser.add_argument('--location', '-l', default=None, help='Location (optional)')
    parser.add_argument('--output', '-o', default=None, help='Output file name (default: <search_term>.txt)')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--format', '-f', choices=['txt', 'csv', 'xlsx'], default='txt', help='Export format (txt, csv, xlsx)')
    parser.add_argument('--cookies', help='Path to LinkedIn cookies JSON file (exported from browser)')
    parser.add_argument('--username', help='LinkedIn username (email)')
    parser.add_argument('--password', help='LinkedIn password')
    args = parser.parse_args()

    if not args.search or (not args.cookies and (not args.username or not args.password)):
        # No command-line arguments: run interactive CLI
        search_term, location, output_file, headless, export_format, cookies_path, username, password = interactive_cli()
    else:
        search_term = args.search
        location = args.location
        output_file = args.output or f"{search_term.replace(' ', '_')}.{args.format}"
        headless = args.headless
        export_format = args.format
        cookies_path = args.cookies
        username = args.username
        password = args.password

    url = linkedin_job_search_url(search_term, location)
    logging.info("Opening LinkedIn Jobs page: %s", url)

    driver = get_driver(headless=headless)
    try:
        if cookies_path:
            load_cookies(driver, cookies_path)
        else:
            login_linkedin(driver, username, password)
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        scroll_to_load_jobs(driver)
        html = driver.page_source
        companies = extract_companies_from_html(html)
        if not companies:
            logging.warning("No companies found. LinkedIn may have changed their page structure or you may need to log in.")
        else:
            export_companies(companies, output_file, export_format)
            logging.info("Found %d companies. Results saved to %s", len(companies), output_file)
    except Exception as e:
        # Broad exception is caught here to ensure all errors are logged in production
        logging.error("An error occurred: %s", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()