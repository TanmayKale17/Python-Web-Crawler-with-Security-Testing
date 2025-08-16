# 🕷️ Python Web Crawler with Form Extraction

## 🔍 Overview
This project is a **Python-based web crawler** that:
- Starts from a given URL
- Crawls links within the same domain
- Handles **JavaScript-rendered pages** using Selenium
- Extracts and prints details of **HTML forms** (action, method, input fields)

It is designed for learning, automation, and as a foundation for security testing tasks like form analysis.

---

## 🚀 Features
- **Domain-restricted crawling** – prevents infinite crawling across sites.
- **Headless browsing** – uses Selenium in headless mode (no GUI).
- **Form extraction** – captures form actions, methods, and input fields.
- **JavaScript support** – can parse dynamically rendered pages.
- **Safe stop condition** – crawler stops after 100 pages to prevent runaway loops.

---

## 🛠️ Tech Stack
- Python 3.x
- [Selenium]  
- [BeautifulSoup4]  
- [Chrome WebDriver]

---

## 📌 How It Works
1. Starts crawling from the given `start_url` (`http://localhost:3000/` by default).  
2. Visits links within the same domain.  
3. Uses **Selenium + BeautifulSoup** to:
   - Render JavaScript content
   - Collect forms and their attributes
   - Print form details (action, method, input fields)  
4. Stops crawling after 100 pages (for safety).  

---

## ⚙️ Setup & Usage

### 1. Install dependencies
```bash
pip install selenium beautifulsoup4
