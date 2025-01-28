import spacy
from fuzzywuzzy import fuzz
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import scrolledtext


nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')

books_df = pd.read_csv("books/bookcollection.csv")

# print(books_df.columns)

def classify_intent(user_input):
    summary_keywords: list = ["summary", "summarize", "short", "brief"]
    recommend_keywords: list = ["recommend", "suggest"]
    user_input_lower = user_input.lower()
    summary_score = max([fuzz.partial_ratio(user_input_lower, keyword) for keyword in summary_keywords])
    recommend_score = max([fuzz.partial_ratio(user_input_lower, keyword) for keyword in recommend_keywords])
    if summary_score > recommend_score and summary_score > 60:
        return "summary"
    elif recommend_score > summary_score and recommend_score > 60:
        return "recommend"
    else:
        return "general"


def get_book_summary(book_title):
    try:
        book_matches = books_df['Book'].apply(lambda x : fuzz.partial_ratio(x.lower(), book_title.lower()))
        best_match_idx = book_matches.idxmax()
        if book_matches[best_match_idx] > 60:
            summary = books_df.iloc[best_match_idx]['Description']
            return f"Here's the summary of {books_df.iloc[best_match_idx]['Book']} : \n {summary}"
        else:
            return f"This is a dumb model"
    except KeyError as e:
        return f"ERROR WHILE GETTING SUMMARY :: {e}"



