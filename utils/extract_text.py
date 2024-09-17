def split_text_into_paragraphs(text, max_words=400):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
