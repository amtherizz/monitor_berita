from flask import Flask, render_template,request,send_file,jsonify
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scrapt,io
import json,re,os
from collections import Counter
stopwords = set(['a','ada','adalah','adanya','adapun','agak','agaknya','agar','akan','akankah','akhir','akhiri','akhirnya','aku','akulah','amat','amatlah','anda','andalah','antar','antara','antaranya','apa','apaan','apabila','apakah','apalagi','apatah','arti','artinya','asal','asalkan','atas','atau','ataukah','ataupun','awal','awalnya','b','bagai','bagaikan','bagaimana','bagaimanakah','bagaimanapun','bagainamakah','bagi','bagian','bahkan','bahwa','bahwasannya','bahwasanya','baik','baiklah','bakal','bakalan','balik','banyak','bapak','baru','bawah','beberapa','begini','beginian','beginikah','beginilah','begitu','begitukah','begitulah','begitupun','bekerja','belakang','belakangan','belum','belumlah','benar','benarkah','benarlah','berada','berakhir','berakhirlah','berakhirnya','berapa','berapakah','berapalah','berapapun','berarti','berawal','berbagai','berdatangan','beri','berikan','berikut','berikutnya','berjumlah','berkali-kali','berkata','berkehendak','berkeinginan','berkenaan','berlainan','berlalu','berlangsung','berlebihan','bermacam','bermacam-macam','bermaksud','bermula','bersama','bersama-sama','bersiap','bersiap-siap','bertanya','bertanya-tanya','berturut','berturut-turut','bertutur','berujar','berupa','besar','betul','betulkah','biasa','biasanya','bila','bilakah','bisa','bisakah','boleh','bolehkah','bolehlah','buat','bukan','bukankah','bukanlah','bukannya','bulan','bung','c','cara','caranya','cukup','cukupkah','cukuplah','cuma','d','dahulu','dalam','dan','dapat','dari','daripada','datang','dekat','demi','demikian','demikianlah','dengan','depan','di','dia','diakhiri','diakhirinya','dialah','diantara','diantaranya','diberi','diberikan','diberikannya','dibuat','dibuatnya','didapat','didatangkan','digunakan','diibaratkan','diibaratkannya','diingat','diingatkan','diinginkan','dijawab','dijelaskan','dijelaskannya','dikarenakan','dikatakan','dikatakannya','dikerjakan','diketahui','diketahuinya','dikira','dilakukan','dilalui','dilihat','dimaksud','dimaksudkan','dimaksudkannya','dimaksudnya','diminta','dimintai','dimisalkan','dimulai','dimulailah','dimulainya','dimungkinkan','dini','dipastikan','diperbuat','diperbuatnya','dipergunakan','diperkirakan','diperlihatkan','diperlukan','diperlukannya','dipersoalkan','dipertanyakan','dipunyai','diri','dirinya','disampaikan','disebut','disebutkan','disebutkannya','disini','disinilah','ditambahkan','ditandaskan','ditanya','ditanyai','ditanyakan','ditegaskan','ditujukan','ditunjuk','ditunjuki','ditunjukkan','ditunjukkannya','ditunjuknya','dituturkan','dituturkannya','diucapkan','diucapkannya','diungkapkan','dong','dua','dulu','e','empat','enak','enggak','enggaknya','entah','entahlah','f','g','guna','gunakan','h','hadap','hai','hal','halo','hallo','hampir','hanya','hanyalah','hari','harus','haruslah','harusnya','helo','hello','hendak','hendaklah','hendaknya','hingga','i','ia','ialah','ibarat','ibaratkan','ibaratnya','ibu','ikut','ingat','ingat-ingat','ingin','inginkah','inginkan','ini','inikah','inilah','itu','itukah','itulah','j','jadi','jadilah','jadinya','jangan','jangankan','janganlah','jauh','jawab','jawaban','jawabnya','jelas','jelaskan','jelaslah','jelasnya','jika','jikalau','juga','jumlah','jumlahnya','justru','k','kadar','kala','kalau','kalaulah','kalaupun','kali','kalian','kami','kamilah','kamu','kamulah','kan','kapan','kapankah','kapanpun','karena','karenanya','kasus','kata','katakan','katakanlah','katanya','ke','keadaan','kebetulan','kecil','kedua','keduanya','keinginan','kelamaan','kelihatan','kelihatannya','kelima','keluar','kembali','kemudian','kemungkinan','kemungkinannya','kena','kenapa','kepada','kepadanya','kerja','kesampaian','keseluruhan','keseluruhannya','keterlaluan','ketika','khusus','khususnya','kini','kinilah','kira','kira-kira','kiranya','kita','kitalah','kok','kurang','l','lagi','lagian','lah','lain','lainnya','laku','lalu','lama','lamanya','langsung','lanjut','lanjutnya','lebih','lewat','lihat','lima','luar','m','macam','maka','makanya','makin','maksud','malah','malahan','mampu','mampukah','mana','manakala','manalagi','masa','masalah','masalahnya','masih','masihkah','masing','masing-masing','masuk','mata','mau','maupun','melainkan','melakukan','melalui','melihat','melihatnya','memang','memastikan','memberi','memberikan','membuat','memerlukan','memihak','meminta','memintakan','memisalkan','memperbuat','mempergunakan','memperkirakan','memperlihatkan','mempersiapkan','mempersoalkan','mempertanyakan','mempunyai','memulai','memungkinkan','menaiki','menambahkan','menandaskan','menanti','menanti-nanti','menantikan','menanya','menanyai','menanyakan','mendapat','mendapatkan','mendatang','mendatangi','mendatangkan','menegaskan','mengakhiri','mengapa','mengatakan','mengatakannya','mengenai','mengerjakan','mengetahui','menggunakan','menghendaki','mengibaratkan','mengibaratkannya','mengingat','mengingatkan','menginginkan','mengira','mengucapkan','mengucapkannya','mengungkapkan','menjadi','menjawab','menjelaskan','menuju','menunjuk','menunjuki','menunjukkan','menunjuknya','menurut','menuturkan','menyampaikan','menyangkut','menyatakan','menyebutkan','menyeluruh','menyiapkan','merasa','mereka','merekalah','merupakan','meski','meskipun','meyakini','meyakinkan','minta','mirip','misal','misalkan','misalnya','mohon','mula','mulai','mulailah','mulanya','mungkin','mungkinkah','n','nah','naik','namun','nanti','nantinya','nya','nyaris','nyata','nyatanya','o','oleh','olehnya','orang','p','pada','padahal','padanya','pak','paling','panjang','pantas','para','pasti','pastilah','penting','pentingnya','per','percuma','perlu','perlukah','perlunya','pernah','persoalan','pertama','pertama-tama','pertanyaan','pertanyakan','pihak','pihaknya','pukul','pula','pun','punya','q','r','rasa','rasanya','rupa','rupanya','s','saat','saatnya','saja','sajalah','salam','saling','sama','sama-sama','sambil','sampai','sampai-sampai','sampaikan','sana','sangat','sangatlah','sangkut','satu','saya','sayalah','se','sebab','sebabnya','sebagai','sebagaimana','sebagainya','sebagian','sebaik','sebaik-baiknya','sebaiknya','sebaliknya','sebanyak','sebegini','sebegitu','sebelum','sebelumnya','sebenarnya','seberapa','sebesar','sebetulnya','sebisanya','sebuah','sebut','sebutlah','sebutnya','secara','secukupnya','sedang','sedangkan','sedemikian','sedikit','sedikitnya','seenaknya','segala','segalanya','segera','seharusnya','sehingga','seingat','sejak','sejauh','sejenak','sejumlah','sekadar','sekadarnya','sekali','sekali-kali','sekalian','sekaligus','sekalipun','sekarang','sekaranglah','sekecil','seketika','sekiranya','sekitar','sekitarnya','sekurang-kurangnya','sekurangnya','sela','selain','selaku','selalu','selama','selama-lamanya','selamanya','selanjutnya','seluruh','seluruhnya','semacam','semakin','semampu','semampunya','semasa','semasih','semata','semata-mata','semaunya','sementara','semisal','semisalnya','sempat','semua','semuanya','semula','sendiri','sendirian','sendirinya','seolah','seolah-olah','seorang','sepanjang','sepantasnya','sepantasnyalah','seperlunya','seperti','sepertinya','sepihak','sering','seringnya','serta','serupa','sesaat','sesama','sesampai','sesegera','sesekali','seseorang','sesuatu','sesuatunya','sesudah','sesudahnya','setelah','setempat','setengah','seterusnya','setiap','setiba','setibanya','setidak-tidaknya','setidaknya','setinggi','seusai','sewaktu','siap','siapa','siapakah','siapapun','sini','sinilah','soal','soalnya','suatu','sudah','sudahkah','sudahlah','supaya','t','tadi','tadinya','tahu','tak','tambah','tambahnya','tampak','tampaknya','tandas','tandasnya','tanpa','tanya','tanyakan','tanyanya','tapi','tegas','tegasnya','telah','tempat','tentang','tentu','tentulah','tentunya','tepat','terakhir','terasa','terbanyak','terdahulu','terdapat','terdiri','terhadap','terhadapnya','teringat','teringat-ingat','terjadi','terjadilah','terjadinya','terkira','terlalu','terlebih','terlihat','termasuk','ternyata','tersampaikan','tersebut','tersebutlah','tertentu','tertuju','terus','terutama','tetap','tetapi','tiap','tiba','tiba-tiba','tidak','tidakkah','tidaklah','tiga','toh','tuju','tunjuk','turut','tutur','tuturnya','u','ucap','ucapnya','ujar','ujarnya','umumnya','ungkap','ungkapnya','untuk','usah','usai','v','w','waduh','wah','wahai','waktunya','walau','walaupun','wong','x','y','ya','yaitu','yakin','yakni','yang','z'])
stopwords.update(['lebih','menjadi','terus','badan','geospasial','big','informasi','depan','dasar','merupakan','hingga','penting','termasuk','hari','sehari','minggu','tahun','bukan','sangat','semoga','bukan','bentuk'])
app = Flask(__name__)
def bersihkan_kalimat(teks):
    teks = re.sub(r'[^a-zA-Z\s]', ' ', teks)
    kata2 = teks.lower().split()
    hasil = [
        kata for kata in kata2
        if kata not in stopwords
    ]
    return ' '.join(hasil)
