from newspaper import Article
import requests,re,os
import pandas as pd
import requests,base64
from datetime import timedelta,datetime

# -------- import dan setup module selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
options = Options()
options.add_argument('--headless') # agar berkalan tanpa ui
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-logging')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--log-level=3')
options.add_argument("--window-size=1920,1080") # ukuran window
# nonaktifkan media
prefs = {
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.video": 2,
    "profile.managed_default_content_settings.audio": 2
}
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)") # user agent
options.add_experimental_option("prefs", prefs)

# -------- load model dan fungsi fungsi ektrak berita (narasumber,sentiment,rangkuman)
from transformers import pipeline
ner_model = pipeline("ner",model='model_ner',tokenizer='model_sent',aggregation_strategy="first")
sen_model = pipeline("text-classification",model="model_sent",tokenizer='model_sent')
sum_model = pipeline("summarization", model="bert-indonesian-news-summarization",tokenizer="bert-indonesian-news-summarization")


# membersihkan text dari url,domain,simbol,enter berlebih,dan sepasi berlebih
def clean_text(text: str) -> str:
    text = re.sub(r'http\S+|www\S+|\S+\.(com|id|org|net|co|xyz|info)\S*', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.lower()
    return text
# sentiment analys
def sentiment(judul,full):
    if type(full)==str:
        pos = 0
        neg = 0
        full = clean_text(full).split('\n')+[judul]
        for x in full:
            try:
                sen = sen_model(x[0:512])[0]
            except:
                print(x)
                raise
            if sen['label']=='POSITIVE':
                pos+=sen['score']
            elif sen['label']=='NEGATIVE':
                neg+=sen['score']
        return ('positif' if pos>neg else 'negatif' if neg>pos else 'netral')
    return 'netral'
# bagi text per part 500
def split_text(text,model, max_length=500):
    tokens = model.tokenizer(text, add_special_tokens=False)["input_ids"]
    chunks = [tokens[i:i+max_length] for i in range(0, len(tokens), max_length)]
    return [model.tokenizer.decode(chunk) for chunk in chunks]
# menemukan nama narasumber
def narasumber(full):
    if type(full) != str:
        return []
    nar = set()
    for chunk in split_text(full,ner_model):
        doc = ner_model(chunk)
        for x in doc:
            if x["entity_group"] == "PERSON":
                nar.add(x["word"])
    return nar
# utama 
def ekstrak_berita(news):
    sen = sentiment(*news)
    nar = narasumber(news[0])
    return {
        'inti_berita':','.join([x['summary_text'] for x in sum_model(split_text(news[0].strip(),sum_model))]),
        'sentiment':sen,
        'narasumber':nar,
        'reporter':''
    }

        
folderberita = 'data2'
# temukan keyword yang ada di artikel(sesuai file keyword.json)
def find_keywords(article: str, keywords: list) -> list:
        # ubah jadi huruf kecil semua biar pencarian tidak case-sensitive
        if not isinstance(article, str):
            return []
        article_lower = article.lower()
        found = [kw for kw in keywords if kw.lower() in article_lower]
        return found

# screenshot website 
def fullpage_screenshot(driver, file_path):
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "fromSurface": True,
        "captureBeyondViewport": True
    })
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(result['data']))
# ---------- fungsi utama (ambil data,proses data, simpan data, kembalikan data)

