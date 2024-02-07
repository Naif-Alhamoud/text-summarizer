import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def summarize_text(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    tokens = [token.text for token in doc]
    st.write("Tokens:", tokens)
    punctuation = punctuation + '\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    st.write("Word Frequencies:", word_frequencies)

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    st.write("Normalized Word Frequencies:", word_frequencies)

    sentence_tokens = [sent for sent in doc.sents]
    st.write("Sentence Tokens:", sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    st.write("Sentence Scores:", sentence_scores)

    select_length = int(len(sentence_tokens) * 0.3)
    st.write("Select Length:", select_length)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    st.write("Summary:", summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary


# Streamlit app
st.title("Text Summarizer")

text_input = st.text_area("Enter the Text to Summarize")
if st.button("Summarize"):
    if text_input:
        summary_result = summarize_text(text_input)
        st.subheader("Summary")
        st.write(summary_result)
    else:
        st.warning("Please enter some text to summarize.")