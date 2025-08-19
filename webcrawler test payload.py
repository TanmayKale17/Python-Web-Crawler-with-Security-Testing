from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

start_url = "http://localhost:5000/"
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
                full_url = urljoin(current_url, str(href))
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == domain_name and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)

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
                input_type = str(input_tag.get("type", "text")).lower()
                input_value = input_tag.get("value", "")
                print(f"  🔹 Input name: {input_name}, type: {input_type}, default: {input_value}")

    except Exception as e:
        print(f"❌ Error extracting forms from {currentform}: {e}")

print("\n\n====== 🧪 Submitting Test Payloads with Selenium ======\n")

test_payload = "<script>alert('XSS')</script>"

for currentform in form_set:
    try:
        driver.get(currentform)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        forms = soup.find_all("form")

        for form in forms:
            if not isinstance(form, Tag):
                continue

            method = str(form.get("method", "get")).lower()
            inputs = form.find_all("input")

            print(f"\n🔍 Submitting form on: {currentform} | Method: {method.upper()}")

            for input_tag in inputs:
                if not isinstance(input_tag, Tag):
                    continue

                input_name = input_tag.get("name")
                input_type = str(input_tag.get("type", "text")).lower()
                input_disabled = input_tag.get("disabled")
                input_readonly = input_tag.get("readonly")
                input_hidden = input_type == "hidden"

                if not input_name:
                    continue
                if input_disabled or input_readonly or input_hidden:
                    print(f"  ⚠️ Skipping hidden/disabled/readonly input: {input_name}")
                    continue
                if input_type not in ["text", "email", "search", "url", "tel", "password"]:
                    print(f"  ⚠️ Skipping unsupported input type: {input_type}")
                    continue

                try:
                    selenium_input = driver.find_element("name", str(input_name))
                    driver.execute_script("arguments[0].scrollIntoView(true);", selenium_input)
                    if not selenium_input.is_displayed() or not selenium_input.is_enabled():
                        print(f"  ⚠️ Skipping non-visible or disabled element: {input_name}")
                        continue
                    selenium_input.clear()
                    selenium_input.send_keys(test_payload)
                    print(f"  🧪 Filled: {input_name}")

                except Exception as e:
                    print(f"  ⚠️ Could not interact with {input_name}: {e}")

         
            try:
                submit = driver.find_element("xpath", "//form//input[@type='submit' or @type='button']")
                try:
                    submit.click()
                except UnexpectedAlertPresentException as e:
                    print(f"🚨 Alert triggered during click: {e}")
                    try:
                        alert = driver.switch_to.alert
                        print(f"🚨 Alert text: {alert.text}")
                        alert.accept()
                    except NoAlertPresentException:
                        print("⚠️ Alert disappeared before handling.")
                time.sleep(2)
                print("✅ Form submitted.")
            except:
                
                try:
                    driver.find_element("tag name", "form").submit()
                    time.sleep(2)
                    print("✅ Form submitted via fallback.")
                except UnexpectedAlertPresentException as e:
                    print(f"🚨 Alert triggered during fallback submit: {e}")
                    try:
                        alert = driver.switch_to.alert
                        print(f"🚨 Alert text: {alert.text}")
                        alert.accept()
                    except NoAlertPresentException:
                        print("⚠️ Alert disappeared before handling.")
                except Exception as e:
                    print(f"❌ Submission failed: {e}")

            try:
                alert = driver.switch_to.alert
                print(f"🚨 Leftover alert found: {alert.text}")
                alert.accept()
            except NoAlertPresentException:
                pass

            if test_payload in driver.page_source:
                print("🚨 Possible XSS vulnerability detected (reflection).")
            else:
                print("✅ No reflection detected.")

    except Exception as e:
        print(f"❌ Error testing form at {currentform}: {e}")

driver.quit()