def fetch_and_process_news(date_str, query, folderberita, force, dw):
    """Mengambil berita untuk satu tanggal dan memprosesnya."""
    filename = datetime.strptime(date_str, '%m/%d/%Y').strftime('%m-%d') + '.xlsx'
    file_path = os.path.join(folderberita, filename)

    # Cek apakah file sudah ada dan tidak perlu di-force
    if not force and os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        # Perbarui keyword jika dw True atau tanggal sudah lewat 2 hari
        if dw or datetime.strptime(date_str, '%m/%d/%Y') <= (datetime.now() - timedelta(days=2)):
            df_existing["keyword"] = df_existing["full"].apply(lambda x: find_keywords(x, query))
            df_existing = df_existing.loc[:, ~df_existing.columns.str.contains('^Unnamed')]
            df_existing.to_excel(file_path, index=False)
            return df_existing

    # Jika file tidak ada atau di-force, lakukan scraping
    print(f'[INFO] mengambil berita tanggal {date_str}')
    df_new = pd.DataFrame(columns=['media', 'waktu', 'isi isu', 'narasumber', 'sentiment', 'judul', 'link', 'reporter', 'full', 'keyword'])

    for q in query:
        url = f'https://serpapi.com/search.json?engine=google&q={q}&location=Indonesia&google_domain=google.co.id&gl=id&hl=id&tbs=cdr:1,cd_min:{date_str},cd_max:{date_str}&tbm=nws&api_key=2a7541196951883a06ca6d92ac203f21571a303682cf95ee5adeda2935091f2d'
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Cek jika ada error HTTP
            news_results = response.json().get('news_results', [])
        except requests.RequestException as e:
            print(f"[GAGAL] request ke SerpApi untuk query '{q}': {e}")
            continue
        driver = webdriver.Chrome(options=options)
        for news_item in news_results:
            link = news_item.get('link')
            if not link:
                continue
            if (filename in os.listdir(folderberita+'')):
                dfx = pd.read_excel(folderberita+'/'+filename)
                if news_item['link'] in dfx['link']:
                    dfx["keyword"] = dfx["full"].apply(lambda x: find_keywords(x, query))
                    dfx = dfx.loc[:, ~dfx.columns.str.contains('^Unnamed')]
                    dfx.to_excel(folderberita+'/'+filename)
                    return dfx

            
            try:
                print(f'[INFO] mengambil berita dari {link}')
                driver.get(link)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
                
                article = Article(link, language="id")
                article.download(driver.page_source)
                article.parse()
                
                full_text = article.text
                extracted_data = ekstrak_berita((full_text, news_item.get('title', '')))

            except Exception as e:
                print(f"[GAGAL] mengambil {link} dengan error: {e}")
                full_text, extracted_data = '', None

            if extracted_data:
                try:
                    narasumber = ','.join(extracted_data['narasumber']) if isinstance(extracted_data['narasumber'], list) else extracted_data['narasumber'] or ''
                    sentimen = extracted_data.get('sentiment', 'netral') or 'netral'
                    reporter = extracted_data.get('reporter', '') or ''
                except KeyError as e:
                    print(f"[ERROR] key tidak ditemukan di hasil ekstraksi: {e}")
                    narasumber, sentimen, reporter = '', 'netral', ''

                new_row = {
                    'media': news_item.get('source', link.split('/')[2]),
                    'waktu': date_str,
                    'isi isu': extracted_data.get('inti_berita', ''),
                    'narasumber': narasumber,
                    'sentiment': sentimen,
                    'judul': news_item.get('title', ''),
                    'link': link,
                    'reporter': reporter,
                    'full': full_text,
                    'keyword': find_keywords(full_text, query)
                }
                df_new = pd.concat([df_new, pd.DataFrame([new_row])], ignore_index=True)
        driver.quit()

    df_new.to_excel(file_path, index=False)
    return df_new

def main(start="08-01", end="08-02", query=['badan informasi geospasial'], dw=False, force=False) -> pd.DataFrame:
    """Fungsi utama untuk mengambil data berita dalam rentang tanggal tertentu."""
    
    start_date = datetime.strptime("2025-" + start, "%Y-%m-%d")
    end_date = datetime.strptime("2025-" + end, "%Y-%m-%d")
    
    print(f'[INFO] tanggal awal {start_date.strftime("%Y/%m/%d")}')
    print(f'[INFO] tanggal akhir {end_date.strftime("%Y/%m/%d")}')
    
    all_results = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%m/%d/%Y")
        
        # Panggil fungsi yang lebih spesifik untuk satu hari
        daily_df = fetch_and_process_news(date_str, query, folderberita, force, dw)
        
        all_results = pd.concat([all_results, daily_df], ignore_index=True)
        current_date += timedelta(days=1)
        
    return all_results