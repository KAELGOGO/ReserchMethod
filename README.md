# ReserchMethod
# IndoFinBERT-BiLSTM for Stock Volatility Prediction

This repository contains the source code, datasets, and models for our research on predicting Indonesian stock market volatility (BBCA, ANTM, BRPT) using a hybrid Deep Learning architecture.

## 📝 Abstract
Stock price volatility in the Indonesian market presents a significant challenge for investors and financial analysts. This study proposes a hybrid Deep Learning framework, IndoFinBERT-BiLSTM, designed to quantify market sentiment from over 202,348 Indonesian financial news articles. We fine-tuned the IndoBERT model on a curated dataset of 3,300 expert-labeled entries to develop IndoFinBERT. These sentiment scores were subsequently fused with historical trading data and processed through a Bidirectional Long Short-Term Memory (BiLSTM) network.

## 🗂️ Dataset
Due to GitHub's file size limits, the full raw dataset (>200,000 articles) and the pre-trained IndoFinBERT model are hosted externally.
* **Gold Standard Dataset (3,300 rows):** Available in the `data/` folder of this repository.
* **Full Raw Dataset:** [Insert Google Drive/Kaggle Link Here]
* **Fine-tuned IndoFinBERT Model:** [Insert HuggingFace/Drive Link Here]

## 🚀 Repository Structure
* `/data`: Contains the curated and labeled datasets.
* `/notebooks`: Jupyter notebooks for model training (IndoFinBERT fine-tuning and BiLSTM).
* `/src`: Python scripts used for automated web scraping (Bisnis.com & CNBC Indonesia).

## 🛠️ Tech Stack
* **Scraping:** `undetected_chromedriver`, `BeautifulSoup4`
* **NLP Model:** `HuggingFace Transformers`, `PyTorch` (IndoBERT Base)
* **Time-Series Model:** `TensorFlow` / `Keras` (BiLSTM)
* **Data Processing:** `Pandas`, `Scikit-Learn` (MinMaxScaler)

## 👥 Authors
* **Kelvin Leandi** - Research Design, Data Engineering, Expert Labeling.
* **Michael Owen Muliawan** - Deep Learning Architecture, Model Fine-Tuning.

School of Computer Science, BINUS University (2026).
