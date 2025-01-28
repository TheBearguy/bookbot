from collections import Counter
import string
# import matplotlib.pyplot as plt

def main():
    book_path = "books/frankenstein.txt"
    text = get_book_text(book_path)

    while True:
        print("\nChoose an option:")
        print("1. Word Count")
        print("2. Character Frequency")
        print("3. Word Frequency")
        print("4. Unique Words")
        print("5. Sentence Count")
        print("6. Longest and Shortest Words")
        print("7. Visualize Character Frequency")
        print("8. Export Analysis")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num_words = get_num_words(text)
            print(f"\nThe document contains {num_words} words.")

        elif choice == "2":
            char_freq = count_char_freq(text)
            print("\nCharacter Frequency:")
            for char, freq in sorted(char_freq.items(), key=lambda x: x[1], reverse=True):
                print(f"'{char}': {freq}")

        elif choice == "3":
            word_freq = count_word_freq(text)
            top_n = int(input("How many top words do you want to see? "))
            print(f"\nTop {top_n} Words by Frequency:")
            for word, freq in word_freq.most_common(top_n):
                print(f"'{word}': {freq}")

        elif choice == "4":
            unique_words = get_unique_words(text)
            print(f"\nThe document contains {len(unique_words)} unique words.")

        elif choice == "5":
            num_sentences = count_sentences(text)
            print(f"\nThe document contains {num_sentences} sentences.")

        elif choice == "6":
            longest, shortest = get_longest_shortest_words(text)
            print(f"\nLongest word: {longest}")
            print(f"Shortest word: {shortest}")

        # elif choice == "7":
        #     char_freq = count_char_freq(text)
        #     visualize_char_freq(char_freq)

        elif choice == "8":
            export_analysis(text)
            print("\nAnalysis exported successfully!")

        elif choice == "9":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

def get_book_text(book_path):
    with open(book_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_num_words(text):
    return len(text.split())

def count_char_freq(text):
    text = text.lower()
    char_freq = {}
    for char in text:
        if char.isalpha():
            char_freq[char] = char_freq.get(char, 0) + 1
    return char_freq

def count_word_freq(text):
    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    return Counter(words)

def get_unique_words(text):
    words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    return set(words)

def count_sentences(text):
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])

def get_longest_shortest_words(text):
    words = text.translate(str.maketrans('', '', string.punctuation)).split()
    longest = max(words, key=len)
    shortest = min(words, key=len)
    return longest, shortest

def export_analysis(text):
    char_freq = count_char_freq(text)
    word_freq = count_word_freq(text)
    num_words = get_num_words(text)
    num_sentences = count_sentences(text)

    with open("analysis.txt", "w") as file:
        file.write(f"Word Count: {num_words}\n")
        file.write(f"Sentence Count: {num_sentences}\n\n")

        file.write("Character Frequency:\n")
        for char, freq in sorted(char_freq.items(), key=lambda x: x[1], reverse=True):
            file.write(f"'{char}': {freq}\n")

        file.write("\nWord Frequency (Top 10):\n")
        for word, freq in word_freq.most_common(10):
            file.write(f"'{word}': {freq}\n")

# Run the program
if __name__ == "__main__":
    main()
