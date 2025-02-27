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



def recommend_books(book_title):
    # Find the book in the dataset using fuzzy matching
    book_matches = books_df['Book'].apply(lambda x: fuzz.partial_ratio(x.lower(), book_title.lower()))
    best_match_idx = book_matches.idxmax()

    if book_matches[best_match_idx] < 60:  # Eğer eşleşme yoksa
        return ["Kitap bulunamadı."]

    book = books_df.iloc[best_match_idx]


    genres = [book['Genre1'], book['Genre2'], book['Genre3']]


    temp = books_df[
        ((books_df['Genre1'].isin(genres)) | (books_df['Genre2'].isin(genres)) | (books_df['Genre3'].isin(genres)))
    ]
    temp.reset_index(drop=True, inplace=True)

    # Convert the book description into vectors
    tf = TfidfVectorizer(analyzer='word', stop_words='english')
    tfidf_matrix = tf.fit_transform(temp['Description'])

    # Calculating the similarity measures based on Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index corresponding to the book title
    idx = temp.index[temp['Book'].str.lower() == book['Book'].lower()].tolist()[0]

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 5 most similar books
    sim_scores = sim_scores[1:6]

    # Book indices
    book_indices = [i[0] for i in sim_scores]

    # Top 5 book recommendation
    recs = temp.iloc[book_indices]['Book'].tolist()
    return recs


def general_response():
    return "I'm a dumb bot after all"


def extract_book_title(user_input):
    doc = nlp(user_input)
    book_titles = [ent.text for ent in doc.ents if ent.label == "BOOK"]
    if book_titles:
        return book_titles[0]
    else:
        return user_input


def chatbot_response(user_input):
    intent = classify_intent(user_input)
    if intent == "summary":
        book_title = extract_book_title(user_input)
        response = get_book_summary(book_title)
        return response
    elif intent == "recommend":
        book_title = classify_intent(user_input)
        recommendations = recommend_books(book_title)
        return recommendations
    else:
        return general_response()


# Tkinter GUI
class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with a book")

        self.root.configure(bg='#f0f0f0')

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg='#ffffff', fg='#000000', font=('Arial', 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(root, width=100, bg='#ffffff', fg='#000000', font=('Arial', 12))
        self.user_input.pack(padx=10, pady=10, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Enter", command=self.send_message, bg='#4CAF50', fg='#ffffff', font=('Arial', 12))
        self.send_button.pack(padx=10, pady=10)

        self.chatbot_greet()

    def chatbot_greet(self):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "Chatbot: Hello! How can i help you? \n", 'chatbot')
        self.chat_area.config(state='disabled')
        self.chat_area.tag_config('chatbot', foreground='#4CAF50', font=('Arial', 12, 'bold'))

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.lower() == 'exit':
            self.root.quit()
        self.display_message("You", user_message)
        self.user_input.delete(0, tk.END)
        response = chatbot_response(user_message)
        self.display_message("Chatbot", response)

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')
        if sender == "Chatbot":
            self.chat_area.tag_add('chatbot', f"{self.chat_area.index('end')}-2l", f"{self.chat_area.index('end')}-1l")
            self.chat_area.tag_config('chatbot', foreground='#4CAF50', font=('Arial', 12, 'bold'))
        else:
            self.chat_area.tag_add('user', f"{self.chat_area.index('end')}-2l", f"{self.chat_area.index('end')}-1l")
            self.chat_area.tag_config('user', foreground='#0000FF', font=('Arial', 12, 'italic'))


if __name__=="__main__":
    root=tk.Tk()
    chatbot_gui = ChatBotGUI(root)
    root.mainloop()