def hapus_duplikat(kalimat):
    kata_kata = kalimat.split()
    hasil = []
    for kata in kata_kata:
        if kata not in hasil:
            hasil.append(kata)
    return " ".join(hasil)
# enpoin download file 
@app.route('/download')
def download():
    start = request.args.get('start') or (datetime.now() - timedelta(days=7)).strftime('%m-%d')
    end = request.args.get('end') or datetime.now().strftime('%m-%d') 
    df = scrapt.main(start,end,dw=True)
    output = io.BytesIO()
    df.to_excel(output)
    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name="berita.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def load_keywords():
    try:
        with open("keywords.json","r") as f:
            return json.load(f)
    except:
        return []

def save_keywords(kws):
    with open("keywords.json","w") as f:
        json.dump(kws, f)
# enpoin admin
@app.route('/admin', methods=['GET','POST'])
def admin():
    act = request.args.get("act")
    if act == "update_kw":
        data = request.get_json()
        save_keywords(list(set(data.get("keywords", [])+["badan informasi geospasial"])))
        return jsonify({"keywords": load_keywords()})
    return render_template("admin.html", keywords=load_keywords())

# encpoin scrapt
@app.route('/scrapt')
def scrapt_news():
    start = request.args.get('start') or (datetime.now() - timedelta(days=7)).strftime('%m-%d')
    end = request.args.get('end') or datetime.now().strftime('%m-%d')
    df = scrapt.main(start,end,query=load_keywords(),force=True)
    return jsonify({
        "status":"ok",
        "jumlah":len(df)
    })
