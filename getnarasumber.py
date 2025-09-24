import pandas as pd

# Load data
df = pd.read_excel("berita.xlsx")[["narasumber","full"]]

# Ubah NaN menjadi label "TidakAdaNarasumber"
df["narasumber"] = df["narasumber"].fillna("TidakAdaNarasumber")

# print(df["narasumber"].value_counts().head())
# print(len(df))
import spacy

# Load model bahasa Indonesia (misalnya id_core_news_sm kalau tersedia)
nlp = spacy.load("xx_ent_wiki_sm")  # multilingual NER

text = "oleh Tito Karnavian. menurut adi situasi saat ini aman terkendali."

doc = nlp(text)
df = df.dropna(subset=["full"])

# Kalau ada string kosong juga, buang
df = df[df["full"].str.strip() != ""]
# for ent in doc.ents:
#     if ent.label_ == "PER":  # PERSON
#         print("Narasumber ditemukan:", ent.text)
# Install transformers untuk menggunakan model NER Indonesia
# pip install transformers torch

# Load model directly
# Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("token-classification", model="cahya/bert-base-indonesian-NER")
# res = pipe("Kemarin Ahmad Rizki bertemu dengan Dr. Sari Wijaya di Jakarta.")
# for x in res:
#     print(x)
import stanza
stanza.download('id')
nlp = stanza.Pipeline(lang='id', processors='tokenize,ner')
teks_artikel = """
Presiden Joko Widodo, atau akrab disapa Jokowi, hari ini bertemu dengan Menteri Pertahanan Prabowo Subianto di Istana Negara. Mereka membahas beberapa isu penting. Selain itu, ada juga Menteri Keuangan Sri Mulyani yang hadir dalam pertemuan tersebut.
"""

doc = nlp(teks_artikel)

nama_orang = set()
for ent in doc.ents:
    if ent.type == 'PER':
        nama_orang.add(ent.text)

print("Nama orang yang ditemukan:")
for nama in sorted(nama_orang):
    print(nama)