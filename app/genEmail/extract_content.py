from bs4 import BeautifulSoup

def extract_email_content(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract visible text
    content = soup.get_text(separator='\n')

    # Clean and remove extra whitespace or lines
    clean_content = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])

    return clean_content