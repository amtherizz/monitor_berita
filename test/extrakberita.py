from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = "https://surabaya.tribunnews.com/2025/08/01/sengketa-16-pulau-dengan-tulungagung-menggantung-dprd-trenggalek-tunggu-ketegasan-kemendagri"
# from bs4 import BeautifulSoup
options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-logging')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--log-level=3')
options.add_argument("--window-size=1920,1080")  
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.video": 2,
    "profile.managed_default_content_settings.audio": 2
}
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_experimental_option("prefs", prefs)
# url = "https://...link_berita..."

article = Article(url, language="id")
driver = webdriver.Chrome(options=options)
driver.get(url)
article.download(driver.page_source)
article.parse()
# Ambil judul & isi
print("Judul:", article.title)
print("Tanggal (auto):", article.publish_date)  # sering None
print("Author (auto):", article.authors)
print(article.text)
# html = BeautifulSoup(article.html,'html.parser')
# print(html.text)