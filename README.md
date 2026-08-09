# IndoBERT Sentiment Analysis — DANA App Reviews

Sentiment analysis project untuk mengklasifikasikan ulasan pengguna aplikasi DANA menggunakan **IndoBERT** yang di-fine-tune untuk 3 kelas sentimen: Negatif, Netral, dan Positif.

## Dataset

Dataset: **Review Aplikasi DANA**  
Source: https://www.kaggle.com/datasets/puteriameliaazli/review-aplikasi-dana

- Total data: ±740,000 reviews
- Periode: 2023–2026
- Kolom utama: `ulasan`, `rating`, `tanggal`, `versi_aplikasi`
- Format dataset: Parquet

Label sentimen dibuat berdasarkan rating:

| Rating | Sentimen |
|---|---|
| 1–2 | Negatif |
| 3 | Netral |
| 4–5 | Positif |

> Rating digunakan sebagai proxy label, bukan anotasi sentimen manual. Oleh karena itu, terdapat kemungkinan label noise.

## Workflow

```text
Dataset
   ↓
EDA
   ↓
Sentiment Labeling
   ↓
Text Preprocessing
   ↓
Train / Validation / Test Split
   ↓
IndoBERT Tokenization
   ↓
Fine-tuning
   ↓
Model Evaluation
   ↓
Error Analysis
```

## Data Preparation

Dataset dibagi menggunakan stratified split:

- Train: 592,000 (80%)
- Validation: 74,000 (10%)
- Test: 74,000 (10%)

Analisis panjang token menghasilkan:

- 95th percentile: 35 tokens
- 99th percentile: 65 tokens
- `MAX_LENGTH`: 64

## Model

Model yang digunakan:

```text
indobenchmark/indobert-base-p1
```

Konfigurasi utama:

| Parameter | Value |
|---|---:|
| Classes | 3 |
| Max Length | 64 |
| Batch Size | 16 |
| Gradient Accumulation | 2 |
| Learning Rate | 2e-5 |
| Epochs | 3 |
| Weight Decay | 0.01 |
| Precision | FP16 |

Training dilakukan menggunakan **Kaggle Notebook dengan 2× NVIDIA Tesla T4 GPU**.

## Results

### Validation

Model memperoleh performa terbaik pada Epoch 2:

| Metric | Score |
|---|---:|
| Accuracy | 88.59% |
| Precision | 86.86% |
| Recall | 88.59% |
| F1-score | 86.65% |

### Test Set

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Negatif | 79.38% | 86.53% | 82.80% |
| Netral | 43.06% | 0.90% | 1.76% |
| Positif | 92.09% | 95.14% | 93.59% |
| **Weighted Avg** | **86.66%** | **88.61%** | **86.64%** |

**Test Accuracy: 88.61%**  
**Weighted F1-score: 86.64%**

Model memiliki performa kuat pada sentimen Positif dan Negatif, sementara kelas Netral masih menjadi tantangan karena ketidakseimbangan kelas dan penggunaan rating sebagai proxy label.

## Visualization

Visualisasi yang digunakan:

- Rating distribution
- Training vs Validation Loss
- Validation metrics
- Confusion Matrix
- Sentiment distribution
- Sentiment by rating
- Sentiment trend by year

## Tech Stack

- Python
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- IndoBERT
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Kaggle GPU

## Project Structure

```text
indobert-dana-sentiment/
│
├── README.md
├── requirements.txt
├── notebooks/
│   └── indobert_dana_sentiment.ipynb
│
├── results/
│   ├── confusion_matrix.png
│   ├── training_validation_loss.png
│   └── classification_report.csv
│
└── src/
    └── inference.py
```

## Limitations

- Sentiment labels berasal dari rating, bukan anotasi manual.
- Dataset memiliki class imbalance yang cukup tinggi.
- Performa kelas Netral masih rendah.
- Review pengguna mengandung bahasa informal, slang, dan typo.

## Future Improvements

- Manual sentiment annotation
- Class weighting
- Hyperparameter tuning
- Topic modeling untuk review negatif
- Aspect-based sentiment analysis
Interested in Data Science, Machine Learning, NLP, and Artificial Intelligence.
