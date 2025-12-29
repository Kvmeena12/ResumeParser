from langchain_core.documents import Document

def jd_to_documents(jd_text):
    chunks = jd_text.split("\n")
    docs = []
    for chunk in chunks:
        if len(chunk.strip()) > 20:
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": "job_description"}
                )
            )

    return docs
