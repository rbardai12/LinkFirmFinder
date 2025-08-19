# Requirements: pip install flask selenium beautifulsoup4 webdriver-manager openpyxl
import os
import tempfile
from flask import Flask, render_template_string, request, send_file, redirect, url_for, flash
import logging
from Main import linkedin_job_search_url, get_driver, scroll_to_load_jobs, extract_companies_from_html, export_companies

app = Flask(__name__)
app.secret_key = os.urandom(24)

HTML_FORM = '''
<!doctype html>
<title>LinkFirmFinder Web</title>
<h2>LinkedIn Company Finder</h2>
<form method=post enctype=multipart/form-data>
  <label>Search Term: <input type=text name=search required></label><br><br>
  <label>Location: <input type=text name=location></label><br><br>
  <label>Export Format:
    <select name=format>
      <option value="txt">TXT</option>
      <option value="csv">CSV</option>
      <option value="xlsx">Excel</option>
    </select>
  </label><br><br>
  <label>Headless Mode: <input type=checkbox name=headless checked></label><br><br>
  <input type=submit value="Find Companies">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul style="color:red;">
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
{% if download_url %}
  <a href="{{ download_url }}">Download Results</a>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    download_url = None
    if request.method == 'POST':
        search = request.form['search'].strip()
        location = request.form.get('location', '').strip() or None
        export_format = request.form.get('format', 'txt')
        headless = 'headless' in request.form
        if not search:
            flash('Search term is required!')
            return render_template_string(HTML_FORM, download_url=None)
        url = linkedin_job_search_url(search, location)
        logging.info("Web UI: Opening LinkedIn Jobs page: %s", url)
        driver = get_driver(headless=headless)
        try:
            driver.get(url)
            import time; time.sleep(5)
            scroll_to_load_jobs(driver)
            html = driver.page_source
            companies = extract_companies_from_html(html)
            if not companies:
                flash('No companies found. LinkedIn may have changed their page structure or you may need to log in.')
            else:
                fd, temp_path = tempfile.mkstemp(suffix=f'.{export_format}')
                os.close(fd)
                export_companies(companies, temp_path, export_format)
                filename = f"{search.replace(' ', '_')}.{export_format}"
                download_url = url_for('download_file', path=os.path.basename(temp_path), filename=filename)
                # Store temp_path in session or a global dict if needed for cleanup
                flash(f'Found {len(companies)} companies!')
        except Exception as e:
            flash(f'Error: {e}')
        finally:
            driver.quit()
    return render_template_string(HTML_FORM, download_url=download_url)

@app.route('/download/<path:path>')
def download_file(path):
    filename = request.args.get('filename', path)
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, path)
    if not os.path.exists(file_path):
        flash('File not found or expired.')
        return redirect(url_for('index'))
    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