# enpoin utama
@app.route('/')
def index():
    query = request.args.getlist("query")
    if not query:
        query = ["badan informasi geospasial"]
    start = request.args.get('start') or (datetime.now() - timedelta(days=7)).strftime('%m-%d')
    end = request.args.get('end') or datetime.now().strftime('%m-%d')
    df = scrapt.main(start,end,dw=True,query=query)
    df = df[df['full'].str.contains("|".join(query), case=False, na=False)]
    
    if df.empty:
        return {
            "error":"data kosong"
        }
    
    # Pie chart sentimen
    warna_sentimen = {
        'positif': '#90ee90', 
        'negatif': '#ff0000', 
        'netral': '#add8e6' 
    }
    
    fig_sentimen = px.pie(
        df,
        names='sentiment',
        title='Distribusi Sentimen',
        color='sentiment',
        color_discrete_map=warna_sentimen
    )
    
    # Bar chart media
    # Bar chart media
    media_counts = df['media'].value_counts().reset_index()
    media_counts.columns = ['media', 'count']
    fig_media = px.bar(media_counts, 
                    x='media', y='count', 
                    labels={'media': 'Media', 'count': 'Jumlah'},
                    title='Jumlah Berita per Media')

    # --- Logika Kelipatan Dinamis ---
    max_count = media_counts['count'].max() if not media_counts.empty else 0
    y_range = max(10, max_count) if max_count else 10

    if max_count <= 5:
        tick_interval = 1
        y_range = 5 # Menetapkan rentang y maksimal 5 jika datanya sedikit
    elif max_count > 5 and max_count <= 10:
        tick_interval = 2
        y_range = 10
    else:
        tick_interval = 5
        y_range = max_count + (5 - (max_count % 5)) # Membulatkan ke kelipatan 5 terdekat

    fig_media.update_yaxes(
        range=[0, y_range],
        dtick=tick_interval
    )

    fig_media.update_layout(
        xaxis_tickangle=-45,
        yaxis_title_text="Jumlah"
    )

