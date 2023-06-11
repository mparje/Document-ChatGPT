import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os

os.environ['OPENAI_API_KEY'] = 'sk-'  # Your API key


class MyApp:
    def __init__(self):
        self.directory = ""
        self.index_path = "index.json"
        self.documents = []
        self.index = None

    def select_directory(self):
        self.directory = st.sidebar.selectbox("Select a directory", [""], help="Selected directory")
        if self.directory:
            st.sidebar.write(f"Selected directory: {self.directory}")

    def search(self):
        if not self.directory:
            st.error("Please select a directory first.")
            return

        query = st.text_input("Query:")
        if st.button("Search Documents"):
            self.load_documents()
            self.create_index()
            response = self.query_index(query)
            self.display_results(response)

    def load_documents(self):
        reader = SimpleDirectoryReader(self.directory)
        self.documents = reader.load_data()

    def create_index(self):
        self.index = GPTSimpleVectorIndex(self.documents)
        self.index.save_to_disk(self.index_path)

    def query_index(self, query):
        loaded_index = GPTSimpleVectorIndex.load_from_disk(self.index_path)
        response = loaded_index.query(query)
        return response

    def display_results(self, response):
        if len(response) > 0:
            st.subheader("Search Results")
            for result in response:
                st.write(result)
                st.markdown("---")
        else:
            st.write("No results found.")


def main():
    st.title("Document Chatbot")
    st.geometry("500x500")

    app = MyApp()
    app.select_directory()
    app.search()


if __name__ == "__main__":
    main()
