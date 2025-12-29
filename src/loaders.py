from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_resume(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file format")

    documents = loader.load()
    text = " ".join([doc.page_content for doc in documents])
    return text
