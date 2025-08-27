from newspaper import Article
import json,requests,bs4
import dateparser,csv
import pandas as pd
import uuid
import json,re,os
import requests  # masih bisa dipakai untuk fallback
import time,base64
import dateparser
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import queue
# from tkinter import *
# from tkinter.scrolledtext import ScrolledText
# from tkinter import messagebox
# should_stop = False

# # Queue untuk komunikasi log antar thread
# log_queue = queue.Queue()
# Setup Selenium (headless)
options = Options()
options.add_argument('--headless')
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
folderberita = 'data2'
def fullpage_screenshot(driver, file_path):
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "fromSurface": True,
        "captureBeyondViewport": True
    })
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(result['data']))
system_prompt = """
        Anda adalah asisten yang ahli dalam mengekstraksi informasi penting dari berita. Tugas Anda adalah mengidentifikasi paragraf-paragraf inti, sumber media, narasumber (jika ada), reporter (jika ada), sentimen terhadap Badan Informasi Geospasial (BIG) beserta buktinya, dan juga menyajikan teks berita lengkap yang sudah bersih dari elemen non-berita.

        **Instruksi Detail:**
        1.  **inti_berita**: Ekstrak paragraf-paragraf utama yang paling relevan dan padat informasi. Pastikan ini adalah ringkasan yang komprehensif dari isi berita. Jangan hanya mengambil paragraf pertama atau terakhir, tetapi cari esensi beritanya.
        2.  **sumber_media**: Identifikasi nama media yang memublikasikan berita ini.
        3.  **narasumber**: Cari nama-nama orang yang dikutip atau diwawancarai dalam berita. Jika tidak ada, biarkan kosong.
        4.  **reporter**: Cari nama penulis atau reporter berita. Jika tidak ada, biarkan kosong.
        5. **sentiment**: Lakukan analisis sentimen terhadap **peran atau tindakan BIG dalam konteks artikel**. Pilih salah satu dari: `"positif"`, `"netral"`, atau `"negatif"`. 
            - Fokuskan pada konteks nyata, bukan pada opini subjektif dari satu pihak saja.
            - Jangan menilai sentimen hanya berdasarkan **pendapat atau kutipan satu orang**, terutama jika orang tersebut **tidak memiliki pengaruh signifikan atau tidak mewakili sudut pandang utama berita**.
            - Abaikan bias institusional atau pujian kosong yang tidak didukung fakta atau dampak nyata.


        **Format Output (HARUS JSON):**
        ```json
        {
          "inti_berita": "...",
          "sumber_media": "...",
          "narasumber": null,
          "reporter": null,
          "sentiment": "positif/netral/negatif",

        }
        ```
        **Catatan Penting:**
        Jika suatu kolom tidak ditemukan, set nilainya ke null (kecuali sentiment, yang harus selalu diisi dengan salah satu dari tiga nilai yang ditentukan).


        Sentimen dan bukti_sentiment harus benar-benar berfokus pada peran, tindakan, atau dampak spesifik BIG yang dijelaskan dalam berita, bukan hanya pada pernyataan umum atau komitmen.

"""
#8.  **full_berita**: Berikan kembali keseluruhan teks berita **yang sudah bersih dari segala macam menu navigasi, iklan, footer, header, daftar postingan terkait, komentar, atau elemen-elemen lain yang bukan bagian inti dari artikel berita**. Pastikan hanya teks naratif utama berita yang tersisa, termasuk judul dan sub-judul jika relevan, tetapi tanpa sisa-sisa HTML atau string yang tidak relevan (seperti 'Likes', 'Followers', 'Trending', dll. yang sering muncul dari `BeautifulSoup.text`). Ini harus merupakan teks berita lengkap yang ringkas dan mudah dibaca.
# idsys,idusr = "d81d6fdb-f80c-40fc-9da9-feedc160c0df","85265ea2-fb6d-427c-b61a-ebdf0444f339"
idusr,idsys = str(uuid.uuid4()),str(uuid.uuid4())
def ekstrak_berita(news: str) -> str:
    headers = {
        'User-Agent': 'ktor-client',
        'Accept': 'application/json,text/event-stream',
        'streaming': 'true',
        'x-accel-buffering': 'no',
        'accept-charset': 'UTF-8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIzYzM1YTRiMi1mZGRhLTQyOGUtYWZhNi1jYTVkMzE3YzYxYTYiLCJpbnRlZ3JpdHlDaGVjayI6dHJ1ZSwiYmFzZVVybCI6ImNoYXRseTovL29hdXRoIiwicHJvZHVjdFZhbGlkRm9yIjoiQ0hBVExZIiwiaWF0IjoxNzU2MTgzMDYzLCJleHAiOjE3NTYyMDQ2NjMsInN1YiI6IjNjMzVhNGIyLWZkZGEtNDI4ZS1hZmE2LWNhNWQzMTdjNjFhNiJ9.3CX-AckFj3a-wmyDhZhOL0E-XP8Dx6vLFMRNiZTPbJE',
    }
    files = {
        'data': (None, json.dumps({
    "id": "109dc4ec-cbcf-41fb-95d2-5e49b2076cce",
    "model": "vgpt-g3-m",
    "messages": [
                    {
                        "content": system_prompt,
                        "id": idsys,
                        "role": "system",
                        "model": "vgpt-g2-4"
                    },
                    {
                        "content": [
                                {
                                "type": "text",
                                "text": news
                                }
                            ],
                        "id": idusr,
                        "role": "user",
                        "model": "vgpt-g2-4"
                    }
                ],
    "temperature": 0.5,
    "stream": True
    }), None, {'Content-Type': 'application/json'}),
    }

    response = requests.post('https://streaming-chatly.vyro.ai/v1/chat/completions', headers=headers, files=files)

    output = ""
    # print(response.content)
    for line in response.iter_lines(decode_unicode=True):
        # print(line)
        if not line:
            continue

        if line.startswith("event: done"):
            break

        if line.startswith("data: "):
            try:
                data_json = json.loads(line[6:])
                content = data_json.get("content", "")
                # print(content)
                output += content
            except json.JSONDecodeError as e:
                print("Gagal parse JSON:", line)
    try:
        json_match = re.search(r"```(?:json)?(.*?)```", output, re.DOTALL).group(1).strip()
        return json.loads(json_match)
    except:print(response.text)
