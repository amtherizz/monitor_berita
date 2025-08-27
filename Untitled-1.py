import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# =======================================
# 1. Dataset contoh (artikel berita panjang)
# =======================================
data = pd.read_excel(r"C:\Users\idris\Downloads\berita(3).xlsx")
# Mapping label ke angka
label2id = {"negatif": -1, "positif": 1,'netral':0}
data["sentiment"] = [label2id[x] for x in data["sentiment"]]
data['full'] = data['full'].astype(str)
# Convert ke HuggingFace Dataset
dataset = Dataset.from_pandas(data)

# =======================================
# 2. Tokenisasi IndoBERT
# =======================================
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p1")

def tokenize(batch):
    return tokenizer(batch["full"], padding="max_length", truncation=True, max_length=1000)

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.train_test_split(test_size=0.2)

# =======================================
# 3. Load Model IndoBERT
# =======================================
model = BertForSequenceClassification.from_pretrained(
    "indobenchmark/indobert-base-p1",
    num_labels=2
)

# =======================================
# 4. Training
# =======================================
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()

# =======================================
# 5. Evaluasi & Prediksi
# =======================================
preds = trainer.predict(dataset["test"])
print(preds.predictions.argmax(axis=1))  # hasil prediksi label

# Uji dengan artikel baru
test_text = ["BIG meningkatkan kualitas layanan peta digital nasional",
             "Banyak masalah dalam proyek BIG terbaru"]

tokens = tokenizer(test_text, padding=True, truncation=True, max_length=256, return_tensors="pt")
outputs = model(**tokens)
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

for i, text in enumerate(test_text):
    label = "Positif" if predictions[i][1] > predictions[i][0] else "Negatif"
    print(text, "=>", label)
