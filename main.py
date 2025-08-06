from flask import Flask, render_template,request
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly
import scrapt
import json,re,os
from wordcloud import WordCloud
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


@app.route('/')
def index():
    start = request.args.get('start') or (datetime.now() - timedelta(days=7)).strftime('%m-%d')
    end = request.args.get('end') or datetime.now().strftime('%m-%d')
    df = scrapt.main(start,end)
    # df = pd.read_excel('/home/user/app/output/server/data/17-31juli.xlsx')

    # Pie chart sentimen
    # Warna yang cocok untuk sentimen
    warna_sentimen = {
        'positif': '#90ee90',  # hijau muda
        'negatif': '#ff0000',  # merah
        'netral': '#add8e6'    # biru muda
    }

    # Pie chart sentimen
    fig_sentimen = px.pie(
        df,
        names='sentiment',
        title='Distribusi Sentimen',
        color='sentiment',
        color_discrete_map=warna_sentimen
    )
    # Bar chart media
    media_counts = df['media'].value_counts().reset_index()
    media_counts.columns = ['media', 'count']
    fig_media = px.bar(media_counts, 
                   x='media', y='count', 
                   labels={'media': 'Media', 'count': 'Jumlah'},
                   title='Jumlah Berita per Media')
    # waktu
    df['waktu'] = pd.to_datetime(df['waktu'], errors='coerce')
    df_time = df.groupby(df['waktu'].dt.date).size().reset_index(name='jumlah')
    fig_waktu = px.line(df_time, x='waktu', y='jumlah', title='Jumlah Berita per Hari')
    positif_text = ' '.join(df[df['sentiment'] == 'positif']['bukti_sentiment'].dropna().astype(str))
    positif_text = bersihkan_kalimat(positif_text)
    wcp = False
    if positif_text:
        wc_positif = WordCloud(width=800, height=400, background_color='white').generate(positif_text)
        wc_positif.to_file('static/wordcloud_positif.png')
        wcp = True

    # WordCloud Negatif
    negatif_text = ' '.join(df[df['sentiment'] == 'negatif']['bukti_sentiment'].dropna().astype(str))
    negatif_text = bersihkan_kalimat(negatif_text)
    wcn = False
    if negatif_text:
        wc_negatif = WordCloud(width=800, height=400, background_color='white').generate(negatif_text)
        wc_negatif.to_file('static/wordcloud_negatif.png')
        wcn = True

    # sentimen bar

    sentimen_count = df['sentiment'].value_counts().reset_index()
    sentimen_count.columns = ['sentiment', 'count']
    sentimen_count['count'] = sentimen_count['count'].astype(int)

    fig_bar_sentimen = px.bar(
        sentimen_count,
        x='sentiment',
        y='count',
        text=sentimen_count['count'].tolist(),  # FIXED: gunakan list
        color='sentiment',
        color_discrete_map=warna_sentimen,
        title='Jumlah Berita per Sentimen'
    )
    fig_bar_sentimen.update_traces(textposition='outside')
    fig_bar_sentimen.update_layout(yaxis_range=[0, sentimen_count['count'].max() + 5])
    return render_template('index.html', 
                           tables=[df.to_html(classes='table table-striped', index=False)],
                           wc_p=wcp,
                           wc_n=wcn,
                           graph_sentimen=fig_sentimen.to_html(full_html=False),
                           graph_media=fig_media.to_html(full_html=False,include_plotlyjs=False),
                           graph_waktu=fig_waktu.to_html(full_html=False,include_plotlyjs=False),
                           graph_sentimenbar=fig_bar_sentimen.to_html(full_html=False,include_plotlyjs=False))

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