def find_keywords(article: str, keywords: list) -> list:
    # try:
        # ubah jadi huruf kecil semua biar pencarian tidak case-sensitive
        if not isinstance(article, str):
            return []
        article_lower = article.lower()

        # cek keyword satu per satu
        found = [kw for kw in keywords if kw.lower() in article_lower]
        return found
    # except:
        # print(article)
        # raise
def main(start="08-01",end="08-02",query=['badan informasi geospasial'],dw=False,force=False) -> pd.DataFrame:
    from datetime import datetime, timedelta
    start_date = datetime.strptime("2025-"+start, "%Y-%m-%d")
    end_date = datetime.strptime("2025-"+end, "%Y-%m-%d")
    result = pd.DataFrame(columns=['media', 'waktu', 'isi isu', 'narasumber', 'sentiment', 'judul', 'link', 'reporter','full',"keyword"])
    # Loop per tanggal
    print('[INFO] tanggal awal '+start_date.strftime("%Y/%m/%d"))
    print('[INFO] tanggal akhir '+end_date.strftime("%Y/%m/%d"))
    # return filename
    current_date = start_date
    while current_date <= end_date:
        filename = current_date.strftime('%m-%d')+'.xlsx'
        if not force:
            if (filename in os.listdir(folderberita+'')) and (datetime.now().strftime('%m-%d') != current_date.strftime('%m-%d')):
                dfx = pd.read_excel(folderberita+'/'+filename)
                if dw or current_date<=(datetime.now() - timedelta(days=2)):
                # if True:
                    # dfx.columns.append("keyword")
                    dfx["keyword"] = dfx["full"].apply(lambda x: find_keywords(x, query))
                    dfx = dfx.loc[:, ~dfx.columns.str.contains('^Unnamed')]
                    dfx.to_excel(folderberita+'/'+filename)
                    # mask = dfx["keyword"].apply(lambda kws: "badan informasi geospasial" in kws if isinstance(kws, list) else False)
                    # dfx = dfx[mask]
                    result = pd.concat([result,dfx],ignore_index=True)
                    current_date += timedelta(days=1)
                    continue
        # try :
        if True:
            df = pd.DataFrame(columns=['media', 'waktu', 'isi isu', 'narasumber', 'sentiment', 'judul', 'link', 'reporter','full','keyword'])
            date_str = current_date.strftime("%m/%d/%Y")  # Format: MM/DD/YYYY untuk `cd_min` dan `cd_max`
            print('[INFO] mengambil berita tanggal '+date_str)
            # def wrap(text, char='"'):return char + text + char
            # q =  ' | '.join( wrap(x) for x in query)
            # print(q)
            for q in query:
                url = (
                    f'https://serpapi.com/search.json?engine=google&q={q}'
                    "&location=Indonesia&google_domain=google.co.id&gl=id&hl=id"
                    f"&tbs=cdr:1,cd_min:{date_str},cd_max:{date_str}&tbm=nws"
                    "&api_key=2a7541196951883a06ca6d92ac203f21571a303682cf95ee5adeda2935091f2d"
                )
                # print(url)
                # exit()
                # Lakukan request
                response = requests.get(url)
                js = response.json()
                news = js.get('news_results',[])

                for x in news:
                    if (filename in os.listdir(folderberita+'')):
                        dfx = pd.read_excel(folderberita+'/'+filename)
                        if x['link'] in dfx['link']:
                            dfx["keyword"] = dfx["full"].apply(lambda x: find_keywords(x, query))
                            dfx = dfx.loc[:, ~dfx.columns.str.contains('^Unnamed')]
                            dfx.to_excel(folderberita+'/'+filename)
                            df = pd.concat([result,dfx],ignore_index=True)
                            # current_date += timedelta(days=1)
                            continue
                    driver = webdriver.Chrome(options=options)
                    link : str= x['link']
                    title = x['title']
                    media = x.get('source',link.split('/')[2])
                    date = date_str

                    try:
                        print('[INFO] mengambil berita dari '+link)
                        driver.get(link)
                        # time.sleep(3)  # Tunggu render JS
                        WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.TAG_NAME, "p"))
                        )
                        page_html = driver.page_source
                        # beauti = bs4.BeautifulSoup(page_html, 'html.parser')
                        article = Article(link, language="id")
                        article.download(page_html)
                        article.parse()
                        beauti = article.text
                    except Exception as e:
                        print(f"[GAGAL] mengambil {link} dengan error: {e}")
                        beauti = ''

                    ex_news = ekstrak_berita(beauti) if beauti else None
                    # print(ex_news)
                    if ex_news:
                        try:
                            print('[INFO] extrak berita dari '+link)
                            narasumber = ','.join(ex_news['narasumber']) if isinstance(ex_news['narasumber'], list) else ex_news['narasumber'] or ''
                            sentimen = ex_news['sentiment'] if ex_news['sentiment'] else 'netral'
                            reporter = ex_news['reporter'] if ex_news['reporter'] else ''
                            # bukti = ex_news['bukti_sentiment']
                        except Exception as e:
                            print(f"[ERROR parsing ex_news] {e} => {ex_news}")
                            narasumber, sentimen, reporter  = '', 'netral', ''
                        if not ex_news.get('inti_berita'):
                            fullpage_screenshot(driver,media+".png")
                    else:
                        narasumber, sentimen, reporter  = '', 'netral', ''
                    
                    driver.quit()
                    df.loc[len(df)] = [media, date, ex_news['inti_berita'] if ex_news else '', narasumber, sentimen , title, link, reporter,beauti,find_keywords(beauti,query)]
                # print(df.loc[len(df)-1])
            # Lanjut ke hari berikutnya
            current_date += timedelta(days=1)
            result = pd.concat([result,df],ignore_index=True)
            df.to_excel(folderberita+'/'+filename,index=False)   
        # except Exception as e:
        #     print('[ERROR] '+str(e))
    return result
# os.makedirs(folderberita+'',exist_ok=True)
# main(start='08-01',end='08-14').to_excel('08_01-08_14.xlsx',index=False)