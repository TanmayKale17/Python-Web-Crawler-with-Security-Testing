from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

start_url = "http://localhost:3000/"
domain_name = urlparse(start_url).netloc

visited = set()
to_visit = [start_url]
form_set = set()
count = 0

while to_visit:
    count += 1
    print(f"Visited {count} pages")

    if len(to_visit) > 100:
        print("STOPPING")
        break

    current_url = to_visit.pop(0)
    if current_url in visited:
        continue

    print(f"\n🔍 Visiting: {current_url}")
    try:
        driver.get(current_url)
        time.sleep(2) 
        visited.add(current_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        forms = soup.find_all("form")
        print(f"📝 Found {len(forms)} forms in {current_url}")
        if forms:
            form_set.add(current_url)

        links = soup.find_all("a")
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

    except Exception as e:
        print(f"❌ Error visiting {current_url}: {e}")
        continue


print("\n\n====== 🔍 Extracting Forms From Stored Pages ======\n")

for currentform in form_set:
    try:
        driver.get(currentform)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        forms = soup.find_all("form")
        print(f"\n📝 Page: {currentform} | Found {len(forms)} forms")

        for form in forms:
            if not isinstance(form, Tag):
                continue
            action = form.get("action")
            method = str(form.get("method", "get")).lower()
            inputs = form.find_all("input")

            print(f"📤 Form Action: {action}")
            print(f"🧾 Form Method: {method}")

            for input_tag in inputs:
                if not isinstance(input_tag, Tag):
                    continue
                input_name = input_tag.get("name")
                input_type = input_tag.get("type", "text")
                input_value = input_tag.get("value", "")
                print(f"  🔹 Input name: {input_name}, type: {input_type}, default: {input_value}")

    except Exception as e:
        print(f"❌ Error extracting forms from {currentform}: {e}")

driver.quit()
