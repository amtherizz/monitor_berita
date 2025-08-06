import json,requests,bs4
import dateparser,csv
import pandas as pd
import uuid
import json,re
import requests  # masih bisa dipakai untuk fallback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import dateparser
import threading
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
options.add_argument('--log-level=3')
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.video": 2,
    "profile.managed_default_content_settings.audio": 2
}
options.add_experimental_option("prefs", prefs)

system_prompt = """
        Anda adalah asisten yang ahli dalam mengekstraksi informasi penting dari berita. Tugas Anda adalah mengidentifikasi paragraf-paragraf inti, sumber media, narasumber (jika ada), reporter (jika ada), sentimen terhadap Badan Informasi Geospasial (BIG) beserta buktinya, dan juga menyajikan teks berita lengkap yang sudah bersih dari elemen non-berita.

        **Instruksi Detail:**
        1.  **inti_berita**: Ekstrak paragraf-paragraf utama yang paling relevan dan padat informasi. Pastikan ini adalah ringkasan yang komprehensif dari isi berita. Jangan hanya mengambil paragraf pertama atau terakhir, tetapi cari esensi beritanya.
        2.  **sumber_media**: Identifikasi nama media yang memublikasikan berita ini.
        3.  **narasumber**: Cari nama-nama orang yang dikutip atau diwawancarai dalam berita. Jika tidak ada, biarkan kosong.
        4.  **reporter**: Cari nama penulis atau reporter berita. Jika tidak ada, biarkan kosong.
        5.  **sentiment**: Analisis sentimen berita **khususnya terhadap Badan Informasi Geospasial (BIG)**. Pertimbangkan bagaimana peran, tindakan, atau dampak BIG digambarkan dalam berita secara objektif. Berikan nilai 'positif', 'netral', atau 'negatif'. **Jangan berasumsi sentimen selalu positif hanya karena BIG adalah lembaga pemerintah atau karena ada komitmen positif secara umum. Fokus pada *peran BIG* dalam narasi berita.**
        6.  **bukti_sentiment**: Ekstrak **satu atau beberapa kalimat langsung dari berita yang paling jelas dan *objektif* menunjukkan atau mendukung sentimen yang Anda berikan untuk Badan Informasi Geospasial (BIG)**. Kalimat ini harus secara eksplisit menyebutkan atau merujuk pada BIG dan secara konkret menunjukkan nuansa positif dan negatif terkait peran atau kontribusi BIG dalam konteks berita tersebut. Jika sentimennya 'netral', kosongkan saja.

        **Format Output (HARUS JSON):**
        ```json
        {
          "inti_berita": "...",
          "sumber_media": "...",
          "narasumber": null,
          "reporter": null,
          "sentiment": "positif/netral/negatif",
          "bukti_sentiment":"..."
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
        'User-Agent': 'Ktor client',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Charset': 'UTF-8',
    }

    files = {
        'data': (None, json.dumps({
            "id": str(uuid.uuid4()),
            "model": "vgpt-g2-4",
            "messages": [
                {
                    "content": system_prompt,
                    "id": idsys,
                    "role": "system",
                    "model": "vgpt-g2-4"
                },
                {
                    "content": news,
                    "id": idusr,
                    "role": "user",
                    "model": "vgpt-g2-4"
                }
            ]
        })),
    }

    response = requests.post(
        'https://streaming.vyro.ai/v1/chatly/android/chat/completions',
        headers=headers,
        files=files,
        stream=True
    )

    output = ""
    # print(response.content)
    for line in response.iter_lines(decode_unicode=True):
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
    except:print(output)

def main(start="08-01",end="08-04"):
    global should_stop
    from datetime import datetime, timedelta
    filename = start+'--'+end+'.xlsx'
    # print('success')

    start_date = datetime.strptime("2025-"+start, "%Y-%m-%d")
    end_date = datetime.strptime("2025-"+end, "%Y-%m-%d")
    df = pd.DataFrame(columns=['media', 'waktu', 'isi isu', 'narasumber', 'sentiment', 'bukti_sentiment', 'judul', 'link', 'reporter'])
    # Loop per tanggal
    print('[INFO] tanggal awal '+start_date.strftime("%Y/%m/%d"))
    print('[INFO] tanggal akhir '+end_date.strftime("%Y/%m/%d"))
    # return filename
    current_date = start_date
    while current_date <= end_date:
        try :
            date_str = current_date.strftime("%m/%d/%Y")  # Format: MM/DD/YYYY untuk `cd_min` dan `cd_max`
            print('[INFO] mengambil berita tanggal '+date_str)
            url = (
                "https://serpapi.com/search.json?engine=google&q=badan informasi geospasial"
                "&location=Indonesia&google_domain=google.co.id&gl=id&hl=id"
                f"&tbs=cdr:1,cd_min:{date_str},cd_max:{date_str}&tbm=nws"
                "&api_key=2a7541196951883a06ca6d92ac203f21571a303682cf95ee5adeda2935091f2d"
            )

            # Lakukan request
            response = requests.get(url)
            js = response.json()
            news = js.get('news_results',[])
            for x in news:
                driver = webdriver.Chrome(options=options)
                link = x['link']
                title = x['title']
                media = x['source']
                date = date_str

                try:
                    print('[INFO] mengambil berita dari '+link)
                    driver.get(link)
                    time.sleep(3)  # Tunggu render JS
                    page_html = driver.page_source
                    beauti = bs4.BeautifulSoup(page_html, 'html.parser')
                    beauti = beauti.text
                except Exception as e:
                    print(f"[GAGAL] mengambil {link} dengan error: {e}")
                    beauti = ''

                ex_news = ekstrak_berita(beauti) if beauti else None

                if ex_news:
                    try:
                        print('[INFO] extrak berita dari '+link)
                        narasumber = ','.join(ex_news['narasumber']) if isinstance(ex_news['narasumber'], list) else ex_news['narasumber'] or ''
                        sentimen = ex_news['sentiment'] if ex_news['sentiment'] else 'netral'
                        reporter = ex_news['reporter'] if ex_news['reporter'] else ''
                        bukti = ex_news['bukti_sentiment']
                    except Exception as e:
                        print(f"[ERROR parsing ex_news] {e} => {ex_news}")
                        narasumber, sentimen, reporter, bukti = '', 'netral', '', ''
                else:
                    narasumber, sentimen, reporter, bukti = '', 'netral', '', ''
                driver.quit()
                df.loc[len(df)] = [media, date, ex_news['inti_berita'] if ex_news else '', narasumber, sentimen, bukti , title, link, reporter]
                print(df.loc[len(df)-1])
            # Lanjut ke hari berikutnya
            current_date += timedelta(days=1)
        except Exception as e:
            print('[ERROR] '+str(e))
    df.to_excel(filename)
    return filename
main()