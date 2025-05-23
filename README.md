# 🧠 Natural Language Processing Coursework - Reddit Israel-Gaza Analysis

This repository contains the complete solution for the **PUSL3189 - Natural Language Processing** coursework. The project involves applying core NLP techniques on a dataset scraped from Reddit using the PRAW (Python Reddit API Wrapper), focusing on discussions around the **Israel-Gaza conflict**.

## 📌 Overview

The goal of this coursework is to demonstrate proficiency in text mining, sentiment analysis, topic modeling, and other NLP techniques using Python libraries such as NLTK, SpaCy, Scikit-learn, and Gensim.

## 📂 Contents

- `notebook.ipynb` – Jupyter Notebook with all tasks implemented, code, outputs, and explanations.
- `report.pdf` – A summarized report of each task, methodology, and analysis.
- `data/` – Contains the scraped Reddit dataset on the Israel-Gaza topic.
- `README.md` – Project documentation and description.

## 🚀 Project Tasks

### 1. **Data Collection**
- Scraped Reddit posts using PRAW.
- Focused on subreddits related to current affairs, news, and politics.

### 2. **Text Preprocessing**
- Performed stop word removal, lemmatization, punctuation cleanup, tokenization, and n-gram generation.

### 3. **POS Tagging & Named Entity Recognition**
- Identified linguistic features and named entities using SpaCy.

### 4. **Sentiment Analysis**
- Used VADER to classify sentiments into Positive, Neutral, and Negative.
- Visualized sentiment distribution.

### 5. **Topic Modeling**
- Applied LDA (Latent Dirichlet Allocation) to uncover key discussion themes.

### 6. **Stylometric Analysis**
- Conducted PCA and KMeans clustering for author or pattern detection.
- Generated dendrograms and scatter plots for visualization.

### 7. **Document Clustering with Word2Vec**
- Represented text using Word2Vec and clustered similar documents.

### 8. **Dependency Parsing**
- Visualized syntactic relationships between sentence components using SpaCy.

### 9. **Insights & Real-World Applications**
- Discussed insights derived from Reddit discussions and their applicability in journalism, sentiment tracking, and sociopolitical research.


## 📦 Requirements

```bash
pip install praw nltk spacy gensim sklearn matplotlib seaborn wordcloud
python -m spacy download en_core_web_sm
