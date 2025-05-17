from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

start_url = "https://owasp.org/www-project-juice-shop/"
domain_name = urlparse(start_url).netloc

visited = set()
to_visit = [start_url]
count=0
while to_visit:

    count+=1
    print(f"Visited {count} pages")
    if(len(to_visit) > 10):
        print("STOPPING")
        break
    
    current_url = to_visit.pop(0)  

    if current_url in visited:
        continue

    print(f"\n🔍 Visiting: {current_url}")
    try:
        response = requests.get(current_url, timeout=5)
        visited.add(current_url)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error visiting {current_url}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        if not isinstance(link, Tag):
            continue
        href = link.get("href")
        if href:
            full_url = urljoin(current_url,str(href))
            parsed_url = urlparse(full_url)

            if parsed_url.netloc == domain_name and full_url not in visited and full_url not in to_visit:
                to_visit.append(full_url)
                print("➕ Found:", full_url)
