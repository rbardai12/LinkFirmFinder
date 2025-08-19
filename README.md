# LinkFirmFinder

LinkFirmFinder is a robust, cross-platform, fully automated tool to find companies hiring for a specific role on LinkedIn. It uses Selenium and BeautifulSoup to scrape job postings and extract company names, outputting a clean, deduplicated list for your job search or business outreach.

---

## Features
- **Automated LinkedIn job search** for any keyword and location
- **No manual steps**: everything is handled in code (no clipboard, no mouse automation)
- **Cross-platform**: works on macOS, Windows, and Linux
- **Command-line interface**: specify search term, location, and output file
- **Robust error handling and logging**
- **Production-ready**: easy to extend and maintain

---

## Requirements
- Python 3.8+
- Google Chrome browser
- ChromeDriver (auto-managed if you install `webdriver-manager`)

### Python Packages
Install all required packages with:
```bash
pip install selenium beautifulsoup4 webdriver-manager
```

---

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd LinkFirmFinder
   ```
2. Install the requirements (see above).
3. Ensure Google Chrome is installed and up to date.

---

## Usage
Run the script from the command line:
```bash
python Main.py --search "Data Scientist" --location "San Francisco" --output results.txt --headless
```

### Arguments
- `--search` or `-s` (required): The job title or keyword to search for (e.g., "Data Scientist").
- `--location` or `-l` (optional): The location to search in (e.g., "San Francisco").
- `--output` or `-o` (optional): Output file name (default: `<search_term>.txt`).
- `--headless` (optional): Run Chrome in headless mode (no browser window).

### Example
```bash
python Main.py --search "Product Manager" --location "New York" --headless
```

---

## Output
- The script will create a text file (default: `<search_term>.txt`) with a deduplicated, alphabetized list of company names hiring for the specified role.

---

## Troubleshooting
- **Import errors**: Make sure you have installed all required Python packages.
- **ChromeDriver issues**: The script uses `webdriver-manager` to auto-download the correct driver. If you have issues, ensure Chrome is installed and up to date.
- **No results**: LinkedIn may change their page structure, or you may need to log in. Try running without `--headless` to debug visually.
- **CAPTCHA or login required**: For some searches, LinkedIn may require login or show a CAPTCHA. This script does not handle authentication.

---

## Contributing
Pull requests and issues are welcome! Please:
- Follow PEP8 style guidelines
- Add clear commit messages
- Test your changes on multiple platforms if possible

---

## License
MIT License