# --- Akhir Logika Dinamis ---
    
    # waktu
# waktu
    df['waktu'] = pd.to_datetime(df['waktu'], errors='coerce')
    df_time = df.groupby(df['waktu'].dt.date).size().reset_index(name='jumlah')
    fig_waktu = px.line(df_time, x='waktu', y='jumlah', title='Jumlah Berita per Hari')

    # Logika Kelipatan Dinamis untuk Sumbu Y
    max_jumlah = df_time['jumlah'].max() if not df_time.empty else 0

    if max_jumlah <= 5:
        tick_interval = 1
    elif max_jumlah > 5 and max_jumlah <= 10:
        tick_interval = 2
    else:
        tick_interval = 5
    
    fig_waktu.update_yaxes(
        dtick=tick_interval,
        title_text="Jumlah",
        range=[0, max_jumlah + 1]
    )

    # Pemrosesan data untuk WordCloud Positif
    positif_text = ' '.join([hapus_duplikat(x) for x in df[df['sentiment'] == 'positif']['isi isu'] if x])
    positif_text = bersihkan_kalimat(positif_text)
    common_words_pos = Counter(re.findall(r'\b[a-zA-Z]{2,}\b', positif_text)).most_common(20)
    df_kata_pos = pd.DataFrame(common_words_pos, columns=['kata', 'jumlah'])
    
    # Pemrosesan data untuk WordCloud Negatif
    negatif_text = ' '.join([hapus_duplikat(x) for x in df[df['sentiment'] == 'negatif']['isi isu'] if x])
    negatif_text = bersihkan_kalimat(negatif_text)
    common_words_neg = Counter(re.findall(r'\b[a-zA-Z]{2,}\b', negatif_text)).most_common(20)
    df_kata_neg = pd.DataFrame(common_words_neg, columns=['kata', 'jumlah'])
    
    # Filter kata negatif, hanya tampilkan yang jumlahnya > 2
    df_kata_neg = df_kata_neg[df_kata_neg['jumlah'] > 2]

    # --- Bagian yang Direvisi ---
    
    wcn = None
    # Periksa jika salah satu DataFrame tidak kosong
    if not df_kata_pos.empty or not df_kata_neg.empty:
        
        # Tentukan jumlah baris yang diperlukan
        num_rows = 0
        subplot_titles = []
        
        if not df_kata_pos.empty:
            num_rows += 1
            subplot_titles.append('20 Kata Paling Sering Muncul dalam sentimen positif')
        
        if not df_kata_neg.empty:
            num_rows += 1
            subplot_titles.append('20 Kata Paling Sering Muncul dalam sentiment negatif')

        # Buat subplots dengan jumlah baris yang dinamis
        fig_gabungan = make_subplots(
            rows=num_rows, 
            cols=1, 
            subplot_titles=subplot_titles
        )

        row_index = 1
        # Tambahkan grafik positif
        if not df_kata_pos.empty:
            fig_gabungan.add_trace(
                go.Bar(
                    x=df_kata_pos['jumlah'],
                    y=df_kata_pos['kata'],
                    orientation='h',
                    name='Positif'
                ),
                row=row_index, col=1
            )
            row_index += 1
        
        # Tambahkan grafik negatif
        if not df_kata_neg.empty:
            fig_gabungan.add_trace(
                go.Bar(
                    x=df_kata_neg['jumlah'],
                    y=df_kata_neg['kata'],
                    orientation='h',
                    name='Negatif'
                ),
                row=row_index, col=1
            )
        
        # Menemukan rentang maksimal
        max_x = 0
        if not df_kata_pos.empty:
            max_x = max(max_x, df_kata_pos['jumlah'].max())
        if not df_kata_neg.empty:
            max_x = max(max_x, df_kata_neg['jumlah'].max())
        
        # Perbarui sumbu untuk setiap subplot
        for i in range(1, num_rows + 1):
            fig_gabungan.update_xaxes(title_text="Frekuensi", row=i, col=1, range=[0, max_x + 1])
            fig_gabungan.update_yaxes(title_text="Kata", row=i, col=1)

        # Mengatur tinggi figur berdasarkan jumlah plot
        fig_height = 400 if num_rows == 1 else 700
        fig_gabungan.update_layout(height=fig_height, showlegend=False)

        wcn = fig_gabungan.to_html(full_html=False)
    
    # --- Akhir dari Bagian yang Direvisi ---

    sentimen_count = df['sentiment'].value_counts().reset_index()
    sentimen_count.columns = ['sentiment', 'count']
    sentimen_count['count'] = sentimen_count['count'].astype(int)

    fig_bar_sentimen = px.bar(
        sentimen_count,
        x='sentiment',
        y='count',
        text=sentimen_count['count'].tolist(),
        color='sentiment',
        color_discrete_map=warna_sentimen,
        title='Jumlah Berita per Sentimen'
    )
    fig_bar_sentimen.update_traces(textposition='outside')
    fig_bar_sentimen.update_layout(yaxis_range=[0, sentimen_count['count'].max() + 5])
    df['full'] = df['full'].apply(lambda x : x[:100])
    return render_template('index.html', 
                            tables=[df.to_html(classes='table table-striped', index=False,table_id="myTable")],
                            wc_n=wcn,
                            keywords=load_keywords(),
                            keywords_=query,
                            graph_sentimen=fig_sentimen.to_html(full_html=False),
                            graph_media=fig_media.to_html(full_html=False, include_plotlyjs=False),
                            graph_waktu=fig_waktu.to_html(full_html=False, include_plotlyjs=False),
                            graph_sentimenbar=fig_bar_sentimen.to_html(full_html=False, include_plotlyjs=False))
# enpoin edit file
@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    filename = data.get("filename")
    edits = data.get("write", [])

    df = pd.read_excel("data2/"+filename,index_col=False)

    for x in edits:
        row_index = int(x["wow"])
        col_name = x["col"]
        new_value = x["val"]

        if col_name in df.columns and 0 <= row_index < len(df):
            df.at[row_index, col_name] = new_value
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_excel("data2/"+filename, index=False)
    return jsonify({"status": "ok", "msg": "Data berhasil diupdate"})
# melihat list file di folder data2
@app.route("/list_files")
def list_files():
    files = [f for f in os.listdir('data2') if f.endswith(".xlsx")]
    return jsonify(files)

#  membuka file sesuai nama dari filename
@app.route("/get_file")
def get_file():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"status":"error","msg":"No filename"}),400
    df = pd.read_excel("data2/"+filename)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df.to_json(orient="records")

if __name__ == '__main__':
    os.makedirs('data2', exist_ok=True)
    app.run(host='0.0.0.0',debug=True)
