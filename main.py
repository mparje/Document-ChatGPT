import PyPDF2
import streamlit as st
import threading
import time
import pyperclip
from tkinter.ttk import Progressbar
import openai

openai.api_key = "YOUR_API_KEY"

def extract_text(filepath, progress_var):
    # Open the PDF file in read-binary mode
    with open(filepath, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create an empty string to store the text
        text = ''

        # Loop through each page in the PDF file
        for page_num in range(len(pdf_reader.pages)):
            # Update the progress bar
            progress_var.set(page_num + 1)
            st.experimental_rerun()

            # Get the page object
            page_obj = pdf_reader.pages[page_num]

            # Extract the text from the page
            page_text = page_obj.extract_text()

            # Add the text to the string
            text += page_text

    return text


def generate_summary(text, status_var):
    status_var.set('Generating summary...')
    words = text.split()
    max_words = 300
    prompt = " ".join(words[:max_words])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this: {prompt}",
        temperature=0.9,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text
    status_var.set('Summary generated')
    progress_var.set(100)
    return summary


def summarize(filepath):
    if filepath:
        progress_var = st.empty()
        pdf_text = extract_text(filepath, progress_var)
        status_var = st.empty()
        summary = generate_summary(pdf_text, status_var)
        st.text_area('Summary:', value=summary, height=200)


def main():
    st.title('Chatgpt PDF Summarizer')

    # File path input
    filepath = st.file_uploader('Upload a PDF file', type='pdf')

    if filepath:
        if st.button('Generate Summary'):
            summarize(filepath.name)


if __name__ == '__main__':
    main()
