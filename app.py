from flask import Flask, request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

import glob

app = Flask("junos_release_analyzer")

folder_path = "db"

cached_llm = Ollama(model="llama3.2")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant good at searching docuemnts. If you do not have an answer from the provided information say so. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)


@app.route("/ai", methods=["POST"])
def aiPost():
    print("POST /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer

    #Example curl
    #curl -X 'POST' \
	#    'http://127.0.0.1:8080/ai' \
	#    -H 'accept: application/json' \
	#    -H 'Content-Type: application/json' \
	#    -d ' {
	#    "query": "how can you help me?"
	#    }'

@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    print("POST /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.4, #relevance score when retrieving info from DB
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)

    sources = []
    for doc in result["context"]:
        sources.append(
            {"source": doc.metadata["source"], "page_content": doc.page_content}
        )

    response_answer = {"answer": result["answer"], "sources": sources}
    return response_answer

    #Example curl
    #curl -X 'POST' \
	#    'http://127.0.0.1:8080/ai' \
	#    -H 'accept: application/json' \
	#    -H 'Content-Type: application/json' \
	#    -d ' {
	#    "query": "what new features brings the junos release 22.2r1?"
	#    }'

@app.route("/add_pdf", methods=["POST"])
def pdfAddPost():
    print("POST /add_pdf called")
    file = request.files["file"]
    file_name = file.filename
    save_file = "pdf/" + file_name
    file.save(save_file)
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response

@app.route("/embed_pdfs", methods=["GET"])
def pdfEmbed():
    print("GET /embed_pdfs called")
    
    path = './pdf/' #this could be loaded from env.txt
    files_path = ''.join([path, '*.pdf'])
    saved_files = []

    for document in glob.glob(files_path):
        #file_name = document.replace('./pdf')
        #save_file = "pdf/" + file_name
        #file.save(document)
        print(f"filename: {document}")

        loader = PDFPlumberLoader(document)
        docs = loader.load_and_split()
        print(f"docs len={len(docs)}")

        chunks = text_splitter.split_documents(docs)
        print(f"chunks len={len(chunks)}")

        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )

        vector_store.persist()
        
        message = {
            "filelist": document,
            "doc_len": len(docs),
            "chunks": len(chunks),
        }
        
        saved_files.append(document)
        print (f"Files successfully uploaded: \n {message}")

    response = {
        "status": "Files Successfully Uploaded",
        #"filelist": file_name,
        "filelist": saved_files,
        "total_docs": len(saved_files),
    }
    return response

    #example curls
    #curl -X 'GET' \
	#'http://127.0.0.1:8080/embed_pdfs' \
	#-H 'accept: application/json' \
	#-H 'Content-Type: application/json' 

@app.route("/list_pdfs", methods=["GET"])
def pdfList():
    print("GET /list_pdfs called")
    
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
    all_documents = vector_store.get() #['documents']
    print (f"all_document is {all_documents}")
    response = {
        "documents": all_documents,
        "total_docs": len(all_documents),
    }
    return response

    #example curl
    #curl -X 'GET' \
	#'http://127.0.0.1:8080/list_pdfs' \
	#-H 'accept: application/json' \
	#-H 'Content-Type: application/json' 

def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    start_app()
