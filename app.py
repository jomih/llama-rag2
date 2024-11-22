from flask import Flask, request
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#for instruct model
from langchain_ollama import OllamaLLM
#for chat model
from langchain_ollama import ChatOllama

import glob
from doc_tagging import doc_tagging
import chromadb, re
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pprint import pprint

#Init of chroma db non-persistent
#chroma_client = chromadb.Client()
#collection = chroma_client.get_or_create_collection(name="junos_releases_collection")
#Init of chroma db persistent
chroma_client = chromadb.PersistentClient(path="./db/")
collection = chroma_client.get_or_create_collection(name="junos_releases_collection")

#Init of App
app = Flask("junos_release_analyzer")
folder_path = "db"

#Init of LLAMA as chat
model="llama3.2"
temperature=0
chat_ollama_model = ChatOllama(model=model, temperature=temperature)
system_prompt = '''You are a technical assistant good at searching documents. If you do not have an answer from the provided information, say so.'''
create_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        #
        #MessagesPlaceholder("chat_history"),
        #
        ("user", "Question: {query}")
    ]
)
format_answer = StrOutputParser()
chat_ollama = create_prompt | chat_ollama_model | format_answer

#Init of LLama as Instruct
#ollama_llm = OllamaLLM(model=model)


def format_output(text):
    """Convert Markdown bold syntax to HTML strong tags."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

#Start with Flask routes
@app.route("/ai", methods=["POST"])
def aiPost():
    '''AI route to ask LLM'''
    print("POST /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    answer = chat_ollama.invoke({'query': query})
    response = format_output(answer)

    print(response)

    #response_answer = {"answer": response['content']}
    return response

    #Example curl
    #curl -X 'POST' \
	#    'http://127.0.0.1:8080/ai' \
	#    -H 'accept: application/json' \
	#    -H 'Content-Type: application/json' \
	#    -d ' {
	#    "query": "why is the sky blue?"
	#    }'

@app.route("/ask_text", methods=["POST"])
def askTextPost():
    '''AI route to ask about the text'''
    print("POST /ask_text called")
    
    #identify the query
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    if "ACX" in query:
        print("ACX query")
        metadata = {
            "file": "./txt/junos-release-notes-22.3r1with_tags.txt", #hard-coded - change it
            "section": "ACX_newfeatures"
        }
        filter_word = "ACX"
    if "MX" in query:
        print("MX query")
        metadata = {
            "file": "./txt/junos-release-notes-22.3r1with_tags.txt", #hard-coded - change it
            "section": "MX_newfeatures" #parece que al cargar se está metiendo on \n y luego no filtra bien
        }
        filter_word = "MX"

    results=collection.query(
        query_texts=query,
        n_results=1,
        where= {
            "$and": [
                {
                    "file": metadata['file']
                },
                {
                    "section": metadata['section']
                }
            ]
        },
        #where_document={"$contains": filter_word}
    )

    print(f"results is: {results}")

    response = {
        "answer": results['documents'],
        "distance": results['distances'],
        "metadatas": results['metadatas']
    }
    return(response)

    #curl -X 'POST' \
    #'http://127.0.0.1:8080/ask_text' \
    #-H 'accept: application/json' \
    #-H 'Content-Type: application/json' \
    #-d ' {
    #    "query": "what new features brings the junos to ACX platforms?"
    #}'

@app.route("/list_db", methods=["GET"])
def pdfList():
    '''AI route to list entries in Chroma DB'''
    print("GET /list_db called")
    
    count = collection.count()
    result = collection.get()

    print (f"result is: {result}")
    response = {
        "documents": result['documents'],
        "metadatas": result['metadatas'],
        "total_docs": count
    }
    return response

    #example curl
    #curl -X 'GET' \
	#'http://127.0.0.1:8080/list_db' \
	#-H 'accept: application/json' \
	#-H 'Content-Type: application/json' 

@app.route("/add_text", methods=["POST"])
def pdfAddText():
    '''AI route to upload a .txt to Chroma DB'''
    print("POST /add_text called")

    #tag the documents in ./txt/. This should be run in advance
    #doc_tagging() #the path could be passed as argument

    json_content = request.json
    file = json_content.get("file")
    path = './txt/' #this could be loaded from env.txt
    document = ''.join([path, file])

    #load the tagged documents in ./txt/
    path = './txt/' #this could be loaded from env.txt
    files_path = ''.join([path, '*.txt'])
    saved_files = []

    #for document in glob.glob(files_path):
    with open(document) as my_file:
        block = 'default'
        text2append = ''
        chunks = []
        metadata = []
        for line in my_file:
            #print (f"line is: {line}")
            if line.startswith('<_tag_'):
                #previous block
                chunks.append(text2append)
                metadatas = { 
                    "file": str(document), 
                    "section": str(block) 
                }
                print(f"metadatas is: {metadatas}")
                metadata.append(metadatas)
                
                #new block
                block=str(line.replace('<_tag_','').replace('>','').replace('\n',''))
                text2append = ''
            else:
                text2append = text2append + line

    count = collection.count()
    collection.add(
        documents=chunks,
        metadatas=metadata,
        ids=[str(i) for i in range(count+1, count+1+len(chunks))]
    )

    response = {
        "status": "Text successfully Uploaded to the Collection",
    }
    print(response)
    return response

    #curl -X 'POST' \
    #'http://127.0.0.1:8080/add_text' \
    #-H 'accept: application/json' \
    #-H 'Content-Type: application/json' \
    #-d ' {
    #    "file": "junos-release-notes-22.3r1with_tags.txt"
    #}'

@app.route("/add_pdf", methods=["POST"])
def pdfAddPDF():
    response = = {
        "status": "API under construction",
    }
    return response

#@app.route("/add_pdf", methods=["POST"])
#def pdfAddPost():
#    print("POST /add_pdf called")
#    file = request.files["file"]
#    file_name = file.filename
#    save_file = "pdf/" + file_name
#    file.save(save_file)
#    print(f"filename: {file_name}")
#
#    loader = PDFPlumberLoader(save_file)
#    docs = loader.load_and_split()
#    print(f"docs len={len(docs)}")
#
#    chunks = text_splitter.split_documents(docs)
#    print(f"chunks len={len(chunks)}")
#
#    vector_store = Chroma.from_documents(
#        documents=chunks, embedding=embedding, persist_directory=folder_path
#    )
#
#    vector_store.persist()
#
#    response = {
#        "status": "Successfully Uploaded",
#        "filename": file_name,
#        "doc_len": len(docs),
#        "chunks": len(chunks),
#    }
#    return response

#@app.route("/embed_pdfs", methods=["GET"])
#def pdfEmbed():
#    print("GET /embed_pdfs called")
#    
#    path = './pdf/' #this could be loaded from env.txt
#    files_path = ''.join([path, '*.pdf'])
#    saved_files = []
#
#    for document in glob.glob(files_path):
#        #file_name = document.replace('./pdf')
#        #save_file = "pdf/" + file_name
#        #file.save(document)
#        print(f"filename: {document}")
#
#        loader = PDFPlumberLoader(document)
#        docs = loader.load_and_split()
#        print(f"docs len={len(docs)}")
#
#        chunks = text_splitter.split_documents(docs)
#        print(f"chunks len={len(chunks)}")
#
#        vector_store = Chroma.from_documents(
#            documents=chunks, embedding=embedding, persist_directory=folder_path
#        )
#
#        vector_store.persist()
#        
#        message = {
#            "filelist": document,
#            "doc_len": len(docs),
#            "chunks": len(chunks),
#        }
#        
#        saved_files.append(document)
#        print (f"Files successfully uploaded: \n {message}")
#
#    response = {
#        "status": "Files Successfully Uploaded",
#        #"filelist": file_name,
#        "filelist": saved_files,
#        "total_docs": len(saved_files),
#    }
#    return response
#
#    #example curls
#    #curl -X 'GET' \
#   #'http://127.0.0.1:8080/embed_pdfs' \
#   #-H 'accept: application/json' \
#   #-H 'Content-Type: application/json' 

#@app.route("/ask_pdf", methods=["POST"])
#def askPDFPost():
#    print("POST /ask_pdf called")
#    json_content = request.json
#    query = json_content.get("query")
#
#    print(f"query: {query}")
#
#    print("Loading vector store")
#    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
#
#    print("Creating chain")
#    retriever = vector_store.as_retriever(
#        search_type="similarity_score_threshold",
#        search_kwargs={
#            "k": 20,
#            "score_threshold": 0.4, #relevance score when retrieving info from DB
#        },
#    )
#
#    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
#    chain = create_retrieval_chain(retriever, document_chain)
#
#    result = chain.invoke({"input": query})
#
#    print(result)
#
#    sources = []
#    for doc in result["context"]:
#        sources.append(
#            {"source": doc.metadata["source"], "page_content": doc.page_content}
#        )
#
#    response_answer = {"answer": result["answer"], "sources": sources}
#    return response_answer
#
#    #Example curl
#    #curl -X 'POST' \
#   #    'http://127.0.0.1:8080/ai' \
#   #    -H 'accept: application/json' \
#   #    -H 'Content-Type: application/json' \
#   #    -d ' {
#   #    "query": "what new features brings the junos release 22.2r1?"
#   #    }'


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()
