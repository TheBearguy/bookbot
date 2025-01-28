from collections import Counter

# print("hello world")

def main():
    book_path="books/frankenstein.txt"
    text:str=get_book_text(book_path)
    num_words:int=get_num_words(text)
    char_freq=count_char_freq(text)
    char_freq_list = list(char_freq.items())
    char_freq_list.sort(reverse=True, key=lambda x : x[1])
    print(f"{num_words} was found in the document")
    for items in char_freq_list:
        print(f"The '{items[0]}' character was found {items[1]} times")
    # print(char_freq_list)


def get_num_words(text:str):
    words=text.split()
    return len(words)


def get_book_text(book_path):
    with open(book_path) as file:
        text=file.read(); return text;


def count_char_freq(text:str):
    text=text.lower()
    char_freq = {}
    for char in text:
        if char.isalpha():
            char_freq[char] = char_freq.get(char, 0) + 1
    return char_freq


main()
