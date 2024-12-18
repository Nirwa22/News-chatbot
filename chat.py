from langchain_community.document_loaders import TextLoader
with open("document_files/History.txt", encoding="utf-8") as history:
    text_new = history.read()
with open(self.file_path) as file:
    text = file.read()
chunks = self.text_splitter.create_documents(self.text_splitter.split_text(text))
print(loader.load())
print(text_new)